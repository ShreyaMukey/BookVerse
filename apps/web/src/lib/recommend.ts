import { findBookLink } from "./openlibrary";
import type { BookRecommendation, RecommendationRequest, RecommendationResponse } from "./types";

const ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages";
const DEFAULT_MODEL = "claude-sonnet-5";

interface RawBook {
  title?: string;
  author?: string;
  year?: number | null;
  whyRecommended?: string;
}

interface RawResponse {
  niche?: RawBook[];
  mainstream?: RawBook[];
  bestChoice?: RawBook[];
}

function buildPrompt(request: RecommendationRequest): string {
  const likedBooksList =
    request.likedBooks.length > 0
      ? request.likedBooks.map((b) => `- "${b.title}" by ${b.author}`).join("\n")
      : "(none provided)";

  return `A reader wants book recommendations based on these preferences:

- Genre: ${request.genre || "any"}
- Preferred ending type: ${request.endingType || "any"}
- Favorite author / style to match: ${request.favoriteAuthor || "none specified"}
- Pace: ${request.pace || "any"}
- Length: ${request.length || "any"}
- Books they already liked:
${likedBooksList}

Recommend real, published books (no invented titles) that fit these preferences, split into three buckets of exactly 10 books each:
1. "niche" - lesser-known, under-the-radar books that fit well but most readers haven't heard of
2. "mainstream" - popular, widely-read books that fit well
3. "bestChoice" - your single best 10 picks overall, regardless of popularity, ranked by fit

For each book include: title, author, year (publication year as a number, or null if unsure), and a one-sentence whyRecommended explaining the specific match to the reader's stated preferences.

Respond with ONLY valid JSON, no markdown code fences, no commentary, matching exactly this shape:
{"niche": [{"title": "", "author": "", "year": 0, "whyRecommended": ""}, ...10 items], "mainstream": [...10 items], "bestChoice": [...10 items]}`;
}

function stripCodeFences(text: string): string {
  const trimmed = text.trim();
  const fenced = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/);
  return fenced ? fenced[1] : trimmed;
}

function toRecommendation(book: RawBook): BookRecommendation | null {
  if (!book.title || !book.author) return null;
  return {
    title: book.title,
    author: book.author,
    year: typeof book.year === "number" ? book.year : null,
    whyRecommended: book.whyRecommended ?? "",
    findLink: findBookLink(book.title, book.author),
  };
}

export async function getRecommendations(
  request: RecommendationRequest
): Promise<RecommendationResponse> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error(
      "ANTHROPIC_API_KEY is not configured. Add it to apps/web/.env.local to enable recommendations."
    );
  }

  const response = await fetch(ANTHROPIC_API_URL, {
    method: "POST",
    headers: {
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: process.env.ANTHROPIC_MODEL || DEFAULT_MODEL,
      max_tokens: 4096,
      messages: [{ role: "user", content: buildPrompt(request) }],
    }),
    signal: AbortSignal.timeout(60000),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`Anthropic API request failed (${response.status}): ${errorBody}`);
  }

  const data = await response.json();
  const text = data.content?.[0]?.text;
  if (typeof text !== "string") {
    throw new Error("Anthropic API returned an unexpected response shape");
  }

  let parsed: RawResponse;
  try {
    parsed = JSON.parse(stripCodeFences(text));
  } catch {
    throw new Error("Failed to parse recommendation JSON from the model response");
  }

  return {
    niche: (parsed.niche ?? []).map(toRecommendation).filter((b): b is BookRecommendation => b !== null).slice(0, 10),
    mainstream: (parsed.mainstream ?? [])
      .map(toRecommendation)
      .filter((b): b is BookRecommendation => b !== null)
      .slice(0, 10),
    bestChoice: (parsed.bestChoice ?? [])
      .map(toRecommendation)
      .filter((b): b is BookRecommendation => b !== null)
      .slice(0, 10),
  };
}

import type { BookSearchResult } from "./types";

const OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json";

export async function searchBooks(query: string, limit = 8): Promise<BookSearchResult[]> {
  const url = new URL(OPEN_LIBRARY_SEARCH_URL);
  url.searchParams.set("q", query);
  url.searchParams.set("limit", String(limit));
  url.searchParams.set("fields", "title,author_name,first_publish_year,cover_i");

  const response = await fetch(url, {
    headers: { "User-Agent": "BookVerse/0.1 (recommendation-site)" },
    signal: AbortSignal.timeout(5000),
  });

  if (!response.ok) {
    throw new Error(`Open Library search failed with status ${response.status}`);
  }

  const data = await response.json();
  const docs: Array<{
    title?: string;
    author_name?: string[];
    first_publish_year?: number;
    cover_i?: number;
  }> = data.docs ?? [];

  return docs
    .filter((doc) => doc.title)
    .map((doc) => ({
      title: doc.title as string,
      author: doc.author_name?.[0] ?? "Unknown author",
      year: doc.first_publish_year ?? null,
      coverId: doc.cover_i ?? null,
    }));
}

export function findBookLink(title: string, author: string): string {
  const query = encodeURIComponent(`${title} ${author}`);
  return `https://openlibrary.org/search?q=${query}`;
}

export function coverUrl(coverId: number, size: "S" | "M" | "L" = "M"): string {
  return `https://covers.openlibrary.org/b/id/${coverId}-${size}.jpg`;
}

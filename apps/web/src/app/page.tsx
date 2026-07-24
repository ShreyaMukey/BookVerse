"use client";

import { useState } from "react";
import LikedBooksInput from "@/components/LikedBooksInput";
import RecommendationResults from "@/components/RecommendationResults";
import type { LikedBook, RecommendationRequest, RecommendationResponse } from "@/lib/types";

const GENRES = [
  "Any",
  "Fantasy",
  "Science Fiction",
  "Mystery / Thriller",
  "Romance",
  "Literary Fiction",
  "Historical Fiction",
  "Horror",
  "Young Adult",
  "Non-fiction",
  "Classic",
];

const ENDING_TYPES = [
  "Any",
  "Happy",
  "Bittersweet",
  "Tragic",
  "Twist",
  "Open-ended",
  "Full-circle",
];

const PACES = ["Any", "Slow-burn", "Balanced", "Fast-paced"];

const LENGTHS = ["Any", "Short (<300pg)", "Medium (300-500pg)", "Long (500pg+)"];

export default function Home() {
  const [genre, setGenre] = useState("Any");
  const [endingType, setEndingType] = useState("Any");
  const [favoriteAuthor, setFavoriteAuthor] = useState("");
  const [pace, setPace] = useState("Any");
  const [length, setLength] = useState("Any");
  const [likedBooks, setLikedBooks] = useState<LikedBook[]>([]);

  const [status, setStatus] = useState<"idle" | "loading" | "done" | "error">("idle");
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<RecommendationResponse | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    setError(null);

    const request: RecommendationRequest = {
      genre: genre === "Any" ? "" : genre,
      endingType: endingType === "Any" ? "" : endingType,
      favoriteAuthor,
      pace: pace === "Any" ? "" : pace,
      length: length === "Any" ? "" : length,
      likedBooks,
    };

    try {
      const res = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error ?? "Failed to get recommendations");
      }
      setResults(data);
      setStatus("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
      setStatus("error");
    }
  }

  function startOver() {
    setResults(null);
    setStatus("idle");
    setError(null);
  }

  return (
    <div className="mx-auto w-full max-w-5xl flex-1 px-6 py-12">
      <h1 className="text-3xl font-bold">Find your next book</h1>
      <p className="mt-2 text-zinc-600 dark:text-zinc-400">
        Tell us what you&apos;re in the mood for and we&apos;ll suggest 10 niche picks, 10
        mainstream picks, and our 10 best choices for you.
      </p>

      {status !== "done" && (
        <form onSubmit={handleSubmit} className="mt-8 flex flex-col gap-6">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label className="block text-sm font-medium mb-1">Genre</label>
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              >
                {GENRES.map((g) => (
                  <option key={g}>{g}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Preferred ending</label>
              <select
                value={endingType}
                onChange={(e) => setEndingType(e.target.value)}
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              >
                {ENDING_TYPES.map((t) => (
                  <option key={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Favorite author (optional)</label>
              <input
                type="text"
                value={favoriteAuthor}
                onChange={(e) => setFavoriteAuthor(e.target.value)}
                placeholder="e.g. Ursula K. Le Guin"
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Pace</label>
              <select
                value={pace}
                onChange={(e) => setPace(e.target.value)}
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              >
                {PACES.map((p) => (
                  <option key={p}>{p}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Length</label>
              <select
                value={length}
                onChange={(e) => setLength(e.target.value)}
                className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm dark:border-zinc-700 dark:bg-zinc-900"
              >
                {LENGTHS.map((l) => (
                  <option key={l}>{l}</option>
                ))}
              </select>
            </div>
          </div>

          <LikedBooksInput value={likedBooks} onChange={setLikedBooks} />

          <button
            type="submit"
            disabled={status === "loading"}
            className="w-full rounded-md bg-zinc-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900 sm:w-auto"
          >
            {status === "loading" ? "Finding books..." : "Get recommendations"}
          </button>

          {status === "error" && error && (
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          )}
        </form>
      )}

      {status === "done" && results && (
        <div className="mt-8">
          <button
            type="button"
            onClick={startOver}
            className="mb-6 text-sm font-medium underline underline-offset-2"
          >
            ← Start over
          </button>
          <RecommendationResults results={results} />
        </div>
      )}
    </div>
  );
}

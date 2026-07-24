"use client";

import { useEffect, useRef, useState } from "react";
import type { BookSearchResult, LikedBook } from "@/lib/types";

interface LikedBooksInputProps {
  value: LikedBook[];
  onChange: (books: LikedBook[]) => void;
}

export default function LikedBooksInput({ value, onChange }: LikedBooksInputProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<BookSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const visibleResults = query.trim().length >= 2 ? results : [];

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (query.trim().length < 2) {
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setLoading(true);
      try {
        const res = await fetch(`/api/search-books?q=${encodeURIComponent(query)}`);
        const data = await res.json();
        setResults(data.results ?? []);
      } catch {
        setResults([]);
      } finally {
        setLoading(false);
      }
    }, 300);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query]);

  function addBook(book: BookSearchResult) {
    const alreadyAdded = value.some((b) => b.title === book.title && b.author === book.author);
    if (!alreadyAdded) {
      onChange([...value, { title: book.title, author: book.author }]);
    }
    setQuery("");
    setResults([]);
  }

  function removeBook(book: LikedBook) {
    onChange(value.filter((b) => !(b.title === book.title && b.author === book.author)));
  }

  return (
    <div className="relative">
      <label className="block text-sm font-medium mb-1">Books you liked</label>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search for a book title..."
        className="w-full rounded-md border border-zinc-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900 dark:border-zinc-700 dark:bg-zinc-900"
      />

      {loading && <p className="mt-1 text-xs text-zinc-500">Searching...</p>}

      {query.trim().length >= 2 && visibleResults.length > 0 && (
        <ul className="absolute z-10 mt-1 max-h-64 w-full overflow-auto rounded-md border border-zinc-300 bg-white shadow-lg dark:border-zinc-700 dark:bg-zinc-900">
          {visibleResults.map((book, i) => (
            <li key={`${book.title}-${book.author}-${i}`}>
              <button
                type="button"
                onClick={() => addBook(book)}
                className="w-full px-3 py-2 text-left text-sm hover:bg-zinc-100 dark:hover:bg-zinc-800"
              >
                <span className="font-medium">{book.title}</span>
                <span className="text-zinc-500"> by {book.author}{book.year ? ` (${book.year})` : ""}</span>
              </button>
            </li>
          ))}
        </ul>
      )}

      {value.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {value.map((book, i) => (
            <span
              key={`${book.title}-${book.author}-${i}`}
              className="inline-flex items-center gap-1 rounded-full bg-zinc-100 px-3 py-1 text-xs dark:bg-zinc-800"
            >
              {book.title}
              <button
                type="button"
                onClick={() => removeBook(book)}
                aria-label={`Remove ${book.title}`}
                className="text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100"
              >
                ×
              </button>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

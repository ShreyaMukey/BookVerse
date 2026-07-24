import type { BookRecommendation } from "@/lib/types";

export default function BookCard({ book }: { book: BookRecommendation }) {
  return (
    <div className="rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
      <h3 className="font-semibold leading-tight">{book.title}</h3>
      <p className="text-sm text-zinc-500">
        {book.author}
        {book.year ? ` · ${book.year}` : ""}
      </p>
      {book.whyRecommended && (
        <p className="mt-2 text-sm text-zinc-700 dark:text-zinc-300">{book.whyRecommended}</p>
      )}
      <a
        href={book.findLink}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-block text-sm font-medium text-zinc-900 underline underline-offset-2 dark:text-zinc-50"
      >
        Find this book →
      </a>
    </div>
  );
}

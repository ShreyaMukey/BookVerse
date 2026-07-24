import type { RecommendationResponse } from "@/lib/types";
import BookCard from "./BookCard";

const SECTIONS: Array<{ key: keyof RecommendationResponse; title: string; blurb: string }> = [
  { key: "bestChoice", title: "Best choice for you", blurb: "Our top picks for your exact preferences" },
  { key: "mainstream", title: "Mainstream", blurb: "Popular books that fit well" },
  { key: "niche", title: "Niche", blurb: "Under-the-radar books worth discovering" },
];

export default function RecommendationResults({ results }: { results: RecommendationResponse }) {
  return (
    <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
      {SECTIONS.map((section) => (
        <div key={section.key}>
          <h2 className="text-lg font-semibold">{section.title}</h2>
          <p className="mb-3 text-sm text-zinc-500">{section.blurb}</p>
          <div className="flex flex-col gap-3">
            {results[section.key].map((book, i) => (
              <BookCard key={`${book.title}-${i}`} book={book} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

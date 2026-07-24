export type EndingType =
  | "Happy"
  | "Bittersweet"
  | "Tragic"
  | "Twist"
  | "Open-ended"
  | "Full-circle";

export type Pace = "Slow-burn" | "Balanced" | "Fast-paced";

export type Length = "Short (<300pg)" | "Medium (300-500pg)" | "Long (500pg+)";

export interface LikedBook {
  title: string;
  author: string;
}

export interface RecommendationRequest {
  genre: string;
  endingType: string;
  favoriteAuthor: string;
  pace: string;
  length: string;
  likedBooks: LikedBook[];
}

export interface BookRecommendation {
  title: string;
  author: string;
  year: number | null;
  whyRecommended: string;
  findLink: string;
}

export interface RecommendationResponse {
  niche: BookRecommendation[];
  mainstream: BookRecommendation[];
  bestChoice: BookRecommendation[];
}

export interface BookSearchResult {
  title: string;
  author: string;
  year: number | null;
  coverId: number | null;
}

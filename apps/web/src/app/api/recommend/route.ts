import { NextRequest, NextResponse } from "next/server";
import { getRecommendations } from "@/lib/recommend";
import type { RecommendationRequest } from "@/lib/types";

export async function POST(request: NextRequest) {
  const body = (await request.json()) as Partial<RecommendationRequest>;

  const recommendationRequest: RecommendationRequest = {
    genre: body.genre ?? "",
    endingType: body.endingType ?? "",
    favoriteAuthor: body.favoriteAuthor ?? "",
    pace: body.pace ?? "",
    length: body.length ?? "",
    likedBooks: Array.isArray(body.likedBooks) ? body.likedBooks : [],
  };

  try {
    const recommendations = await getRecommendations(recommendationRequest);
    return NextResponse.json(recommendations);
  } catch (error) {
    console.error("recommend failed", error);
    const message = error instanceof Error ? error.message : "Failed to generate recommendations";
    return NextResponse.json({ error: message }, { status: 502 });
  }
}

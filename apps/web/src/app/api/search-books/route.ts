import { NextRequest, NextResponse } from "next/server";
import { searchBooks } from "@/lib/openlibrary";

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams.get("q")?.trim();
  if (!query) {
    return NextResponse.json({ results: [] });
  }

  try {
    const results = await searchBooks(query);
    return NextResponse.json({ results });
  } catch (error) {
    console.error("search-books failed", error);
    return NextResponse.json({ results: [], error: "Search temporarily unavailable" }, { status: 502 });
  }
}

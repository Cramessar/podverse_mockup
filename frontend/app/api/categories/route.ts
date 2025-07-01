///categories (GET) — returns placeholder, but route exists
// frontend/app/api/categories/route.ts

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Categories endpoint works!" });
}
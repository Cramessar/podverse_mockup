
//health (GET) — returns API status
// frontend/app/api/categories/route.ts

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Categories endpoint works!" });
}
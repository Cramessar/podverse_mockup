//stats/channels/<id> (GET) — returns placeholder, but route exists
//stats/items (GET) — likely exists (based on naming, not shown in
// frontend/app/api/categories/route.ts

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Statsendpoint works!" });
}
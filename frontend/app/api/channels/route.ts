
//Channel Endpoints (channel_bp):
//GET /channels — Get all channels
//GET /channels/<int:channel_id> — Get a specific channel by ID (via query param)
//POST /channels — Create a new channel
//PUT /channels/<int:channel_id> — Update a channel
// frontend/app/api/categories/route.ts

import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ message: "Categories endpoint works!" });
}

//Channel Endpoints (channel_bp):
//GET /channels — Get all channels
//GET /channels/<int:channel_id> — Get a specific channel by ID (via query param)
//POST /channels — Create a new channel
//PUT /channels/<int:channel_id> — Update a channel
// frontend/app/api/categories/route.ts

import { NextRequest, NextResponse } from "next/server"

// Use Docker Compose service name for backend URL
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(req: NextRequest) {
  const query = req.nextUrl.searchParams.toString();
  const url = `${BACKEND_URL}/admin/channels${query ? `?${query}` : ""}`;
  console.log("API route /api/channels called with URL:", url);
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch channels");
    const data = await response.json();
    return NextResponse.json(data.data, { status: response.status });
  } catch (error: any) {
    console.error("API route error:", error, error?.stack);
    return NextResponse.json(
      { error: error.message || "Failed to fetch feeds" },
      { status: 500 }
    );
  }
}
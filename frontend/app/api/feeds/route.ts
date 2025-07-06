import axios from "axios";
import { NextRequest, NextResponse } from "next/server";
import { auth0 } from "@/lib/auth0";

// Use Docker Compose service name for backend URL
const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(req: NextRequest) {
  const query = req.nextUrl.searchParams.toString();
  const url = `${BACKEND_URL}/admin/feeds${query ? `?${query}` : ""}`;
  console.log("API route /api/feeds called with URL:", url);
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error("Failed to fetch feeds");
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

// POST /feeds — Create a new feed
export async function POST(req: NextRequest) {
  const session = await auth0.getSession();
  const data = await req.json();
  try {
    const response = await axios.post(`${BACKEND_URL}/feeds`, data);
    return NextResponse.json(response.data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to create feed" },
      { status: error.response?.status || 500 }
    );
  }
}
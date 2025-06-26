import axios from "axios";
import { NextRequest, NextResponse } from "next/server";
import { auth0 } from "@/lib/auth0";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

// GET /feeds — Get all feeds
export async function GET(req: NextRequest) {
  const session = await auth0.getSession();
  try {
    const response = await axios.get(`${BACKEND_URL}/feeds`);
    return NextResponse.json(response.data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to fetch feeds" },
      { status: error.response?.status || 500 }
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
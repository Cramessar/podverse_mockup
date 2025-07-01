// /app/api/feeds/[feed_id]/route.ts
import axios from "axios";
import { NextResponse } from "next/server";
import { auth0 } from "@/lib/auth0";

const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:5000";

// GET /feeds/:feed_id
export async function GET(_request: Request, context: any) {
  const { feed_id } = context.params;
  const session = await auth0.getSession();
  try {
    const response = await axios.get(`${BACKEND_URL}/feeds/${feed_id}`);
    return NextResponse.json(response.data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to fetch feed" },
      { status: error.response?.status || 500 }
    );
  }
}

// PUT /feeds/:feed_id
export async function PUT(request: Request, context: any) {
  const { feed_id } = context.params;
  const session = await auth0.getSession();
  const data = await request.json();
  try {
    const response = await axios.put(`${BACKEND_URL}/feeds/${feed_id}`, data);
    return NextResponse.json(response.data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to update feed" },
      { status: error.response?.status || 500 }
    );
  }
}

// DELETE /feeds/:feed_id
export async function DELETE(_request: Request, context: any) {
  const { feed_id } = context.params;
  const session = await auth0.getSession();
  try {
    const response = await axios.delete(`${BACKEND_URL}/feeds/${feed_id}`);
    return NextResponse.json(response.data, { status: response.status });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Failed to delete feed" },
      { status: error.response?.status || 500 }
    );
  }
}
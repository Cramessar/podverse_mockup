import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Allow all requests through without restriction
  return NextResponse.next();
}

export const config = {
  matcher: ["/admin/:path*", "/admin"],
};

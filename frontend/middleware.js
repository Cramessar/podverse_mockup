import { NextResponse } from "next/server";
import { auth0 } from "./lib/auth0";

export async function middleware(request) {
  if (process.env.NODE_ENV === "development") {
    return NextResponse.next();
  }

  const authRes = await auth0.middleware(request);

  if (request.nextUrl.pathname.startsWith("/auth")) {
    return authRes;
  }

  const session = await auth0.getSession();
  if (!session) {
    const { origin } = new URL(request.url);
    return NextResponse.redirect(`${origin}/auth/login`);
  }

  return authRes;
}
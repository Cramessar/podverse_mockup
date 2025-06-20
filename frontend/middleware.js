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
<<<<<<< Updated upstream
    return NextResponse.redirect(`${origin}/auth/login`);
  }

  return authRes;
=======
    return NextResponse.redirect(`${origin}/auth/login?returnTo=/dashboard`);
  }

export const config = {
    matcher: [
        /*
         * Match all request paths except for the ones starting with:
         * - _next/static (static files)
         * - _next/image (image optimization files)
         * - favicon.ico, sitemap.xml, robots.txt (metadata files)
         * - api (API routes)
         */
        "/((?!_next/static|_next/image|favicon.ico|sitemap.xml|robots.txt|api).*)",
    ],
>>>>>>> Stashed changes
}
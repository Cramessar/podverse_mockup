import { NextResponse } from "next/server";
import { auth0 } from "./lib/auth0"

export async function middleware(request) {
    const authRes = await auth0.middleware(request);

    // authentication routes — let the middleware handle it
    if (request.nextUrl.pathname.startsWith("/auth")) {
        return authRes;
    }

    // public routes — no need to check for session
    if (request.nextUrl.pathname === ("/")) {
        return authRes;
    }

    const session = await auth0.getSession();
    if (!session) {
        const { origin } = new URL(request.url);
        return NextResponse.redirect(`${origin}/auth/login?returnTo=/dashboard`);
    }
    // <-- MISSING CLOSING BRACE HERE
} // <-- Add this closing brace

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
}
// frontend/lib/auth0.js
export const auth0 = {
  middleware: async (request) => {
    // Just return a NextResponse with status 200 to allow all requests for now
    return new Response(null, { status: 200 });
  },
  getSession: async () => {
    // Return null to simulate no session (forces login redirect)
    return null;
  }
};

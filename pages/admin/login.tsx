import { useState } from "react";
import { signInWithGoogle } from "./utils/firebaseClient";
import { useRouter } from "next/router";

export default function AdminLogin() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleGoogleLogin = async () => {
    setLoading(true);
    setError(null);
    try {
      await signInWithGoogle();
      router.push("/admin"); // redirect to admin dashboard on success
    } catch (err) {
      setError("Failed to login. Please try again.");
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-podverse-background flex flex-col justify-center items-center px-4">
      <div className="max-w-md w-full bg-podverse-surface rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-extrabold mb-6 text-podverse-text text-center">
          Admin Login
        </h1>
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full py-3 bg-purple-700 hover:bg-purple-800 text-white rounded-md flex items-center justify-center gap-3 transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <svg
              className="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8z"
              ></path>
            </svg>
          ) : (
            <>
              <img
                src="/google-logo.svg"
                alt="Google"
                className="h-6 w-6"
              />
              <span>Sign in with Google</span>
            </>
          )}
        </button>
        {error && (
          <p className="mt-4 text-center text-red-500 font-semibold">{error}</p>
        )}
      </div>
    </main>
  );
}

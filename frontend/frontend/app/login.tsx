"use client";
import { useRouter } from "next/navigation";

export default function AdminLogin() {
  const router = useRouter();

  const handleContinue = () => {
    router.push("/auth/login?returnTo=/dashboard");
  };

  return (
    <main className="min-h-screen bg-podverse-background flex flex-col justify-center items-center px-4">
      <div className="max-w-md w-full bg-podverse-surface rounded-lg shadow-lg p-8 text-center">
        <h1 className="text-4xl font-extrabold mb-6 text-podverse-text">
          Admin Access
        </h1>
        <button
          onClick={handleContinue}
          className="w-full py-3 bg-purple-700 hover:bg-purple-800 text-white rounded-md transition"
        >
          Continue to Dashboard
        </button>
      </div>
    </main>
  );
}

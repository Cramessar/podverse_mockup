"use client";
import { useRouter } from "next/navigation";

export default function AdminLogin() {
  const router = useRouter();

  const handleContinue = () => {
    router.push("/auth/login?returnTo=/dashboard");
  };

  return (
    <main className="min-h-screen bg-podverse-background flex flex-col justify-center items-center px-4">
      <div className="max-w-md w-full bg-podverse-surface rounded-lg shadow-xl p-8 text-center border border-podverse-border">
        <div className="mx-auto mb-6 w-56">
          <img
            src="/podverse-brand-blue.svg"
            alt="Podverse Logo"
            className="w-full object-contain"
          />
        </div>

        <h1 className="text-3xl font-bold mb-6 text-podverse-text">
          Podverse Support Dashboard
        </h1>

        <button
          onClick={handleContinue}
          className="w-full py-3 bg-podverse-accent hover:bg-podverse-primary text-white rounded-md font-semibold transition"
        >
          Log In
        </button>
      </div>
    </main>
  );
}

"use client";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function AdminLogin() {
  const router = useRouter();

  const handleContinue = () => {
    router.push("/auth/login?returnTo=/dashboard");
  };

  return (
    <main className="min-h-screen bg-[#121212] flex flex-col justify-center items-center px-2">
      <div className="max-w-md w-full bg-podverse-surface rounded-lg shadow-lg p-8 text-center">
      <div className="mx-auto mb-4 w-62">
        <img
          src="/podverse-brand-blue.svg"
          alt="Podverse Logo"
          className="object-contain w-full"
        />
      </div>
        <h1 className="text-4xl font-extrabold mb-6 text-black">
            Support Dashboard
        </h1>
        <button
          onClick={handleContinue}
          className="w-full py-3 bg-podverse-accent hover:bg-podver-accent text-white rounded-md transition"
        >
          Log In
        </button>
      </div>
    </main>
  );
}

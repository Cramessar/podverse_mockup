// pages/admin/login.tsx
import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import {
  signInWithGoogle,
  signOutUser,
  onAuthStateChangedListener,
  getCurrentUser,
} from "./utils/firebaseClient";

const ADMIN_EMAILS = [
  "admin1@example.com",
  "admin2@example.com",
  // Add your admin emails here
];

export default function AdminLogin() {
  const router = useRouter();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChangedListener(async (user) => {
      if (user && user.email) {
        if (ADMIN_EMAILS.includes(user.email)) {
          setUserEmail(user.email);
          setError(null);
          router.push("/admin/dashboard"); // or wherever your admin dashboard is
        } else {
          setError("Access denied: You are not an admin.");
          await signOutUser();
          setUserEmail(null);
        }
      } else {
        setUserEmail(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  const handleSignIn = async () => {
    try {
      setLoading(true);
      const user = await signInWithGoogle();
      if (user.email && ADMIN_EMAILS.includes(user.email)) {
        setUserEmail(user.email);
        setError(null);
        router.push("/admin/dashboard");
      } else {
        setError("Access denied: You are not an admin.");
        await signOutUser();
        setUserEmail(null);
      }
    } catch (err) {
      setError("Failed to sign in.");
      setLoading(false);
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="min-h-screen flex flex-col justify-center items-center p-6 bg-gray-50">
      <h1 className="text-3xl mb-6">Admin Login</h1>
      {error && <p className="text-red-600 mb-4">{error}</p>}
      {!userEmail && (
        <button
          onClick={handleSignIn}
          className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Sign in with Google
        </button>
      )}
      {userEmail && (
        <div>
          <p>Welcome, {userEmail}</p>
          <button
            onClick={async () => {
              await signOutUser();
              setUserEmail(null);
              setError(null);
            }}
            className="mt-4 px-6 py-3 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}

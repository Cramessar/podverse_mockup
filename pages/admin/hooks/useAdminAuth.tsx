// hooks/useAdminAuth.tsx
import { useEffect, useState } from "react";
import { onAuthStateChanged, signOut, User } from "firebase/auth";
import { auth } from "../utils/firebaseClient"; // Adjust if needed
import { useRouter } from "next/router";

const ADMIN_EMAILS = (process.env.NEXT_PUBLIC_ADMIN_EMAILS || "").split(",");

export function useAdminAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      if (currentUser && ADMIN_EMAILS.includes(currentUser.email || "")) {
        setUser(currentUser);
      } else {
        if (currentUser) signOut(auth);
        setUser(null);
        if (router.pathname.startsWith("/admin") && router.pathname !== "/admin/login") {
          router.replace("/admin/login");
        }
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  return { user, loading };
}

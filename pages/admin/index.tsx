import { useEffect } from "react";
import { useRouter } from "next/router";
import { useAdminAuth } from "./hooks/useAdminAuth";


export default function AdminIndex() {
  const { user, loading } = useAdminAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.replace("/admin/login");
    }
  }, [loading, user, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-podverse-background text-podverse-text">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-podverse-background text-podverse-text p-8">
      <h1 className="text-4xl font-bold mb-4">Welcome to the Admin Dashboard</h1>
      <p className="text-lg">
        This is the protected admin dashboard area. Add your admin components here.
      </p>
    </div>
  );
}

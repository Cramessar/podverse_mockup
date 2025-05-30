// pages/admin/index.tsx
import { useAdminAuth } from "./hooks/useAdminAuth";

export default function AdminIndex() {
  const { user, loading } = useAdminAuth();

  if (loading) return <p>Loading...</p>;

  if (!user) {
    // Redirect handled in hook, so show nothing here
    return null;
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Admin Dashboard</h1>
      <p>Welcome, {user.email}</p>
      {/* TODO: Add your admin dashboard content here */}
    </div>
  );
}

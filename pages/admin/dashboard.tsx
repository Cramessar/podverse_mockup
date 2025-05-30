// pages/admin/dashboard.tsx
import { useAdminAuth } from "./hooks/useAdminAuth";

export default function AdminDashboard() {
  const { user, loading } = useAdminAuth();

  if (loading) return <p>Loading...</p>;

  if (!user) {
    // Redirect handled inside useAdminAuth hook
    return null;
  }

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-6">Admin Dashboard</h1>
      <p>Welcome back, {user.email}!</p>

      {/* Add dashboard components, stats, controls, etc. here */}
      <section className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Dashboard Overview</h2>
        <p>Coming soon: analytics, user management, content controls...</p>
      </section>
    </div>
  );
}

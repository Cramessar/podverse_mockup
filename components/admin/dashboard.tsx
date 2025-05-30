// pages/admin/dashboard.tsx
import DashboardLayout from "@/layouts/DashboardLayout";

export default function AdminDashboard() {
  return (
    <DashboardLayout>
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      <p className="text-podverse-muted">
        This is where we’ll show key metrics and system health.
      </p>
    </DashboardLayout>
  );
}

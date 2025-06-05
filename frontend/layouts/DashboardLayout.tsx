// TODO: Admin Layout
// layouts/DashboardLayout.tsx
import Sidebar from "@/components/admin/Sidebar";
import { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export default function DashboardLayout({ children }: Props) {
  return (
    <div className="flex h-screen bg-podverse-background text-white">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">{children}</main>
    </div>
  );
}

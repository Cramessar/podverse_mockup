// components/Sidebar.tsx
import Link from "next/link";

export default function Sidebar() {
  return (
    <aside className="w-20 bg-[#121214] flex flex-col items-center py-6 space-y-8 border-r border-gray-800">
      <Link
        href="/admin/dashboard"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="Home"
        aria-label="Home"
      >
        🏠
      </Link>
      <Link
        href="/admin/podcast"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="Podcasts"
        aria-label="Podcasts"
      >
        🎧
      </Link>
      <Link
        href="/admin/feeds"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="RSS Feeds"
        aria-label="RSS Feeds"
      >
        📡
      </Link>
      <Link
        href="#"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="Analytics"
        aria-label="Analytics"
      >
        📊
      </Link>
      <Link
        href="#"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="Notifications"
        aria-label="Notifications"
      >
        🔔
      </Link>
      <Link
        href="#"
        className="p-3 rounded hover:bg-[#1e1e23] transition inline-block"
        title="Profile"
        aria-label="Profile"
      >
        👤
      </Link>
    </aside>
  );
}

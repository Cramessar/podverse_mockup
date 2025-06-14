// components/admin/Sidebar.tsx
import Link from "next/link";
import { useRouter, usePathname } from "next/navigation";
// Simple class name joiner utility
function cn(...classes: (string | false | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}

const navLinks = [
  { href: "/admin/dashboard", label: "Dashboard" },
  { href: "/admin/feeds", label: "Feeds" },
  { href: "/admin/channel/123", label: "Channel Detail" },
];

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-podverse-surface p-6 space-y-4 border-r border-podverse-border">
      <h2 className="text-xl font-bold mb-4">Podverse Admin</h2>
      <nav className="flex flex-col gap-2">
        {navLinks.map(({ href, label }) => (
          <Link key={href} href={href}>
            <span
              className={cn(
                "block px-4 py-2 rounded hover:bg-podverse-highlight transition cursor-pointer",
                pathname === href ? "bg-podverse-highlight text-black font-semibold" : ""
              )}
            >
              {label}
            </span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}

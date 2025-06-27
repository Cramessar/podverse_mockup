// components/admin/Sidebar.tsx
import Link from "next/link";
import Image from "next/image";
import { useRouter, usePathname } from "next/navigation";
import {ChartBarIcon, RssIcon, BellIcon,UserIcon,SwatchIcon} from "@heroicons/react/24/outline";
// Simple class name joiner utility
function cn(...classes: (string | false | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}

const navLinks = [
  { href: "/dashboard", label: "Dashboard", icon: "/Dark_Podverse_Logo.svg" },
  { href: "/rssfeed", label: "Feeds", icon: <RssIcon className= "w-6 h-6"/> },
  { href: "/statistics", label: "Podverse Statistics", icon: <ChartBarIcon className= "w-6 h-6"/> },
  { href: "/notifications", label: "Notifications", icon: <BellIcon className= "w-6 h-6"/> },
  { href: "/profile", label: "Profile", icon: <UserIcon className= "w-6 h-6"/> },
  { href: "/theme", label: "Theme Editor", icon: <SwatchIcon className= "w-6 h-6"/> },
  { href: "/channels", label: "Channels", icon: <RssIcon className="w-6 h-6" /> },

];

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();

  return (
    <aside className="w-18 bg-podverse-surface p-4 space-y-4">
  <nav className="flex flex-col gap-2">
    {navLinks.map(({ href, label, icon }) => (
      <Link key={href} href={href}>
        <span
          className={cn(
            "block px-2 py-2 rounded hover:bg-podverse-highlight transition cursor-pointer flex items-center gap-2",
            pathname === href ? "bg-podverse-highlight text-black font-semibold" : ""
          )}
          title={label}
        >
          {typeof icon === "string"
        ? <Image src={icon} alt={label} width={24} height={24} />
        : icon}

        </span>
      </Link>
    ))}
  </nav>
    </aside>
  );
}



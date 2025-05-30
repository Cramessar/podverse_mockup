import { useState, useEffect, useRef } from "react";

interface FloatingHamburgerMenuProps {
  categories?: { id: number; name: string }[];
}

export default function FloatingHamburgerMenu({ categories = [] }: FloatingHamburgerMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Close menu if clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  // Dropdown expand state for menu sections
  const [expandedItems, setExpandedItems] = useState<{ [key: string]: boolean }>({});

  const toggleExpand = (item: string) => {
    setExpandedItems((prev) => ({ ...prev, [item]: !prev[item] }));
  };

  return (
    <>
      {/* Hamburger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-5 left-5 z-50 p-2 bg-purple-700 rounded-md text-white hover:bg-purple-800 focus:outline-none focus:ring-2 focus:ring-purple-600"
        aria-label="Toggle menu"
        aria-expanded={isOpen}
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          viewBox="0 0 24 24"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>
      </button>

      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-40 z-40"
          onClick={() => setIsOpen(false)}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Menu */}
      <div
        ref={menuRef}
        className={`fixed top-0 left-0 h-full bg-podverse-surface shadow-lg transition-transform duration-300 ease-in-out z-50
          ${isOpen ? "translate-x-0 pointer-events-auto w-64" : "-translate-x-full pointer-events-none w-64"}
        `}
      >
        <nav className="flex flex-col p-4 text-podverse-text h-full overflow-y-auto">
          {/* Categories Dropdown */}
          <button
            onClick={() => toggleExpand("categories")}
            className="flex justify-between items-center py-2 px-3 rounded hover:bg-podverse-highlight focus:outline-none"
            aria-expanded={expandedItems["categories"] || false}
          >
            Browse Categories
            <span>{expandedItems["categories"] ? "▲" : "▼"}</span>
          </button>
          {expandedItems["categories"] && (
            <div className="pl-4 text-sm max-h-64 overflow-y-auto">
              {categories.length === 0 && <p className="italic text-podverse-muted">No categories found</p>}
              {categories.map((cat) => (
                <a
                  key={cat.id}
                  href={`/explore?category=${encodeURIComponent(cat.name)}`}
                  className="block py-1 hover:underline"
                  onClick={() => setIsOpen(false)} // close menu on click
                >
                  {cat.name}
                </a>
              ))}
            </div>
          )}

          {/* Other menu options */}
          <a
            href="/explore"
            className="py-2 px-3 rounded hover:bg-podverse-highlight mt-4 block"
            onClick={() => setIsOpen(false)}
          >
            Trending Shows
          </a>
          <a
            href="/live"
            className="py-2 px-3 rounded hover:bg-podverse-highlight block"
            onClick={() => setIsOpen(false)}
          >
            Live Episodes
          </a>
          <a
            href="/spotlight"
            className="py-2 px-3 rounded hover:bg-podverse-highlight block"
            onClick={() => setIsOpen(false)}
          >
            Spotlight
          </a>
        </nav>
      </div>
    </>
  );
}

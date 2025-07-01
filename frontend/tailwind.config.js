/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,ts,jsx,tsx}",
    "./layouts/**/*.{js,ts,jsx,tsx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        podverse: {
          // 🎨 Base theme
          background: "#0f172a",      // Dark slate / page background
          surface: "#1e293b",         // Cards / table rows
          border: "#334155",          // Soft border gray
          text: "#f1f5f9",            // Off-white readable text
          muted: "#94a3b8",           // Muted labels/subtext

          // 🌈 Primary palette
          primary: "#3b82f6",         // Sky Blue (e.g. buttons, links)
          secondary: "#0ea5e9",       // Cyan (accents or secondary CTAs)
          accent: "#6366f1",          // Indigo / purple accent
          highlight: "#c084fc",       // Soft purple highlight
          cream: "#fef3c7",           // Soft warm yellow cream (for cards?)

          // ✅ Status colors
          success: "#22c55e",         // Green
          warning: "#facc15",         // Yellow
          error: "#ef4444",           // Red
          info: "#38bdf8",            // Light blue

          // 🧪 Dev/test colors if needed
          test: "#7dd3fc",
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};

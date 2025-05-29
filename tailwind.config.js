/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./layouts/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        podverse: {
          background: "#121212",     // Very dark gray (main site bg)
          surface: "#1e1e1e",        // Lighter panel backgrounds
          primary: "#00AEEF",        // Cyan/bright blue accent
          secondary: "#F95F0B",      // Orange CTA/accent
          highlight: "#7FDBFF",      // Lighter sky blue
          border: "#2a2a2a",         // Subtle dividers
          text: "#FFFFFF",           // Primary text
          muted: "#A0A0A0",          // Secondary text
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
}

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
          // Original base colors
          background: "#FFFFFF",//White
          surface: "#E5EAF2",
          text: "#000000", //Black
          muted: "#A0A0A0",
          border: "#2a2a2a",

          // Updated palette for podverse.fm vibe
          primary: "#000000",      // Black
          secondary: "#741b47",    // Burgundy
          accent: "#0D7AB3",       // Podverse Blue
          highlight: "#B1CAE3",    // 
          cream: "#fae7b5",        // Soft Cream
        },
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
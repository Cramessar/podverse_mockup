// frontend/app/layout.tsx

import '../styles/globals.css';
import { ReactNode } from "react";

export const metadata = {
  title: 'Podverse Admin',
  description: 'Admin dashboard for podcast management',
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div style={{ padding: 20, background: "lightgray" }}>
          <p>✅ Layout rendered</p>
        </div>
        {children}
      </body>
    </html>
  );
}

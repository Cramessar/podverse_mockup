// hooks/useAdminAuth.tsx
import { useState } from "react";

export function useAdminAuth() {
  // Disable auth checking: always no user and no loading
  const [user] = useState(null);
  const [loading] = useState(false);

  return { user, loading };
}

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isLoggedIn, getUserRoleFromToken } from "@/lib/auth";

export function ProtectedRoute({
  children,
  allowedRoles,
}: {
  children: React.ReactNode;
  allowedRoles?: string[];
}) {
  const router = useRouter();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    if (!isLoggedIn()) {
      router.replace("/logowanie");
      return;
    }
    if (allowedRoles && allowedRoles.length > 0) {
      const role = getUserRoleFromToken();
      if (!role || !allowedRoles.includes(role)) {
        router.replace("/konto");
        return;
      }
    }
    setChecked(true);
  }, [router, allowedRoles]);

  if (typeof window !== "undefined" && !isLoggedIn()) {
    return null;
  }

  if (!checked) {
    return null;
  }

  return <>{children}</>;
}

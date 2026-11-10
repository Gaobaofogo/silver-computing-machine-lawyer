/**
 * AuthContext — barrel export para retrocompatibilidade de imports legados.
 * A implementação real vive em `useAuth.tsx` (RBAC, ADR-0006).
 */
export { AuthProvider, useAuth } from './useAuth';

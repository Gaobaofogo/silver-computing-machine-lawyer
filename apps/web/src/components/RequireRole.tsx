/**
 * RequireRole — Route guard client-side (ADR-0007).
 *
 * Responsabilidade:
 *  - autenticado? redireciona para `/login` (em qualquer caminho).
 *  - `roles` prop opcional: filtra a role do usuário; fora dela, redireciona.
 *  - admin/assistente/advogado viajam no JWT cookie httpOnly (HttpOnly; Strict).
 *
 * Rendering:
 *   children apenas para usuários autenticados com role permitida.
 *
 * Testid: o componente só emite `data-testid="role-guard"` no estado
 * carregando; smoke test de integração (Vite) cobre rotas reais.
 */
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export interface RequireRoleProps {
  roles?: string[];
  children?: React.ReactNode;
}

export const RequireRole: React.FC<RequireRoleProps> = ({ roles, children }) => {
  const { isAuthenticated, user, loading } = useAuth();
  if (loading) {
    return <div data-testid="role-guard">Verificando sessão…</div>;
  }
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }
  if (roles && roles.length > 0 && !roles.includes(user.role)) {
    return <Navigate to="/login" replace />;
  }
  return <>{children ?? <Outlet />}</>;
};

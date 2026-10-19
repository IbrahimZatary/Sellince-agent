import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../providers/AuthContext';

export default function ProtectedRoute() {
  const { status } = useAuth();

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--color-bg-app)]">
        <div className="text-[var(--color-text-secondary)]">Loading session...</div>
      </div>
    );
  }

  if (status !== 'authenticated') {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
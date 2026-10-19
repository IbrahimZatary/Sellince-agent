import { Bell, LogOut, Search, User } from 'lucide-react';
import { useAuth } from '../../app/providers/AuthContext';

export default function Topbar() {
  const { user, signOut } = useAuth();

  return (
    <header className="h-16 bg-[var(--color-bg-card)] border-b border-[var(--color-border)] flex items-center justify-between px-6">
      <div className="flex-1 flex items-center">
        {/* Optional Context or Breadcrumbs can go here */}
        <h2 className="text-lg font-medium text-[var(--color-text-main)]">
          {user?.company_name || 'Company Dashboard'}
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        <button className="text-[var(--color-text-secondary)] hover:text-[var(--color-brand-orange)] transition-colors">
          <Search className="h-5 w-5" />
        </button>
        <button className="text-[var(--color-text-secondary)] hover:text-[var(--color-brand-orange)] transition-colors">
          <Bell className="h-5 w-5" />
        </button>
        <div
          className="h-8 w-8 rounded-full bg-[var(--color-brand-orange-light)] text-[var(--color-brand-orange)] flex items-center justify-center border border-[var(--color-brand-orange)]/20 cursor-pointer"
          title={user?.full_name || 'Account'}
        >
          <User className="h-5 w-5" />
        </div>
        <button
          onClick={signOut}
          title="Logout"
          className="text-[var(--color-text-secondary)] hover:text-red-600 transition-colors"
        >
          <LogOut className="h-5 w-5" />
        </button>
      </div>
    </header>
  );
}
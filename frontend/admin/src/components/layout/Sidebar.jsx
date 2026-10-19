import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Bot, BarChart3, Settings } from 'lucide-react';

const navItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Conversations', path: '/conversations', icon: MessageSquare },
  { name: 'AI Agent', path: '/agent', icon: Bot },
  { name: 'Analytics', path: '/analytics', icon: BarChart3 },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-[var(--color-bg-sidebar)] text-white flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-gray-800">
        <span className="text-xl font-bold tracking-wider text-[var(--color-brand-orange)]">SELLINCE</span>
      </div>
      
      <div className="flex-1 overflow-y-auto py-6">
        <nav className="space-y-1 px-3">
          {navItems.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-[var(--color-brand-orange)] text-white'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`
              }
            >
              <item.icon className="mr-3 h-5 w-5 flex-shrink-0" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </div>
      
      <div className="p-4 border-t border-gray-800">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              isActive
                ? 'bg-[var(--color-brand-orange)] text-white'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
            }`
          }
        >
          <Settings className="mr-3 h-5 w-5 flex-shrink-0" />
          Settings
        </NavLink>
      </div>
    </aside>
  );
}

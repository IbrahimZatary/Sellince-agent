import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppLayout() {
  return (
    <div className="flex h-screen bg-[var(--color-bg-app)]">
      {/* Sidebar - fixed width */}
      <Sidebar />
      
      {/* Main Content Area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        <Topbar />
        
        {/* Scrollable Content */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

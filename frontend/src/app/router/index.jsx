import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// Layouts
import AppLayout from '../../components/layout/AppLayout';
import OnboardingLayout from '../../components/layout/OnboardingLayout';

// Auth Pages
import Login from '../../pages/auth/Login';
import Signup from '../../pages/auth/Signup';

// Onboarding Pages
import CompanyInfo from '../../pages/onboarding/CompanyInfo';
import AgentBehavior from '../../pages/onboarding/AgentBehavior';
import Completion from '../../pages/onboarding/Completion';

import Dashboard from '../../pages/dashboard/Dashboard';
import Conversations from '../../pages/conversations/Conversations';
import AgentChat from '../../pages/agent/AgentChat';
import Settings from '../../pages/settings/Settings';
import ProtectedRoute from './ProtectedRoute';

// Placeholder Pages for future phases
const PlaceholderPage = ({ title }) => (
  <div className="p-8">
    <h1 className="text-2xl font-bold mb-4">{title}</h1>
    <p className="text-text-secondary">This page is under construction.</p>
  </div>
);

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: 'dashboard',
            element: <Dashboard />,
          },
          {
            path: 'conversations',
            element: <Conversations />,
          },
          {
            path: 'agent',
            element: <AgentChat />,
          },
          {
            path: 'analytics',
            element: <PlaceholderPage title="Analytics" />,
          },
          {
            path: 'settings',
            element: <Settings />,
          },
          {
            path: 'demo',
            element: <PlaceholderPage title="Product Demo (Walkthrough)" />,
          },
        ],
      },
    ],
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/signup',
    element: <Signup />,
  },
  {
    path: '/onboarding',
    element: <OnboardingLayout />,
    children: [
      {
        element: <ProtectedRoute />,
        children: [
          {
            path: 'company',
            element: <CompanyInfo />,
          },
          {
            path: 'agent',
            element: <AgentBehavior />,
          },
          {
            path: 'complete',
            element: <Completion />,
          },
        ],
      },
    ],
  },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}
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
        path: 'dashboard',
        element: <PlaceholderPage title="Dashboard" />,
      },
      {
        path: 'conversations',
        element: <PlaceholderPage title="Conversations" />,
      },
      {
        path: 'agent',
        element: <PlaceholderPage title="AI Agent" />,
      },
      {
        path: 'analytics',
        element: <PlaceholderPage title="Analytics" />,
      },
      {
        path: 'settings',
        element: <PlaceholderPage title="Settings" />,
      },
      {
        path: 'demo',
        element: <PlaceholderPage title="Product Demo (Walkthrough)" />,
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
      }
    ]
  }
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}

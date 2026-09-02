import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import AppLayout from '../../components/layout/AppLayout';

// Pages placeholders
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
        element: <PlaceholderPage title="Product Demo" />,
      },
    ],
  },
  {
    path: '/login',
    element: <PlaceholderPage title="Login" />,
  },
  {
    path: '/signup',
    element: <PlaceholderPage title="Signup" />,
  },
  {
    path: '/onboarding',
    children: [
      {
        path: 'company',
        element: <PlaceholderPage title="Company Info" />,
      },
      {
        path: 'agent',
        element: <PlaceholderPage title="Agent Behavior" />,
      },
      {
        path: 'complete',
        element: <PlaceholderPage title="Onboarding Complete" />,
      }
    ]
  }
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}

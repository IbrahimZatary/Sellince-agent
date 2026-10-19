import { Navigate, Outlet } from "react-router";

export default function ProtectedRoute() {
  if (!localStorage.getItem("customer_access_token") || !localStorage.getItem("customer_id")) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}

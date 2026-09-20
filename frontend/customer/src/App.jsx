import { Route, Routes } from "react-router";

import Login from "@/components/auth/Login";
import SignUp from "@/components/auth/SignUp";
import Chat from "@/pages/Chat";
import Home from "@/pages/Home";
import Onboarding from "@/pages/Onboarding";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route
        element={<ProtectedRoute />}
        children={[
          { path: "onboarding", element: <Onboarding /> },
          { path: "chat", element: <Chat /> },
        ]}
      />
    </Routes>
  );
}

export default App;

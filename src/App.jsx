import { Route, Routes } from "react-router";

import Login from "@/components/auth/Login";
import SignUp from "@/components/auth/SignUp";
import Chat from "@/pages/Chat";
import Home from "@/pages/Home";
import Onboarding from "@/pages/Onboarding";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/onboarding" element={<Onboarding />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/dashboard" element={<Chat />} />
    </Routes>
  );
}

export default App;

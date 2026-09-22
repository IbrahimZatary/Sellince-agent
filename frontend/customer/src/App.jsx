import { Route, Routes } from "react-router";

import Checkout from "@/pages/Checkout";
import Chat from "@/pages/Chat";
import Home from "@/pages/Home";
import Login from "@/components/auth/Login";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/chat" element={<Chat />} />
      </Route>
      <Route path="/checkout" element={<Checkout />} />
      <Route path="/dashboard" element={<Login />} />
    </Routes>
  );
}

export default App;

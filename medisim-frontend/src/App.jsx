import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import LoginForm from "./components/LoginForm";
import CaseList from "./components/CaseList";
import ChatWindow from "./components/ChatWindow";
import Navbar from "./components/Navbar";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("access"));

  return (
    <BrowserRouter>
      {loggedIn && <Navbar />}   {/* only show when logged in */}
      <Routes>
        <Route
          path="/login"
          element={<LoginForm onLogin={() => setLoggedIn(true)} />}
        />
        <Route
          path="/cases"
          element={loggedIn ? <CaseList /> : <Navigate to="/login" />}
        />
        <Route
          path="/runs/:id"
          element={loggedIn ? <ChatWindow /> : <Navigate to="/login" />}
        />
        <Route path="*" element={<Navigate to="/cases" />} />
      </Routes>
    </BrowserRouter>
  );
}
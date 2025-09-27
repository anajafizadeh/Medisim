import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState } from "react";
import LoginForm from "./components/LoginForm";
import CaseList from "./components/CaseList";
import ChatWindow from "./components/ChatWindow";
import CaseBuilder from "./pages/CaseBuilder";
import AppLayout from "./components/AppLayout";
import SignupForm from "./components/SignupForm";


export default function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("access"));

  return (
    <BrowserRouter>
      <Routes>
        {/* Public route */}
        <Route
          path="/login"
          element={<LoginForm onLogin={() => setLoggedIn(true)} />}
        />

        {/* Protected routes */}
        <Route
          path="/cases"
          element={
            loggedIn ? (
              <AppLayout>
                <CaseList />
              </AppLayout>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/runs/:id"
          element={
            loggedIn ? (
              <AppLayout>
                <ChatWindow />
              </AppLayout>
            ) : (
              <Navigate to="/login" />
            )
          }
        />
        <Route
          path="/instructor/cases/new"
          element={
            loggedIn ? (
              <AppLayout>
                <CaseBuilder />
              </AppLayout>
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        {/* Fallback */}
        <Route
          path="*"
          element={<Navigate to={loggedIn ? "/cases" : "/login"} />}
        />
        <Route path="/signup" element={<SignupForm />} />
      </Routes>
    </BrowserRouter>
  );
}
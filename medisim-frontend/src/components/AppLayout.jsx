import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function AppLayout({ children }) {
  const navigate = useNavigate();
  const [role, setRole] = useState(null);

  useEffect(() => {
    // Fetch role from localStorage (or later from an API like /me/)
    const storedRole = localStorage.getItem("role");
    if (storedRole) setRole(storedRole);
  }, []);

  function handleLogout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("role"); // clear role on logout
    navigate("/login");
  }

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="p-4 border-b bg-blue-600 text-white flex justify-between items-center shadow">
        <h1 className="text-xl font-bold">
          <Link to="/cases" className="hover:text-white text-white" >Medisim</Link>
        </h1>
        <nav className="flex gap-4 items-center">
          <Link to="/cases" className="hover:text-white text-white">
            Cases
          </Link>

          {/* Instructor-only nav item */}
          {role === "instructor" && (
            <Link
              to="/instructor/cases/new"
              className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-200 transition"
            >
              + Create Case
            </Link>
          )}

          <button
            onClick={handleLogout}
            className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-200 transition"
          >
            Logout
          </button>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}

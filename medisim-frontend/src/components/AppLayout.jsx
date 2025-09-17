import { Link, useNavigate } from "react-router-dom";

export default function AppLayout({ children }) {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  }

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="p-4 border-b bg-blue-600 text-white flex justify-between items-center shadow">
        <h1 className="text-xl font-bold">
          <Link to="/cases">Medisim</Link>
        </h1>
        <nav className="flex gap-4">
          <Link to="/cases" className="hover:underline">
            Cases
          </Link>
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
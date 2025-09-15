import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  function handleLogout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  }

  return (
    <nav className="bg-blue-600 text-white px-6 py-3 flex items-center justify-between shadow-md">
      {/* Left side: logo */}
      <Link to="/cases" className="text-xl font-bold hover:text-gray-200">
        Medisim
      </Link>

      {/* Right side: links + logout */}
      <div className="flex items-center gap-6">
        <Link to="/cases" className="hover:text-gray-200">
          Cases
        </Link>
        <button
          onClick={handleLogout}
          className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-100 transition"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
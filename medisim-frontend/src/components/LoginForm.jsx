import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await client.post("/token/", { username, password });
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      onLogin();
      navigate("/cases");
    } catch (err) {
      setError("Invalid username or password");
    }
  }

  return (
    <div className="flex h-screen items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-xl shadow-md w-80"
      >
        <h1 className="text-2xl font-bold text-center mb-2 text-blue-600">
          Medisim
        </h1>
        <p className="text-center text-gray-500 mb-6">
          Virtual patient practice
        </p>
        <input
          className="border p-2 w-full mb-2 rounded"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="border p-2 w-full mb-2 rounded"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="text-red-500 text-sm mb-2">{error}</p>}
        <button
          className="bg-blue-500 w-full text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          type="submit"
        >
          Login
        </button>
      </form>
    </div>
  );
}
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      // 1. Get JWT tokens
      const res = await client.post("/token/", { username, password });
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // 2. Fetch user info (/me/) and store role
      const meRes = await client.get("/me/");
      localStorage.setItem("role", meRes.data.role);

      // 3. Continue normal login flow
      onLogin();
      navigate("/cases");
    } catch (err) {
      alert("Login failed");
    }
  }

  return (
    <div className="w-screen h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="w-full max-w-sm p-6 bg-white shadow-lg rounded-lg">
        <h2 className="text-2xl font-bold text-center text-blue-600 mb-2">Medisim</h2>
        <p className="text-center text-gray-600 mb-6">Virtual patient practice</p>

        <input
          className="border p-2 w-full mb-3 rounded"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="border p-2 w-full mb-3 rounded"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

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

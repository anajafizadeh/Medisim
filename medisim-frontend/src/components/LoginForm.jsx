import { useState } from "react";
import { useNavigate } from "react-router-dom";   // 👈 add this
import client from "../api/client";

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();                // 👈 hook

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await client.post("/token/", { username, password });
      console.log("Login success:", res.data);
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      onLogin();
      navigate("/cases");                         // 👈 redirect to cases page
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      alert("Login failed");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-sm mx-auto p-4 bg-white shadow rounded">
      <h2 className="text-lg font-bold mb-2">Login</h2>
      <input
        className="border p-2 w-full mb-2"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded" type="submit">
        Login
      </button>
    </form>
  );
}
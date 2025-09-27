import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function SignupForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await client.post("/signup/", { username, password, role });
      alert("Account created! Please log in.");
      navigate("/login");
    } catch (err) {
      alert("Signup failed: " + (err.response?.data?.detail || "Unknown error"));
    }
  }

  return (
    <div className="w-screen h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-sm p-6 bg-white shadow-lg rounded-lg"
      >
        <h2 className="text-2xl font-bold text-center text-blue-600 mb-2">
          Medisim
        </h2>
        <p className="text-center text-gray-600 mb-6">Sign up for an account</p>

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

        <select
          className="border p-2 w-full mb-3 rounded"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <option value="student">Student</option>
          <option value="instructor">Instructor</option>
        </select>

        <button
          className="bg-blue-500 w-full text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          type="submit"
        >
          Sign Up
        </button>
      </form>
    </div>
  );
}

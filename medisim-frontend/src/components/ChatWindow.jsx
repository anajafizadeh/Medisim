import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import client from "../api/client";

export default function ChatWindow() {
  const { id: runId } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  // Fetch messages from backend
  async function fetchMessages() {
    const res = await client.get(`/runs/${runId}/messages/`);
    console.log("Fetched messages:", res.data);
    setMessages(res.data);
  }

  // Initial + polling every 2s
  useEffect(() => {
    fetchMessages();
    const interval = setInterval(fetchMessages, 2000);
    return () => clearInterval(interval);
  }, [runId]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;

    await client.post(`/runs/${runId}/messages/`, {
      sender: "student",
      text: input,
    });

    await fetchMessages();
    setInput("");
  }

  return (
  <div className="w-screen h-screen flex flex-col bg-gray-100">
    {/* Header */}
    <div className="p-4 border-b bg-white shadow flex justify-between items-center">
      <h2 className="text-xl font-bold">Case #{runId}</h2>
      <button
        onClick={() => navigate("/cases")}
        className="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition"
      >
        ← Back to Cases
      </button>
    </div>

    {/* Messages */}
    <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-3 w-full">
      {messages.map((m) => (
        <div
          key={m.id}
          className={`flex w-full ${
            m.sender === "student" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`p-3 rounded-lg max-w-md break-words ${
              m.sender === "student"
                ? "bg-blue-500 text-white"
                : "bg-gray-200 text-black"
            }`}
          >
            {m.text}
          </div>
        </div>
      ))}
    </div>

    {/* Input */}
    <form
      onSubmit={sendMessage}
      className="p-4 bg-white border-t flex gap-2 sticky bottom-0 w-full"
    >
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-1 border rounded px-3 py-2"
        placeholder="Type your message..."
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
      >
        Send
      </button>
    </form>
  </div>
);
}
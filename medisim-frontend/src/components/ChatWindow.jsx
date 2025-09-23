import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import client from "../api/client";

function PatientInfo({ patient }) {
  if (!patient) {
    return (
      <div className="w-1/3 bg-gray-50 p-6 border-l border-gray-200">
        <h2 className="text-lg font-semibold mb-4">Patient Info</h2>
        <p className="text-gray-500">Loading patient data...</p>
      </div>
    );
  }

  return (
    <div className="w-1/3 bg-gray-50 p-6 border-l border-gray-200">
      <h2 className="text-lg font-semibold mb-4">Patient Info</h2>
      <div className="space-y-2">
        <p><span className="font-medium">Name:</span> {patient.name}</p>
        <p><span className="font-medium">Age:</span> {patient.age}</p>
        <p><span className="font-medium">Gender:</span> {patient.gender}</p>
        <div>
          <span className="font-medium">History:</span>
          <ul className="list-disc list-inside ml-2">
            {patient.history?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default function ChatWindow() {
  const { id: runId } = useParams();
  const [messages, setMessages] = useState([]);
  const [patient, setPatient] = useState(null);
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  // 🔹 Fetch messages
  async function fetchMessages() {
    const res = await client.get(`/runs/${runId}/messages/`);
    setMessages(res.data);
  }

  // 🔹 Fetch patient info
  async function fetchPatient() {
    try {
      const res = await client.get(`/runs/${runId}/patient/`);
      setPatient(res.data);
    } catch (err) {
      console.error("Error fetching patient info:", err);
    }
  }

  useEffect(() => {
    fetchMessages();
    fetchPatient();

    const interval = setInterval(fetchMessages, 2000);
    return () => clearInterval(interval);
  }, [runId]);

  async function sendMessage(e) {
    e.preventDefault();
    if (!input.trim()) return;

    await client.post(`/runs/${runId}/messages/`, { sender: "student", text: input });
    await fetchMessages();
    setInput("");
  }

  return (
    <div className="w-screen h-screen flex">
      {/* Chat Section */}
      <div className="flex flex-col flex-1 bg-gray-100">
        {/* Header */}
        <div className="p-4 border-b bg-white shadow flex items-center justify-between">
          <h2 className="text-lg font-bold">Case #{runId}</h2>
          <div className="flex gap-2">
            <button
              onClick={() => navigate("/cases")}
              className="bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition"
            >
              ← Back to Cases
            </button>
            <button
              onClick={() => { localStorage.clear(); navigate("/login"); }}
              className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-3 w-full">
          {messages.map((m) => (
            <div key={m.id} className={`flex w-full ${m.sender === "student" ? "justify-end" : "justify-start"}`}>
              <div
                className={`p-3 rounded-lg max-w-md break-words ${
                  m.sender === "student" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"
                }`}
              >
                {m.text}
              </div>
            </div>
          ))}
        </div>

        {/* Input */}
        <form onSubmit={sendMessage} className="p-4 bg-white border-t flex gap-2 sticky bottom-0 w-full">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-1 border rounded px-3 py-2"
            placeholder="Type your message..."
          />
          <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">
            Send
          </button>
        </form>
      </div>

      {/* Patient Info Sidebar */}
      <PatientInfo patient={patient} />
    </div>
  );
}
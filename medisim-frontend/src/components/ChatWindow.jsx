import { useEffect, useState } from "react";
import client from "../api/client";

export default function ChatWindow({ runId }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    client.get(`/runs/${runId}/messages/`).then((res) => setMessages(res.data));
  }, [runId]);

  async function sendMessage() {
    const res = await client.post(`/runs/${runId}/messages/`, {
      sender: "student",
      text,
    });
    setMessages((prev) => [...prev, res.data]);
    setText("");
  }

  return (
    <div className="p-4 border rounded">
      <div className="h-64 overflow-y-auto border mb-2 p-2 bg-gray-50">
        {messages.map((m) => (
          <div key={m.id} className={m.sender === "student" ? "text-right" : "text-left"}>
            <span className="inline-block bg-white shadow px-2 py-1 rounded m-1">
              <b>{m.sender}:</b> {m.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          className="border flex-1 p-2"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your message"
        />
        <button onClick={sendMessage} className="bg-blue-500 text-white px-4 ml-2 rounded">
          Send
        </button>
      </div>
    </div>
  );
}
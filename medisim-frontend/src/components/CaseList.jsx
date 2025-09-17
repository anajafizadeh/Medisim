import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function CaseList() {
  const [cases, setCases] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    client.get("/cases/").then((res) => setCases(res.data));
  }, []);

  async function startCase(caseId) {
    const res = await client.post("/runs/", { case: caseId });
    navigate(`/runs/${res.data.id}`);
  }

  return (
    <div className="w-screen h-screen flex flex-col bg-gray-100">
      {/* header */}
      <div className="p-4 border-b bg-white shadow flex items-center justify-between">
        <h2 className="text-xl font-bold text-gray-800">Available Cases</h2>
        <button
          onClick={() => {
            localStorage.clear();
            navigate("/login");
          }}
          className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
        >
          Logout
        </button>
      </div>

      {/* grid wrapper */}
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="grid grid-cols-3 gap-6">
          {cases.map((c) => (
            <div key={c.id} className="bg-white p-4 shadow rounded-lg flex flex-col">
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-gray-800">{c.title}</h3>
                <p className="text-sm text-gray-600">{c.specialty}</p>
                <span className="inline-block mt-2 text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                  {c.difficulty}
                </span>
              </div>
              <button
                onClick={() => startCase(c.id)}
                className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
              >
                Start Case
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

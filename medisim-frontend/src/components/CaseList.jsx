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
    <div className="p-6 bg-gray-50 min-h-screen">
      <h2 className="text-2xl font-bold mb-6">Available Cases</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {cases.map((c) => (
          <div
            key={c.id}
            className="bg-white shadow rounded-lg p-4 hover:shadow-md transition"
          >
            <h3 className="text-lg font-bold">{c.title}</h3>
            <p className="text-sm text-gray-500 mb-2">{c.specialty}</p>
            <span className="inline-block px-2 py-1 text-xs rounded bg-blue-100 text-blue-700">
              {c.difficulty}
            </span>
            <button
              onClick={() => startCase(c.id)}
              className="mt-3 w-full bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600 transition"
            >
              Start Case
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
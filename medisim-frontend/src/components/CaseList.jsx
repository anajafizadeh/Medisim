import { useEffect, useState } from "react";
import client from "../api/client";
import { Link } from "react-router-dom";

export default function CaseList() {
  const [cases, setCases] = useState([]);

  useEffect(() => {
    client.get("/cases/").then((res) => setCases(res.data));
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Available Cases</h2>
      <ul>
        {cases.map((c) => (
          <li key={c.id} className="mb-2">
            <Link className="text-blue-600" to={`/runs/${c.id}`}>
              {c.title} ({c.specialty})
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
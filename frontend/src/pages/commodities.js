import { useEffect, useState } from "react";
import { getCommodities } from "../services/api";

function Commodities() {
  const [commodities, setCommodities] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getCommodities()
      .then(res => {
        if (res.success) setCommodities(res.data);
        else setError("Failed to load commodities");
      })
      .catch(() => setError("Backend not reachable"));
  }, []);

  return (
    <div>
      <h2>Commodities</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <ul>
        {commodities.map(c => (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
    </div>
  );
}


export default Commodities;

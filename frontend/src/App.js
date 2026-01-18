import { useEffect, useState } from "react";

function App() {
  const [commodities, setCommodities] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/commodities")
      .then(res => res.json())
      .then(data => {
        console.log("API RESPONSE:", data); // 👈 IMPORTANT
        setCommodities(data);
      })
      .catch(err => {
        console.error("FETCH ERROR:", err);
        setError("Fetch failed");
      });
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Commodity Storage Management</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <pre>{JSON.stringify(commodities, null, 2)}</pre>
    </div>
  );
}

export default App;

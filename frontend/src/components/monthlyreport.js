import { useEffect, useState } from "react";

function MonthlyReport() {
  const [report, setReport] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
  fetch("http://localhost:5000/reports/monthly-net")
    .then(res => res.json())
    .then(data => {
      console.log("MONTHLY API RESPONSE:", data);
      setReport(data.data || []);
    })
    .catch(err => {
      console.error(err);
      setError("Failed to load monthly report");
    });
}, []);

  return (
    <div>
      <h2>Monthly Net Movement</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Commodity ID</th>
            <th>Year</th>
            <th>Month</th>
            <th>Net Quantity</th>
          </tr>
        </thead>
        <tbody>
          {report.map((row, index) => (
            <tr key={index}>
              <td>{row.commodity_id}</td>
              <td>{row.year}</td>
              <td>{row.month}</td>
              <td>{row.net_quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MonthlyReport;
/// MONTHLY

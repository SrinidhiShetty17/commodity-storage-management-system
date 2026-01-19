import React, { useEffect, useState } from "react";

function MonthlyReport() {
  const [report, setReport] = useState([]);
  const [commodityId, setCommodityId] = useState("");
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
const filteredReport = report.filter((row) => {
  return (
    (commodityId === "" || row.commodity_id === Number(commodityId)) &&
    (year === "" || row.year === Number(year)) &&
    (month === "" || row.month === Number(month))
  );
});


  useEffect(() => {
    fetch("http://localhost:5000/reports/monthly")
      .then(res => res.json())
      .then(data => {
        console.log("MONTHLY API RESPONSE:", data);
        setReport(data);
      })
      .catch(err => {
        console.error("Error fetching monthly report:", err);
      });
  }, []);

  return (
    <div>
      <h2>Monthly Net Movement</h2>
<div style={{ marginBottom: "20px" }}>
  <label>
    Commodity ID:
    <input
      type="number"
      value={commodityId}
      onChange={(e) => setCommodityId(e.target.value)}
      style={{ marginRight: "10px", marginLeft: "5px" }}
    />
  </label>

  <label>
    Year:
    <input
      type="number"
      value={year}
      onChange={(e) => setYear(e.target.value)}
      style={{ marginRight: "10px", marginLeft: "5px" }}
    />
  </label>

  <label>
    Month:
    <input
      type="number"
      min="1"
      max="12"
      value={month}
      onChange={(e) => setMonth(e.target.value)}
      style={{ marginLeft: "5px" }}
    />
  </label>
</div>

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
          {report.length === 0 ? (
            <tr>
              <td colSpan="4">No data available</td>
            </tr>
          ) : (
            filteredReport.map((row, index) => (
              <tr key={index}>
                <td>{row.commodity_id}</td>
                <td>{row.year}</td>
                <td>{row.month}</td>
                <td>{row.net_quantity}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default MonthlyReport;

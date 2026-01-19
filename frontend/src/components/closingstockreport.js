import React, { useEffect, useState } from "react";

function ClosingStockReport() {
  const [closingStock, setClosingStock] = useState([]);
  const [commodityId, setCommodityId] = useState("");                        
  const [year, setYear] = useState("");
  const [month, setMonth] = useState("");
  const filteredClosingStock = closingStock.filter((row) => {
  return (
    (commodityId === "" || row.commodity_id === Number(commodityId)) &&
    (year === "" || row.year === Number(year)) &&
    (month === "" || row.month === Number(month))
  );
});


  useEffect(() => {
    fetch("http://localhost:5000/reports/monthly-closing")
      .then(res => res.json())
      .then(data => {
        console.log("CLOSING STOCK API RESPONSE:", data);
        setClosingStock(data);
      })
      .catch(err => {
        console.error("Error fetching closing stock report:", err);
      });
  }, []);

  return (
    <div style={{ marginTop: "40px" }}>
      <h2>Monthly Closing Stock</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Commodity ID</th>
            <th>Year</th>
            <th>Month</th>
            <th>Closing Stock</th>
          </tr>
        </thead>

        <tbody>
          {closingStock.length === 0 ? (
            <tr>
              <td colSpan="4">No data available</td>
            </tr>
          ) : (
            filteredClosingStock.map((row, index) => (
              <tr key={index}>
                <td>{row.commodity_id}</td>
                <td>{row.year}</td>
                <td>{row.month}</td>
                <td>{row.closing_stock}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ClosingStockReport;

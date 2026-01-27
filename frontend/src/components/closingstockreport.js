import React, { useEffect, useState } from "react";
import axios from "axios";

function ClosingStockReport() {
  // ================= STATES =================
  const [closingStock, setClosingStock] = useState([]);
  const [commodities, setCommodities] = useState([]);

  const [selectedCommodity, setSelectedCommodity] = useState("");
  const [selectedMonth, setSelectedMonth] = useState("");
  const [selectedYear, setSelectedYear] = useState("");

  // ================= FETCH COMMODITIES =================
  useEffect(() => {
    axios
      .get("http://localhost:5000/commodities")
      .then((res) => {
        // 🔐 SAFETY: force array
        if (Array.isArray(res.data)) {
          setCommodities(res.data);
        } else if (Array.isArray(res.data.data)) {
          setCommodities(res.data.data);
        } else {
          setCommodities([]);
        }
      })
      .catch((err) => {
        console.error("Commodity fetch error:", err);
        setCommodities([]);
      });
  }, []);

  // ================= FETCH CLOSING STOCK =================
  useEffect(() => {
    const params = {};

    if (selectedCommodity) params.commodity_id = selectedCommodity;
    if (selectedMonth) params.month = selectedMonth;
    if (selectedYear) params.year = selectedYear;

    axios
      .get("http://localhost:5000/closing-stock-report", { params })
      .then((res) => {
        console.log("CLOSING STOCK API RESPONSE:", res.data);

        // 🔐 SAFETY: always array
        if (Array.isArray(res.data)) {
          setClosingStock(res.data);
        } else if (Array.isArray(res.data.data)) {
          setClosingStock(res.data.data);
        } else {
          setClosingStock([]);
        }
      })
      .catch((err) => {
        console.error("Closing stock fetch error:", err);
        setClosingStock([]);
      });
  }, [selectedCommodity, selectedMonth, selectedYear]);

  // ================= UI =================
  return (
    <div style={{ marginTop: "40px" }}>
      <h2>Monthly Closing Stock Report</h2>

      {/* ================= FILTERS ================= */}
      <div style={{ marginBottom: "20px" }}>
        {/* Commodity Dropdown */}
        <select
          value={selectedCommodity}
          onChange={(e) => setSelectedCommodity(e.target.value)}
        >
          <option value="">All Commodities</option>
          {Array.isArray(commodities) &&
            commodities.map((c) => (
              <option key={c.commodity_id} value={c.commodity_id}>
                {c.commodity_name}
              </option>
            ))}
        </select>

        {/* Month Dropdown */}
        <select
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          style={{ marginLeft: "10px" }}
        >
          <option value="">All Months</option>
          {[1,2,3,4,5,6,7,8,9,10,11,12].map((m) => (
            <option key={m} value={m}>
              {m}
            </option>
          ))}
        </select>

        {/* Year Dropdown */}
        <select
          value={selectedYear}
          onChange={(e) => setSelectedYear(e.target.value)}
          style={{ marginLeft: "10px" }}
        >
          <option value="">All Years</option>
          {[2023, 2024, 2025, 2026].map((y) => (
            <option key={y} value={y}>
              {y}
            </option>
          ))}
        </select>
      </div>

      {/* ================= TABLE ================= */}
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Commodity</th>
            <th>Year</th>
            <th>Month</th>
            <th>Closing Stock</th>
          </tr>
        </thead>

        <tbody>
          {closingStock.length === 0 ? (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>
                No data available
              </td>
            </tr>
          ) : (
            closingStock.map((row, index) => (
              <tr key={index}>
                <td>{row.commodity_name}</td>
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

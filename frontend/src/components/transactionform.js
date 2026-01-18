import { useEffect, useState } from "react";

function TransactionForm() {
  const [commodities, setCommodities] = useState([]);
  const [availableStock, setAvailableStock] = useState(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const [form, setForm] = useState({
    commodity_id: "",
    transaction_type: "IN",
    quantity: "",
    date: "",
  });

  // 🔹 Load commodities
  useEffect(() => {
    fetch("http://localhost:5000/commodities")
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setCommodities(data.data);
        }
      })
      .catch(() => setError("Failed to load commodities"));
  }, []);

  // 🔹 Fetch available stock when commodity + date changes
  useEffect(() => {
    if (!form.commodity_id || !form.date) return;

    fetch(
      `http://localhost:5000/stock/available?commodity_id=${form.commodity_id}&date=${form.date}`
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setAvailableStock(Number(data.available_stock));
        } else {
          setAvailableStock(null);
        }
      })
      .catch(() => setAvailableStock(null));
  }, [form.commodity_id, form.date]);

  // 🔹 Handle input change
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // 🔹 Handle submit
  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    if (
      form.transaction_type === "OUT" &&
      availableStock !== null &&
      Number(form.quantity) > availableStock
    ) {
      setError("Insufficient stock for OUT transaction");
      return;
    }

    const payload = {
      commodity_id: Number(form.commodity_id),
      transaction_type: form.transaction_type,
      quantity: Number(form.quantity),
      transaction_date: form.date,
    };

    fetch("http://localhost:5000/transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setMessage("Transaction saved successfully");

          // 🔹 Reset form
          setForm({
            commodity_id: "",
            transaction_type: "IN",
            quantity: "",
            date: "",
          });

          setAvailableStock(null);
        } else {
          setError(data.error || "Transaction failed");
        }
      })
      .catch(() => setError("Server error"));
  };

  return (
    <div style={{ padding: "20px", maxWidth: "400px" }}>
      <h2>Add Transaction</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {message && <p style={{ color: "green" }}>{message}</p>}

      <form onSubmit={handleSubmit}>
        {/* Commodity */}
        <select
          name="commodity_id"
          value={form.commodity_id}
          onChange={handleChange}
          required
        >
          <option value="">Select Commodity</option>
          {commodities.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <br /><br />

        {/* Transaction Type */}
        <select
          name="transaction_type"
          value={form.transaction_type}
          onChange={handleChange}
        >
          <option value="IN">IN</option>
          <option value="OUT">OUT</option>
        </select>

        <br /><br />

        {/* Quantity */}
        <input
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={form.quantity}
          onChange={handleChange}
          required
        />

        <br /><br />

        {/* Date */}
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          required
        />

        <br /><br />

        {/* Available stock */}
        {availableStock !== null && (
          <p>
            Available Stock: <strong>{availableStock}</strong>
          </p>
        )}

        {/* Save button */}
        <button
          type="submit"
          disabled={
            form.transaction_type === "OUT" &&
            availableStock !== null &&
            Number(form.quantity) > availableStock
          }
        >
          Save
        </button>
      </form>
    </div>
  );
}

export default TransactionForm;
///TRANSACTION
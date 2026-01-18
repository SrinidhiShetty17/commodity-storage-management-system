const BASE_URL = "http://127.0.0.1:5000";

export const getCommodities = async () => {
  const res = await fetch(`${BASE_URL}/commodities`);
  return res.json();
};

export const createTransaction = async (payload) => {
  const res = await fetch(`${BASE_URL}/transactions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return res.json();
};

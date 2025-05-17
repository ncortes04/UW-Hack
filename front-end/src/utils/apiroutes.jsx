// utils/apiroutes.js
const BASE_URL = "http://localhost:5000";

export const sendUserInput = async (text) => {
  const res = await fetch(`${BASE_URL}/api/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!res.ok) {
    throw new Error("Failed to fetch from server");
  }

  // ✅ Parse the JSON response
  const data = await res.json();
  return data;
};

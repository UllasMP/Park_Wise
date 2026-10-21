// All calls to the Django backend live here, so components stay simple.
// The server sends errors as { code, message }; we throw that object.

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch("/api" + path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw { code: "NETWORK", message: "Cannot reach the server. Is the backend running?" };
  }
  const data = await response.json();
  if (!response.ok) throw data;
  return data;
}

const post = (path, body) => request(path, { method: "POST", body: JSON.stringify(body) });

export const api = {
  getSlots: (gate) => request("/slots/?gate=" + encodeURIComponent(gate)),
  setSlotBlocked: (gate, number, blocked) => post("/slots/block/", { gate, number, blocked }),
  issueTicket: (body) => post("/entry/", body),
  lookupExit: (q) => request("/exit/lookup/?q=" + encodeURIComponent(q)),
  collectPayment: (body) => post("/exit/collect/", body),
  getDashboard: (gate) => request("/dashboard/?gate=" + encodeURIComponent(gate)),
  getClock: () => request("/dev/clock/"),
  advanceClock: (minutes) => post("/dev/clock/", { minutes }),
  resetData: () => post("/dev/reset/", {}),
};

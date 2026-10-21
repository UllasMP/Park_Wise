import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { useParking } from "../context/ParkingContext.jsx";
import { formatTime } from "../utils.js";

// DEV ONLY: move the server clock forward so time rules can be tested.
export default function DevClock() {
  const { refreshAll } = useParking();
  const [clock, setClock] = useState(null);

  const loadClock = () => api.getClock().then(setClock).catch(() => {});
  useEffect(() => { loadClock(); }, []);

  async function advance(minutes) {
    setClock(await api.advanceClock(minutes));
    refreshAll();
  }

  async function reset() {
    await api.resetData();
    loadClock();
    refreshAll();
  }

  return (
    <footer className="dev-clock">
      <strong>Dev tools</strong>
      <span>Server time: {clock ? formatTime(clock.server_time) : "..."}</span>
      <button onClick={() => advance(60)}>+1 hour</button>
      <button onClick={() => advance(1440)}>+1 day</button>
      <button onClick={reset}>Clear all data</button>
    </footer>
  );
}

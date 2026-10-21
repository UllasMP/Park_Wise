import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { TYPE_LABEL, formatStay, formatTime } from "../utils.js";

// Pop-up with the full ticket of a booked slot. Everything comes from the server.
export default function TicketDetails({ ticket, onClose }) {
  const [info, setInfo] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api.lookupExit(ticket).then(setInfo).catch((err) => setError(err.message));
  }, [ticket]);

  return (
    <div className="overlay" onClick={onClose}>
      {/* stopPropagation: clicking inside the card should not close it */}
      <div className="card modal" onClick={(e) => e.stopPropagation()}>
        <h3>Ticket {ticket}</h3>
        {error && <p className="error">{error}</p>}
        {!info && !error && <p>Loading...</p>}
        {info && (
          <>
            <p className="big">{info.gate} · Slot {info.slot}</p>
            <p>Vehicle {info.vehicle_number} · {TYPE_LABEL[info.vehicle_type]}</p>
            <p>In: {formatTime(info.entry_time)}</p>
            <p>Stay so far: {formatStay(info.stay_minutes)}</p>
            <p>Fee if paid now: ₹{info.fee.fee}</p>
          </>
        )}
        <button className="primary" onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

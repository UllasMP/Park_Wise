import { useState } from "react";
import { api } from "../api/client.js";
import { useParking } from "../context/ParkingContext.jsx";
import { TYPE_LABEL, formatStay, formatTime } from "../utils.js";

// Shows how the server worked out the fee (the server sends these numbers).
function FeeBreakdown({ fee }) {
  return (
    <ul className="breakdown">
      <li>Base fee (first 2 hours): ₹{fee.base}</li>
      {fee.extra_hours > 0 && (
        <li>{fee.extra_hours} extra hour(s) × ₹{fee.hourly_rate} = ₹{fee.extra_charge}</li>
      )}
      {fee.extra_days > 0 && (
        <li>{fee.extra_days} extra day(s) after 24 hours × ₹{fee.day_fee} = ₹{fee.day_charge}</li>
      )}
      <li><strong>Fee: ₹{fee.fee}</strong></li>
    </ul>
  );
}

// Screen 2: find the vehicle, show the fee, collect payment, release the slot.
export default function ExitPage() {
  const { gate, refreshAll } = useParking();
  const [query, setQuery] = useState("");
  const [info, setInfo] = useState(null);       // lookup result
  const [receipt, setReceipt] = useState(null); // shown after payment
  const [method, setMethod] = useState("CASH");
  const [error, setError] = useState("");

  async function handleLookup(event) {
    event.preventDefault();
    setError("");
    setReceipt(null);
    try {
      setInfo(await api.lookupExit(query));
    } catch (err) {
      setInfo(null);
      setError(err.message);
    }
  }

  async function handleCollect() {
    setError("");
    try {
      // The server calculates the fee again at this moment.
      const newReceipt = await api.collectPayment({ q: info.ticket, payment_method: method, gate });
      setReceipt(newReceipt);
      setInfo(null);
      setQuery("");
      refreshAll();
    } catch (err) {
      setError(err.message);
    }
  }

  const fee = info ? info.fee.fee : 0;
  return (
    <div className="narrow">
      <form className="card" onSubmit={handleLookup}>
        <h2>Exit and payment</h2>
        <p className="muted">Collecting at {gate}</p>
        <label>
          Vehicle number (or last 4 digits) or ticket number
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="1234, KA01AB1234 or PK-0001" />
        </label>
        <button className="primary" type="submit">Find vehicle</button>
      </form>

      {error && <p className="error">{error}</p>}

      {info && (
        <div className="card">
          <h3>{info.ticket} · {info.gate} · Slot {info.slot}</h3>
          <p>{info.vehicle_number} · {TYPE_LABEL[info.vehicle_type]}</p>
          <p>In: {formatTime(info.entry_time)} · Now: {formatTime(info.time_now)}</p>
          <p>Stay: {formatStay(info.stay_minutes)} ({info.stay_minutes} min)</p>
          <FeeBreakdown fee={info.fee} />

          <div className="type-toggle">
            {["CASH", "UPI"].map((m) => (
              <button key={m} className={m === method ? "toggle active" : "toggle"} onClick={() => setMethod(m)}>
                {m === "CASH" ? "Cash" : "UPI"}
              </button>
            ))}
          </div>
          <button className="primary" onClick={handleCollect}>
            {fee === 0 ? "Exit (free)" : `Collect ₹${fee} & release slot`}
          </button>
        </div>
      )}

      {receipt && (
        <div className="card ticket">
          <h3>Receipt · {receipt.ticket}</h3>
          <p>Vehicle {receipt.vehicle_number} · {TYPE_LABEL[receipt.vehicle_type]}</p>
          <p>Entered at {receipt.gate} (slot {receipt.slot}) · Paid at {receipt.exit_gate}</p>
          <p>In: {formatTime(receipt.entry_time)}</p>
          <p>Out: {formatTime(receipt.exit_time)}</p>
          <p>Stay: {formatStay(receipt.stay_minutes)}</p>
          <p className="big">₹{receipt.amount} · {receipt.payment_method === "CASH" ? "Cash" : "UPI"}</p>
        </div>
      )}
    </div>
  );
}

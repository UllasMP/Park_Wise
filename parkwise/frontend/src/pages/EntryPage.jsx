import { useState } from "react";
import { api } from "../api/client.js";
import SlotMap from "../components/SlotMap.jsx";
import { useParking } from "../context/ParkingContext.jsx";
import { TYPE_LABEL, formatTime } from "../utils.js";

// Screen 1: type the vehicle number, pick a type, issue a ticket.
export default function EntryPage() {
  const { gate, refreshAll, setJustAssigned } = useParking();
  const [vehicleNumber, setVehicleNumber] = useState("");
  const [vehicleType, setVehicleType] = useState("4W");
  const [ticket, setTicket] = useState(null);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      // The server picks the slot and checks every rule.
      const newTicket = await api.issueTicket({
        vehicle_number: vehicleNumber, vehicle_type: vehicleType, gate,
      });
      setTicket(newTicket);
      setJustAssigned(newTicket.slot);
      setVehicleNumber("");
      refreshAll(); // slot map + counts come from the server again
    } catch (err) {
      setTicket(null);
      setError(err.message);
    }
  }

  return (
    <div className="two-columns">
      <SlotMap />

      <div>
        <form className="card" onSubmit={handleSubmit}>
          <h2>Vehicle entry</h2>
          <p className="muted">Entering at {gate}</p>

          <label>
            Vehicle number
            <input value={vehicleNumber} onChange={(e) => setVehicleNumber(e.target.value)}
                   placeholder="MH 12 GH 3456" />
          </label>

          <div className="type-toggle">
            {["2W", "4W"].map((type) => (
              <button type="button" key={type}
                      className={type === vehicleType ? "toggle active" : "toggle"}
                      onClick={() => setVehicleType(type)}>
                {TYPE_LABEL[type]}
              </button>
            ))}
          </div>

          {error && <p className="error">{error}</p>}
          <button className="primary" type="submit">Issue ticket</button>
        </form>

        {ticket && (
          <div className="card ticket">
            <h3>Ticket {ticket.ticket}</h3>
            <p className="big">{ticket.gate} · Slot {ticket.slot}</p>
            <p>{ticket.level}</p>
            <p>Vehicle {ticket.vehicle_number}</p>
            <p>Type {TYPE_LABEL[ticket.vehicle_type]}</p>
            <p>In: {formatTime(ticket.entry_time)}</p>
          </div>
        )}
      </div>
    </div>
  );
}

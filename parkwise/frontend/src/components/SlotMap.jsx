import { useState } from "react";
import { api } from "../api/client.js";
import { useParking } from "../context/ParkingContext.jsx";
import { TYPE_LABEL } from "../utils.js";
import TicketDetails from "./TicketDetails.jsx";

// One slot. What a click does depends on the slot and on "manage mode":
//  - occupied slot -> open the ticket details
//  - free / blocked slot (manage mode only) -> block / unblock it
function SlotBox({ slot, manageMode, onClick }) {
  const { justAssigned } = useParking();
  // Black = occupied, white = free, grey = just assigned, striped = blocked
  let className = "slot " + slot.status;
  if (slot.number === justAssigned) className += " just-assigned";

  const clickable = slot.status === "occupied" || manageMode;
  return (
    <button className={className} disabled={!clickable} onClick={() => onClick(slot)}>
      <strong>{slot.number}</strong>
      <small>{slot.status === "blocked" ? "blocked" : slot.vehicle_number}</small>
    </button>
  );
}

// One group of slots (e.g. all 2-wheeler slots) with its free count.
function SlotGroup({ type, title, slots, counts, manageMode, onSlotClick }) {
  return (
    <section>
      <h3>{TYPE_LABEL[type]}: {counts.free} free of {counts.total}</h3>
      <p className="muted">{title}</p>
      <div className="slot-grid">
        {slots.map((slot) => (
          <SlotBox key={slot.number} slot={slot} manageMode={manageMode} onClick={onSlotClick} />
        ))}
      </div>
    </section>
  );
}

export default function SlotMap() {
  const { gate, slotData, refreshAll } = useParking();
  const [openTicket, setOpenTicket] = useState(null); // ticket shown in the pop-up
  const [manageMode, setManageMode] = useState(false); // block / unblock mode
  const [error, setError] = useState("");
  if (!slotData) return <p>Loading slots...</p>;

  async function handleSlotClick(slot) {
    setError("");
    if (slot.status === "occupied") {
      setOpenTicket(slot.ticket);
      return;
    }
    try {
      // free -> block, blocked -> unblock. The server checks the rules.
      await api.setSlotBlocked(gate, slot.number, slot.status === "free");
      refreshAll(); // counts and map come from the server again
    } catch (err) {
      setError(err.message);
    }
  }

  const slotsOfType = (type) => slotData.slots.filter((s) => s.type === type);
  const groupProps = { manageMode, onSlotClick: handleSlotClick };
  return (
    <div className={manageMode ? "slot-map manage-mode" : "slot-map"}>
      <h2>{gate} parking area</h2>

      <label className="manage-bar">
        <input type="checkbox" checked={manageMode} onChange={(e) => setManageMode(e.target.checked)} />
        Block / unblock slots
      </label>
      {manageMode && <p className="muted">Click a free slot to block it, or a blocked slot to unblock it.</p>}
      {error && <p className="error">{error}</p>}

      <SlotGroup type="2W" title="Ground level" slots={slotsOfType("2W")}
                 counts={slotData.counts["2W"]} {...groupProps} />
      <SlotGroup type="4W" title="Level 1" slots={slotsOfType("4W")}
                 counts={slotData.counts["4W"]} {...groupProps} />
      <p className="muted">Black = occupied (click for ticket) · White = free · Grey = just assigned · Striped = blocked</p>

      {openTicket && <TicketDetails ticket={openTicket} onClose={() => setOpenTicket(null)} />}
    </div>
  );
}

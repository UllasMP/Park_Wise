import { GATES, useParking } from "../context/ParkingContext.jsx";

// "No login: a simple picker at the top of the page". Switching gate switches
// the whole parking area (slots, counts) shown on every screen.
export default function GatePicker() {
  const { gate, setGate } = useParking();
  return (
    <div className="gate-picker">
      {GATES.map((name) => (
        <button key={name} className={name === gate ? "toggle active" : "toggle"}
                onClick={() => setGate(name)}>
          {name}
        </button>
      ))}
    </div>
  );
}

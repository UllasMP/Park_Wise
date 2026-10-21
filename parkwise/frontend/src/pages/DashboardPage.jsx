import { useEffect } from "react";
import { GATES, useParking } from "../context/ParkingContext.jsx";
import { TYPE_LABEL, formatStay, formatTime } from "../utils.js";

// Screen 3: free slots, money collected today, today's exits.
export default function DashboardPage() {
  const { gate, dashboard, refreshDashboard } = useParking();

  useEffect(() => { refreshDashboard(); }, [refreshDashboard]); // fresh data on open

  if (!dashboard) return <p>Loading dashboard...</p>;
  const { free_slots, total_collected_today, collected_by_gate, exits_today } = dashboard;

  return (
    <div>
      <div className="stats">
        <div className="card stat"><span>{gate}: 2-Wheeler free</span>
          <strong>{free_slots["2W"].free} / {free_slots["2W"].total}</strong></div>
        <div className="card stat"><span>{gate}: 4-Wheeler free</span>
          <strong>{free_slots["4W"].free} / {free_slots["4W"].total}</strong></div>
        <div className="card stat"><span>Collected today</span>
          <strong>₹{total_collected_today}</strong>
          {/* simple extra: how much each gate collected */}
          <small className="muted">{GATES.map((g) => `${g}: ₹${collected_by_gate[g]}`).join(" · ")}</small></div>
      </div>

      <div className="card">
        <h2>Today's exits</h2>
        {exits_today.length === 0 ? (
          <p className="muted">No vehicles have left yet today.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Ticket</th>
                <th>Vehicle</th>
                <th>Gate in / out</th>
                <th>In</th>
                <th>Out</th>
                <th>Stay</th>
                <th>Amount</th>
                <th>Method</th>
              </tr>
            </thead>
            <tbody>
              {exits_today.map((row) => (
                <tr key={row.ticket}>
                  <td>{row.ticket}</td>
                  <td>{row.vehicle_number} ({TYPE_LABEL[row.vehicle_type]})</td>
                  <td>{row.gate} / {row.exit_gate}</td>
                  <td>{formatTime(row.entry_time)}</td>
                  <td>{formatTime(row.exit_time)}</td>
                  <td>{formatStay(row.stay_minutes)}</td>
                  <td>₹{row.amount}</td>
                  <td>{row.payment_method === "CASH" ? "Cash" : "UPI"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

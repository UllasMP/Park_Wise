import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "../api/client.js";

// Shared state for the whole app (useContext - no Redux).
// Anything several screens need lives here: gate, slot map, dashboard data.
const ParkingContext = createContext(null);

export const GATES = ["Gate A", "Gate B"];

export function ParkingProvider({ children }) {
  const [gate, setGateState] = useState(GATES[0]);        // simple gate picker (no login)
  const [slotData, setSlotData] = useState(null);         // { counts, slots } of the picked gate
  const [dashboard, setDashboard] = useState(null);
  const [justAssigned, setJustAssigned] = useState(null); // slot shown in grey on the map
  const [loadError, setLoadError] = useState("");

  // Each gate has its own parking area, so changing gate shows different slots.
  function setGate(newGate) {
    setGateState(newGate);
    setJustAssigned(null);
  }

  const refreshSlots = useCallback(async () => {
    try {
      setSlotData(await api.getSlots(gate));
      setLoadError("");
    } catch (error) {
      setLoadError(error.message);
    }
  }, [gate]);

  const refreshDashboard = useCallback(async () => {
    try {
      setDashboard(await api.getDashboard(gate));
    } catch (error) {
      setLoadError(error.message);
    }
  }, [gate]);

  // Call this after every entry / exit so every screen shows fresh server data.
  const refreshAll = useCallback(() => {
    refreshSlots();
    refreshDashboard();
  }, [refreshSlots, refreshDashboard]);

  // Runs on first load AND whenever the gate changes (refreshAll depends on gate).
  useEffect(() => {
    refreshAll();
  }, [refreshAll]);

  const value = {
    gate, setGate,
    slotData, dashboard, loadError,
    justAssigned, setJustAssigned,
    refreshSlots, refreshDashboard, refreshAll,
  };
  return <ParkingContext.Provider value={value}>{children}</ParkingContext.Provider>;
}

// Custom hook: const { gate } = useParking();
export function useParking() {
  return useContext(ParkingContext);
}

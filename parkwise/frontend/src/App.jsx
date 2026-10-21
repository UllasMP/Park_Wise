import { useState } from "react";
import DevClock from "./components/DevClock.jsx";
import GatePicker from "./components/GatePicker.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import EntryPage from "./pages/EntryPage.jsx";
import ExitPage from "./pages/ExitPage.jsx";
import { useParking } from "./context/ParkingContext.jsx";

const TABS = [
  { id: "entry", label: "Entry", Page: EntryPage },
  { id: "exit", label: "Exit & payment", Page: ExitPage },
  { id: "dashboard", label: "Dashboard", Page: DashboardPage },
];

export default function App() {
  const [tab, setTab] = useState("entry"); // which screen is open
  const { loadError } = useParking();
  const ActivePage = TABS.find((t) => t.id === tab).Page;

  return (
    <div className="app">
      <header className="topbar">
        <h1>ParkWise</h1>
        <GatePicker />
      </header>

      <nav className="tabs">
        {TABS.map((t) => (
          <button key={t.id} className={t.id === tab ? "tab active" : "tab"} onClick={() => setTab(t.id)}>
            {t.label}
          </button>
        ))}
      </nav>

      {loadError && <p className="error">{loadError}</p>}
      <ActivePage />
      <DevClock />
    </div>
  );
}

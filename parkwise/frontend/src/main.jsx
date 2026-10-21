import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import { ParkingProvider } from "./context/ParkingContext.jsx";
import "./styles.css";

// ParkingProvider makes the shared state available to every component.
ReactDOM.createRoot(document.getElementById("root")).render(
  <ParkingProvider>
    <App />
  </ParkingProvider>
);

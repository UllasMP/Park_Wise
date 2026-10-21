import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Any request to /api/... is forwarded to Django, so no CORS setup is needed.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, proxy: { "/api": "http://127.0.0.1:8000" } },
});

// Small display helpers. The server decides all prices - we only format them.

export const TYPE_LABEL = { "2W": "2-Wheeler", "4W": "4-Wheeler" };

export function formatTime(iso) {
  return new Date(iso).toLocaleString("en-IN", {
    day: "2-digit", month: "short", hour: "2-digit", minute: "2-digit",
  });
}

// 320 -> "5h 20m"
export function formatStay(minutes) {
  return `${Math.floor(minutes / 60)}h ${minutes % 60}m`;
}

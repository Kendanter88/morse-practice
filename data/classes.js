// Registry of available classes. Add a new entry here to surface a new class
// in the selector. Each module is loaded lazily on demand.

export const classes = [
  {
    id: "cwops-intermediate",
    shortName: "CWA Intermediate",
    subtitle: "16 sessions · 10→25 WPM",
    blurb: "CW Academy's Intermediate curriculum. Speed-building over eight weeks with daily practice files, callsign drills, and CWT events.",
    status: "ready",
    loader: () => import("./cwops-intermediate.js"),
  },
];

const cache = new Map();

export async function loadClass(id) {
  if (cache.has(id)) return cache.get(id);
  const entry = classes.find((c) => c.id === id);
  if (!entry) throw new Error(`Unknown class: ${id}`);
  const mod = await entry.loader();
  cache.set(id, mod.default);
  return mod.default;
}

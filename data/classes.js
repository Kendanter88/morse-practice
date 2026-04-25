// Registry of available classes. Add a new entry here to surface a new class
// in the selector. Each module is loaded lazily on demand.

export const classes = [
  {
    id: "licw-overlearn-int1",
    shortName: "LICW Overlearn — INT1 Prep",
    subtitle: "Flow Foundations · 8 lessons",
    blurb: "Long Island CW Club's bootcamp for transitioning into Intermediate 2. Focus: Flow over recognition.",
    status: "ready",
    loader: () => import("./licw-overlearn-int1.js"),
  },
  {
    id: "cwops-intermediate",
    shortName: "CWA Intermediate",
    subtitle: "16 sessions · 10→25 WPM",
    blurb: "CW Academy's Intermediate curriculum. Speed-building over eight weeks. (Lesson detail in progress.)",
    status: "stub",
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

// CWops Intermediate (placeholder).
// The full curriculum has a different shape than the LICW one — 16 sessions
// over 8 weeks, target speeds 10→25 WPM, exercises drawn from LCWO,
// MorseCode.World ICR, Morse Runner, and CWops practice files. Filling in
// the per-session homework is a future pass.

export default {
  id: "cwops-intermediate",
  shortName: "CWA Intermediate",
  longName: "CW Academy Intermediate Curriculum (v2.2)",
  subtitle: "16 sessions, 10→25 WPM",
  description: "CW Academy's Intermediate curriculum. Sixteen sessions over eight weeks, building from 10 WPM through 25 WPM with daily LCWO ICR, Morse Runner callsign practice, QSO/POTA exchanges, and CWT events.",
  source: {
    org: "CW Academy / CWops",
    pdfUrl: "https://cwa.cwops.org/wp-content/uploads/Practice-Instructions-Intermediate-ver.2.2.pdf",
    referenceUrl: "https://cwa.cwops.org/wp-content/uploads/Practice-Instructions-Intermediate-ver.2.2.htm",
  },
  intro: {
    title: "About This Class",
    sections: [
      {
        heading: "Coming Soon",
        body: "Full lesson breakdown is being built. For now, the canonical document is linked above. The CWA Intermediate curriculum focuses on building send/receive speed in 2-3 WPM increments per session, with daily callsign drills, ICR practice, and live CWT participation as the capstone.",
      },
      {
        heading: "Tools You'll Use",
        list: [
          ["LCWO", "Instant Character Recognition training."],
          ["MorseCode.World", "Word/prefix/suffix file playback."],
          ["Morse Runner CE", "Callsign and contest simulator."],
          ["Morse Code Ninja", "Speed-matched practice files."],
          ["CWT", "Live weekly contests as the capstone exercise."],
        ],
      },
    ],
  },
  assessment: null,
  lessons: [
    {
      id: 1,
      title: "Sessions 1–3 · Target 10–13 WPM",
      summary: "Send and receive comfortably at 10 to 13 WPM. Daily Scales, ICR drills, callsign practice, QSO/POTA exchanges.",
      goals: [
        "Send and receive comfortably at 10–13 WPM.",
        "Build daily-practice habit: Scales warm-up, ICR drill, Morse Runner round.",
      ],
      guidance: "Three-day session structure. Each day: Scales as warm-up, then word/prefix files at 10–13 WPM, LCWO ICR, Morse Runner callsign practice, finishing with QSO and POTA exchange practice.",
      homework: [],
      exercises: [
        { name: "Morse Code Scales", category: "Warm-up", mpp: "https://cwops.org/wp-content/uploads/2024/08/Everyday-Send-Code-Web.htm", wlt: "" },
        { name: "LCWO ICR Guidelines", category: "ICR", mpp: "https://cwops.org/wp-content/uploads/2025/03/LCWO-ICR-Guidelines.htm", wlt: "" },
        { name: "MorseCode.World ICR Guidelines", category: "ICR", mpp: "https://cwops.org/wp-content/uploads/2024/08/MorseCode.World-ICR-Guidelines.htm", wlt: "" },
        { name: "Morse Runner CE", category: "Callsigns", mpp: "https://github.com/w7sst/MorseRunner/releases", wlt: "" },
        { name: "Morse Code Ninja", category: "Practice files", mpp: "https://morsecode.ninja/", wlt: "" },
        { name: "CWA Intermediate Practice Files", category: "Practice files", mpp: "https://cwops.org/intermediate-practice-files/", wlt: "" },
      ],
    },
  ],
};

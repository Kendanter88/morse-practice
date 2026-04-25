"""Build the LICW class data JS file from the mapped JSON and hand-curated narratives.

Usage: python build_class_data.py
Reads:  _sources/licw-mapped.json
Writes: data/licw-overlearn-int1.js
"""
import json
from pathlib import Path
from textwrap import indent

ROOT = Path(__file__).parent.parent
MAPPED = ROOT / "_sources" / "licw-mapped.json"
OUT = ROOT / "data" / "licw-overlearn-int1.js"

# ---------------------------------------------------------------------------
# Lesson narratives (paraphrased from the PDF). Order matches lesson IDs 1..8.
# ---------------------------------------------------------------------------

LESSON_NARRATIVES = {
    1: {
        "title": "Familiarity Building + Intro to Flow",
        "summary": "Build alphabet and number familiarity. Meet the Flow Train. Listen for each character's single unique acoustic sound.",
        "goals": [
            "Repeat alphabet and number listening + sending exercises.",
            "Emphasize the Flow Train; ignore the Recognition Train.",
            "Building Flow Proficiency IS the objective. Recognition success is NOT (temporarily).",
            "Listen for the unique single acoustic sound of each character.",
        ],
        "guidance": (
            "Relax, sit back, close your eyes, hear every character's sound with an Alert "
            "Indifference mindset. Match your listening rate to the flow rate. Let recognition "
            "happen as you sync with the flow — don't try to make it happen."
        ),
        "homework": [
            "Conduct a self-assessment.",
            "Start each daily practice with an Alphabet or Number exercise.",
            "Think of the letter or number every time you hear its unique sound rhythm.",
            "Stay on the Flow Train — missing is valuable IFR practice.",
            "Do the Sending exercises; sending flow improves comprehension flow.",
            "Review \"The Path to Morse Code Fluency\".",
            "Read the Loose Focus and Alert Indifference section of the Academic Reference Guide.",
            "Think about Instant Flow Recovery's value relative to de-emphasizing recognition success.",
        ],
    },
    2: {
        "title": "Added Flow + Instant Flow Recovery",
        "summary": "Practice IFR: accept misses, never look back, hear every character's sound. Match listening pace to flow pace.",
        "goals": [
            "Practice Instant Flow Recovery: accept misses, remain unconcerned, never look back.",
            "Match listening pace to flow pace. Accept imperfection. Emphasize relaxed listening.",
        ],
        "guidance": (
            "Settle into relaxed listening. TTR reduction comes from familiarity, and familiarity "
            "is built, not learned. Over-learning unique acoustic sound patterns during flow is how "
            "you transition from Thinking to Knowing. Try giving your subconscious a shot at "
            "recognition — wonder what word is being spelled instead of trying to recognize the letter."
        ),
        "homework": [
            "Maintain a relaxed yet alert mindset — desire recognition, but with no emotional urgency.",
            "A miss is just a mystery sound — ignore it, blame lack of familiarity, never look back.",
            "TTR reduction is a natural result of repetitive practice with character sounds during flow.",
            "Do the Sending exercises.",
            "Review the TTR and IFR sections of the Academic Reference Guide.",
        ],
    },
    3: {
        "title": "Flow Rates — Part 1",
        "summary": "Sync your listening rate to faster character flow rates. Improved non-recognition acceptance equals Character Flow Proficiency.",
        "goals": [
            "Accept imperfection — missing is just practice synchronizing your listening rate with the character flow rate.",
            "Improved non-recognition acceptance = Character Flow Proficiency.",
        ],
        "guidance": (
            "Focus on hearing unique acoustic sound units instead of dits and dahs — that's how you "
            "improve sound/meaning retrieval speed (TTR). Do NOT try to maximize recognition; just "
            "expand your ability to hear every character sound. Hear-it-send-it exercises are "
            "introduced to improve flow-sending muscle memory."
        ),
        "homework": [
            "Maintain forward momentum at faster flow rates — never abandon the stream for a missed character.",
            "Accept misses as components of normal, relaxed practice.",
            "Continue IFR improvement: miss → ignore → remain engaged. No pausing to think.",
            "Do the Sending exercises.",
            "Review the Increasing Effective Speed section of the Academic Reference Guide.",
        ],
    },
    4: {
        "title": "Flow Rates — Part 2",
        "summary": "Listen well above your comfort zone. If recognition happens, it's a surprise — because you let it instead of making it.",
        "goals": [
            "Deepen skill and familiarity with increased character flow; listen to faster flow rates.",
            "Surrender control and listen alertly to the flow.",
            "If recognition occurs it's a surprise — because you let it happen instead of trying to make it happen.",
        ],
        "guidance": (
            "You're listening well above your current comfort zone. Mental fatigue may trigger a "
            "capitulation shift — completely giving up on conscious recognition efforts. This is a "
            "significant breakthrough if it happens. You can finally relax, listen, maintain forward "
            "momentum, and start relying on passive, intuitive reception."
        ),
        "homework": [
            "Conduct a self-assessment.",
            "Stay relaxed when fatigue sets in — don't fight it. This may invite your subconscious pattern recognition into the game.",
            "Let sound patterns wash over and through you. Notice when meaning emerges without effort.",
            "Get completely comfortable not catching everything while staying fully engaged with flow.",
            "Do the Sending exercises.",
            "Review the Increasing Effective Speed section of the Academic Reference Guide.",
        ],
    },
    5: {
        "title": "Character Flow Proficiency — Part 1",
        "summary": "Relaxed, fluent character flow at faster rates. Wonder what word is being spelled — each letter as a word clue.",
        "goals": [
            "Focus on more relaxed, fluent character flow perception at faster rates — if recognition happens, it was an accident.",
            "Occasionally wonder what word is being spelled. Treat each letter as a word clue (a significant mindset shift).",
        ],
        "guidance": (
            "TTR, IFR, resilience, and CFP are all building. Focus on occasionally capturing a thread "
            "of comprehension across continuous character streams. Relax and keep moving forward despite "
            "non-recognition setbacks. Never look back."
        ),
        "homework": [
            "Subliminal recognition happens when you're not trying to get everything. Learn to listen to every character.",
            "Once you can follow the flow and easily hear each character, recognition during flow will begin to improve.",
            "Always warm up with the Alphabet exercise, but spend more practice time with longer content flows.",
            "Do the Sending exercises.",
            "Review the Character Flow Proficiency section of the Academic Reference Guide.",
        ],
    },
    6: {
        "title": "Character Flow Proficiency — Part 2",
        "summary": "Sustain alertness under fatigue. Abandon character-by-character recognition. Open the door to subliminal recognition.",
        "goals": [
            "Sustain character flow alertness under fatigue as you abandon intense, conscious, character-by-character recognition efforts.",
            "Open the door to subliminal recognition based on effortless pattern recognition fetches of known data.",
        ],
        "guidance": (
            "More conversational character flow via phrases. Mentally lean forward into the flow. "
            "CFP improvements are essential now — never look back at missed details."
        ),
        "homework": [
            "Stay relaxed and alertly indifferent, but notice meaning when and if it happens to unfold.",
            "Non-recognition events have no effect as you remain alert and cruise the flow.",
            "Give your subconscious a shot at recognition. Get the conscious mind out of the way.",
            "Step back and listen to more short single-word exercises occasionally.",
            "Do the Sending exercises.",
            "Review the Character Flow Proficiency section of the Academic Reference Guide.",
        ],
    },
    7: {
        "title": "Intro to Extended Flow",
        "summary": "3-word binomial expressions. Stay on the Flow Train. Equal indifference to gets and misses.",
        "goals": [
            "3-word binomial expressions exercises are introduced (up and down, this and that, yes and no, give and take).",
            "Stay on the Flow Train, ignore the Recognition Train.",
            "Hear every character's sound. Be alert. Equally indifferent to gets and misses. Give pattern recognition during flow a chance.",
        ],
        "guidance": (
            "High character familiarity will enable occasional recognition as you stay current with the "
            "flow. Abandon tedious character-by-character recognition; allow subliminal recognition and "
            "word anticipation to happen now and then. This shift usually happens over months of flow "
            "practice — be patient."
        ),
        "homework": [
            "Conduct a self-assessment.",
            "Each letter can be a clue to the word if you're relaxed and current with the flow.",
            "Context and previous words enable predictions and anticipations.",
            "Maintain forward momentum — never stop to repair what you missed.",
            "Continue warming up with Alphabet and Numbers; spend extra time on multi-word streams.",
            "Do the Sending exercises.",
            "Review the Word Building and Word Discovery sections of the Academic Reference Guide.",
        ],
    },
    8: {
        "title": "INT2 Bootcamp Summary + Ongoing Practice",
        "summary": "You've learned a new way to listen. Reflect on improved comfort with flow and forward momentum. Keep going.",
        "goals": [
            "Time To Recognize (TTR).",
            "Instant Flow Recovery (IFR).",
            "Character Flow Proficiency (CFP).",
            "Subliminal Character Recognition.",
            "A Word Discovery attitude (replaces intense letter-by-letter focus).",
        ],
        "guidance": (
            "Reflect on your improved comfort level with imperfection, flow, and your ability to "
            "maintain forward momentum. Continue with on-air QSOs and rag chews, practice with "
            "OverLearn exercises, and attend LICW classes. Fearlessly engage with character flow "
            "rates beyond your comfort zone."
        ),
        "homework": [
            "Flow priority — stay engaged with the flow and alert for meaning as it occasionally unfolds.",
            "Let subliminal character recognition happen through pattern recognition during flow. Quit conscious character recognition efforts.",
            "Trust your anticipation skills — predict the word, confirm or disprove with each incoming character (Word Discovery mindset).",
            "Automate IFR: miss → ignore → continue. Don't let dopamine or cortisol derail engagement with flow.",
            "Embrace imperfect comprehension — relax; you'll begin to get the gist if you continue cruising the flow.",
        ],
    },
}

# Map exercise display name → category bucket for grouping in the UI.
def categorize(name: str) -> str:
    n = name.lower()
    if n.startswith("sending"):
        return "Sending"
    if "alphabet" in n:
        return "Alphabet"
    if "number" in n:
        return "Numbers"
    if "states and provinces" in n:
        return "States & Provinces"
    if "phrase" in n or "binomial" in n:
        return "Phrases"
    return "Words"


CLASS_HEADER = '''// Auto-generated by _sources/build_class_data.py — do not edit by hand.
// Re-run the script after updating the source PDF or lesson narratives.

export default {
'''


def js_string(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def js_array(items, formatter=js_string, indent_str="    "):
    if not items:
        return "[]"
    inner = ",\n".join(f"{indent_str}{indent_str}{formatter(it)}" for it in items)
    return f"[\n{inner}\n{indent_str}]"


def main():
    mapped = json.loads(MAPPED.read_text())
    by_id = {L["id"]: L for L in mapped}

    OUT.parent.mkdir(parents=True, exist_ok=True)

    out = []
    out.append(CLASS_HEADER)
    out.append('  id: "licw-overlearn-int1",')
    out.append('  shortName: "LICW Overlearn — INT1 Prep",')
    out.append('  longName: "LICW Overlearn Bootcamp — INT2 Student Guide v1.3",')
    out.append('  subtitle: "Flow Foundations",')
    out.append('  description: "A month-long jump-start into the flow-pressure phase. Replaces the recognition-perfectionist mindset with Alert Indifference, Instant Flow Recovery, and Character Flow Proficiency.",')
    out.append('  source: {')
    out.append('    org: "Long Island CW Club",')
    out.append('    pdfUrl: "https://longislandcwclub.org/wp-content/uploads/2026/04/INT2-BOOTCAMP-STUDENT-GUIDE-V1.3.pdf",')
    out.append('    referenceUrl: "https://longislandcwclub.org/academic-downloads/",')
    out.append('  },')
    out.append('  intro: {')
    out.append('    title: "Flow vs. Recognition",')
    out.append('    sections: [')
    out.append('      {')
    out.append('        heading: "The Recognition Train vs. The Flow Train",')
    out.append('        body: "Traditional Morse practice is a constant strain to recognize every character. Falling off feels like failure. Bootcamp flips that — match your listening pace to the character flow, hear every sound, and treat misses as cognitive silence rather than failures.",')
    out.append('      },')
    out.append('      {')
    out.append('        heading: "Alert Indifference",')
    out.append('        body: "Be alert for recognition, but indifferent to whether it lands. Neutralize both the dopamine hit of a win and the cortisol hit of a loss. A regulated nervous system is what unlocks higher flow rates.",')
    out.append('      },')
    out.append('      {')
    out.append('        heading: "The Five Pillars",')
    out.append('        list: [')
    out.append('          ["Alert Indifference", "Calm, normalized misses, no celebration of gets."],')
    out.append('          ["Instant Flow Recovery (IFR)", "Miss → ignore → next character. No looking back."],')
    out.append('          ["Character Flow Proficiency (CFP)", "Comfortably hear every character\'s unique acoustic sound during flow."],')
    out.append('          ["Time To Recognize (TTR)", "Sound→meaning association strengthened by over-learning during flow."],')
    out.append('          ["Subliminal Recognition", "Pattern recognition takes over; words and meaning emerge effortlessly."],')
    out.append('        ],')
    out.append('      },')
    out.append('      {')
    out.append('        heading: "Thinking vs. Knowing",')
    out.append('        body: "Thinking is a slow, exhausting process — one letter at a time. Knowing is a state where sound and meaning are synonymous. You get to Knowing by prioritizing Flow, not by trying harder to recognize.",')
    out.append('      },')
    out.append('    ],')
    out.append('  },')
    out.append('  assessment: {')
    out.append('    title: "Self-Assessment — Where Are You Today?",')
    out.append('    questions: [')
    out.append('      {')
    out.append('        q: "How are you listening?",')
    out.append('        thinking: "Maximum Recognition Success listening. Constantly working to stay on the Recognition Train. \\"Wait — what was that?\\"",')
    out.append('        flowing: "Matching your listening rate to the flow rate. Alert for recognition but indifferent to results. Flow Train is the priority.",')
    out.append('      },')
    out.append('      {')
    out.append('        q: "The Echo Test",')
    out.append('        thinking: "Repeating character elements in your head (\\"dah-di-di-dit… okay, that\'s a B\\"). Adds a step and slows you down.",')
    out.append('        flowing: "No need to echo. Pattern recognition matches a single acoustic sound to meaning, or it doesn\'t. You\'re relaxed either way.",')
    out.append('      },')
    out.append('      {')
    out.append('        q: "Handling Misses",')
    out.append('        thinking: "You freeze and try to look back. You fell off the Recognition Train.",')
    out.append('        flowing: "You flow through the miss and stay alert to the next character\'s sound. Still on the Flow Train.",')
    out.append('      },')
    out.append('    ],')
    out.append('    summary: "Evaluate yourself by how you keep going (Flowing), not by how much you \'get\' (Thinking).",')
    out.append('  },')
    out.append('  lessons: [')

    for lesson_id in sorted(LESSON_NARRATIVES.keys()):
        n = LESSON_NARRATIVES[lesson_id]
        m = by_id[lesson_id]
        out.append("    {")
        out.append(f"      id: {lesson_id},")
        out.append(f"      title: {js_string(n['title'])},")
        out.append(f"      summary: {js_string(n['summary'])},")
        out.append("      goals: [")
        for g in n["goals"]:
            out.append(f"        {js_string(g)},")
        out.append("      ],")
        out.append(f"      guidance: {js_string(n['guidance'])},")
        out.append("      homework: [")
        for h in n["homework"]:
            out.append(f"        {js_string(h)},")
        out.append("      ],")
        out.append("      exercises: [")
        # Build the merged exercise list. Each unique exercise name should appear
        # once, with whichever URLs it has on MPP and/or WLT.
        merged = {}
        order = []
        for name, uri in m["mpp"]:
            if name not in merged:
                merged[name] = {"name": name, "category": categorize(name), "mpp": uri, "wlt": ""}
                order.append(name)
            else:
                merged[name]["mpp"] = uri
        for name, uri in m["wlt"]:
            if name not in merged:
                merged[name] = {"name": name, "category": categorize(name), "mpp": "", "wlt": uri}
                order.append(name)
            else:
                merged[name]["wlt"] = uri
        for name in order:
            ex = merged[name]
            out.append("        {")
            out.append(f"          name: {js_string(ex['name'])},")
            out.append(f"          category: {js_string(ex['category'])},")
            out.append(f"          mpp: {js_string(ex['mpp'])},")
            out.append(f"          wlt: {js_string(ex['wlt'])},")
            out.append("        },")
        out.append("      ],")
        out.append("    },")

    out.append("  ],")
    out.append("};")
    out.append("")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

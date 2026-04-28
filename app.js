// Morse Practice Companion — vanilla JS SPA.
// Hash routes:
//   #/                                — class selector
//   #/c/<classId>                     — class home (lessons + intro/assessment)
//   #/c/<classId>/intro               — class intro / mindset
//   #/c/<classId>/assessment          — self-assessment
//   #/c/<classId>/lesson/<n>          — lesson detail

import { classes, loadClass } from "./data/classes.js";
import { extras } from "./data/extras.js";

const app = document.getElementById("app");

// ---------------------------------------------------------------------------
// Theme
// ---------------------------------------------------------------------------

const THEME_KEY = "mpc.theme";

function applyTheme(t) {
  document.documentElement.dataset.theme = t;
}

(function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  const prefersLight = window.matchMedia?.("(prefers-color-scheme: light)").matches;
  applyTheme(saved || (prefersLight ? "light" : "dark"));
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    applyTheme(next);
    localStorage.setItem(THEME_KEY, next);
  });
})();

// ---------------------------------------------------------------------------
// Progress (per class+lesson) and homework checks (per class+lesson+item)
// ---------------------------------------------------------------------------

const STATE_KEY = "mpc.state.v1";

function loadState() {
  try {
    return JSON.parse(localStorage.getItem(STATE_KEY) || "{}");
  } catch {
    return {};
  }
}
function saveState(s) {
  localStorage.setItem(STATE_KEY, JSON.stringify(s));
}

function isChecked(classId, lessonId, itemIdx) {
  const s = loadState();
  return !!s[classId]?.[lessonId]?.homework?.[itemIdx];
}
function setChecked(classId, lessonId, itemIdx, value) {
  const s = loadState();
  s[classId] ??= {};
  s[classId][lessonId] ??= {};
  s[classId][lessonId].homework ??= {};
  if (value) s[classId][lessonId].homework[itemIdx] = true;
  else delete s[classId][lessonId].homework[itemIdx];
  saveState(s);
}
function lessonProgress(classId, lessonId, total) {
  const s = loadState();
  const checks = s[classId]?.[lessonId]?.homework || {};
  const done = Object.values(checks).filter(Boolean).length;
  return { done, total, frac: total ? done / total : 0 };
}

function isDayDone(classId, lessonId, dayKey) {
  return !!loadState()[classId]?.[lessonId]?.days?.[dayKey];
}
function setDayDone(classId, lessonId, dayKey, value) {
  const s = loadState();
  s[classId] ??= {};
  s[classId][lessonId] ??= {};
  s[classId][lessonId].days ??= {};
  if (value) s[classId][lessonId].days[dayKey] = true;
  else delete s[classId][lessonId].days[dayKey];
  saveState(s);
}

// Track most-recent class+lesson so the landing page can offer "Resume".
function rememberLast(classId, lessonId) {
  const s = loadState();
  s._last = { classId, lessonId, at: Date.now() };
  saveState(s);
}
function getLast() {
  return loadState()._last || null;
}

// ---------------------------------------------------------------------------
// Tiny DOM helpers
// ---------------------------------------------------------------------------

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v == null || v === false) continue;
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") {
      node.addEventListener(k.slice(2).toLowerCase(), v);
    } else if (k === "dataset") {
      Object.assign(node.dataset, v);
    } else if (k in node && typeof v !== "object") {
      try { node[k] = v; } catch { node.setAttribute(k, v); }
    } else {
      node.setAttribute(k, v);
    }
  }
  for (const child of children.flat()) {
    if (child == null || child === false) continue;
    node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }
  return node;
}

function clear(node) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

function parseHash() {
  const h = location.hash.replace(/^#/, "") || "/";
  const parts = h.split("/").filter(Boolean);
  if (parts.length === 0) return { route: "home" };
  if (parts[0] === "c" && parts[1]) {
    const classId = parts[1];
    if (parts[2] === "intro") return { route: "intro", classId };
    if (parts[2] === "assessment") return { route: "assessment", classId };
    if (parts[2] === "lesson" && parts[3]) {
      return { route: "lesson", classId, lessonId: Number(parts[3]) };
    }
    return { route: "class", classId };
  }
  return { route: "notfound" };
}

async function render() {
  const r = parseHash();
  clear(app);
  app.appendChild(el("p", { class: "loading" }, "Loading…"));
  try {
    if (r.route === "home") return renderHome();
    const cls = await loadClass(r.classId);
    if (!cls) return renderNotFound();
    if (r.route === "class") return renderClass(cls);
    if (r.route === "intro") return renderIntro(cls);
    if (r.route === "assessment") return renderAssessment(cls);
    if (r.route === "lesson") return renderLesson(cls, r.lessonId);
    return renderNotFound();
  } catch (err) {
    console.error(err);
    clear(app);
    app.appendChild(el("p", { class: "empty" }, "Something went wrong loading this page. Try refreshing."));
  }
  window.scrollTo(0, 0);
}

window.addEventListener("hashchange", render);
window.addEventListener("DOMContentLoaded", render);

// Intercept clicks on internal links so we can scroll to top on navigation.
document.addEventListener("click", (e) => {
  const a = e.target.closest("a[href^='#/']");
  if (!a) return;
  // Let the hashchange listener handle it; just scroll on next tick.
  setTimeout(() => window.scrollTo(0, 0), 0);
});

// ---------------------------------------------------------------------------
// Views
// ---------------------------------------------------------------------------

function crumbs(items) {
  const c = el("nav", { class: "crumbs" });
  items.forEach((item, i) => {
    if (i > 0) c.appendChild(el("span", { class: "sep" }, "›"));
    if (item.href) c.appendChild(el("a", { href: item.href }, item.label));
    else c.appendChild(el("span", {}, item.label));
  });
  return c;
}

function renderHome() {
  clear(app);
  app.appendChild(el("h1", {}, "Practice classes"));
  app.appendChild(el("p", { class: "subtitle" }, "Pick a class to begin. Progress is saved per class in your browser."));

  const last = getLast();
  if (last) {
    const cls = classes.find((c) => c.id === last.classId);
    if (cls) {
      app.appendChild(
        el("div", { class: "callout section" },
          el("strong", {}, "Resume: "),
          el("a", { href: `#/c/${cls.id}/lesson/${last.lessonId}` },
            `${cls.shortName} · Lesson ${last.lessonId}`
          )
        )
      );
    }
  }

  const grid = el("div", { class: "grid" });
  for (const c of classes) {
    const card = el("a", { class: "card", href: `#/c/${c.id}` });
    card.appendChild(el("h2", {}, c.shortName));
    card.appendChild(el("div", { class: "meta" }, c.subtitle));
    card.appendChild(el("p", {}, c.blurb));
    if (c.status === "stub") {
      card.appendChild(el("div", { class: "section", style: "margin: 0.6rem 0 0" },
        el("span", { class: "tag muted" }, "In progress")
      ));
    }
    grid.appendChild(card);
  }

  const home = el("div", { class: "home-grid" });
  home.appendChild(el("section", { class: "home-classes" }, grid));
  home.appendChild(renderExtras());
  app.appendChild(home);
}

function renderExtras() {
  const aside = el("aside", { class: "home-extras" });
  aside.appendChild(el("h2", {}, "Extra practice"));

  const groups = [
    { key: "copy", title: "Copy", items: extras.copy || [] },
    { key: "sending", title: "Sending", items: extras.sending || [] },
  ];

  for (const g of groups) {
    if (!g.items.length) continue;
    const group = el("div", { class: "extras-group" });
    group.appendChild(el("h3", {}, g.title));
    const list = el("ul", { class: "extras-list" });
    for (const item of g.items) {
      const li = el("li", { class: "extras-item" });
      li.appendChild(el("div", { class: "extras-name" }, item.name));
      if (item.blurb) li.appendChild(el("div", { class: "extras-blurb" }, item.blurb));
      if (item.speeds?.length) {
        const chips = el("ul", { class: "tool-strip" });
        for (const s of item.speeds) {
          chips.appendChild(el("li", {},
            el("a", {
              class: "tool-chip audio",
              href: encodeURI(s.url),
              target: "_blank",
              rel: "noopener",
              title: `${item.name} · ${s.wpm} wpm`,
            }, `${s.wpm} ▶`)
          ));
        }
        li.appendChild(chips);
      } else if (item.url) {
        const isAudio = /\.mp3$/i.test(item.url);
        li.appendChild(el("a", {
          class: `tool-chip${isAudio ? " audio" : ""}`,
          href: encodeURI(item.url),
          target: "_blank",
          rel: "noopener",
          title: item.url,
        }, isAudio ? "Listen ▶" : "Open PDF ↗"));
      }
      list.appendChild(li);
    }
    group.appendChild(list);
    aside.appendChild(group);
  }

  return aside;
}

function renderClass(cls) {
  clear(app);
  app.appendChild(crumbs([{ label: "Classes", href: "#/" }, { label: cls.shortName }]));
  app.appendChild(el("h1", {}, cls.longName || cls.shortName));
  if (cls.subtitle) app.appendChild(el("p", { class: "subtitle" }, cls.subtitle));
  if (cls.description) app.appendChild(el("p", {}, cls.description));

  const buttons = el("div", { class: "button-row section" });
  buttons.appendChild(el("a", { class: "btn ghost", href: `#/c/${cls.id}/intro` }, "Mindset / Intro"));
  if (cls.assessment) {
    buttons.appendChild(el("a", { class: "btn ghost", href: `#/c/${cls.id}/assessment` }, "Self-assessment"));
  }
  if (cls.source?.pdfUrl) {
    buttons.appendChild(el("a", { class: "btn ghost", href: cls.source.pdfUrl, target: "_blank", rel: "noopener" }, "Source PDF ↗"));
  }
  if (cls.source?.referenceUrl) {
    buttons.appendChild(el("a", { class: "btn ghost", href: cls.source.referenceUrl, target: "_blank", rel: "noopener" }, "Reference materials ↗"));
  }
  app.appendChild(buttons);

  app.appendChild(el("h2", { class: "section" }, "Lessons"));
  const grid = el("div", { class: "grid" });
  for (const lesson of cls.lessons) {
    const homeworkTotal = lesson.homework?.length || 0;
    const prog = lessonProgress(cls.id, lesson.id, homeworkTotal);
    const card = el("a", { class: "card", href: `#/c/${cls.id}/lesson/${lesson.id}` });
    card.appendChild(el("h2", {}, `${lesson.id}. ${lesson.title}`));

    const metaParts = [];
    if (lesson.days?.length) {
      metaParts.push(`${lesson.days.length} days`);
      const audioCount = lesson.days.flatMap((d) => d.tools || []).filter((t) => /\.mp3$/i.test(t.url)).length;
      if (audioCount) metaParts.push(`${audioCount} audio files`);
    } else if (lesson.exercises?.length) {
      metaParts.push(`${lesson.exercises.length} exercises`);
    }
    if (homeworkTotal) metaParts.push(`${prog.done}/${homeworkTotal} homework`);
    card.appendChild(el("div", { class: "meta" }, metaParts.join(" · ")));

    if (lesson.summary) card.appendChild(el("p", {}, lesson.summary));
    if (homeworkTotal) {
      const bar = el("div", { class: "progress" },
        el("div", { class: "bar" }, el("span", { style: `width:${(prog.frac * 100).toFixed(0)}%` })),
      );
      card.appendChild(bar);
    }
    grid.appendChild(card);
  }
  app.appendChild(grid);
}

function renderIntro(cls) {
  clear(app);
  app.appendChild(crumbs([
    { label: "Classes", href: "#/" },
    { label: cls.shortName, href: `#/c/${cls.id}` },
    { label: "Intro" },
  ]));
  app.appendChild(el("h1", {}, cls.intro?.title || "Introduction"));

  for (const sec of cls.intro?.sections || []) {
    const block = el("div", { class: "section" });
    block.appendChild(el("h2", {}, sec.heading));
    if (sec.body) block.appendChild(el("p", {}, sec.body));
    if (sec.html) {
      const wrap = el("div", { class: "rich" });
      wrap.innerHTML = sec.html;
      block.appendChild(wrap);
    }
    if (sec.list) {
      const ul = el("ul");
      for (const [name, body] of sec.list) {
        ul.appendChild(el("li", {}, el("strong", {}, name + ": "), body));
      }
      block.appendChild(ul);
    }
    app.appendChild(block);
  }
}

function renderAssessment(cls) {
  clear(app);
  app.appendChild(crumbs([
    { label: "Classes", href: "#/" },
    { label: cls.shortName, href: `#/c/${cls.id}` },
    { label: "Self-assessment" },
  ]));
  const a = cls.assessment;
  if (!a) {
    app.appendChild(el("p", { class: "empty" }, "No self-assessment for this class."));
    return;
  }
  app.appendChild(el("h1", {}, a.title));
  for (const q of a.questions) {
    const block = el("div", { class: "assess-question" });
    block.appendChild(el("h3", {}, q.q));
    const row = el("div", { class: "assess-row" });
    row.appendChild(el("div", { class: "assess-cell thinking" },
      el("div", { class: "ttl" }, "Thinking"),
      el("div", {}, q.thinking)
    ));
    row.appendChild(el("div", { class: "assess-cell flowing" },
      el("div", { class: "ttl" }, "Flowing"),
      el("div", {}, q.flowing)
    ));
    block.appendChild(row);
    app.appendChild(block);
  }
  if (a.summary) app.appendChild(el("div", { class: "callout section" }, a.summary));
}

const TOOL_LABEL = { mpp: "MPP", wlt: "WLT" };

function renderLesson(cls, lessonId) {
  clear(app);
  const lesson = cls.lessons.find((l) => l.id === lessonId);
  if (!lesson) return renderNotFound();
  rememberLast(cls.id, lessonId);

  app.appendChild(crumbs([
    { label: "Classes", href: "#/" },
    { label: cls.shortName, href: `#/c/${cls.id}` },
    { label: `Lesson ${lesson.id}` },
  ]));

  const head = el("div", { class: "lesson-head" },
    el("h1", {}, `Lesson ${lesson.id}: ${lesson.title}`)
  );
  app.appendChild(head);
  if (lesson.summary) app.appendChild(el("p", { class: "subtitle" }, lesson.summary));

  if (lesson.goals?.length) {
    const sec = el("section", { class: "section" });
    sec.appendChild(el("h3", {}, "Goals"));
    const ul = el("ul");
    lesson.goals.forEach((g) => ul.appendChild(el("li", {}, g)));
    sec.appendChild(ul);
    app.appendChild(sec);
  }

  if (lesson.guidance) {
    app.appendChild(el("div", { class: "callout section" }, lesson.guidance));
  }

  if (lesson.homework?.length) {
    const sec = el("section", { class: "section" });
    sec.appendChild(el("h3", {}, "Homework"));
    const list = el("ul", { class: "checklist" });
    lesson.homework.forEach((item, idx) => {
      const cb = el("input", {
        type: "checkbox",
        checked: isChecked(cls.id, lesson.id, idx),
        onChange: (e) => {
          setChecked(cls.id, lesson.id, idx, e.target.checked);
        },
      });
      const li = el("li", {},
        el("label", {}, cb, el("span", { class: "text" }, item))
      );
      list.appendChild(li);
    });
    sec.appendChild(list);
    app.appendChild(sec);
  }

  if (lesson.days?.length) {
    const sec = el("section", { class: "section" });
    sec.appendChild(el("h3", {}, "Daily practice"));
    lesson.days.forEach((day, dayIdx) => {
      const dayKey = `day-${dayIdx}`;
      const block = el("div", { class: "day-block" });
      const head = el("div", { class: "day-head" });
      head.appendChild(el("h2", {}, day.label));
      const dayChecked = isDayDone(cls.id, lesson.id, dayKey);
      const dayCheck = el("label", { class: "day-done" },
        el("input", {
          type: "checkbox",
          checked: dayChecked,
          onChange: (e) => {
            setDayDone(cls.id, lesson.id, dayKey, e.target.checked);
            block.classList.toggle("done", e.target.checked);
          },
        }),
        el("span", {}, "Done")
      );
      head.appendChild(dayCheck);
      block.appendChild(head);
      if (dayChecked) block.classList.add("done");

      const body = el("div", { class: "rich" });
      body.innerHTML = day.bodyHtml || "";
      block.appendChild(body);

      if (day.tools?.length) {
        const toolList = el("ul", { class: "tool-strip" });
        day.tools.forEach((t) => {
          const isAudio = /\.mp3$/i.test(t.url);
          toolList.appendChild(el("li", {},
            el("a", {
              class: `tool-chip${isAudio ? " audio" : ""}`,
              href: t.url,
              target: "_blank",
              rel: "noopener",
              title: t.url,
            }, t.name, isAudio ? " ▶" : " ↗")
          ));
        });
        const wrap = el("details", { class: "tool-wrap" },
          el("summary", {}, `Quick links · ${day.tools.length}`),
          toolList,
        );
        block.appendChild(wrap);
      }

      sec.appendChild(block);
    });
    app.appendChild(sec);
  }

  if (lesson.exercises?.length) {
    const sec = el("section", { class: "section" });
    sec.appendChild(el("h3", {}, "Exercises"));

    // Build category set
    const cats = [...new Set(lesson.exercises.map((e) => e.category))];

    // Filter chips
    const filterState = { active: "all" };
    const filterbar = el("div", { class: "filterbar" });
    const allChip = el("button", { class: "chip", type: "button", "aria-pressed": "true" }, "All");
    filterbar.appendChild(allChip);
    const chipMap = { all: allChip };
    cats.forEach((cat) => {
      const c = el("button", { class: "chip", type: "button", "aria-pressed": "false" }, cat);
      filterbar.appendChild(c);
      chipMap[cat] = c;
    });
    Object.entries(chipMap).forEach(([key, chip]) => {
      chip.addEventListener("click", () => {
        filterState.active = key;
        Object.entries(chipMap).forEach(([k, c]) => {
          c.setAttribute("aria-pressed", k === key ? "true" : "false");
        });
        applyFilter();
      });
    });
    sec.appendChild(filterbar);

    function applyFilter() {
      sec.querySelectorAll("[data-cat]").forEach((g) => {
        const show = filterState.active === "all" || g.dataset.cat === filterState.active;
        g.style.display = show ? "" : "none";
      });
    }

    // Group by category, preserve original order
    const groups = new Map();
    for (const ex of lesson.exercises) {
      if (!groups.has(ex.category)) groups.set(ex.category, []);
      groups.get(ex.category).push(ex);
    }
    for (const [cat, list] of groups) {
      const group = el("div", { class: "exercise-group", dataset: { cat } });
      group.appendChild(el("div", { class: "group-head" },
        el("h3", {}, cat),
        el("span", { class: "tag muted" }, `${list.length}`)
      ));
      const ul = el("ul", { class: "ex-list" });
      for (const ex of list) {
        const row = el("li", { class: "ex-row" });
        row.appendChild(el("span", { class: "name" }, ex.name));
        row.appendChild(toolLink("mpp", ex.mpp));
        row.appendChild(toolLink("wlt", ex.wlt));
        ul.appendChild(row);
      }
      group.appendChild(ul);
      sec.appendChild(group);
    }
    app.appendChild(sec);
  }

  // Lesson nav
  const nav = el("div", { class: "lesson-nav" });
  const prev = cls.lessons.find((l) => l.id === lesson.id - 1);
  const next = cls.lessons.find((l) => l.id === lesson.id + 1);
  if (prev) {
    nav.appendChild(el("a", { class: "btn ghost", href: `#/c/${cls.id}/lesson/${prev.id}` }, `← Lesson ${prev.id}`));
  }
  if (next) {
    nav.appendChild(el("a", { class: "btn", href: `#/c/${cls.id}/lesson/${next.id}` }, `Lesson ${next.id} →`));
  }
  if (nav.children.length) app.appendChild(nav);
}

function toolLink(kind, url) {
  const label = TOOL_LABEL[kind] || kind.toUpperCase();
  if (!url) {
    return el("span", { class: "ex-link", "data-empty": "1", title: `No ${label} link` },
      el("span", { class: "label" }, label),
      "—"
    );
  }
  return el("a", { class: "ex-link", href: url, target: "_blank", rel: "noopener", title: `${label}: ${url}` },
    el("span", { class: "label" }, label),
    "↗"
  );
}

function renderNotFound() {
  clear(app);
  app.appendChild(el("h1", {}, "Not found"));
  app.appendChild(el("p", {}, "That page doesn't exist. ", el("a", { href: "#/" }, "Back to classes.")));
}

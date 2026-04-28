# Morse Practice Companion

Static webapp that turns CW class study guides into a phone-friendly practice
launcher. Lessons, mindset notes, homework checklists with progress tracking,
and one-tap links to the exercise tools (MPP and WLT).

Live at https://cwops.morsecodepractice.com

## What's in the box

```
morse/
├── index.html              # SPA shell
├── styles.css              # Dark-first theme
├── app.js                  # Vanilla JS router + views
├── data/
│   ├── classes.js                # Registry — add new classes here
│   └── cwops-intermediate.js     # CWA Intermediate — generated
├── _sources/               # Build inputs, NOT deployed
│   ├── cwops-int.htm                # Curriculum HTML (fetched)
│   ├── cwops-practice-files.htm     # Practice-files index (fetched)
│   ├── cwops-practice-audio.json    # Generated audio map
│   ├── extract_pdf_links.py         # Generic helper: list URI annotations in a PDF
│   ├── extract_practice_audio.py    # Builds cwops-practice-audio.json
│   └── build_cwops_data.py          # Emits data/cwops-intermediate.js
└── README.md
```

## Running locally

It's plain HTML/CSS/JS. The shell uses ES modules, so you need a real HTTP
server (not `file://`):

```bash
# Any of these work
python -m http.server 8000
# or
npx serve .
# or use the Live Server extension in VS Code
```

Then open http://localhost:8000.

## Adding a new class

1. Create `data/<your-class-id>.js` exporting a `default` object with the
   shape used by `data/cwops-intermediate.js` (`id`, `shortName`, `longName`,
   `subtitle`, `description`, `source`, `intro`, `assessment`, `lessons`).
2. Register it in `data/classes.js` by adding an entry to the `classes` array.
3. That's it — the selector picks it up automatically.

## Updating the CWA Intermediate class

The CWA build runs from two source files: the curriculum HTML and the
practice-files index page (which is where the audio mp3 URLs live).

```bash
# 1. Refresh the source HTML files
curl -A "Mozilla/5.0" -o _sources/cwops-int.htm \
  https://cwa.cwops.org/wp-content/uploads/Practice-Instructions-Intermediate-ver.2.2.htm
curl -A "Mozilla/5.0" -o _sources/cwops-practice-files.htm \
  https://cwops.org/intermediate-practice-files/

# 2. Rebuild the audio file map
python _sources/extract_practice_audio.py

# 3. Regenerate the class data file
python _sources/build_cwops_data.py
```

In-prose codes like `WD101-10`, `PR101-15`, `SS201-20` are auto-detected and
turned into direct mp3 links during the build. The script reports how many
audio files it linked.

## Deploying

The site lives on the Odroid XU4 home server, served by Nginx behind the
Cloudflare Tunnel for `cwops.morsecodepractice.com`. Deploys are a git pull
from [Kendanter88/morse-practice](https://github.com/Kendanter88/morse-practice).

```bash
# First time
sudo git clone https://github.com/Kendanter88/morse-practice.git /var/www/cwops

# Subsequent updates
cd /var/www/cwops && sudo git pull
```

No build step — Nginx serves the working tree directly. `_sources/` is
harmless if it ships, but you can add it to a `.gitignore`-style exclude
on the server if you want to keep the deploy clean.

## Resetting your progress

Open browser devtools → Application → Local Storage → your origin →
delete the `mpc.state.v1` key. Or in the console:

```js
localStorage.removeItem("mpc.state.v1");
```

## Credits

Source materials are © their respective owners (CW Academy / CWops). This
app is a personal study companion, not affiliated with or endorsed by
either organization.

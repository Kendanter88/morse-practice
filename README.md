# Morse Practice Companion

Static webapp that turns CW class study guides into a phone-friendly practice
launcher. Lessons, mindset notes, homework checklists with progress tracking,
and one-tap links to the exercise tools (MPP and WLT).

Live at https://morse.triplehatsecurity.com

## What's in the box

```
morse/
├── index.html              # SPA shell
├── styles.css              # Dark-first theme
├── app.js                  # Vanilla JS router + views
├── data/
│   ├── classes.js                # Registry — add new classes here
│   ├── licw-overlearn-int1.js    # LICW Overlearn (INT2 v1.3) — generated
│   └── cwops-intermediate.js     # CWA Intermediate — stub
├── _sources/               # Build inputs, NOT deployed
│   ├── licw-int2-v13.pdf         # Original PDF
│   ├── extract_pdf_links.py      # Helper: list every URI annotation
│   ├── map_licw_links.py         # Maps PDF link rects → exercise list
│   └── build_class_data.py       # Emits data/licw-overlearn-int1.js
└── README.md
```

The `_sources/` folder is excluded from deployment via `.gitignore` for
release branches if you want; for the main branch we keep it so the build
process is reproducible.

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
   shape used by the existing class files (`id`, `shortName`, `longName`,
   `subtitle`, `description`, `source`, `intro`, `assessment`, `lessons`).
2. Register it in `data/classes.js` by adding an entry to the `classes` array.
3. That's it — the selector picks it up automatically.

If your class is built from a PDF with hyperlink-bearing exercises, copy
`_sources/build_class_data.py` and adjust the `LESSON_NARRATIVES` and the
page-to-lesson mapping in `_sources/map_licw_links.py` to match your source.

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

## Updating the LICW class from the PDF

If the LICW guide gets a new revision:

```bash
# 1. Drop the new PDF into _sources/
# 2. Re-extract URIs
python _sources/map_licw_links.py _sources/<new-pdf> _sources/licw-mapped.json
# 3. Edit lesson narratives in _sources/build_class_data.py if they changed
# 4. Regenerate the class data file
python _sources/build_class_data.py
```

The script will report any lesson where the URL count doesn't match the
expected exercise count — usually a sign the page layout or exercise list
shifted in the new revision.

## Deploying to Hostinger

Two options:

### Option A — Git pull on the server (recommended)

If you have SSH access (Hostinger Business plan and up):

```bash
ssh u409587525@<host>
cd /home/u409587525/domains/triplehatsecurity.com/public_html/morse
git clone https://github.com/<you>/morse-practice .   # first time
git pull                                              # subsequent updates
```

Or use Hostinger's built-in Git deployment in hPanel:
*Websites → Manage → Advanced → Git*. Connect the GitHub repo and set the
deploy path to `/morse`. Auto-deploy on push if you turn on the webhook.

### Option B — Drag-and-drop via File Manager / SFTP

Upload everything except `_sources/` and `.git` to
`/home/u409587525/domains/triplehatsecurity.com/public_html/morse/`.

The site is fully static — no `.htaccess` or server config required.

## Resetting your progress

Open browser devtools → Application → Local Storage → your origin →
delete the `mpc.state.v1` key. Or in the console:

```js
localStorage.removeItem("mpc.state.v1");
```

## Credits

Source materials are © their respective owners (Long Island CW Club Inc.,
CW Academy / CWops). This app is a personal study companion, not affiliated
with or endorsed by either organization.

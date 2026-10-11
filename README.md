# 🛍️ MallOfAmericans — Etsy AI Launch Studio

A functional Python + **Streamlit web application** developed from the MallOfAmericans Claude Etsy Digital Launch Skill. Generate buyer-ready original US Letter printable/fillable PDFs, **10 actual 2400×1800 JPG listing mockups**, **two actual 15-second silent HD MP4 previews**, structured SEO, manifest checks and separate download ZIPs.

![Status: Python](https://img.shields.io/badge/Python-3.11-blue) ![UI: Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b) ![License: MIT](https://img.shields.io/badge/License-MIT-green)

> **Not affiliated with Etsy or Anthropic.** This app is an independently authored content-production tool, not an Etsy publishing integration. Product opportunity scores are heuristic and do not establish sales, true search volume or low competition.

## ✨ Features & the real limits

| Function | Implementation | Conditions |
|---|---|---|
| 10 US digital-product opportunities | Curated, scored shortlist | Without live search results these are **UNVERIFIED ideas**, not market winners |
| Live keyword and competitor discovery | Brave Search API, US-region public web results | Optional `BRAVE_SEARCH_API_KEY`; do not infer sales/hidden tags from results |
| Five competitor URLs | Etsy listing links with title/snippet *if visibly returned* | Search snippets are not complete listing audits; no fake competitor data |
| Original products | ReportLab, printable + working AcroForm fillable PDF | Built-in tested multi-pet example works offline; other niches require Anthropic key |
| Claude product generation | Anthropic Messages API generates useful original structured pages | Optional `ANTHROPIC_API_KEY`, billable, model access required |
| Claude listing SEO | Actual title, description, 13 validated Etsy tags | Without key, example SEO is editorial draft (not validated search-volume evidence) |
| 10 product mockups | Pillow + rendered PDF pages | 2400 × 1800 JPG, no fictitious product screenshots |
| Two product videos | FFmpeg from real mockups | Two 15-second 1080×1080 silent MP4s; server must have `ffmpeg` |
| QA + Downloads | PyMuPDF, Pillow, ffprobe + ZIP | Verifies files/dimensions/durations, marks missing transparently |

## 🚀 GitHub upload & deploy (recommended: Streamlit Community Cloud)

**1 — Create a GitHub repository.** Create an empty repo like `mallofamericans-etsy-studio` (private if preferred). Extract the contents of the provided repository ZIP **directly into the repo root**. Upload/commit `app.py`, `engine/`, `templates/`, `scripts/`, `.streamlit/config.toml`, `requirements.txt` and `packages.txt` together. **Never upload real API keys.**

**2 — Deploy:** Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** → choose your GitHub repository and branch → main file `app.py` → Deploy. A static GitHub Pages site cannot run the Python backend.

**3 — Optional credentials:** In Streamlit app settings → **Secrets**, add:

```toml
ANTHROPIC_API_KEY = "your_anthropic_key"
BRAVE_SEARCH_API_KEY = "your_brave_search_key"
```

You can alternatively paste keys in the app sidebar for that session only. Keys in `secrets.toml` must NEVER be committed. A Claude subscription is not the same as an Anthropic API account; API use may incur separate charges. Brave Search may also charge for API access. You can run the included sample **without either key**.

**4 — Use the tool:** Open the deployed URL. Run opportunity research; choose a niche; add/verify real competitor links; create an original product blueprint; generate buyer PDF files and final SEO; click **Generate complete launch package** and download the *separate* buyer and seller ZIPs. The full generation can take several minutes due to two HD videos.

**5 — Review before Etsy publication:** Verify product contents, legal rights, dimensions, listing text, truthful mockups and current Etsy rules. The tool does not log in to or publish on Etsy.

### Local development

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Ensure ffmpeg and ffprobe are on your PATH
streamlit run app.py
```

For Ubuntu/Debian: `sudo apt-get install ffmpeg fonts-dejavu-core`.

### Demo mode without paid APIs

Choose **Multi-Pet Sitter Handoff Kit**, select **Use built-in original sample**, and click **Prepare product blueprint and SEO**. This creates a **12-page, 96-fillable-field** buyer PDF kit, draft SEO, ten JPG mockups, two videos and structured ZIPs. It is a functional offline production demo, **not proof of market demand**. To design a different niche, supply your Anthropic API key.

### Data and privacy

- Keys typed in the UI remain in the session. Deployment secrets are stored by Streamlit, not in committed code.
- Projects are written to temporary server storage; Streamlit Community Cloud may clear files on restart. Download your ZIPs immediately.
- Public search-result titles/snippets may not match live Etsy listing contents or prices. Verify directly, and do not repackage competitor content.
- Generated form PDFs may contain buyers' private data after filling; do not ask customers to send completed forms to a public website.
- Media generator needs enough time/CPU/memory for ten images and two HD videos. If video generation is disabled or fails, QA marks the project **incomplete**.
- Original designs and AI-assisted content must comply with current Etsy rules, including AI disclosure where applicable; no guarantee of sales or ranking.

## Repository structure

```text
app.py                         # Streamlit user interface
engine/research.py             # opportunity ideas, Brave public results, competitor URLs
engine/ai.py                   # optional Anthropic JSON blueprint & SEO
engine/product.py              # genuine printable + fillable PDFs, preview rendering
engine/seo.py                  # SEO draft, validation, export
engine/package.py              # media QA, manifests, seller & buyer ZIPs
scripts/asset_factory.py       # ten JPG mockups, two 15 s MP4s from real PDF previews
templates/pet_sitter.json       # included original offline demo product blueprint
requirements.txt / packages.txt
.streamlit/config.toml
.streamlit/secrets.toml.example
.github/workflows/tests.yml    # auto tests on push
CLAUDE_SKILL.md                # associated skill instructions
```

## Test

```bash
python -m pytest -q
```

## Notes for production deployment

On Streamlit Community Cloud, concurrent HD video jobs can overload smaller instances. For many concurrent users, move rendering to a background worker (Celery/RQ) and use authenticated private storage; the supplied version is designed as a single-seller operational prototype, not a scaled SaaS. Do not treat its subjective opportunity heuristic as a paid search analytics tool.

## Originality & license

Code MIT licensed (see LICENSE). User-generated product files remain the user's responsibility. No claim of affiliation or endorsement by Etsy/Claude/Anthropic. Check latest marketplace rules before listing.

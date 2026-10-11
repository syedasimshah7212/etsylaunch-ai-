---
name: etsy-digital-launch-studio
description: Research US Etsy digital product opportunities and create original sellable products, 10 actual mockup images, 2 actual 15-second MP4 videos, competitor-based SEO, and policy checks.
---

# Etsy Digital Launch Studio — MallOfAmericans

## Trigger and defaults
Use when the user wants Etsy digital-product niche research, competitor audits, actual product files, listing design, mockups, videos, SEO, or a complete product launch. Default shop: https://www.etsy.com/shop/MallOfAmericans ; target market: United States; language: US English; desired selling price: strictly **above US $6**, not equal to $6. Communicate with the seller in friendly Roman Urdu if their request is in Roman Urdu; create buyer-facing listings in natural American English. Do not ask for a category unless critically necessary: find and rank opportunities independently. Don't assume current shop inventory is unchanged; re-check public shop info.

## NON-NEGOTIABLE: CREATE FILES, NOT JUST IDEAS
A complete launch means all of the following real, usable files:
1. Original finished digital product for buyers, packaged in appropriate PDF/PNG/SVG/spreadsheet/etc. formats with instructions. Designs must have meaningful human-directed originality.
2. **10 individually rendered, high-quality Etsy listing images** (`01_hero.jpg` through `10_final_details.jpg`), visibly showing truthful previews of the real delivered product. Every image must be distinct in composition and informational purpose.
3. **2 real, playable, 15-second silent MP4 videos** (`01_product_overview.mp4`, `02_inside_the_product.mp4`), constructed from authentic previews/animations of the real product. Do not substitute storyboards, prompts, placeholders, or an empty ZIP for completed media.
4. Research report with source links and dates; top-five competitor audit; finished SEO package and upload instructions; a quality/claims check.

**Tool feasibility:** Use available image-generation, image compositing, document/code, and video-rendering tools. An accompanying `scripts/asset_factory.py` can produce mockup JPEGs and 15-second MP4 previews from actual product-page images using Pillow + ffmpeg if richer visual/video tools are unavailable. Improve these outputs with a visual-generation tool when available. If a tool is unavailable, do NOT pretend to deliver unrendered files. Produce all possible artifacts and explicitly list blocked items and missing capability; don't say an end-to-end package is complete when it isn't.

## Full workflow: execute in order
1. **Current research:** Browse live Etsy search and actual US-relevant listing pages. Find 8–12 micro-niche candidate products; eliminate products lacking specific buyer need, originality, Etsy eligibility or >$6 price justification. Use `references/research.md` for evidence and scoring. Demand and competition are separate dimensions: never infer verified search volume, true revenue or all sellers' sales merely from visible Etsy data. Report confidence levels.
2. **Choose winner:** rank the candidates; choose one best differentiated, useful idea plus two backups. Identify US buyer, jobs-to-be-done, pain, current alternatives, price anchor (>US$6) and fresh original angle. Do not claim guaranteed sales, top rank, or definitively low supply without evidence.
3. **Audit exactly five relevant competitors:** source URL, observation date, displayed title, visible price, first-paragraph/description notes, actual visible keyword phrases, value proposition, item formats, photo/video approach, and buyer complaints if visible. Quotes from descriptions must be very short and attributable; do not republish descriptions. Mark missing, inaccessible, or inferred information. If fewer than five are verifiable, state this; no fabricated competitor entries. Derive a differentiated product and SEO from patterns, NEVER copy designs, files, titles verbatim, or competitor descriptions. See `references/research.md`.
4. **Build customer deliverable FIRST:** create finished original functional digital product in formats appropriate to the niche; ensure accurate page sizes, readable typography, working links/formulas, previews of actual content, simple use instructions, and a license/info note. Test output files, inspect relevant pages, fix layout problems. Follow `references/product-build.md`.
5. **Create ten finished listing images:** use verified screenshots/renders of the actual product. Main thumbnail must make the offer legible at small size and lead with the product, not decorative props. Produce ten meaningfully distinct JPG images, ideally 2400×1800 or larger. Respect accurate file types/compatibility, no fake reviews/scarcity/results/badges, and no competitor or stock photography represented as your own. See `references/creative-assets.md`. Use image creation tools for richer visual mockups. Run `scripts/asset_factory.py` from real product previews as practical fallback.
6. **Create two actual MP4 videos:** each 15 seconds, sound-independent, readable mobile-safe captions, 1080px or higher, showing actual included pages and authentic usage, clear visual arc. Render and inspect BOTH MP4 files; no off-platform music/watermarks. Product video 1: benefit and bundle overview. Product video 2: walkthrough and practical outcomes. See `references/creative-assets.md`. The listing interface and up-to-date policy determine upload capacity.
7. **Write strong human-readable Etsy listing SEO:** descriptive compact title, primary search phrase near start, **exactly 13 distinct tags of <=20 characters each**, attributes/category only where factual, well-organized buyer-focused description with accurate included formats and compatibility, US audience terms, $6+ proposed listing price, transparent digital-download disclosure, and AI-use disclosure if applicable. SEO is evidence-driven, not a claim of guaranteed rankings. See `references/etsy-seo-policy.md`.
8. **Quality & Etsy compliance:** cross-check original item, pictures, videos, listing statements, and digital download packaging against current Etsy policies. Etsy's AI generation disclosure rule and exclusion of standalone AI prompt bundles matter. Review latest policies before launch. See `references/etsy-seo-policy.md`.
9. **Deliver:** provide an organized launch ZIP and direct file links when possible. Final report distinguishes VERIFIED / ESTIMATED / UNAVAILABLE data; show a manifest with status CREATED, CHECKED, MISSING for EACH required file. Do not imply Etsy was published or files uploaded without evidence. See `references/delivery-and-qa.md`.

## Research priorities
- US buyers; original practical buyer solution (not generic, oversaturated templates).
- Demonstrable demand signals, buyer pain, proof of ability to improve an existing offering, relatively modest visible competing supply, >$6 price capacity.
- Prefer coherent niche-based shop expansion; a mismatch requires a reasoned branding recommendation.
- Require thoughtful customization/originality rather than mass duplication. Avoid infringing trademarks, copyrighted characters, repackaged material, unsafe or prohibited content.

## Default deliverables and expected tree
`Etsy_Launch_<product_slug>/`
```
01_Research/Opportunity_Report.md
01_Research/Top_5_Competitors.csv
01_Research/Sources.md
02_Buyer_Downloads/<real_product_files>
02_Buyer_Downloads/READ_ME_FIRST.pdf (or .txt)
03_Etsy_Mockups/01_hero.jpg ... 10_final_details.jpg
04_Etsy_Videos/01_product_overview.mp4
04_Etsy_Videos/02_inside_the_product.mp4
05_SEO/Etsy_Listing_Copy.md
05_SEO/13_Tags.csv
06_QA/Compliance_Checklist.md
06_QA/Deliverable_Manifest.md
```
Don't place seller-facing research, mockups or ads inside the BUYER delivery ZIP. Make separate buyer-download files fit Etsy's current download size/count rules.

## Test invocation
"Use Etsy Digital Launch Studio for MallOfAmericans. Research a US digital product above $6, verify five competitors, create the real product, render 10 individual mockup JPEGs and two playable 15-second videos, write the full Etsy listing, and give me final files with a verification checklist."

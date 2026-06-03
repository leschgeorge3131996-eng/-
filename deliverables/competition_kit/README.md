# Competition Kit

This folder contains near-final static deliverables for judging/demo material
production.

Current printable baseline:

- `deck_3page_final.pdf`
  - repo-generated export with `3` pages for the official judged-deck storyline
- `deck.pdf`
  - repo-generated export with `6` pages as the older compression baseline
- `poster.pdf`
  - repo-generated export with `1` page
- `node scripts/export_competition_pdfs.js`
  - now performs HTML/PDF sanity checks before a baseline is treated as valid

Important:

- `evidence/materials/PPT_DECK_3PAGES_FINAL.md` and `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md` are now the current official-source drafts for the judged submission assets.
- `deck_3page_final.html` / `deck_3page_final.pdf` are the current repo-native printable baseline for the official `3`-page judged deck.
- `deck.html` / `deck.pdf` remain the older `6`-page visual baseline, not the final official `3`-page submission deck.
- `video_subtitles_5min_final.srt` is the current timed narration baseline for the official `5`-minute submission video.
- `video_subtitles.srt` remains the older `2`-minute narration baseline.

## Files

- `deck_3page_final.html`
  - repo-native `3`-page judged-deck HTML that follows `PPT_DECK_3PAGES_FINAL.md`
- `deck_3page_final.pdf`
  - current repo-generated PDF export from `deck_3page_final.html`
- `deck.html`
  - six-slide presentation draft that can be printed to PDF or imported into a
    slide workflow as a visual baseline
- `deck.pdf`
  - current repo-generated PDF export from `deck.html`
- `poster.html`
  - poster draft that can be printed to PDF or used as a layout reference
- `poster.pdf`
  - current repo-generated PDF export from `poster.html`
- `video_subtitles_5min_final.srt`
  - timed subtitles / narration baseline for the 5-minute judged video
- `video_subtitles.srt`
  - timed subtitles / narration baseline for the 2-minute demo video
- `styles.css`
  - shared visual system for both files

## Source Of Truth

These HTML deliverables are intentionally aligned to the locked gold-sample
story:

- `evidence/materials/COMPETITION_ASSET_PACK.md`
- `evidence/materials/PPT_DECK_3PAGES_FINAL.md`
- `evidence/materials/PPT_DECK_6SLIDES.md`
- `evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md`
- `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
- `evidence/materials/POSTER_COPY.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`

## Suggested Use

1. Open `deck_3page_final.html` in a browser when you need the official judged-deck story in printable form.
2. Open `deck.html` only when you need the older `6`-page compression baseline.
3. Open `poster.html` in a browser for the poster layout reference.
4. Use `video_subtitles_5min_final.srt` for the official `5`-minute narration timing.
5. If a designer or another operator takes over, hand them this folder, `PPT_DECK_3PAGES_FINAL.md`, `VIDEO_SHOTLIST_5MIN_FINAL.md`, plus the export bundle from `scripts/export_competition_asset_pack.ps1`.
6. To export repo-native PDFs directly, run `node scripts/export_competition_pdfs.js`.

## Editing Notes

- Screenshot references point to `evidence/screenshots/20260529_gold_*`（最终金标截图集）。
- If the locked sample changes, update the source markdown files first, then
  update these HTML files.
- Keep the main story centered on evidence-backed `ask`; do not reframe this as
  generic chat.
- If `deck_3page_final.pdf` is not `3` pages, `deck.pdf` is not `6` pages, or
  `poster.pdf` is not `1` page, treat the export as invalid and rerun
  `node scripts/export_competition_pdfs.js` after fixing the source HTML/CSS.

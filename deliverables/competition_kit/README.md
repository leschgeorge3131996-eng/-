# Competition Kit

This folder contains near-final static deliverables for judging/demo material
production.

## Files

- `deck.html`
  - six-slide presentation draft that can be printed to PDF or imported into a
    slide workflow as a visual baseline
- `deck.pdf`
  - current repo-generated PDF export from `deck.html`
- `poster.html`
  - poster draft that can be printed to PDF or used as a layout reference
- `poster.pdf`
  - current repo-generated PDF export from `poster.html`
- `styles.css`
  - shared visual system for both files

## Source Of Truth

These HTML deliverables are intentionally aligned to the locked gold-sample
story:

- `evidence/materials/COMPETITION_ASSET_PACK.md`
- `evidence/materials/PPT_DECK_6SLIDES.md`
- `evidence/materials/VIDEO_SHOTLIST_2MIN.md`
- `evidence/materials/POSTER_COPY.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`

## Suggested Use

1. Open `deck.html` in a browser.
2. Print to PDF in landscape mode with background graphics enabled.
3. Open `poster.html` in a browser.
4. Print to PDF in portrait mode with background graphics enabled.
5. If a designer or another operator takes over, hand them this folder plus the
   export bundle from `scripts/export_competition_asset_pack.ps1`.
6. To export repo-native PDFs directly, run `node scripts/export_competition_pdfs.js`.

## Editing Notes

- Screenshot references point to `evidence/screenshots/20260418_*`.
- If the locked sample changes, update the source markdown files first, then
  update these HTML files.
- Keep the main story centered on evidence-backed `ask`; do not reframe this as
  generic chat.

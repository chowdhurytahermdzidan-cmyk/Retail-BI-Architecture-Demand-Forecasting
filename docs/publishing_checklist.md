# Read before publishing publicly

This project is staged for **review**, not automatically authorised for public publication.

- [ ] Confirm the institution allows publication of work derived from the coursework and any Power BI/dashboard screenshots containing summaries of the course dataset.
- [ ] Confirm the original retail workbook is permitted to be redistributed **before** adding it. The current repo excludes original transaction-level data.
- [ ] Check whether your `.pbix` files embed course data. They are **excluded** from this package by default to avoid exposing restricted records. Only upload them if the data rights allow it; otherwise produce a sanitized/demo `.pbix` with new synthetic source data and verify every report visual.
- [ ] Remove student ID, personal contact information, university cover page, lecturer details, rubrics and submission material from anything uploaded.
- [ ] Review every screenshot for disclosure-sensitive totals/labels and publication permission. If permission is unclear, keep `assets/` screenshots private or replace them with independently generated demo visuals.
- [ ] Make sure no notebook contains local file paths, execution metadata identifying you, hidden Excel data, personal IDs or API credentials.
- [ ] Verify the forecast results in README are labelled as **original coursework** results, not the synthetic demo results.
- [ ] Do not claim a deployed SQL warehouse, automated ETL, RLS, forecast-dashboard integration or operational forecasting accuracy.
- [ ] Update `README.md` with a public dashboard/demo link only if you have published it lawfully.
- [ ] Choose and add a `LICENSE` only after deciding how others may reuse your original code/screenshots.

## Suggested publication process

1. Review and confirm rights for all files.
2. Test the notebook and script locally.
3. Create a GitHub repository, initially **Private**.
4. Upload the reviewed files and check Markdown images/code blocks display properly.
5. Make it public only after rights and privacy checks have passed.

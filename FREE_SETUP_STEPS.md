# Free setup checklist

## Step 1 — GitHub
1. Create a public repository named `data-engineering-portfolio`.
2. Extract this ZIP locally.
3. Copy the project folders into the repository.
4. Commit the files. Keep any real data files out of Git if they are large or subject to dataset terms.

## Step 2 — Databricks Free Edition
1. Visit https://docs.databricks.com/aws/en/getting-started/free-edition
2. Create a Free Edition workspace.
3. Use serverless notebook compute; do not create a paid cloud resource.
4. Upload your Olist CSV data to a Unity Catalog Volume.
5. Replace placeholder paths/catalog/schema values in the code with your actual values.
6. Run each notebook in order and verify row counts.

## Step 3 — Olist dataset
1. Search Kaggle for “Brazilian E-Commerce Public Dataset by Olist”.
2. Download the relevant CSV files.
3. Upload the order dataset first. For a richer project, later include customers, items, products, payments, and sellers.
4. Keep data files local or in your Databricks Volume; do not push raw data into GitHub.

## Step 4 — Validate, document, and show evidence
- Record Bronze/Silver/Gold row counts.
- Show invalid-row/quarantine counts and duplicate checks.
- Capture the Gold summary output.
- For performance work, record the execution plan and measured durations from your actual run.
- For automation, capture the GitHub Actions test result and Databricks job run history.
- Update each README with exact commands, screenshots, and real results.

## Step 5 — Resume honesty
Only list features as completed after you have run and verified them. For features not supported by the free workspace, write “designed/tested locally” rather than claiming cloud deployment.

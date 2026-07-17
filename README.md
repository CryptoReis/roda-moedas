# 💰 Roda Moedas

Streamlit app for recording monthly coin and bill counts, calculating how much goes to **troca-notas** and **banco**, and saving the same v1-compatible columns to Google Sheets.

## V2 changes

- `Reis` is now the second option in the user dropdown.
- `0,10 €` and `0,05 €` coins are part of the initial coin form.
- `0,10 €` and `0,05 €` always count toward **banco**.
- The user can choose how much of the available `1 €` coin value goes to **troca-notas**.
- The user can choose how much of the available `0,50 €` coin value goes to **troca-notas**.
- Any `1 €` / `0,50 €` amount not assigned to **troca-notas** automatically counts toward **banco**.
- The Google Sheets output columns are preserved from v1.

## Google Sheets columns

The app writes the same columns as the original version:

```text
Timestamp
User
Date
Moeda_2EUR_Qty
Moeda_2EUR_Total
Moeda_1EUR_Qty
Moeda_1EUR_Total
Moeda_05EUR_Qty
Moeda_05EUR_Total
Moeda_02EUR_Qty
Moeda_02EUR_Total
Moeda_01EUR_Qty
Moeda_01EUR_Total
Moeda_005EUR_Qty
Moeda_005EUR_Total
Nota_20EUR_Qty
Nota_20EUR_Total
Nota_10EUR_Qty
Nota_10EUR_Total
Nota_5EUR_Qty
Nota_5EUR_Total
Troca_Total
Banco_Total
Grand_Total
Notes
```

## Safe testing without live data

### Option A — local dry-run test

If Google Sheets secrets are absent, the app automatically uses session-only dry-run storage.
Nothing is written to Google Sheets.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Option B — Streamlit Cloud test app with no writes

Create a second Streamlit Cloud app from the `v2-rewrite` branch and add this to the app secrets:

```toml
[app]
dry_run = true
```

You can also paste the production `[connections.gsheets]` secrets into the test app; `dry_run = true` prevents writes and uses session-only test data.

### Option C — Streamlit Cloud test app with a test Google Sheet

Recommended before production use:

1. Create a separate Google Sheet for testing.
2. Share it with the same Google service account email as **Editor**.
3. Create a second Streamlit Cloud app from the `v2-rewrite` branch.
4. Copy the same secrets as production, but change only:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_TEST_SHEET_ID/edit"
```

Do **not** set `dry_run = true` if you want to test real writes to the test sheet.

## Production secrets

For live Google Sheets writes, Streamlit secrets must include:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

Never commit `.streamlit/secrets.toml` or service-account JSON files.

## Run tests

```bash
. .venv/bin/activate
pip install pytest
PYTHONPATH=src pytest -q
```

## Run locally

```bash
. .venv/bin/activate
streamlit run app.py
```

## Deployment recommendation

Keep the current production app on `main` until v2 is approved.
Deploy a separate Streamlit Cloud test app from a separate branch, for example:

```text
Repository: CryptoReis/roda-moedas
Branch: v2-rewrite
Main file: app.py
Suggested URL: roda-moedas-v2.streamlit.app
```

After testing and approval, merge v2 into `main` or repoint the production Streamlit app to the approved branch.

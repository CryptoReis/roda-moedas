# 💰 Roda Moedas - Financial Input Tool

A Streamlit web application for tracking monthly coin and bill data with automatic calculations and Google Sheets storage.

## 🚀 Features

- **User-friendly form** with dropdown user selection
- **Coin inputs**: 2 EUR, 1 EUR, 0.5 EUR, 0.2 EUR
- **Bill inputs**: 20 EUR, 10 EUR, 5 EUR
- **Automatic calculations** (quantity × denomination)
- **Two summary tables**:
  - **Para troca-notas**: 1 EUR + 0.5 EUR totals
  - **Para banco**: 20, 10, 5, 2, 0.2 EUR totals (with optional 0.1 and 0.05 EUR)
- **Google Sheets integration** for persistent storage
- **Recent entries view** showing last 5 submissions

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account (free tier is sufficient)
- Google Sheets spreadsheet

## 🔧 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit streamlit-gsheets-connection pandas
```

### 2. Set Up Google Sheets API

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name your project (e.g., "Roda Moedas") and click "Create"

#### Step 2: Enable Google Sheets API

1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"

#### Step 3: Create Service Account Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in the service account details:
   - Name: `roda-moedas-service`
   - ID: (auto-generated)
   - Click "Create and Continue"
4. Skip "Grant this service account access to project" (optional)
5. Click "Done"

#### Step 4: Generate JSON Key

1. Find your newly created service account in the list
2. Click on it to open details
3. Go to the "Keys" tab
4. Click "Add Key" → "Create new key"
5. Choose "JSON" format
6. Click "Create" - a JSON file will be downloaded

#### Step 5: Create and Share Google Sheet

1. Create a new Google Sheet (or use an existing one)
2. Copy the Google Sheet URL
3. Click "Share" button
4. Paste the **service account email** (from the JSON file, look for `client_email`)
5. Set permission to **Editor**
6. Click "Send"

### 3. Configure Secrets

1. Copy the template:

   ```bash
   # The .streamlit folder should already exist
   # Edit the secrets.toml file
   ```

2. Open `.streamlit/secrets.toml` and replace the placeholders with values from your downloaded JSON file:

   ```toml
   [connections.gsheets]
   spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
   type = "service_account"
   project_id = "your-project-id"
   private_key_id = "your-private-key-id"
   private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n"
   client_email = "your-service-account@your-project.iam.gserviceaccount.com"
   client_id = "your-client-id"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "your-cert-url"
   ```

   **Important Notes:**
   - Keep the `\n` characters in the private key
   - The spreadsheet URL is your Google Sheet's full URL
   - All values come directly from the downloaded JSON file

## 🌐 Deployment to Streamlit Community Cloud

**RECOMMENDED**: Deploy your app to Streamlit Community Cloud so your 5-10 friends can access it from anywhere via a public URL.

### Why Streamlit Community Cloud?

- ✅ **Free hosting** for public apps
- ✅ **Easy deployment** directly from GitHub
- ✅ **Automatic updates** when you push code changes
- ✅ **24/7 availability** - no need to keep your computer running
- ✅ **Public URL** like `https://roda-moedas.streamlit.app`

### Deployment Steps

#### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in (or create an account)
2. Click the "+" icon → "New repository"
3. Name it: `roda-moedas`
4. Choose **Private** (recommended) or Public
5. Click "Create repository"

#### Step 2: Push Your Code to GitHub

Open a terminal in your project directory and run:

```bash
# Initialize git repository
git init

# Add all files (secrets.toml is already in .gitignore so it won't be uploaded)
git add .

# Commit your files
git commit -m "Initial commit - Roda Moedas app"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/roda-moedas.git

# Push to GitHub
git branch -M main
git push -u origin main
```

> [!IMPORTANT]
> The `.gitignore` file ensures your `secrets.toml` and credentials are NOT uploaded to GitHub.

#### Step 3: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub" and authorize Streamlit
3. Click "New app"
4. Fill in the deployment settings:
   - **Repository**: Select `your-username/roda-moedas`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL like `roda-moedas` (final URL will be `https://roda-moedas.streamlit.app`)
5. Click "Advanced settings"

#### Step 4: Add Secrets to Streamlit Cloud

1. In the "Advanced settings" section, find the "Secrets" text area
2. Copy the entire contents from your local `.streamlit/secrets.toml` file
3. Paste it into the Secrets text area in Streamlit Cloud
4. Click "Deploy!"

#### Step 5: Wait for Deployment

- Streamlit will build and deploy your app (takes 2-5 minutes)
- Once complete, you'll see your app running
- **Share the URL** with your friends! 🎉

### Managing Your Deployed App

**View logs**: Click the "Manage app" button to see logs and errors

**Update secrets**: Go to app settings → Secrets → Edit

**Redeploy**: Any time you push changes to GitHub, the app automatically redeploys

**Restart app**: If needed, click "☰" menu → "Reboot app"

### Accessing the App

Once deployed, your friends can access the app at:

```text
https://YOUR-APP-NAME.streamlit.app
```

They just need to:

1. Open the URL in their browser
2. Fill in the form
3. Submit their data
4. Data is saved to your Google Sheet!

---

## 🎯 Local Usage (Optional)

If you want to run the app locally for testing:

### Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Form

1. Select the **User** from the dropdown
2. Enter quantities for each **coin** category (Moedas)
3. Enter quantities for each **bill** category (Notas)
4. Select the **Date** (defaults to today)
5. Add any optional **Notes**
6. Click **Submit Entry**
7. View calculated totals in two tables:
   - **Para troca-notas**: Exchange coins summary
   - **Para banco**: Bank deposit summary (with optional 0.1 and 0.05 EUR fields)
8. Data is automatically saved to Google Sheets
9. View the last 5 entries at the bottom of the page

### Validation

- The form will not submit if the total amount is 0
- All numeric inputs only accept whole numbers (no decimals)
- Date defaults to today but can be changed

## 📊 Data Structure

Each submission saves the following to Google Sheets:

- Timestamp
- User name
- Date
- Quantities and totals for each coin/bill category
- Troca total (exchange coins)
- Banco total (bank deposit)
- Grand total
- Notes

## 🔒 Security Notes

- **Never commit** `.streamlit/secrets.toml` to version control
- Keep your service account JSON file secure
- Add `.streamlit/secrets.toml` to `.gitignore`

## 🛠️ Troubleshooting

### "Failed to connect to Google Sheets"

- Verify your `secrets.toml` is correctly configured
- Ensure the Google Sheets API is enabled in your project
- Check that you shared the sheet with the service account email

### "Permission denied" errors

- Make sure the service account email has **Editor** permissions on your Google Sheet
- Verify the spreadsheet URL in `secrets.toml` is correct

### Data not appearing

- Check that your Google Sheet has a worksheet named "Sheet1"
- Verify the sheet is not protected or locked

## 📝 License

This project is open source and available for personal use.

## 👥 Users

- Vanda
- Renato
- André
- Daniela
- Silvia
- Parada
- Mafalda
- Reis

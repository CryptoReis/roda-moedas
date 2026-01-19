"""
Financial Input Tool - Monthly Data Entry for Coins and Bills

INSTALLATION REQUIREMENTS:
    pip install streamlit streamlit-gsheets-connection

GOOGLE SHEETS API SETUP:
    1. Go to Google Cloud Console (https://console.cloud.google.com/)
    2. Create a new project or select an existing one
    3. Enable the Google Sheets API
    4. Create a Service Account and download the JSON credentials file
    5. Share your Google Sheet with the service account email address (with Editor permissions)
    
SECRETS.TOML CONFIGURATION:
    Create a file at .streamlit/secrets.toml with the following structure:
    
    [connections.gsheets]
    spreadsheet = "YOUR_GOOGLE_SHEET_URL"
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
"""

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Roda Moedas - Financial Input Tool",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Roda Moedas - Monthly Data Entry")
st.markdown("---")

# Initialize Google Sheets connection
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"❌ Failed to connect to Google Sheets. Please check your configuration.\n\nError: {str(e)}")
    st.stop()

# User list
USERS = ["Vanda", "Renato", "André", "Daniela", "Silvia", "Parada", "Mafalda", "Reis"]

# Create the input form
with st.form("financial_input_form", clear_on_submit=True):
    st.subheader("📋 Input Data")
    
    # User selection
    selected_user = st.selectbox("User", USERS, index=0)
    
    # Create two columns for Moedas and Notas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🪙 Moedas (Coins)")
        moeda_2eur = st.number_input("2 EUR", min_value=0, step=1, value=0, format="%d")
        moeda_1eur = st.number_input("1 EUR", min_value=0, step=1, value=0, format="%d")
        moeda_05eur = st.number_input("0,5 EUR", min_value=0, step=1, value=0, format="%d")
        moeda_02eur = st.number_input("0,2 EUR", min_value=0, step=1, value=0, format="%d")
    
    with col2:
        st.markdown("### 💵 Notas (Bills)")
        nota_20eur = st.number_input("20 EUR", min_value=0, step=1, value=0, format="%d")
        nota_10eur = st.number_input("10 EUR", min_value=0, step=1, value=0, format="%d")
        nota_5eur = st.number_input("5 EUR", min_value=0, step=1, value=0, format="%d")
    
    # Date and notes
    st.markdown("### 📅 Additional Information")
    entry_date = st.date_input("Date", value=datetime.now().date())
    notes = st.text_area("Notes", placeholder="Optional notes about this entry...")
    
    # Submit button
    submitted = st.form_submit_button("✅ Submit Entry", use_container_width=True, type="primary")

# Process form submission
if submitted:
    # Calculate individual totals
    total_moeda_2eur = moeda_2eur * 2.0
    total_moeda_1eur = moeda_1eur * 1.0
    total_moeda_05eur = moeda_05eur * 0.5
    total_moeda_02eur = moeda_02eur * 0.2
    
    total_nota_20eur = nota_20eur * 20.0
    total_nota_10eur = nota_10eur * 10.0
    total_nota_5eur = nota_5eur * 5.0
    
    # Calculate grand total
    total_all = (total_moeda_2eur + total_moeda_1eur + total_moeda_05eur + 
                 total_moeda_02eur + total_nota_20eur + total_nota_10eur + total_nota_5eur)
    
    # Validation: Don't allow submission if total is 0
    if total_all == 0:
        st.error("❌ Cannot submit entry with zero total. Please enter at least one amount.")
    else:
        st.success("✅ Entry submitted successfully!")
        
        # Display calculation results
        st.markdown("### 📊 Calculation Results")
        
        # Individual results
        with st.expander("💡 Individual Category Results", expanded=True):
            results_col1, results_col2 = st.columns(2)
            
            with results_col1:
                st.markdown("**🪙 Moedas:**")
                st.write(f"- 2 EUR: {moeda_2eur} × 2.00 = **{total_moeda_2eur:.2f} EUR**")
                st.write(f"- 1 EUR: {moeda_1eur} × 1.00 = **{total_moeda_1eur:.2f} EUR**")
                st.write(f"- 0.5 EUR: {moeda_05eur} × 0.50 = **{total_moeda_05eur:.2f} EUR**")
                st.write(f"- 0.2 EUR: {moeda_02eur} × 0.20 = **{total_moeda_02eur:.2f} EUR**")
            
            with results_col2:
                st.markdown("**💵 Notas:**")
                st.write(f"- 20 EUR: {nota_20eur} × 20.00 = **{total_nota_20eur:.2f} EUR**")
                st.write(f"- 10 EUR: {nota_10eur} × 10.00 = **{total_nota_10eur:.2f} EUR**")
                st.write(f"- 5 EUR: {nota_5eur} × 5.00 = **{total_nota_5eur:.2f} EUR**")
        
        # Para troca-notas table
        st.markdown("### 🔄 Para troca-notas")
        troca_total = total_moeda_1eur + total_moeda_05eur
        
        troca_data = {
            "Category": ["1 EUR", "0.5 EUR", "**TOTAL**"],
            "Amount (EUR)": [
                f"{total_moeda_1eur:.2f}",
                f"{total_moeda_05eur:.2f}",
                f"**{troca_total:.2f}**"
            ]
        }
        troca_df = pd.DataFrame(troca_data)
        st.table(troca_df)
        
        # Para banco table with optional fields
        st.markdown("### 🏦 Para banco")
        
        # Optional fields for 0.1 and 0.05 EUR
        banco_col1, banco_col2 = st.columns(2)
        with banco_col1:
            moeda_01eur = st.number_input("0,1 EUR (Optional)", min_value=0, step=1, value=0, format="%d", key="banco_01")
        with banco_col2:
            moeda_005eur = st.number_input("0,05 EUR (Optional)", min_value=0, step=1, value=0, format="%d", key="banco_005")
        
        total_moeda_01eur = moeda_01eur * 0.1
        total_moeda_005eur = moeda_005eur * 0.05
        
        banco_total = (total_nota_20eur + total_nota_10eur + total_nota_5eur + 
                      total_moeda_2eur + total_moeda_02eur + 
                      total_moeda_01eur + total_moeda_005eur)
        
        banco_data = {
            "Category": ["20 EUR", "10 EUR", "5 EUR", "2 EUR", "0.2 EUR", "0.1 EUR", "0.05 EUR", "**TOTAL**"],
            "Amount (EUR)": [
                f"{total_nota_20eur:.2f}",
                f"{total_nota_10eur:.2f}",
                f"{total_nota_5eur:.2f}",
                f"{total_moeda_2eur:.2f}",
                f"{total_moeda_02eur:.2f}",
                f"{total_moeda_01eur:.2f}",
                f"{total_moeda_005eur:.2f}",
                f"**{banco_total:.2f}**"
            ]
        }
        banco_df = pd.DataFrame(banco_data)
        st.table(banco_df)
        
        # Prepare data for Google Sheets
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        new_row = {
            "Timestamp": timestamp,
            "User": selected_user,
            "Date": str(entry_date),
            "Moeda_2EUR_Qty": moeda_2eur,
            "Moeda_2EUR_Total": total_moeda_2eur,
            "Moeda_1EUR_Qty": moeda_1eur,
            "Moeda_1EUR_Total": total_moeda_1eur,
            "Moeda_05EUR_Qty": moeda_05eur,
            "Moeda_05EUR_Total": total_moeda_05eur,
            "Moeda_02EUR_Qty": moeda_02eur,
            "Moeda_02EUR_Total": total_moeda_02eur,
            "Moeda_01EUR_Qty": moeda_01eur,
            "Moeda_01EUR_Total": total_moeda_01eur,
            "Moeda_005EUR_Qty": moeda_005eur,
            "Moeda_005EUR_Total": total_moeda_005eur,
            "Nota_20EUR_Qty": nota_20eur,
            "Nota_20EUR_Total": total_nota_20eur,
            "Nota_10EUR_Qty": nota_10eur,
            "Nota_10EUR_Total": total_nota_10eur,
            "Nota_5EUR_Qty": nota_5eur,
            "Nota_5EUR_Total": total_nota_5eur,
            "Troca_Total": troca_total,
            "Banco_Total": banco_total,
            "Grand_Total": total_all,
            "Notes": notes
        }
        
        # Append to Google Sheets
        try:
            # Read existing data
            existing_data = conn.read(worksheet="Folha1", usecols=list(range(25)), ttl=1)
            
            # Append new row
            updated_data = pd.concat([existing_data, pd.DataFrame([new_row])], ignore_index=True)
            
            # Write back to sheet
            conn.update(worksheet="Folha1", data=updated_data)
            
            st.success("💾 Data saved to Google Sheets!")
            
        except Exception as e:
            st.error(f"❌ Error saving to Google Sheets: {str(e)}")

# Display last 5 entries
st.markdown("---")
st.markdown("### 📜 Recent Entries (Last 5)")

try:
    # Read data from Google Sheets
    all_data = conn.read(worksheet="Folha1", usecols=list(range(25)), ttl=1)
    
    if not all_data.empty:
        # Get last 5 entries
        last_5 = all_data.tail(5).sort_values(by="Timestamp", ascending=False)
        
        # Display relevant columns
        display_columns = ["Timestamp", "User", "Date", "Grand_Total", "Troca_Total", "Banco_Total", "Notes"]
        available_columns = [col for col in display_columns if col in last_5.columns]
        
        st.dataframe(
            last_5[available_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No entries yet. Submit the first entry above!")
        
except Exception as e:
    st.warning(f"Unable to load recent entries: {str(e)}")
    st.info("The sheet might be empty or not properly configured.")

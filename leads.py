import streamlit as st
import pandas as pd
import os

# --- Page Configuration ---
st.set_page_config(page_title="LinkedIn Leads Dashboard", layout="wide")

st.title("💼 LinkedIn Leads Dashboard")
st.write("Explore, search, and analyze your LinkedIn leads easily.")

# --- Directory where CSVs are stored ---
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Mapping of service names to CSV files ---
lead_files = {
    "Branding Strategy": "branding_strategy_leads.csv",
    "CRM Services": "crm_services_leads.csv",
    "Creative Copywriting": "creative_copywriting_leads.csv",
    "Tailored Software Development": "tailored_software_development_leads.csv",
    "Social Media Management": "social_media_management_leads.csv",
    "ERP Services": "erp_services_leads.csv",
    "Email Marketing": "email_marketing_leads.csv",
    "Ecommerce Solutions": "ecommerce_solutions_leads.csv",
    "UI/UX Design": "ui_ux_design_leads.csv",
    "Performance Audits": "performance_audits_leads.csv"
}

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["🔍 Global Search", "📁 Individual CSVs"])

# --- Load all CSVs into a dictionary ---
def load_data():
    data = {}
    for name, filename in lead_files.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df["Service"] = name  # Add a column for identifying source
                data[name] = df
            except Exception as e:
                st.warning(f"⚠️ Could not read {filename}: {e}")
        else:
            st.warning(f"⚠️ Missing file: {filename}")
    return data

data_dict = load_data()

# --- GLOBAL SEARCH ---
if page == "🔍 Global Search":
    st.subheader("🌍 Global Lead Search")
    query = st.text_input("Search across all CSV files (name, company, etc.)")

    if query:
        all_data = pd.concat(data_dict.values(), ignore_index=True)
        results = all_data[all_data.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)]

        st.write(f"### 🔎 Found {len(results)} results for '{query}'")
        st.dataframe(results, use_container_width=True)

        # Download results
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Search Results",
            data=csv,
            file_name=f"search_results_{query}.csv",
            mime='text/csv'
        )
    else:
        st.info("Type a keyword above to search across all leads.")

# --- INDIVIDUAL FILE VIEWER ---
elif page == "📁 Individual CSVs":
    selected_file = st.sidebar.selectbox("Select a Service", list(lead_files.keys()))
    file_path = os.path.join(DATA_DIR, lead_files[selected_file])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.subheader(f"📊 {selected_file} Leads Data")
        st.write(f"Total Leads: **{len(df)}**")

        st.dataframe(df, use_container_width=True)

        # --- Download CSV ---
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=lead_files[selected_file],
            mime='text/csv'
        )
    else:
        st.error(f"File not found: {file_path}")

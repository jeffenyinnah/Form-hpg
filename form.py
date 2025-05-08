import streamlit as st
import requests
import datetime
import time
import os
import hashlib

from dotenv import load_dotenv
load_dotenv()

# Authentication configuration
USERNAME = os.getenv("USERNAME")
# Store password as a hash rather than plaintext
PASSWORDLL = os.getenv("PASSWORD")
PASSWORD_HASH = hashlib.sha256(PASSWORDLL.encode()).hexdigest()

# Check if user is authenticated
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def authenticate(username, password):
    """Authenticate user with username and password"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username == USERNAME and hashed_password == PASSWORD_HASH

# Show login page if not authenticated
if not st.session_state.authenticated:
    # Logo Placeholder
    st.image("HPG.png")
    st.title("🔐 Login")
    st.write("Please log in to access the HPG Project Submission Form")
    
    username = st.text_input("Username",placeholder="e.g., username")
    password = st.text_input("Password", type="password", placeholder="e.g., password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    # Stop execution if not authenticated
    st.stop()

# Airtable credentials and endpoint
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("BASE_ID")
if not BASE_ID:
    st.error("❌ Base ID not found. Please set the BASE_ID environment variable.")
    st.stop()
TABLE_NAME = "Projects"
AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"

# Optional: Theme Toggle (simulated using session state)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

def reset_form():
    keys_to_reset = [
        "project_name", "funding_partner", "implementing_partner", "currency", "total_value",
        "year_started", "year_ending", "notes", "url", "contact", "last_modified", "selected_provinces"
    ]

    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

    # Reset dynamic district selections
    for prov in province_districts:
        all_key = f"{prov}-all"
        districts_key = f"{prov}-districts"
        if all_key in st.session_state:
            del st.session_state[all_key]
        if districts_key in st.session_state:
            del st.session_state[districts_key]

# Add logout button in sidebar
st.sidebar.title("User Controls")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

theme_button = "🌙 Switch to Dark Mode" if not st.session_state.dark_mode else "☀️ Switch to Light Mode"
st.sidebar.button(theme_button, on_click=toggle_theme)

# Apply background and text color manually
if st.session_state.dark_mode:
    st.markdown("""
        <style>
            body { background-color: #0e1117; color: #fafafa; }
        </style>
    """, unsafe_allow_html=True)


# Logo Placeholder
st.image("HPG.png")

# Page Title
st.title("🗂️ HPG Project Submission Form")
st.write(f"Welcome, {USERNAME}!")

# Input Fields
project_name = st.text_input("Project Name", placeholder="e.g., Maternal Health Support in Gaza Province", key="project_name")
funding_partner = st.selectbox("Funding Partner", ["Arab Bank for Economic Development in Africa", "Bill and Melinda Gates Foundation", "Canada",
                                                   "European Commission", "Finland", "Flanders", "Fundo Saudita para o Desenvolvimento", "Gavi",
                                                   "Global Financing Facility", "Global Fund", "IOM HQ", "Ireland", "Islamic Development Bank",
                                                   "Italy -AICS", "JICA", "KOICA", "Norway", "PEPFAR", "Rotary International", "Spain", "Sweden",
                                                   "UNFPA HQ/Regional", "UNICEF HQ/Thematic Funds/NatComs)", "UNITAID", "United Kingdom - FCDO",
                                                   "US CDC", "USAID", "World Bank"], key="funding_partner")
implementing_partner = st.text_input("Implementing Partner", placeholder="e.g., UNICEF Mozambique", key="implementing_partner")
currency = st.selectbox("Currency", ["EUR", "CAD", "USD", "MZN", "GBP", "JPY", "CHF", "AUD", "BRL", "NOK", "SEK", "DKK", "NZD", "ZAR"], key="currency")
total_value = st.number_input("Total Value of Project",key="total_value",min_value=0.0, format="%.2f")
year_started = st.number_input("Year Started",key="year_started", min_value=1990, max_value=2050, step=1)
year_ending = st.number_input("Year Ending (Estimate)", key="year_ending", min_value=1990, max_value=2050, step=1)

# Province & Districts
province_districts = {
    "Cabo Delgado": ["Ancuabe", "Balama", "Chiure", "Ibo", "Macomia", "Mecufi", "Meluco", "Metuge", "Mocimboa da Praia", "Montepuez", "Mueda", "Muidumbe", "Namuno", "Nangade", "Palma", "Pemba", "Quissanga"],
    "Gaza": ["Bilene", "Chibuto", "Chicualacuala", "Chigubo", "Chokwe", "Chongoene", "Guija", "Limpopo", "Mabalane", "Manjacaze", "Massangena", "Massingir", "Cidade De Xai-Xai"],
    "Inhambane": ["Funhalouro", "Govuro", "Homoine", "Inhambane", "Inharrime", "Inhassoro", "Jangamo", "Mabote", "Massinga", "Maxixe", "Morrumbene", "Panda", "Vilanculos", "Zavala"],
    "Manica": ["Barue", "Chimoio", "Gondola", "Guro", "Macate (Gondola)", "Machaze", "Macossa", "Manica", "Mossurize", "Sussundenga", "Tambara", "Vanduzi"],
    "Maputo": ["Boane", "Magude", "Manhica", "Marracuene", "Cidade Da Matola", "Matutuine", "Moamba", "Namaacha"],
    "Maputo Cidade": ["KaMavota", "KaMaxaquene", "KaMphumu", "KaMubukwana", "KaNyaka", "KaTembe", "Nlhamankulu"],
    "Nampula": ["Angoche", "Erati", "Ilha de Mocambique", "Lalaua", "Moma", "Mogincual", "Liupo", "Malema", "Meconta", "Mecuburi", "Memba", "Mogovolas", "Monapo", "Mossuril", "Muecate", "Murrupula", "Nacala", "Nacala-a-Velha", "Nacaroa", "Nampula", "Rapale", "Ribaue"],
    "Niassa": ["Chimbonila", "Cuamba", "Lago", "Lichinga", "Majune", "Mandimba", "Marrupa", "Maua", "Mavago", "Mecanhelas", "Mecula", "Metarica", "Muembe", "Ngauma", "Nipepe", "Sanga"],
    "Sofala": ["Beira", "Buzi", "Caia", "Chemba", "Cheringoma", "Chibabava", "Dondo", "Gorongosa", "Machanga", "Maringue", "Marromeu", "Muanza", "Nhamatanda"],
    "Tete": ["Angonia", "Cahora-Bassa", "Changara", "Chifunde", "Chiuta", "Doa", "Macanga", "Magoe", "Marara", "Maravia", "Moatize", "Mutarara", "Tete", "Tsangano", "Zumbo"],
    "Zambezia": ["Alto Molocue", "Chinde", "Derre", "Gile", "Gurue", "Ile", "Inhassunge", "Luabo", "Lugela", "Maganja da Costa", "Milange", "Mocuba", "Mocubela", "Molumbo", "Mopeia", "Morrumbala", "Mulevala", "Namacurra", "Namarroi", "Nicoadala", "Pebane", "Quelimane"]
}

selected_provinces = st.multiselect("Provinces", options=list(province_districts.keys()), key="selected_provinces")
selected_districts = []
map_data = []

for prov in selected_provinces:
    st.subheader(f"Districts in {prov}")
    all_option = st.checkbox(f"Select all districts in {prov}", key=f"{prov}-all")
    if all_option:
        selected_districts += province_districts[prov]
    else:
        districts = st.multiselect(f"Select districts in {prov}", options=province_districts[prov], key=prov)
        selected_districts += districts

notes = st.text_area("Notes", placeholder="Brief project description, goals, or target outcomes.", key="notes")
url = st.text_input("URL", placeholder="e.g., https://unicef.org/project-page", key="url")
contact = st.text_input("Contact Info", placeholder="e.g.,joao@email.com", key="contact")
last_modified = st.date_input("Last Modified", value=datetime.date.today(), key="last_modified")

# Submit button
if st.button("✅ Submit Project"):
    if not project_name or not selected_provinces:
        st.error("Please fill in at least the Project Name and Province.")
    else:
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }

        record_payload = {
            "records": [
                {
                    "fields": {
                        "Name": project_name,
                        "Funding Partner": funding_partner,
                        "Implementing Partner": implementing_partner,
                        "Currency": currency,
                        "Total Value": total_value,
                        "Year Started": int(year_started),
                        "Year Ending (Estimate)": int(year_ending),
                        "Notes": notes,
                        "URL": url,
                        "Contact": contact,
                        "Last Modified": last_modified.strftime("%Y-%m-%d"),
                        "Province": ", ".join(selected_provinces),
                        "District": ", ".join(selected_districts),
                    }
                }
            ]
        }

        response = requests.post(AIRTABLE_ENDPOINT, headers=headers, json=record_payload)

        if response.status_code == 200 or response.status_code == 201:
            st.success("✅ Project submitted to Airtable successfully!")

            if st.button("➕ Submit Another Project"):
                reset_form()
                st.rerun()
        else:
            st.error(f"❌ Failed to submit project. Error {response.status_code}: {response.text}")
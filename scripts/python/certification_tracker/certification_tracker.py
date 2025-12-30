# python3 -m pip install streamlit pandas
# python3 -m streamlit run certification_tracker.py
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# --- Configuration (FIXED PATH for reliable saving) ---
JSON_FILENAME = 'certifications.json' 
JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), JSON_FILENAME) 

# --- JSON Data Management Functions ---

def load_certs():
    """Loads certification data from the JSON file."""
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, 'r') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                required_keys = ['cert_id', 'date', 'expires', 'fee', 'renewal_frequency', 'amf_due_date']
                for cert in data:
                    for key in required_keys:
                        if key not in cert:
                            cert[key] = "" if key not in ['fee'] else 0.00
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return [] 

def save_certs(certs):
    """Saves the current list of certifications to the JSON file."""
    for cert in certs:
        date_val = cert.get('date')
        if isinstance(date_val, (datetime, pd.Timestamp)):
            cert['date'] = date_val.strftime('%Y-%m-%d')

        expires_val = cert.get('expires')
        if expires_val is None or str(expires_val).upper() in ["N/A", "NAT", "NONE", ""]:
            cert['expires'] = "N/A"
        elif isinstance(expires_val, (datetime, pd.Timestamp)):
            cert['expires'] = expires_val.strftime('%Y-%m-%d')
        
        amf_due_date_val = cert.get('amf_due_date')
        if amf_due_date_val is None or str(amf_due_date_val).upper() in ["N/A", "NAT", "NONE", ""]:
            cert['amf_due_date'] = "N/A"
        elif isinstance(amf_due_date_val, (datetime, pd.Timestamp)):
            cert['amf_due_date'] = amf_due_date_val.strftime('%Y-%m-%d')
        
        fee_val = cert.get('fee')
        try:
            cert['fee'] = float(fee_val) if fee_val else 0.00
        except (TypeError, ValueError):
            cert['fee'] = 0.00
            
        cert['cert_id'] = str(cert.get('cert_id', ''))

    try:
        with open(JSON_FILE, 'w') as f:
            json.dump(certs, f, indent=4)
    except Exception as e:
        st.error(f"FATAL SAVE ERROR: Could not write to file! Details: {e}")


# --- Streamlit UI Components ---

def add_certification(certs_list):
    """Streamlit form to add a new certification."""
    st.subheader("➕ Add New Certification")
    
    with st.form("add_cert_form", clear_on_submit=True):
        new_cert = {}
        
        # Certification Details
        new_cert['name'] = st.text_input("Certification Name", key="name_input")
        new_cert['issuer'] = st.text_input("Issuing Organization", key="issuer_input")
        new_cert['cert_id'] = st.text_input("Certificate ID# (Optional)", key="cert_id_input") 
        
        # Date Achieved
        date_achieved = st.date_input("Date Achieved", key="date_input", 
                                        min_value=datetime(2000, 1, 1), 
                                        max_value=datetime.now())
        new_cert['date'] = date_achieved.strftime('%Y-%m-%d')
        
        # Expiration Date
        expires_date = st.date_input("Expiration Date (Optional)", key="expires_input", 
                                        min_value=datetime.now(), value=None)
        new_cert['expires'] = expires_date.strftime('%Y-%m-%d') if expires_date else "N/A"
        
        # MOVED RENEWAL FREQUENCY HERE (Index 3 = Triennial default)
        new_cert['renewal_frequency'] = st.selectbox("Renewal Frequency", 
                                                    ['None/One-Time', 'Annual', 'Biennial (Every 2 years)', 'Triennial (Every 3 years)', 'Other'], 
                                                    index=3, 
                                                    key="frequency_input")
        
        st.markdown("---")
        st.markdown("**Renewal/Financial Details (AMF)**")
        
        # AMF Due Date INPUT
        amf_due_date = st.date_input("AMF Due Date (Optional)", key="amf_due_date_input", 
                                     min_value=datetime.now(), value=None)
        new_cert['amf_due_date'] = amf_due_date.strftime('%Y-%m-%d') if amf_due_date else "N/A"
        
        new_cert['fee'] = st.number_input("Renewal/Annual Fee (USD)", 
                                            min_value=0.00, 
                                            value=0.00, 
                                            step=10.00, 
                                            format="%.2f", 
                                            key="fee_input")

        submitted = st.form_submit_button("Add Certification")

        if submitted:
            if new_cert['name'] and new_cert['issuer']:
                certs_list.append(new_cert)
                save_certs(certs_list)
                st.success(f"Added **{new_cert['name']}**! Changes applied.")
                st.rerun() 
            else:
                st.error("Certification Name and Issuer are required.")

def display_certifications_table(df_certs):
    """Displays all current certifications in an EDITABLE table using st.data_editor."""
    st.subheader("📝 Current Certifications (Click headers to sort)")
    
    if df_certs.empty:
        st.info("No certifications found. Add one using the form.")
        return df_certs
    
    column_config = {
        "Delete": st.column_config.CheckboxColumn(
            "Delete?",
            default=False,
        ),
        "fee": st.column_config.NumberColumn(
            "Renewal/Annual Fee (USD)", 
            format="$%0.2f",
            min_value=0.00,
            required=True
        ),
        "date": st.column_config.DateColumn(
            "Date Achieved", 
            format="YYYY-MM-DD",
            required=True
        ),
        "expires": st.column_config.DateColumn(
            "Expiration Date", 
            format="YYYY-MM-DD"
        ),
        "amf_due_date": st.column_config.DateColumn(
            "AMF Due Date", 
            format="YYYY-MM-DD",
            required=False
        ),
        "renewal_frequency": st.column_config.SelectboxColumn(
            "Renewal Frequency",
            options=['None/One-Time', 'Annual', 'Biennial (Every 2 years)', 'Triennial (Every 3 years)', 'Other'],
            required=True
        ),
        "cert_id": "Certificate ID#",
        "name": st.column_config.TextColumn("Certification Name", required=True),
        "issuer": st.column_config.TextColumn("Issuing Organization", required=True),
    }
    
    # ADDED "Delete" to the beginning of the column order
    column_order = [
        'Delete', 'name', 'issuer', 'cert_id', 'date', 'expires', 'renewal_frequency', 'amf_due_date', 'fee'
    ]

    edited_df = st.data_editor(
        df_certs, 
        use_container_width=True, 
        hide_index=True, 
        column_config=column_config,
        column_order=column_order,
        height=600, 
        key="editable_cert_table" 
    )
    
    # Reliable change detection via Session State
    changes = st.session_state.get('editable_cert_table', {})
    
    if changes.get('edited_rows'):
        st.session_state['data_edited'] = True
    else:
        st.session_state['data_edited'] = False
    
    return edited_df

def display_due_soon_block(certs):
    st.markdown("---")
    st.subheader("🗓️ Certifications Due Soon (Next 180 Days)")
    
    today = datetime.now().date()
    due_soon_certs = []
    
    for cert in certs:
        # Check both Expiration and AMF Due Date for attention
        expiry_val = cert.get('expires')
        amf_due_date_val = cert.get('amf_due_date')
        
        dates_to_check = []
        if expiry_val and str(expiry_val).upper() not in ["N/A", "NAT", "NONE", ""]:
            dates_to_check.append((expiry_val, 'Expiration'))
        if amf_due_date_val and str(amf_due_date_val).upper() not in ["N/A", "NAT", "NONE", ""]:
            dates_to_check.append((amf_due_date_val, 'AMF Payment'))

        if not dates_to_check:
            continue

        attention_needed = False
        
        # Check if the closest attention date is within 180 days
        for date_val, type_str in dates_to_check:
            try:
                if isinstance(date_val, (datetime, pd.Timestamp)):
                    check_date = date_val.date()
                elif isinstance(date_val, str):
                    check_date = datetime.strptime(date_val, '%Y-%m-%d').date()
                else:
                    continue
                
                days_left = (check_date - today).days
                
                if 0 <= days_left <= 180:
                    attention_needed = True
                    break 
            except (ValueError, TypeError):
                continue

        if attention_needed:
            # Determine the closest date for sorting/display
            closest_date = min([datetime.strptime(str(d[0]).split(' ')[0], '%Y-%m-%d').date() for d in dates_to_check if d[0] != 'N/A'], default=today + pd.Timedelta(days=181))
            
            days_left = (closest_date - today).days

            if 0 <= days_left <= 180:
                due_soon_certs.append({
                    'Certification': cert['name'],
                    'Certificate ID#': cert.get('cert_id', ''), 
                    'Issuer': cert['issuer'],
                    'Expiration Date': cert.get('expires', 'N/A'),
                    'AMF Due Date': cert.get('amf_due_date', 'N/A'), 
                    'Renewal Fee': f"${cert.get('fee', 0.00):.2f}",
                    'Days Left': days_left
                })


    if due_soon_certs:
        due_soon_df = pd.DataFrame(due_soon_certs).sort_values(by='Days Left', ascending=True)
        
        st.warning("These certifications require attention for renewal, fee payment, or CE credits!")
        
        st.dataframe(
            due_soon_df, 
            hide_index=True, 
            use_container_width=True,
            column_order=('Certification', 'Expiration Date', 'AMF Due Date', 'Days Left', 'Renewal Fee', 'Certificate ID#', 'Issuer')
        )
    else:
        st.info("No certifications are due for renewal or AMF payment in the next 6 months.")


def display_summary(certs):
    # This section now ONLY calculates the Annual AMF Estimate
    total_annual_fee = 0.00
    
    for cert in certs:
        fee = cert.get('fee', 0.00)
        frequency = cert.get('renewal_frequency', 'None/One-Time')
        
        try:
            fee = float(fee)
        except (TypeError, ValueError):
            fee = 0.00
            
        if frequency == 'Annual':
            total_annual_fee += fee
        elif frequency == 'Biennial (Every 2 years)':
            total_annual_fee += (fee / 2.0)
        elif frequency == 'Triennial (Every 3 years)':
            total_annual_fee += (fee / 3.0)
            
    # Display the Annual Fee metric below the Due Soon block
    st.markdown("---")
    st.metric(
        "Annual Fee Estimate",
        f"${total_annual_fee:.2f}",
        help="Estimated total fees to maintain all annual, biennial, and triennial certifications."
    )


# --- Main Application Logic ---

def main():
    st.set_page_config(layout="wide", page_title="IT Certification Tracker")
    
    st.title("👨‍💻 IT Certification & Fee Tracker")
    st.markdown("Manage your professional certifications, renewal fees (AMFs), and expiration dates. Data is loaded from **`certifications.json`**.")
    
    if 'data_edited' not in st.session_state:
        st.session_state['data_edited'] = False
        
    # --- DEBUG BLOCK START ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("File Path Debug")
    st.sidebar.code(f"JSON File Path:\n{JSON_FILE}", language="text")
    
    if not os.path.exists(JSON_FILE):
        st.sidebar.warning("File not found! Attempting to create empty file...")
        try:
            with open(JSON_FILE, 'w') as f:
                json.dump([], f)
            st.sidebar.success("Empty file created successfully. App will now rerun.")
            st.rerun() 
        except PermissionError:
            st.sidebar.error("PERMISSION DENIED: Cannot create file at this location. Check folder permissions.")
        except Exception as e:
            st.sidebar.error(f"Error creating file: {e}")
    else:
        st.sidebar.info("File exists.")
        try:
            size_bytes = os.path.getsize(JSON_FILE)
            st.sidebar.info(f"File size: {size_bytes} bytes")
        except:
             st.sidebar.info("Could not determine file size (may be permission issue).")

    st.sidebar.markdown("---")
    # --- DEBUG BLOCK END ---
    
    certs_list = load_certs()
    
    # --- Data Type Conversion and Preparation for DataFrame ---
    if certs_list:
        df = pd.DataFrame(certs_list)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['expires'] = df['expires'].replace(['N/A', '', 'None'], pd.NaT)
        df['expires'] = pd.to_datetime(df['expires'], errors='coerce')
        
        # Convert AMF Due Date
        df['amf_due_date'] = df['amf_due_date'].replace(['N/A', '', 'None'], pd.NaT)
        df['amf_due_date'] = pd.to_datetime(df['amf_due_date'], errors='coerce')

        # Add the 'Delete' checkbox column for display in the editor
        df['Delete'] = False 
        
        # Initial Data Sorting: Sort by Expiration Date ascending (nearer dates first)
        df = df.sort_values(by='expires', ascending=True, na_position='last')
        
    else:
        df = pd.DataFrame()
        # Initialize an empty dataframe with the 'Delete' column if no data exists
        df = pd.DataFrame(columns=['Delete', 'name', 'issuer', 'cert_id', 'date', 'expires', 'renewal_frequency', 'amf_due_date', 'fee'])

    
    # Column ratio 1:3 for form:table
    col1, col2 = st.columns([1, 3]) 
    
    # --- DISPLAY TOTAL COUNT ---
    # Moved the Total Certifications count up to be prominent
    total_certs = len(certs_list)
    st.metric("Total Certifications Tracked", total_certs)
    st.markdown("---")
    # ---------------------------
    
    with col1:
        add_certification(certs_list)
        
    # st.markdown("---") # Removed this line since the metric added one above
    
    with col2:
        edited_df = display_certifications_table(df)
    
    # 6. Save Edits Logic
    if st.session_state['data_edited']:
        if st.button("💾 Save Changes to JSON", type="primary"):
            
            # --- Deletion and Saving Logic ---
            final_df = edited_df.copy()
            
            # 1. Filter out deleted rows (where Delete checkbox is True)
            final_df = final_df[final_df['Delete'] == False]
            
            # 2. Drop the temporary 'Delete' column before saving to JSON
            final_df = final_df.drop(columns=['Delete'])
            
            # Clean NaT values before final conversion to dictionary for saving
            final_df['expires'] = final_df['expires'].replace({pd.NaT: None})
            # Clean NaT values for AMF Due Date
            final_df['amf_due_date'] = final_df['amf_due_date'].replace({pd.NaT: None})

            updated_certs = final_df.to_dict('records')
            
            save_certs(updated_certs)
            st.success("Changes and deletions saved successfully! Rerunning application...")
            st.session_state['data_edited'] = False 
            st.rerun()
        
        st.warning("Click 'Save Changes to JSON' to make edits/deletions permanent.")
        
        # Prepare data for the due soon block, retaining the 'Delete' column until saved
        certs_for_display = edited_df.drop(columns=['Delete']).to_dict('records')
    else:
        # If no edit happened, use the original df without the 'Delete' column
        certs_for_display = df.drop(columns=['Delete']).to_dict('records')


    display_due_soon_block(certs_for_display)
    display_summary(certs_for_display) # Now only displays Annual Fee Estimate

if __name__ == "__main__":
    main()

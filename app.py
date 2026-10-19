import streamlit as st
from docxtpl import DocxTemplate
from io import BytesIO
import datetime

st.set_page_config(page_title="Weighment Slip Generator - Trail & Error", layout="wide")

# ==================== PROFESSIONAL UI & STYLING ====================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    /* Force ALL form input labels to be bright cyan-blue */
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label, .stNumberInput label, div[data-testid="stForm"] label {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    .brand-title {
        font-size: 3.2rem;
        font-weight: 800;
        letter-spacing: 3px;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .brand-subtitle {
        font-size: 1.4rem;
        font-weight: 500;
        color: #94a3b8;
        letter-spacing: 1.5px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome-banner {
        padding: 1rem;
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== SESSION ROUTING ====================
if "auth_step" not in st.session_state:
    st.session_state["auth_step"] = "image_screen"

if "operator_name" not in st.session_state:
    st.session_state["operator_name"] = ""

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Screen 1: Full-Screen Image & Branding
if st.session_state["auth_step"] == "image_screen":
    st.write("") # Spacer
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("logo.png", use_container_width=True)
        except Exception:
            st.markdown("<h1 style='color: #38bdf8; text-align: center;'>T & E</h1>", unsafe_allow_html=True)
            
        st.markdown("<div class='brand-title'>TRAIL & ERROR</div>", unsafe_allow_html=True)
        st.markdown("<div class='brand-subtitle'>Crafted By Punith Kumar N M</div>", unsafe_allow_html=True)
        
        st.write("")
        if st.button("🚀 Proceed to Secure Portal", use_container_width=True):
            st.session_state["auth_step"] = "login_screen"
            st.rerun()
    st.stop()

# Screen 2: Password and Operator Name Entry
elif st.session_state["auth_step"] == "login_screen":
    st.write("")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #38bdf8;'>🔒 Authentication Required</h2>", unsafe_allow_html=True)
        st.write("")
        
        with st.form("login_form"):
            operator_input = st.text_input("Enter Your Name")
            password_input = st.text_input("Enter Password", type="password")
            submitted_login = st.form_submit_button("Access Portal", use_container_width=True)
            
            if submitted_login:
                if not operator_input.strip():
                    st.error("⚠️ Please enter your name.")
                elif password_input == "7505":  # Change password here if desired
                    st.session_state["operator_name"] = operator_input.strip()
                    st.session_state["authenticated"] = True
                    st.session_state["auth_step"] = "app_screen"
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
                    
        if st.button("⬅️ Back to Home"):
            st.session_state["auth_step"] = "image_screen"
            st.rerun()
    st.stop()

# ==================== SCREEN 3: WELCOME & DATA ENTRY ====================
st.markdown(f"""
    <div class='welcome-banner'>
        <h3 style='margin:0; color: #38bdf8;'>👋 Welcome, {st.session_state["operator_name"]}!</h3>
        <p style='margin:0; color: #cbd5e1;'>Portal unlocked. You can now generate Weighment Slips.</p>
    </div>
""", unsafe_allow_html=True)

st.title("Weighment Slip Data Entry")

with st.form("weighment_form"):
    col1, col2 = st.columns(2)

    with col1:
        ticket_no = st.text_input("Ticket Number", "147")
        vehicle_no = st.text_input("Vehicle Number", "KA51AG4047")
        loaded_weight_num = st.number_input("Loaded Weight (Kgs)", value=41440.0, step=1.0)
        empty_weight_num = st.number_input("Empty Weight (Kgs)", value=11600.0, step=1.0)
        
        net_weight_num = loaded_weight_num - empty_weight_num
        st.info(f"Calculated Net Weight: {net_weight_num:,.0f} Kgs")

    with col2:
        material = st.text_input("Material", "12 MM")
        customer = st.text_input("Customer", "Ishan Enterprises")
        
        slip_date = st.date_input("Date", datetime.date.today())
        slip_time = st.time_input("Time", datetime.datetime.now().time())
        
        rate = st.text_input("Rate Rs.", "00")
        total_amount = st.text_input("Total Amount Rs.", "00")

    submitted = st.form_submit_button("Generate Weighment Slip Document")

if submitted:
    doc = DocxTemplate("weighment_format.docx")

    formatted_date_time = f"{slip_date.strftime('%d/%m/%Y')} TIME {slip_time.strftime('%I:%M %p')}"

    context = {
        "ticket_no": ticket_no,
        "vehicle_no": vehicle_no,
        "loaded_weight": f"{loaded_weight_num:,.0f} Kgs",
        "empty_weight": f"{empty_weight_num:,.0f} Kgs",
        "net_weight": f"{net_weight_num:,.0f} Kgs",
        "material": material,
        "customer": customer,
        "date_time": formatted_date_time,
        "rate": rate,
        "total_amount": total_amount,
        "operator": st.session_state["operator_name"]
    }

    doc.render(context)

    output_io = BytesIO()
    doc.save(output_io)
    output_io.seek(0)

    st.success("Weighment Slip created successfully!")
    st.download_button(
        label="Download Weighment Slip (.docx)",
        data=output_io,
        file_name=f"Weighment_Slip_{ticket_no}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

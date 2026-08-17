import streamlit as st
from fpdf import FPDF
from datetime import datetime, timedelta
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Proposal Studio — B2B Quote Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CUSTOM CSS ---
st.markdown("""
<style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Modern Container Cards */
    .stCard {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .sub-header {
        color: #94A3B8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Primary Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        background: linear-gradient(90deg, #4F46E5 0%, #6366F1 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# --- TITLE HEADER ---
st.markdown('<div class="main-header">⚡ Proposal Studio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create ultra-sleek, professional B2B proposals in real-time.</div>', unsafe_allow_html=True)

# --- SIDEBAR: PROVIDER BRANDING ---
st.sidebar.markdown("### 🏢 Provider Branding")
sender_company = st.sidebar.text_input("Business / Agency Name", value="Apex Automation Ltd")
sender_email = st.sidebar.text_input("Contact Email", value="hello@apexautomation.co.uk")
sender_phone = st.sidebar.text_input("Phone Number", value="+44 7123 456789")
currency = st.sidebar.selectbox("Currency Unit", ["£ (GBP)", "$ (USD)", "€ (EUR)"])
curr_symbol = currency.split()[0]

# --- TWO-COLUMN REAL-TIME LAYOUT ---
col_left, col_right = st.columns([1.1, 1], gap="medium")

# ==================== LEFT COLUMN: INPUT FORM ====================
with col_left:
    st.markdown("#### ⚙️ Configuration & Details")
    
    with st.expander("👤 Client Information", expanded=True):
        client_company = st.text_input("Client Company Name", value="Derby Recruitment Solutions Ltd")
        client_contact = st.text_input("Primary Contact Person", value="John Smith")
        client_email = st.text_input("Client Email Address", value="j.smith@derbyrecruitment.co.uk")

    with st.expander("📋 Proposal Metadata", expanded=False):
        prop_number = st.text_input("Proposal Reference #", value="PROP-2026-001")
        date_today = datetime.now().strftime("%b %d, %Y")
        valid_until = (datetime.now() + timedelta(days=14)).strftime("%b %d, %Y")
        st.text_input("Issue Date", value=date_today, disabled=True)
        st.text_input("Expiration Date", value=valid_until)

    with st.expander("🚀 Scope of Services & Deliverables", expanded=True):
        proposal_title = st.text_input("Project Headline / Title", value="Automated B2B Lead Generation & Workflow Integration")
        scope_desc = st.text_area(
            "Executive Summary & Deliverables",
            value="End-to-end deployment of a high-speed Python scraping pipeline targeting UK recruitment agencies. Includes data enrichment, verification, and live synchronization into Google Sheets with daily automated execution.",
            height=90
        )

    with st.expander("💰 Line Items & Investment Breakdown", expanded=True):
        item1_name = st.text_input("Item 1 Description", value="Custom Python Web Scraper & Data Pipeline")
        c1, c2 = st.columns(2)
        with c1:
            item1_qty = st.number_input("Qty 1", min_value=1, value=1)
        with c2:
            item1_rate = st.number_input("Unit Rate 1", min_value=0.0, value=350.0, step=25.0)

        item2_name = st.text_input("Item 2 Description (Optional)", value="Google Sheets Sync & Automation Workflow")
        c3, c4 = st.columns(2)
        with c3:
            item2_qty = st.number_input("Qty 2", min_value=0, value=1)
        with c4:
            item2_rate = st.number_input("Unit Rate 2", min_value=0.0, value=150.0, step=25.0)

        # Totals Calculation
        total1 = item1_qty * item1_rate
        total2 = item2_qty * item2_rate
        grand_total = total1 + total2
        st.markdown(f"### **Total Investment: {curr_symbol}{grand_total:,.2f}**")

    with st.expander("📝 Payment Terms & Conditions", expanded=False):
        payment_terms = st.text_area(
            "Terms Summary",
            value="50% upfront deposit required upon acceptance. Remaining 50% payable upon deployment. Invoices due within 7 business days via bank transfer.",
            height=60
        )

# ==================== PDF ENGINE CLASS ====================
class ModernProposalPDF(FPDF):
    def header(self):
        # Top Accent Line
        self.set_fill_color(79, 70, 229) # Indigo
        self.rect(0, 0, 210, 4, 'F')
        
        # Header Document Title
        self.set_xy(15, 12)
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(15, 23, 42) # Dark Slate
        self.cell(0, 10, 'BUSINESS PROPOSAL', new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 116, 139) # Slate Grey
        self.cell(0, 4, 'CONFIDENTIAL & PROPRIETARY', new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()}  |  Prepared for {client_company}  |  Generated via Proposal Studio', align='C')

# ==================== REAL-TIME PDF BUILD ====================
pdf = ModernProposalPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# --- SENDER vs CLIENT METADATA GRID ---
pdf.set_y(32)

# Left Column: Provider
pdf.set_font('Helvetica', 'B', 9)
pdf.set_text_color(79, 70, 229)
pdf.cell(90, 5, "PREPARED BY:", new_x="RIGHT")
# Right Column: Client
pdf.cell(90, 5, "PREPARED FOR:", new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(15, 23, 42)
pdf.cell(90, 5, sender_company, new_x="RIGHT")
pdf.cell(90, 5, client_company, new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(71, 85, 105)
pdf.cell(90, 4.5, f"Email: {sender_email}", new_x="RIGHT")
pdf.cell(90, 4.5, f"Attn: {client_contact}", new_x="LMARGIN", new_y="NEXT")

pdf.cell(90, 4.5, f"Phone: {sender_phone}", new_x="RIGHT")
pdf.cell(90, 4.5, f"Email: {client_email}", new_x="LMARGIN", new_y="NEXT")

pdf.ln(5)

# --- PROPOSAL META BAR ---
pdf.set_fill_color(248, 250, 252)
pdf.rect(15, pdf.get_y(), 180, 9, 'F')
pdf.set_xy(18, pdf.get_y() + 1.5)
pdf.set_font('Helvetica', 'B', 8)
pdf.set_text_color(79, 70, 229)

pdf.cell(60, 6, f"REF: {prop_number.upper()}", new_x="RIGHT")
pdf.cell(60, 6, f"ISSUED: {date_today.upper()}", new_x="RIGHT")
pdf.cell(60, 6, f"VALID UNTIL: {valid_until.upper()}", new_x="LMARGIN", new_y="NEXT")

pdf.ln(6)

# --- PROJECT TITLE & SCOPE ---
pdf.set_font('Helvetica', 'B', 13)
pdf.set_text_color(15, 23, 42)
pdf.multi_cell(0, 6, proposal_title)
pdf.ln(2)

pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(79, 70, 229)
pdf.cell(0, 5, "1. Executive Summary & Scope of Work", new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', '', 9)
pdf.set_text_color(51, 65, 85)
pdf.multi_cell(0, 4.5, scope_desc)
pdf.ln(5)

# --- PRICING TABLE ---
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(79, 70, 229)
pdf.cell(0, 5, "2. Pricing & Investment Breakdown", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# Table Header
pdf.set_fill_color(15, 23, 42) # Dark Slate Header
pdf.set_text_color(255, 255, 255)
pdf.set_font('Helvetica', 'B', 8)
pdf.cell(95, 7, "  Description", fill=True, new_x="RIGHT")
pdf.cell(20, 7, "Qty", fill=True, align="C", new_x="RIGHT")
pdf.cell(32, 7, "Unit Rate", fill=True, align="R", new_x="RIGHT")
pdf.cell(33, 7, "Total Amount  ", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")

# Table Rows
pdf.set_text_color(51, 65, 85)
pdf.set_font('Helvetica', '', 9)

# Row 1
pdf.cell(95, 7, f"  {item1_name[:48]}", border="B", new_x="RIGHT")
pdf.cell(20, 7, str(item1_qty), border="B", align="C", new_x="RIGHT")
pdf.cell(32, 7, f"{curr_symbol}{item1_rate:,.2f}", border="B", align="R", new_x="RIGHT")
pdf.cell(33, 7, f"{curr_symbol}{total1:,.2f}  ", border="B", align="R", new_x="LMARGIN", new_y="NEXT")

# Row 2 (Optional)
if item2_qty > 0 and item2_name.strip():
    pdf.cell(95, 7, f"  {item2_name[:48]}", border="B", new_x="RIGHT")
    pdf.cell(20, 7, str(item2_qty), border="B", align="C", new_x="RIGHT")
    pdf.cell(32, 7, f"{curr_symbol}{item2_rate:,.2f}", border="B", align="R", new_x="RIGHT")
    pdf.cell(33, 7, f"{curr_symbol}{total2:,.2f}  ", border="B", align="R", new_x="LMARGIN", new_y="NEXT")

# Grand Total Row
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(15, 23, 42)
pdf.cell(147, 8, "Total Project Investment: ", align="R", new_x="RIGHT")
pdf.set_text_color(79, 70, 229)
pdf.cell(33, 8, f"{curr_symbol}{grand_total:,.2f}  ", align="R", new_x="LMARGIN", new_y="NEXT")

pdf.ln(4)

# --- TERMS & ACCEPTANCE ---
pdf.set_font('Helvetica', 'B', 10)
pdf.set_text_color(79, 70, 229)
pdf.cell(0, 5, "3. Terms of Agreement", new_x="LMARGIN", new_y="NEXT")

pdf.set_font('Helvetica', '', 8)
pdf.set_text_color(71, 85, 105)
pdf.multi_cell(0, 4, payment_terms)
pdf.ln(6)

# --- SIGNATURE BLOCK ---
pdf.set_font('Helvetica', 'B', 8)
pdf.set_text_color(15, 23, 42)
pdf.cell(90, 4, "Accepted & Agreed (Client):", new_x="RIGHT")
pdf.cell(90, 4, "Authorized Representative (Provider):", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.cell(90, 4, "Signature: ___________________________", new_x="RIGHT")
pdf.cell(90, 4, f"Signature: {sender_company}", new_x="LMARGIN", new_y="NEXT")
pdf.cell(90, 4, "Date: ________________________________", new_x="RIGHT")
pdf.cell(90, 4, f"Date: {date_today}", new_x="LMARGIN", new_y="NEXT")

# --- RENDER TO BASE64 FOR PREVIEW ---
pdf_bytes = bytes(pdf.output())
base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')

# ==================== RIGHT COLUMN: LIVE PREVIEW ====================
with col_right:
    st.markdown("#### 👁️ Live PDF Preview")
    
    # Download Button
    st.download_button(
        label="📥 Download PDF Proposal",
        data=pdf_bytes,
        file_name=f"Proposal_{client_company.replace(' ', '_')}_{prop_number}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    
    # Embedded Interactive PDF Viewer
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="720" type="application/pdf" style="border-radius: 10px; border: 1px solid #334155;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

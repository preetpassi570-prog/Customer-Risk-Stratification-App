import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import os
import warnings

# =========================================================================
# CONFIGURATION & SETUP
# =========================================================================
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Enterprise Risk Stratification",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# CUSTOM CSS / UI THEME (Premium Enterprise, Black + Dark Red)
# =========================================================================
def inject_custom_css():
    st.markdown("""
        <style>
        /* Main Application Background */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 50% 0%, #2a0000 0%, #0a0a0a 60%, #000000 100%);
            color: #ffffff;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar Styles */
        [data-testid="stSidebar"] {
            background-color: rgba(15, 15, 15, 0.95) !important;
            border-right: 1px solid rgba(255, 43, 43, 0.2);
        }

        /* Hide Default UI Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Section Header Cards */
        .section-header-card {
            background: linear-gradient(145deg, rgba(40, 5, 5, 0.8), rgba(15, 0, 0, 0.95));
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 43, 43, 0.3);
            border-radius: 12px;
            padding: 20px 30px;
            margin: 40px 0 25px 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.7), inset 0 0 15px rgba(255, 43, 43, 0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            text-align: center;
        }
        
        .section-header-card h2 {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 2px;
            text-transform: uppercase;
            text-shadow: 0 0 10px rgba(255, 43, 43, 0.4);
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(20, 20, 20, 0.5);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 43, 43, 0.2);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7), inset 0 0 10px rgba(255, 43, 43, 0.05);
            margin-bottom: 24px;
            transition: all 0.4s ease;
            height: 100%;
        }
        
        .glass-card:hover {
            border-color: rgba(255, 43, 43, 0.5);
            box-shadow: 0 12px 40px 0 rgba(255, 43, 43, 0.2), inset 0 0 15px rgba(255, 43, 43, 0.15);
        }

        /* KPI Metric Cards */
        .kpi-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 25px 15px;
            background: linear-gradient(145deg, rgba(30,30,30,0.7) 0%, rgba(10,10,10,0.9) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-bottom: 4px solid #ff2b2b;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
            height: 100%;
            transition: transform 0.3s ease;
            margin-bottom: 20px;
        }
        
        .kpi-container:hover {
            transform: translateY(-5px);
            border-bottom: 4px solid #ff5555;
            background: linear-gradient(145deg, rgba(40,40,40,0.8) 0%, rgba(15,15,15,0.95) 100%);
        }

        .kpi-value {
            font-size: 2.2rem;
            font-weight: 900;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 0 15px rgba(255, 43, 43, 0.3);
            letter-spacing: 1px;
        }

        .kpi-label {
            font-size: 0.95rem;
            color: #c0c0c0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 10px;
            font-weight: 700;
        }

        /* Button Styling */
        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(135deg, #ff2b2b 0%, #8B0000 100%) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(255, 43, 43, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover, .stDownloadButton > button:hover {
            box-shadow: 0 8px 25px rgba(255, 43, 43, 0.8) !important;
            transform: scale(1.02) !important;
            background: linear-gradient(135deg, #ff4444 0%, #aa0000 100%) !important;
        }

        /* Input Fields */
        .stNumberInput > div > div > input, .stTextInput > div > div > input, .stSelectbox > div > div {
            background-color: rgba(15, 15, 15, 0.9) !important;
            color: white !important;
            border: 1px solid rgba(255, 43, 43, 0.4) !important;
            border-radius: 8px !important;
            font-size: 1.1rem !important;
            transition: all 0.3s ease;
        }
        
        /* Risk Shields */
        .shield-high {
            background: linear-gradient(145deg, rgba(139, 0, 0, 0.4), rgba(20, 0, 0, 0.8));
            border: 2px solid #ff2b2b;
            border-radius: 12px;
            padding: 35px 20px;
            text-align: center;
            box-shadow: 0 0 30px rgba(255, 43, 43, 0.4);
            animation: pulse-red 2s infinite;
        }

        .shield-low {
            background: linear-gradient(145deg, rgba(0, 100, 0, 0.3), rgba(0, 20, 0, 0.8));
            border: 2px solid #00ff88;
            border-radius: 12px;
            padding: 35px 20px;
            text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        }
        
        @keyframes pulse-red {
            0% { box-shadow: 0 0 15px rgba(255, 43, 43, 0.2); }
            50% { box-shadow: 0 0 40px rgba(255, 43, 43, 0.6); }
            100% { box-shadow: 0 0 15px rgba(255, 43, 43, 0.2); }
        }

        /* Table Styling */
        .stDataFrame {
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_section_header(icon, title):
    st.markdown(f"""
        <div class="section-header-card">
            <span style="font-size: 2rem; margin-right: 10px;">{icon}</span>
            <h2>{title}</h2>
        </div>
    """, unsafe_allow_html=True)

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================
def format_inr(number):
    try:
        if pd.isna(number): return "₹ 0"
        is_negative = number < 0
        number = abs(round(float(number)))
        num_str = str(number)
        if len(num_str) > 3:
            last_3 = num_str[-3:]
            other = num_str[:-3]
            chunks = []
            while len(other) > 0:
                chunks.insert(0, other[-2:])
                other = other[:-2]
            other_str = ",".join(chunks)
            formatted = f"₹ {other_str},{last_3}"
        else:
            formatted = f"₹ {num_str}"
        return f"-{formatted}" if is_negative else formatted
    except:
        return "₹ 0"

def clean_currency(val):
    if pd.isna(val): return 0.0
    return float(str(val).replace('₹', '').replace('$', '').replace(',', '').replace(' ', '').strip())

def create_gauge(probability):
    val = probability * 100
    color = "#ff2b2b" if val >= 50 else "#00ff88"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'suffix': "%", 'font': {'size': 45, 'color': 'white', 'family': 'Segoe UI'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 255, 136, 0.15)'},
                {'range': [50, 100], 'color': 'rgba(255, 43, 43, 0.15)'}
            ],
            'threshold': {'line': {'color': color, 'width': 5}, 'thickness': 0.8, 'value': val}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# =========================================================================
# DATA PROCESSING & MODEL LOADING
# =========================================================================
@st.cache_data
def load_and_preprocess_data():
    if not os.path.exists('Customers.csv') or not os.path.exists('Orders.csv'):
        st.error("🚨 Required dataset files not found.")
        st.stop()
        
    customers = pd.read_csv('Customers.csv')
    orders = pd.read_csv('Orders.csv')

    # Merge data (keep customer columns clean by adding suffix to orders)
    if 'Customer_ID' in customers.columns and 'Customer_ID' in orders.columns:
        df = pd.merge(customers, orders, on='Customer_ID', how="inner", suffixes=('', '_order'))
    else:
        df = customers.copy()

    # Preprocessing pipelines mimicking Risk_Model.ipynb
    for col in ['Lifetime_Value', 'Annual_Income', 'Sales_Amount', 'Profit']:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)

    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce").fillna(df["Age"].median())
    if "Total_Orders" in df.columns:
        df["Total_Orders"] = pd.to_numeric(df["Total_Orders"], errors="coerce").fillna(0)

    if "Last_Purchase_Date" in df.columns:
        df["Last_Purchase_Date"] = pd.to_datetime(df["Last_Purchase_Date"], errors="coerce", dayfirst=True)
        latest_Date = df["Last_Purchase_Date"].max()
        if pd.isna(latest_Date):
            latest_Date = pd.Timestamp.now()
        df["days_Since_Last_Purchase"] = (latest_Date - df["Last_Purchase_Date"]).dt.days
        df["days_Since_Last_Purchase"] = df["days_Since_Last_Purchase"].fillna(0)
    else:
        df["days_Since_Last_Purchase"] = 0

    df["Risk"] = np.where(
        (df["days_Since_Last_Purchase"] > 180) &
        (df["Total_Orders"] < 5) &
        (df["Lifetime_Value"] < 10000),
        "High Risk",
        "Low Risk"
    )
    
    return df

@st.cache_resource
def load_trained_model():
    model_path = 'customer_risk_model.pkl'
    if not os.path.exists(model_path):
        st.error("🚨 Model file not found.")
        st.stop()
    return joblib.load(model_path)

# =========================================================================
# MAIN DASHBOARD APPLICATION
# =========================================================================
def main():
    inject_custom_css()
    # ===========================
    # YOUR HEADER
    # ===========================

    st.markdown("""
<div style="
background:rgba(35,10,10,0.35);
backdrop-filter:blur(20px);
-webkit-backdrop-filter:blur(20px);
border:1px solid rgba(255,70,70,.18);
border-radius:20px;
padding:22px 35px;
margin-bottom:25px;
box-shadow:0 10px 25px rgba(0,0,0,.35);
">

<div style="
display:flex;
align-items:center;
justify-content:center;
gap:18px;
margin-bottom:12px;
">

<div style="
font-size:52px;
">
🛡️
</div>

<div style="
font-size:38px;
font-weight:900;
letter-spacing:1px;
font-family:'Segoe UI',sans-serif;
white-space:nowrap;
">

<span style="color:white;">CUSTOMER RISK STRATIFICATION APP</span>

</div>

</div>

<div style="
text-align:center;
font-size:17px;
font-weight:600;
color:#f2f2f2;
margin-bottom:5px;
">
Enterprise Machine Learning Dashboard
</div>

<div style="
text-align:center;
font-size:13px;
color:#b0b0b0;
margin-bottom:18px;
">
Real-Time Customer Risk Prediction • AI Analytics • Business Intelligence
</div>

<div style="
display:flex;
justify-content:center;
gap:12px;
flex-wrap:wrap;
">

<div style="
background:rgba(255,255,255,.04);
padding:8px 18px;
border-radius:30px;
border-left:3px solid #ff4040;
font-size:13px;
">
👨‍💻 <b>Developed By:</b> Preet
</div>

<div style="
background:rgba(255,255,255,.04);
padding:8px 18px;
border-radius:30px;
border-left:3px solid #00ff88;
font-size:13px;
">
🤖 Machine Learning
</div>

<div style="
background:rgba(255,255,255,.04);
padding:8px 18px;
border-radius:30px;
border-left:3px solid #00bfff;
font-size:13px;
">
📊 Enterprise Dashboard
</div>

</div>

</div>
""", unsafe_allow_html=True)
    df = load_and_preprocess_data()
    model = load_trained_model()

    # --- SIDEBAR FILTERS (SLICERS) ---
    st.sidebar.markdown("""
        <div style='text-align:center; padding: 10px;'>
            <h1 style='font-size: 3rem; margin:0; text-shadow: 0 0 10px #ff2b2b;'>🛡️</h1>
            <h3 style='color: white; font-weight:800; letter-spacing:1px;'>FILTERS</h3>
        </div>
        <hr style='border-color: rgba(255,43,43,0.3);'>
    """, unsafe_allow_html=True)
    
    # Text Search (Customer ID/Name)
    search_query = st.sidebar.text_input("🔍 Search Customer (ID or Name)", "")
    
    # Categorical Filters
    risk_options = df['Risk'].unique().tolist()
    selected_risk = st.sidebar.multiselect("⚠️ Risk Level", options=risk_options, default=risk_options)
    
    if 'Gender' in df.columns:
        gender_options = df['Gender'].dropna().unique().tolist()
        selected_gender = st.sidebar.multiselect("🚻 Gender", options=gender_options, default=gender_options)
    else:
        selected_gender = []

    if 'City' in df.columns:
        city_options = df['City'].dropna().unique().tolist()
        selected_city = st.sidebar.multiselect("🏙️ City", options=city_options, default=[])
    else:
        selected_city = []

    # Numeric Range Filters
    min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.sidebar.slider("👤 Age Range", min_age, max_age, (min_age, max_age))

    min_inc, max_inc = float(df['Annual_Income'].min()), float(df['Annual_Income'].max())
    inc_range = st.sidebar.slider("💰 Annual Income (₹)", min_inc, max_inc, (min_inc, max_inc), step=50000.0)

    min_ltv, max_ltv = float(df['Lifetime_Value'].min()), float(df['Lifetime_Value'].max())
    ltv_range = st.sidebar.slider("💎 Lifetime Value (₹)", min_ltv, max_ltv, (min_ltv, max_ltv), step=10000.0)

    min_orders, max_orders = int(df['Total_Orders'].min()), int(df['Total_Orders'].max())
    order_range = st.sidebar.slider("📦 Total Orders", min_orders, max_orders, (min_orders, max_orders))

    # --- APPLY FILTERS ---
    filtered_df = df.copy()
    
    if search_query:
        mask = filtered_df['Customer_ID'].astype(str).str.contains(search_query, case=False, na=False)
        if 'Customer_Name' in filtered_df.columns:
            mask = mask | filtered_df['Customer_Name'].astype(str).str.contains(search_query, case=False, na=False)
        filtered_df = filtered_df[mask]

    if selected_risk:
        filtered_df = filtered_df[filtered_df['Risk'].isin(selected_risk)]
    if selected_gender:
        filtered_df = filtered_df[filtered_df['Gender'].isin(selected_gender)]
    if selected_city:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_city)]
        
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]
    filtered_df = filtered_df[(filtered_df['Annual_Income'] >= inc_range[0]) & (filtered_df['Annual_Income'] <= inc_range[1])]
    filtered_df = filtered_df[(filtered_df['Lifetime_Value'] >= ltv_range[0]) & (filtered_df['Lifetime_Value'] <= ltv_range[1])]
    filtered_df = filtered_df[(filtered_df['Total_Orders'] >= order_range[0]) & (filtered_df['Total_Orders'] <= order_range[1])]

    # Deduplicate for customer-level metrics
    cust_df = filtered_df.drop_duplicates(subset=['Customer_ID']) if 'Customer_ID' in filtered_df.columns else filtered_df

    # --- KPI SECTION (2x4 Grid) ---
    render_section_header("📊", "Enterprise Key Performance Indicators")
    
    total_sales = filtered_df['Sales_Amount'].sum() if 'Sales_Amount' in filtered_df.columns else 0
    total_profit = filtered_df['Profit'].sum() if 'Profit' in filtered_df.columns else 0
    total_customers = len(cust_df)
    
    high_risk_df = cust_df[cust_df['Risk'] == 'High Risk']
    low_risk_df = cust_df[cust_df['Risk'] == 'Low Risk']
    
    high_risk_count = len(high_risk_df)
    low_risk_count = len(low_risk_df)
    
    avg_age_low = low_risk_df['Age'].mean() if low_risk_count > 0 else 0
    avg_age_high = high_risk_df['Age'].mean() if high_risk_count > 0 else 0
    risk_pct = (high_risk_count / total_customers * 100) if total_customers > 0 else 0

    # Row 1
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='kpi-container' style='border-color: #aaaaaa;'><p class='kpi-value'>{format_inr(total_sales)}</p><p class='kpi-label'>📦 Total Sales (₹)</p></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi-container' style='border-color: #aaaaaa;'><p class='kpi-value'>{format_inr(total_profit)}</p><p class='kpi-label'>💰 Total Profit (₹)</p></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-container' style='border-color: #aaaaaa;'><p class='kpi-value'>{total_customers:,}</p><p class='kpi-label'>👥 Total Customers</p></div>", unsafe_allow_html=True)
    with k4:
        st.markdown(f"<div class='kpi-container' style='border-color: #ff2b2b;'><p class='kpi-value' style='color:#ff2b2b;'>{high_risk_count:,}</p><p class='kpi-label'>🔴 High Risk Customers</p></div>", unsafe_allow_html=True)

    # Row 2
    k5, k6, k7, k8 = st.columns(4)
    with k5:
        st.markdown(f"<div class='kpi-container' style='border-color: #00ff88;'><p class='kpi-value' style='color:#00ff88;'>{low_risk_count:,}</p><p class='kpi-label'>🟢 Low Risk Customers</p></div>", unsafe_allow_html=True)
    with k6:
        st.markdown(f"<div class='kpi-container' style='border-color: #00ff88;'><p class='kpi-value'>{avg_age_low:.0f}</p><p class='kpi-label'>👨 Avg Age (Low Risk)</p></div>", unsafe_allow_html=True)
    with k7:
        st.markdown(f"<div class='kpi-container' style='border-color: #ff2b2b;'><p class='kpi-value'>{avg_age_high:.0f}</p><p class='kpi-label'>👩 Avg Age (High Risk)</p></div>", unsafe_allow_html=True)
    with k8:
        st.markdown(f"<div class='kpi-container' style='border-color: #ff2b2b;'><p class='kpi-value' style='color:#ff2b2b;'>{risk_pct:.1f}%</p><p class='kpi-label'>📈 Overall Risk Percentage</p></div>", unsafe_allow_html=True)

    # --- ENTERPRISE DATA ANALYTICS (Strictly 4 Charts) ---
    render_section_header("📈", "Enterprise Data Analytics")
    
    chart_config = {'template': 'plotly_dark', 'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0,0,0,0.2)'}
    
    c1, c2 = st.columns(2)
    
    # Chart 1: Customer Risk Distribution (Pie Chart)
    with c1:
        st.markdown("<div class='glass-card'><h4 style='padding-top: 10px; margin-bottom: 0px;'>Customer Risk Distribution</h4>", unsafe_allow_html=True)
        if not cust_df.empty:
            risk_counts = cust_df['Risk'].value_counts().reset_index()
            fig1 = px.pie(risk_counts, values='count', names='Risk', color='Risk',
                          color_discrete_map={'High Risk': '#ff2b2b', 'Low Risk': '#00ff88'},
                          title="Pie Chart")
            fig1.update_traces(textposition='inside', textinfo='percent+label+value')
            fig1.update_layout(**chart_config, margin=dict(t=50, b=20, l=10, r=10))
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No Data Available")
        st.markdown("</div>", unsafe_allow_html=True)

    # Chart 2: City Wise Sales (Bar Chart)
    with c2:
        st.markdown("<div class='glass-card'><h4 style='padding-top: 10px; margin-bottom: 0px;'>City Wise Sales</h4>", unsafe_allow_html=True)
        if not filtered_df.empty and 'City' in filtered_df.columns and 'Sales_Amount' in filtered_df.columns:
            city_sales = filtered_df.groupby('City')['Sales_Amount'].sum().reset_index()
            city_sales = city_sales.sort_values('Sales_Amount', ascending=False).head(15) # Top 15 to avoid clutter
            fig2 = px.bar(city_sales, x='City', y='Sales_Amount', text='Sales_Amount',
                          title="Bar Chart", color_discrete_sequence=['#8B0000'])
            fig2.update_traces(texttemplate='%{text:$.2s}'.replace('$', '₹'), textposition='outside')
            fig2.update_layout(**chart_config, margin=dict(t=50, b=20, l=10, r=10), yaxis_title="Total Sales (₹)")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No Data Available")
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    # Chart 3: Age Wise High Risk Customers (Bar Chart)
    with c3:
        st.markdown("<div class='glass-card'><h4 style='padding-top: 10px; margin-bottom: 0px;'>Age Wise High Risk Customers</h4>", unsafe_allow_html=True)
        if not high_risk_df.empty:
            age_high = high_risk_df['Age'].value_counts().reset_index().sort_values('Age')
            fig3 = px.bar(age_high, x='Age', y='count', 
                          title="Bar Chart", color_discrete_sequence=['#ff2b2b'])
            fig3.update_layout(**chart_config, margin=dict(t=50, b=20, l=10, r=10), yaxis_title="High Risk Count")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No Data Available")
        st.markdown("</div>", unsafe_allow_html=True)

    # Chart 4: Age Wise Low Risk Customers (Bar Chart)
    with c4:
        st.markdown("<div class='glass-card'><h4 style='padding-top: 10px; margin-bottom: 0px;'>Age Wise Low Risk Customers</h4>", unsafe_allow_html=True)
        if not low_risk_df.empty:
            age_low = low_risk_df['Age'].value_counts().reset_index().sort_values('Age')
            fig4 = px.bar(age_low, x='Age', y='count', 
                          title="Bar Chart", color_discrete_sequence=['#00ff88'])
            fig4.update_layout(**chart_config, margin=dict(t=50, b=20, l=10, r=10), yaxis_title="Low Risk Count")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No Data Available")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- REAL-TIME RISK INFERENCE ENGINE ---
    render_section_header("⚡", "Real-Time Risk Inference Engine")
    
    col_input, col_result = st.columns([1.2, 1])
    
    feature_cols = ['Age', 'Annual_Income', 'Total_Orders', 'Lifetime_Value', 'days_Since_Last_Purchase']
    if hasattr(model, 'feature_names_in_'):
        feature_cols = list(model.feature_names_in_)
        
    with col_input:
        st.markdown("<div class='glass-card'><h4 style='padding-top: 5px; margin-bottom: 0px;'>Customer Data Input</h4>", unsafe_allow_html=True)
        
        
        with st.form("risk_prediction_form"):
            i1, i2 = st.columns(2)
            with i1:
                age_input = st.number_input("Age", min_value=18, max_value=120, value=int(cust_df['Age'].median() if not cust_df.empty else 35), step=1)
                income_input = st.number_input("Annual Income (₹)", min_value=0.0, value=float(cust_df['Annual_Income'].median() if not cust_df.empty else 500000.0), step=50000.0)
                orders_input = st.number_input("Total Orders", min_value=0, value=int(cust_df['Total_Orders'].median() if not cust_df.empty else 10), step=1)
            with i2:
                ltv_input = st.number_input("Lifetime Value (₹)", min_value=0.0, value=float(cust_df['Lifetime_Value'].median() if not cust_df.empty else 25000.0), step=5000.0)
                days_input = st.number_input("Days Since Last Purchase", min_value=0, value=int(cust_df['days_Since_Last_Purchase'].median() if not cust_df.empty else 60), step=1)
                st.markdown("<br>", unsafe_allow_html=True)
            submit_pred = st.form_submit_button("⚡ PREDICT RISK")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_result:
        if submit_pred:
            input_dict = {'Age': age_input, 'Annual_Income': income_input, 'Total_Orders': orders_input, 'Lifetime_Value': ltv_input, 'days_Since_Last_Purchase': days_input}
            input_data = {feat: [input_dict.get(feat, 0)] for feat in feature_cols}
            input_df = pd.DataFrame(input_data)

            try:
                if hasattr(model, 'predict_proba'):
                    probas = model.predict_proba(input_df)[0]
                    if hasattr(model, 'classes_'):
                        class_names = list(model.classes_)
                        if 'High Risk' in class_names:
                            prob_high = probas[class_names.index('High Risk')]
                        elif 0 in class_names:
                            prob_high = probas[class_names.index(0)]
                        else:
                            prob_high = probas[1] if len(probas) > 1 else probas[0]
                    else:
                        prob_high = probas[1] if len(probas) > 1 else probas[0]
                else:
                    pred_class = model.predict(input_df)[0]
                    prob_high = 0.85 if pred_class == 0 or pred_class == 'High Risk' else 0.15

                risk_level = "High Risk" if prob_high >= 0.5 else "Low Risk"

                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                if risk_level == "High Risk":
                    st.markdown("""
                        <div class='shield-high'>
                            <h1 style='font-size: 3.5rem; margin:0;'>🛡️</h1>
                            <h2 style='color:#ff2b2b; margin:10px 0; font-weight:900; letter-spacing: 2px;'>HIGH RISK</h2>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class='shield-low'>
                            <h1 style='font-size: 3.5rem; margin:0;'>✅</h1>
                            <h2 style='color:#00ff88; margin:10px 0; font-weight:900; letter-spacing: 2px;'>LOW RISK</h2>
                        </div>
                    """, unsafe_allow_html=True)

                st.plotly_chart(create_gauge(prob_high), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Prediction Pipeline Error: {str(e)}")
        else:
            st.markdown("""
                <div class='glass-card' style='display:flex; flex-direction:column; align-items:center; justify-content:center; height:100%; min-height:500px; opacity:0.6; text-align: center;'>
                    <h1 style='font-size:5rem; margin:0;'>📊</h1>
                    <h3 style='color:white; margin-top: 15px;'>Awaiting Parameters</h3>
                </div>
            """, unsafe_allow_html=True)

    # --- RECENT CUSTOMER DATABASE ---
    render_section_header("📋", "Recent Customer Database")
    
    if cust_df.empty:
        st.warning("⚠️ No Data Available for the current filters.")
    else:
        display_cols = ['Customer_ID', 'Customer_Name', 'Age', 'Annual_Income', 'Lifetime_Value', 'Total_Orders', 'days_Since_Last_Purchase', 'Risk']
        display_cols = [c for c in display_cols if c in cust_df.columns]
        
        table_df = cust_df[display_cols].copy()
        if 'Annual_Income' in table_df.columns:
            table_df['Annual_Income'] = table_df['Annual_Income'].apply(format_inr)
        if 'Lifetime_Value' in table_df.columns:
            table_df['Lifetime_Value'] = table_df['Lifetime_Value'].apply(format_inr)
            
        def style_risk(val):
            color = '#00ff88' if val == 'Low Risk' else '#ff2b2b'
            return f'color: {color}; font-weight: bold;'
            
        if 'Risk' in table_df.columns:
            styled_df = table_df.style.map(style_risk, subset=['Risk'])
        else:
            styled_df = table_df
            
        st.dataframe(styled_df, use_container_width=True, height=400)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- DOWNLOAD SECTION ---
    render_section_header("📥", "Download Center")
    
    d1, d2, d3, d4, d5 = st.columns(5)
    
    csv_processed = cust_df.to_csv(index=False).encode('utf-8')
    csv_high_risk = high_risk_df.to_csv(index=False).encode('utf-8')
    csv_low_risk = low_risk_df.to_csv(index=False).encode('utf-8')
    
    summary = f"""Dashboard Summary
Total Customers: {total_customers}
Total Sales: {format_inr(total_sales)}
Total Profit: {format_inr(total_profit)}
High Risk Customers: {high_risk_count}
Low Risk Customers: {low_risk_count}
Risk Percentage: {risk_pct:.2f}%
Avg Age (Low Risk): {avg_age_low:.1f}
Avg Age (High Risk): {avg_age_high:.1f}
"""

    with d1:
        st.download_button("📥 Processed CSV", data=csv_processed, file_name='Processed_Customers.csv', mime='text/csv')
    with d2:
        st.download_button("📥 Prediction Report", data=csv_processed, file_name='Prediction_Report.csv', mime='text/csv')
    with d3:
        st.download_button("📥 High Risk Data", data=csv_high_risk, file_name='High_Risk_Customers.csv', mime='text/csv')
    with d4:
        st.download_button("📥 Low Risk Data", data=csv_low_risk, file_name='Low_Risk_Customers.csv', mime='text/csv')
    with d5:
        st.download_button("📥 Dashboard Summary", data=summary.encode('utf-8'), file_name='Dashboard_Summary.txt', mime='text/plain')

    # --- FOOTER ---
    st.markdown("""
        <b>CUSTOMER RISK STRATIFICATION APP</b><br>
Enterprise Machine Learning Dashboard for Customer Risk Analysis<br><br>

<b>Developed By:</b> Preet<br><br>
<b>Technologies Used:</b><br>
Python • Streamlit • Scikit-Learn • Pandas • NumPy • Plotly<br><br>
<b>Machine Learning Model:</b><br>
Random Forest Classifier<br><br>
<b>Dataset:</b><br>
Customers.csv | Orders.csv<br><br>
<a href="https://github.com/YOUR_GITHUB_USERNAME"
style="color:#ff4d4d; text-decoration:none;" target="_blank">
🔗 GitHub
</a>
&nbsp;&nbsp;|&nbsp;&nbsp;
<a href="https://www.linkedin.com/in/YOUR_LINKEDIN_USERNAME"
style="color:#ff4d4d; text-decoration:none;" target="_blank">
💼 LinkedIn
</a>
<br><br>
<a href="mailto:preetpassi570gmail.com"
style="color:#ff4d4d; text-decoration:none;">
📧 preetpassi570@gmail.com
</a>
<br><br>
<p style="color:#ff4040;">
© 2026 Customer Risk Stratification Dashboard
</p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
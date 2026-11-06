import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title='Motorcycle Sales Analytics | Apple UI',
    page_icon='🏍️',
    layout='wide',
    initial_sidebar_state='expanded',
)

# 2. Sidebar: Switcher Theme Mode
st.sidebar.markdown('### 🎨 Pengaturan Tema')
theme_mode = st.sidebar.radio(
    "Pilih Mode Tampilan:",
    options=["Terang (Light Mode) ☀️", "Gelap (Dark Mode) 🌙"],
    index=0
)
st.sidebar.markdown('---')

is_dark = "Gelap" in theme_mode

# 3. Dynamic Custom CSS (Apple UI Design System)
bg_color = "#16181D" if is_dark else "#F5F5F7"
text_primary = "#FFFFFF" if is_dark else "#1D1D1F"
text_secondary = "#A0A5B5" if is_dark else "#86868B"
sidebar_bg = "#21252D" if is_dark else "rgba(255, 255, 255, 0.85)"
card_bg = "#242832" if is_dark else "#FFFFFF"
card_border = "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.04)"
grid_color = "rgba(255, 255, 255, 0.08)" if is_dark else "#F0F0F2"

st.markdown(
    f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        color: {text_primary} !important;
    }}
    .apple-header {{
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.03em;
        color: {text_primary};
        margin-bottom: 4px;
    }}
    .apple-subtitle {{
        font-weight: 400;
        font-size: 1.05rem;
        color: {text_secondary};
        letter-spacing: -0.01em;
        margin-bottom: 24px;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid {card_border} !important;
    }}
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h3 {{
        color: {text_primary} !important;
    }}
    .apple-card {{
        background: {card_bg};
        border-radius: 20px;
        padding: 22px 24px;
        border: 1px solid {card_border};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        margin-bottom: 16px;
    }}
    .apple-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
    }}
    .metric-label {{
        font-size: 0.82rem;
        font-weight: 600;
        color: {text_secondary};
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -0.03em;
    }}
    .chart-box {{
        background: {card_bg};
        border-radius: 24px;
        padding: 24px;
        border: 1px solid {card_border};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
    }}
    .chart-title {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {text_primary};
        letter-spacing: -0.02em;
        margin-bottom: 12px;
    }}
    .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        border-radius: 12px !important;
        border: 1px solid {card_border} !important;
        color: {text_primary} !important;
    }}
    .stExpander p, .stExpander li {{
        color: {text_primary} !important;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Load Data Kasus 2 (Disesuaikan dengan file DataPenjualanMotor.csv)
@st.cache_data
def load_data():
    data = pd.read_csv('DataPenjualanMotor.csv', sep=';')
    
    # Format Tanggal
    data['Tanggal'] = pd.to_datetime(data['TANGGAL'], format='%d-%b-%y')
    
    # Mapping Nama Kolom
    data['Provinsi'] = data['PROPINSI']
    data['Model Motor'] = data['SERIES']
    data['Jenis Bayar'] = data['JENIS BAYAR']
    
    # Cleaning Format Uang Rupiah
    def clean_money(val):
        if pd.isna(val): return 0
        return int(str(val).replace('.', '').replace(',', '').strip())

    data['Harga Jual (Rp)'] = data['HARGA JUAL'].apply(clean_money)
    data['Diskon (Rp)'] = data['DISKON'].apply(clean_money)
    data['Total Penjualan (Rp)'] = data['Harga Jual (Rp)'] - data['Diskon (Rp)']
    
    return data.sort_values('Tanggal')

df = load_data()

# 5. Header Section
st.markdown(
    '<div class="apple-header">Dashboard Penjualan Motor di Indonesia</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="apple-subtitle">Analisis Operasional & Distribusi Penjualan Motor • Bedah Kasus 2</div>',
    unsafe_allow_html=True,
)

# 6. Sidebar Filter
st.sidebar.markdown('### 🎛️ Filter Data')

min_date = df['Tanggal'].min().date()
max_date = df['Tanggal'].max().date()

date_range = st.sidebar.date_input(
    'Rentang Tanggal',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

list_provinsi = df['Provinsi'].dropna().unique().tolist()
selected_provinsi = st.sidebar.multiselect(
    'Pilih Provinsi:',
    options=list_provinsi,
    default=list_provinsi,
)

list_model = df['Model Motor'].dropna().unique().tolist()
selected_model = st.sidebar.multiselect(
    'Pilih Model Motor:',
    options=list_model,
    default=list_model,
)

selected_bayar = st.sidebar.multiselect(
    'Jenis Pembayaran:',
    options=df['Jenis Bayar'].unique(),
    default=df['Jenis Bayar'].unique(),
)

# Filtering Data
if len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = df[
        (df['Tanggal'].dt.date >= start_d)
        & (df['Tanggal'].dt.date <= end_d)
        & (df['Provinsi'].isin(selected_provinsi))
        & (df['Model Motor'].isin(selected_model))
        & (df['Jenis Bayar'].isin(selected_bayar))
    ]
else:
    filtered_df = df[
        (df['Provinsi'].isin(selected_provinsi))
        & (df['Model Motor'].isin(selected_model))
        & (df['Jenis Bayar'].isin(selected_bayar))
    ]

# 7. Apple KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['Total Penjualan (Rp)'].sum()
total_units = len(filtered_df)
avg_transaction = filtered_df['Total Penjualan (Rp)'].mean() if len(filtered_df) > 0 else 0
total_diskon = filtered_df['Diskon (Rp)'].sum()

col1.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Pendapatan</div>
        <div class="metric-value">Rp {total_revenue/1e9:,.2f}M</div>
    </div>
""",
    unsafe_allow_html=True,
)

col2.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Motor Terjual</div>
        <div class="metric-value">{total_units:,} Unit</div>
    </div>
""",
    unsafe_allow_html=True,
)

col3.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Rata-rata Harga Motor</div>
        <div class="metric-value">Rp {avg_transaction/1e6:,.1f}Jt</div>
    </div>
""",
    unsafe_allow_html=True,
)

col4.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Diskon Diberikan</div>
        <div class="metric-value">Rp {total_diskon/1e6:,.1f}Jt</div>
    </div>
""",
    unsafe_allow_html=True,
)

APPLE_COLORS = ['#0071E3', '#34C759', '#FF9500', '#AF52DE', '#FF2D55', '#5856D6', '#64D2FF']

# 8. Chart Row 1
row1_col1, row1_col2 = st.columns([1.6, 1])

with row1_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Tren Penjualan Harian</div>', unsafe_allow_html=True)

    trend_df = (
        filtered_df.groupby('Tanggal')['Total Penjualan (Rp)']
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        trend_df,
        x='Tanggal',
        y='Total Penjualan (Rp)',
        labels={'Total Penjualan (Rp)': 'Pendapatan (Rp)'},
    )
    fig_line.update_traces(line_color='#0071E3', line_width=3, line_shape='spline')
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_secondary, size=11)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11)),
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💳 Proporsi Jenis Pembayaran</div>', unsafe_allow_html=True)

    fig_pie = px.pie(
        filtered_df,
        names='Jenis Bayar',
        values='Total Penjualan (Rp)',
        hole=0.65,
        color_discrete_sequence=APPLE_COLORS,
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2)),
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 9. Chart Row 2
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Top 10 Model Motor Terlaris</div>', unsafe_allow_html=True)

    top_models = (
        filtered_df['Model Motor'].value_counts().nlargest(10).reset_index()
    )
    top_models.columns = ['Model Motor', 'Jumlah Terjual']

    fig_bar = px.bar(
        top_models,
        x='Jumlah Terjual',
        y='Model Motor',
        orientation='h',
        color='Jumlah Terjual',
        color_continuous_scale=['#64D2FF', '#0071E3'],
        text_auto=True,
    )
    fig_bar.update_traces(marker_cornerradius=6)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        yaxis=dict(autorange='reversed', title='', tickfont=dict(color=text_primary, size=11)),
        xaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11))
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📍 Total Penjualan per Provinsi</div>', unsafe_allow_html=True)

    prov_df = (
        filtered_df.groupby('Provinsi')['Total Penjualan (Rp)'].sum().reset_index()
    )

    fig_prov = px.bar(
        prov_df,
        x='Provinsi',
        y='Total Penjualan (Rp)',
        color_discrete_sequence=['#34C759'],
        text_auto='.2s',
    )
    fig_prov.update_traces(marker_cornerradius=8)
    fig_prov.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_primary, size=10)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11))
    )
    st.plotly_chart(fig_prov, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 10. Tabel Data Expander
with st.expander('📋 Detail Data Penjualan Motor (Terfilter)'):
    st.dataframe(filtered_df, use_container_width=True)

# ============================================================
# app.py — TRADING SUITE UNIFIED
# Semua fitur dari 4 app digabung dalam satu tampilan:
#   Scanner Mode: Open=Low | Low Float | Breakout IDX | SNIPER FX
#   Tabs: Scanner · RS vs IHSG · Sektor · Foreign Flow · Bandarmologi
#         Chart Pattern · AI Confidence · Sentimen · Backtest
#         Leaderboard · Watchlist · Portfolio · Notifikasi
# ============================================================
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd, numpy as np, yfinance as yf, requests
from bs4 import BeautifulSoup
import time, random, os, json, concurrent.futures, html, re
import warnings, zipfile, io
from datetime import datetime, time as dtime, timedelta
import pytz
warnings.filterwarnings("ignore")

# ─── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title = "📊 Trading Suite Unified",
    page_icon  = "📊",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────
# CSS — AKSARA IDX PREMIUM TERMINAL
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-base:       #070711;
    --bg-surface:    #0d0d1a;
    --bg-elevated:   #121220;
    --bg-hover:      #161628;
    --border:        #1e1e36;
    --border-bright: #2a2a48;
    --text-primary:  #e8eeff;
    --text-secondary:#7a84a8;
    --text-muted:    #3a3f5c;
    --accent-cyan:   #00c8ff;
    --accent-green:  #00e87a;
    --accent-gold:   #f5c842;
    --accent-red:    #ff3d5a;
    --accent-purple: #9b6dff;
    --glow-cyan:     0 0 20px rgba(0,200,255,0.15);
    --glow-green:    0 0 20px rgba(0,232,122,0.15);
    --radius-sm:     6px;
    --radius-md:     10px;
    --radius-lg:     16px;
}

html, body, [class*="css"] {
    background: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
.stApp { background: var(--bg-base) !important; }
.main .block-container { padding: 1.25rem 2rem !important; max-width: 100% !important; }

h1 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
    letter-spacing: 6px !important;
    background: linear-gradient(120deg, #00c8ff 0%, #00e87a 50%, #f5c842 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    margin-bottom: 0 !important;
    text-transform: uppercase;
}
h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 3px !important;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 8px !important;
    margin-bottom: 16px !important;
}
h3 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase;
}

[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.5px;
}

.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}
.stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

.stButton > button {
    background: var(--bg-elevated) !important;
    color: var(--accent-cyan) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--bg-base) !important;
    background: var(--accent-cyan) !important;
    box-shadow: var(--glow-cyan) !important;
}
.stButton > button[kind="primary"] {
    background: rgba(0,232,122,0.08) !important;
    color: var(--accent-green) !important;
    border: 1px solid rgba(0,232,122,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent-green) !important;
    color: var(--bg-base) !important;
    box-shadow: var(--glow-green) !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 10px 16px !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"]:hover { color: var(--text-secondary) !important; }
.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
    background: transparent !important;
}

div[data-testid="stExpander"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: var(--text-secondary) !important;
    background: var(--bg-elevated) !important;
}

div[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-green)) !important;
}
div[data-testid="stProgress"] > div {
    background: var(--bg-elevated) !important;
    border-radius: 4px !important;
}

.stDataFrame { border: 1px solid var(--border) !important; border-radius: var(--radius-md) !important; overflow: hidden !important; }
[data-testid="stDataFrame"] table { font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important; }
[data-testid="stDataFrame"] th {
    background: var(--bg-elevated) !important;
    color: var(--text-secondary) !important;
    font-size: 0.65rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-bright) !important;
}
[data-testid="stDataFrame"] td { color: var(--text-primary) !important; border-bottom: 1px solid var(--border) !important; }

[data-testid="stMetric"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px 16px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.62rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

.stSuccess { background: rgba(0,232,122,0.07) !important; border: 1px solid rgba(0,232,122,0.25) !important; border-radius: var(--radius-md) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
.stWarning { background: rgba(245,200,66,0.07) !important; border: 1px solid rgba(245,200,66,0.25) !important; border-radius: var(--radius-md) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
.stError   { background: rgba(255,61,90,0.07)  !important; border: 1px solid rgba(255,61,90,0.25)  !important; border-radius: var(--radius-md) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }
.stInfo    { background: rgba(0,200,255,0.07)  !important; border: 1px solid rgba(0,200,255,0.25)  !important; border-radius: var(--radius-md) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.78rem !important; }

hr { border-color: var(--border) !important; margin: 16px 0 !important; }
.stCaption, small { font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; color: var(--text-muted) !important; }
.stRadio label, .stCheckbox label { font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important; color: var(--text-secondary) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }

.metric-box {
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 14px 16px;
    text-align: center;
    margin: 3px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.metric-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,200,255,0.5), transparent);
}
.metric-box:hover { border-color: var(--border-bright); box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
.metric-val { font-family: 'Syne', sans-serif; font-size: 1.45rem; font-weight: 800; line-height: 1.2; }
.metric-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: var(--text-muted); letter-spacing: 2px; text-transform: uppercase; margin-top: 4px; }

.signal-tag {
    display: inline-block;
    background: rgba(0,232,122,0.07);
    border: 1px solid rgba(0,232,122,0.2);
    color: var(--accent-green);
    border-radius: 4px;
    padding: 3px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    margin: 2px;
    letter-spacing: 0.5px;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
}
.info-row:last-child { border-bottom: none; }

.trade-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.trade-cell { background: var(--bg-elevated); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 12px 14px; }
.trade-cell-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: var(--text-muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 4px; }
.trade-cell-val { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; }
.trade-cell-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.67rem; margin-top: 2px; }

.fase-card {
    display: flex; align-items: center; gap: 12px;
    padding: 14px 16px; border-radius: var(--radius-md); margin-bottom: 16px; border-left: 3px solid;
}
.fase-icon { font-size: 1.5rem; }
.fase-text { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; letter-spacing: 1px; }

.quote-card {
    background: linear-gradient(135deg, rgba(245,200,66,0.04), rgba(0,200,255,0.03));
    border: 1px solid rgba(245,200,66,0.12);
    border-radius: var(--radius-md); padding: 14px 16px; margin-bottom: 10px; text-align: center;
}
.quote-line1 { font-family: 'Syne', sans-serif; font-size: 0.88rem; font-weight: 700; color: var(--accent-gold); }
.quote-line2 { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: rgba(245,200,66,0.55); margin-top: 3px; font-style: italic; }

.sb-card { background: var(--bg-elevated); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 14px 16px; margin-bottom: 10px; text-align: center; }
.sb-card-title { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: var(--text-muted); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }

.empty-state { text-align: center; padding: 80px 20px; }
.empty-state .icon { font-size: 3.5rem; margin-bottom: 16px; }
.empty-state .title { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 800; color: var(--text-secondary); letter-spacing: 4px; text-transform: uppercase; margin-bottom: 8px; }
.empty-state .sub { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-muted); letter-spacing: 1px; line-height: 1.9; max-width: 580px; margin: 0 auto; }

.ai-output {
    background: linear-gradient(180deg, var(--bg-elevated), var(--bg-surface));
    border: 1px solid var(--border-bright); border-radius: var(--radius-lg);
    padding: 24px; color: #c8d4f0; font-size: 0.85rem; line-height: 1.9; margin-top: 16px;
}

.verdict-banner {
    border-radius: var(--radius-md); padding: 14px 18px; text-align: center;
    font-family: 'Syne', sans-serif; font-size: 0.88rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase; margin-top: 10px;
}

.section-card { background: var(--bg-surface); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 20px; margin-bottom: 16px; }
.section-title { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 700; color: var(--text-muted); letter-spacing: 3px; text-transform: uppercase; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }

.badge-new {
    background: linear-gradient(90deg, #00c8ff22, #00e87a22);
    border: 1px solid #00c8ff44;
    color: #00c8ff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    padding: 2px 7px;
    border-radius: 20px;
    letter-spacing: 1px;
    text-transform: uppercase;
    vertical-align: middle;
    margin-left: 6px;
}

.rs-bar {
    height: 6px;
    border-radius: 3px;
    margin-top: 4px;
}

.sector-heatmap-cell {
    border-radius: 8px;
    padding: 12px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ── SNIPER FX additions ── */
.hdr{background:linear-gradient(135deg,#050a0e,#0a1520);border-bottom:2px solid #00ff88;
     padding:20px 24px;margin-bottom:20px;border-radius:0 0 12px 12px;}
.hdr-title{font-family:'Exo 2',sans-serif;font-size:1.8rem;font-weight:900;color:#00ff88;
           letter-spacing:4px;text-shadow:0 0 20px rgba(0,255,136,0.5);}
.hdr-sub{font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#5a7a9a;
         letter-spacing:2px;margin-top:4px;}
.conf-tag{display:inline-block;padding:3px 10px;border-radius:4px;font-size:0.75rem;
          font-family:Share Tech Mono,monospace;margin:2px;}
.conf-pos{background:rgba(0,255,136,0.15);border:1px solid #00ff88;color:#00ff88;}
.conf-neg{background:rgba(255,51,85,0.15);border:1px solid #ff3355;color:#ff3355;}
.alert-box{background:rgba(0,255,136,0.05);border:1px solid #00ff8855;
           border-radius:8px;padding:12px;margin:8px 0;font-family:Share Tech Mono,monospace;font-size:0.85rem;}
.sess-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px;}
.signal-tag{display:inline-block;padding:3px 8px;border-radius:4px;
            background:rgba(0,255,136,0.1);border:1px solid #00ff8844;
            color:#00ff88;font-size:0.78rem;margin:2px;}
</style>
""", unsafe_allow_html=True)


# ─── DATA SAHAM IDX ─────────────────────────────────────────────
# ========== DATA TINGKATAN SAHAM ==========
BLUE_CHIP_STOCKS = [
    'BBCA', 'BBRI', 'BMRI', 'BBNI', 'BTPS', 'BRIS',
    'TLKM', 'ISAT', 'EXCL', 'TOWR', 'MTEL',
    'UNVR', 'ICBP', 'INDF', 'KLBF', 'GGRM', 'HMSP',
    'ASII', 'UNTR', 'ADRO', 'BYAN', 'PTBA', 'ITMG',
    'CPIN', 'JPFA', 'MAIN', 'SIDO', 'ULTJ',
    'SMGR', 'INTP', 'SMCB',
    'PGAS', 'MEDC', 'ELSA',
    'ANTM', 'INCO', 'MDKA', 'HRUM', 'BRPT', 'TPIA',
    'WIKA', 'PTPP', 'WSKT', 'ADHI', 'JSMR',
]

SECOND_LINER_STOCKS = [
    'AKRA', 'INKP', 'BUMI', 'PTRO', 'DOID', 'TINS', 'BRMS', 'DKFT',
    'BMTR', 'MAPI', 'ERAA', 'ACES', 'MIKA', 'SILO', 'HEAL', 'PRAY',
    'CLEO', 'ROTI', 'MYOR', 'GOOD', 'SKBM', 'SKLT', 'STTP',
    'WSBP', 'PBSA', 'MTFN', 'BKSL', 'SMRA', 'CTRA', 'BSDE', 'PWON',
    'LPKR', 'LPCK', 'DILD', 'RDTX', 'MREI', 'PZZA', 'MAPB', 'DMAS',
    'LMPI', 'ARNA', 'TOTO', 'MLIA', 'INTD', 'IKAI', 'JECC', 'KBLI',
    'KBLM', 'VOKS', 'UNIT', 'INAI', 'IMPC', 'ASGR', 'POWR', 'RAJA',
    'PJAA', 'SAME', 'SCCO', 'SPMA', 'SRSN', 'TALF', 'TRST', 'TSPC',
    'UNIC', 'YPAS',
]

FCA_STOCKS = ['COIN', 'CDIA']

SHAREHOLDER_DATA = {
    'CUAN': {
        'pemegang': [
            {'nama': 'BPJS Ketenagakerjaan', 'persen': 1.02, 'tipe': 'Institusi', 'catatan': 'Masuk Q4 2025', 'update': 'Feb 2026'},
            {'nama': 'Vanguard', 'persen': 1.15, 'tipe': 'Asing', 'catatan': 'Nambah Jan 2026', 'update': 'Feb 2026'}
        ],
        'free_float': 13.73, 'total_shares': 12345678900,
        'insider_activity': [
            {'tanggal': '05 Mar 2026', 'insider': 'Direktur Utama', 'aksi': 'BELI', 'jumlah': 100000, 'harga': 15000},
            {'tanggal': '20 Feb 2026', 'insider': 'Komisaris', 'aksi': 'BELI', 'jumlah': 50000, 'harga': 14800}
        ]
    },
    'BRPT': {
        'pemegang': [{'nama': 'BPJS Ketenagakerjaan', 'persen': 1.22, 'tipe': 'Institusi', 'catatan': 'Nambah Feb 2026', 'update': 'Feb 2026'}],
        'free_float': 27.41, 'total_shares': 8765432100,
        'insider_activity': [{'tanggal': '28 Feb 2026', 'insider': 'Komisaris', 'aksi': 'JUAL', 'jumlah': 75000, 'harga': 8500}]
    },
    'TPIA': {
        'pemegang': [{'nama': 'GIC Singapore', 'persen': 3.45, 'tipe': 'Asing', 'catatan': 'Masuk Jan 2026', 'update': 'Feb 2026'}],
        'free_float': 91.52, 'total_shares': 1122334455, 'insider_activity': []
    },
    'TRIM': {
        'pemegang': [{'nama': 'BPJS Ketenagakerjaan', 'persen': 2.15, 'tipe': 'Institusi', 'catatan': 'Nambah Des 2025', 'update': 'Feb 2026'}],
        'free_float': 63.17, 'total_shares': 9988776655, 'insider_activity': []
    },
    'MDKA': {
        'pemegang': [
            {'nama': 'BPJS Ketenagakerjaan', 'persen': 2.15, 'tipe': 'Institusi', 'catatan': 'Nambah', 'update': 'Feb 2026'},
            {'nama': 'Pemerintah Norwegia', 'persen': 1.08, 'tipe': 'Asing', 'catatan': 'Masuk Q1 2026', 'update': 'Feb 2026'}
        ],
        'free_float': 89.31, 'total_shares': 8877665544,
        'insider_activity': [{'tanggal': '15 Feb 2026', 'insider': 'Dirut', 'aksi': 'BELI', 'jumlah': 200000, 'harga': 2500}]
    },
    'BBCA': {
        'pemegang': [
            {'nama': 'BPJS Ketenagakerjaan', 'persen': 1.06, 'tipe': 'Institusi', 'catatan': 'Nambah', 'update': 'Feb 2026'},
            {'nama': 'Vanguard', 'persen': 1.23, 'tipe': 'Asing', 'catatan': 'Nambah', 'update': 'Feb 2026'}
        ],
        'free_float': 95.67, 'total_shares': 123456789000,
        'insider_activity': [
            {'tanggal': '10 Mar 2026', 'insider': 'Presdir', 'aksi': 'BELI', 'jumlah': 1000000, 'harga': 10250},
            {'tanggal': '25 Feb 2026', 'insider': 'Komisaris', 'aksi': 'BELI', 'jumlah': 500000, 'harga': 10100}
        ]
    },
    'BBRI': {
        'pemegang': [{'nama': 'BPJS Ketenagakerjaan', 'persen': 1.09, 'tipe': 'Institusi', 'catatan': 'Nambah', 'update': 'Feb 2026'}],
        'free_float': 98.91, 'total_shares': 123456789000,
        'insider_activity': [{'tanggal': '09 Mar 2026', 'insider': 'Dirut', 'aksi': 'JUAL', 'jumlah': 50000, 'harga': 5800}]
    },
    'KLBF': {
        'pemegang': [
            {'nama': 'Pemerintah Norwegia', 'persen': 1.30, 'tipe': 'Asing', 'catatan': 'Nambah', 'update': 'Feb 2026'},
            {'nama': 'BPJS Ketenagakerjaan', 'persen': 2.01, 'tipe': 'Institusi', 'catatan': 'Nambah', 'update': 'Feb 2026'}
        ],
        'free_float': 96.69, 'total_shares': 5566778899, 'insider_activity': []
    },
    'ARTO': {
        'pemegang': [{'nama': 'Pemerintah Singapura', 'persen': 8.28, 'tipe': 'Asing', 'catatan': 'Masuk besar', 'update': 'Feb 2026'}],
        'free_float': 91.72, 'total_shares': 1122334455, 'insider_activity': []
    },
    'MTEL': {
        'pemegang': [{'nama': 'Pemerintah Singapura', 'persen': 5.33, 'tipe': 'Asing', 'catatan': 'Nambah', 'update': 'Feb 2026'}],
        'free_float': 94.67, 'total_shares': 2233445566, 'insider_activity': []
    }
}

# ========== HELPER FUNCTIONS ==========

def get_stock_level(stock_code):
    if stock_code in BLUE_CHIP_STOCKS:
        return '💎 Blue Chip'
    elif stock_code in SECOND_LINER_STOCKS:
        return '📈 Second Liner'
    else:
        return '🎯 Third Liner'

def get_stocks_by_level(levels):
    result = []
    if 'Blue Chip' in levels:
        result += BLUE_CHIP_STOCKS
    if 'Second Liner' in levels:
        result += SECOND_LINER_STOCKS
    if 'Third Liner' in levels or len(levels) == 0:
        third_liner = [s for s in STOCKS_LIST if s not in BLUE_CHIP_STOCKS and s not in SECOND_LINER_STOCKS]
        result += third_liner
    return list(set(result))

def is_fca(stock_code):
    return stock_code in FCA_STOCKS

def get_free_float_holders(stock_code):
    data = SHAREHOLDER_DATA.get(stock_code, {})
    return data.get('pemegang', [])

def get_free_float_value(stock_code):
    data = SHAREHOLDER_DATA.get(stock_code, {})
    return data.get('free_float', 100.0)

def get_insider_activity(stock_code):
    data = SHAREHOLDER_DATA.get(stock_code, {})
    return data.get('insider_activity', [])

def get_kategori_singkatan(kategori):
    singkatan = {
        'Ultra Low Float': 'ULF',
        'Very Low Float': 'VLF',
        'Low Float': 'LF',
        'Moderate Low Float': 'MLF',
        'Normal Float': 'NF'
    }
    return singkatan.get(kategori, kategori)

def analyze_goreng_potential(free_float):
    if free_float < 10:
        return '🔥 UT'
    elif free_float < 15:
        return '🔥 ST'
    elif free_float < 25:
        return '⚡ TG'
    elif free_float < 40:
        return '📊 SD'
    else:
        return '📉 RD'

def display_free_float_info(stock_code, free_float_value):
    free_float_holders = get_free_float_holders(stock_code)
    
    h = f"""
    <div style='background: linear-gradient(135deg, #0d1117 0%, #161b22 100%); 
                padding: 18px; border-radius: 12px; margin: 12px 0;
                border: 1px solid #30363d; box-shadow: 0 4px 24px rgba(0,0,0,0.4);'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 14px;'>
            <span style='width: 3px; height: 20px; background: linear-gradient(180deg, #00d4aa, #0099ff); 
                         border-radius: 2px; display: inline-block;'></span>
            <h4 style='color: #e6edf3; margin: 0; font-size: 0.95rem; letter-spacing: 0.5px; font-family: "JetBrains Mono", monospace;'>
                FREE FLOAT — {stock_code}
            </h4>
        </div>
    """
    
    if is_fca(stock_code):
        h += """
        <div style='background: rgba(255,170,0,0.1); border: 1px solid rgba(255,170,0,0.3); 
                    padding: 8px 12px; border-radius: 8px; margin-bottom: 12px;'>
            <span style='color: #ffaa00; font-size: 0.82rem; font-weight: 600; letter-spacing: 1px;'>
                ⚠ FCA — PAPAN PEMANTAUAN KHUSUS
            </span>
        </div>
        """
    
    h += f"""
    <div style='background: rgba(0, 212, 170, 0.08); border: 1px solid rgba(0, 212, 170, 0.2);
                padding: 10px 14px; border-radius: 8px; margin-bottom: 14px;
                display: flex; justify-content: space-between; align-items: center;'>
        <span style='color: #8b949e; font-size: 0.82rem; font-family: "JetBrains Mono", monospace;'>FREE FLOAT</span>
        <span style='color: #00d4aa; font-size: 1.4rem; font-weight: 700; font-family: "JetBrains Mono", monospace;'>{free_float_value:.2f}%</span>
    </div>
    """
    
    if free_float_holders:
        h += "<p style='color: #8b949e; font-size: 0.78rem; margin: 0 0 8px 0; letter-spacing: 1px; text-transform: uppercase; font-family: \"JetBrains Mono\", monospace;'>Pemegang Institusi / Asing &gt;1%</p>"
        total_dari_ff = 0
        
        for p in free_float_holders:
            persen_dalam_ff = (p['persen'] / free_float_value) * 100
            total_dari_ff += persen_dalam_ff
            
            color = '#4da6ff' if p['tipe'] == 'Institusi' else '#00d4aa'
            icon = '🏛' if p['tipe'] == 'Institusi' else '🌐'
            
            h += f"""
            <div style='display: flex; justify-content: space-between; align-items: center;
                        background: rgba(255,255,255,0.03); padding: 9px 12px; border-radius: 7px; 
                        margin: 5px 0; border-left: 2px solid {color};'>
                <div>
                    <span style='color: #c9d1d9; font-size: 0.85rem;'>{icon} {p['nama']}</span>
                    <span style='color: #484f58; font-size: 0.75rem; margin-left: 8px;'>{p['catatan']}</span>
                </div>
                <span style='color: {color}; font-weight: 700; font-size: 0.95rem; font-family: "JetBrains Mono", monospace;'>{persen_dalam_ff:.1f}%</span>
            </div>
            """
        
        sisa_ritel = 100 - total_dari_ff
        h += f"""
        <div style='display: flex; justify-content: space-between; align-items: center;
                    background: rgba(0,212,170,0.06); padding: 9px 12px; border-radius: 7px; 
                    margin: 5px 0; border-left: 2px solid #00d4aa;'>
            <span style='color: #c9d1d9; font-size: 0.85rem;'>👥 Ritel</span>
            <span style='color: #00d4aa; font-weight: 700; font-size: 0.95rem; font-family: "JetBrains Mono", monospace;'>{sisa_ritel:.1f}%</span>
        </div>
        """
    else:
        h += """
        <div style='text-align: center; padding: 16px; color: #484f58; font-size: 0.85rem;'>
            Tidak ada institusi/asing &gt;1%
        </div>
        <div style='display: flex; justify-content: space-between; align-items: center;
                    background: rgba(0,212,170,0.06); padding: 9px 12px; border-radius: 7px; border-left: 2px solid #00d4aa;'>
            <span style='color: #c9d1d9; font-size: 0.85rem;'>👥 Ritel</span>
            <span style='color: #00d4aa; font-weight: 700; font-family: "JetBrains Mono", monospace;'>100%</span>
        </div>
        """
    
    insider = get_insider_activity(stock_code)
    if insider:
        h += "<p style='color: #8b949e; font-size: 0.78rem; margin: 16px 0 8px 0; letter-spacing: 1px; text-transform: uppercase; font-family: \"JetBrains Mono\", monospace;'>Aktivitas Insider — 30 Hari</p>"
        for a in insider:
            is_buy = a['aksi'] == 'BELI'
            color = '#00d4aa' if is_buy else '#ff5c5c'
            icon = '▲' if is_buy else '▼'
            h += f"""
            <div style='display: flex; justify-content: space-between; align-items: center;
                        background: rgba(255,255,255,0.03); padding: 9px 12px; border-radius: 7px; margin: 5px 0;'>
                <div>
                    <span style='color: #8b949e; font-size: 0.78rem; font-family: "JetBrains Mono", monospace;'>{a['tanggal']}</span>
                    <span style='color: #484f58; font-size: 0.78rem; margin-left: 8px;'>{a['insider']}</span>
                </div>
                <span style='color: {color}; font-weight: 700; font-size: 0.85rem; font-family: "JetBrains Mono", monospace;'>
                    {icon} {a['aksi']} {a['jumlah']:,}
                </span>
            </div>
            """
    
    h += "</div>"
    return h

def create_download_buttons(data, prefix, key_suffix):
    col1, col2 = st.columns(2)
    with col1:
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name=f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True,
            key=f"csv_{key_suffix}"
        )
    with col2:
        excel = export_to_excel(data)
        if excel:
            st.download_button(
                label="⬇ Download Excel",
                data=excel,
                file_name=f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"excel_{key_suffix}"
            )

def scan_stocks_parallel(stocks_to_scan, scan_function, *args, **kwargs):
    results = []
    failed_stocks = []
    
    with st.spinner(f"Memproses {len(stocks_to_scan)} saham..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_stock = {
                executor.submit(scan_function, stock, *args, **kwargs): stock 
                for stock in stocks_to_scan
            }
            
            completed = 0
            total = len(future_to_stock)
            
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                completed += 1
                
                try:
                    result = future.result(timeout=30)
                    if result:
                        results.append(result)
                except Exception as e:
                    failed_stocks.append(stock)
                
                progress = completed / total
                progress_bar.progress(progress)
                status_text.markdown(
                    f"<span style='color:#00d4aa; font-family:monospace; font-size:0.85rem;'>✓ {completed}/{total} diproses &nbsp;|&nbsp; ✗ {len(failed_stocks)} gagal</span>",
                    unsafe_allow_html=True
                )
        
        progress_bar.empty()
        status_text.empty()
        
        if failed_stocks:
            st.warning(f"{len(failed_stocks)} saham gagal: {', '.join(failed_stocks[:10])}" + 
                      ("..." if len(failed_stocks) > 10 else ""))
    
    return results

def reset_session_data():
    keys_to_reset = ['scan_results', 'enhanced_df', 'watchlist_df', 'display_df', 'df_results']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

# ─── ENGINE AKSARA IDX v2.0 (ALL_TICKERS + functions) ──────────

# ============================================================
# DATA SAHAM IDX (956 SAHAM)
# ============================================================
ALL_TICKERS = [
    "AALI","ABBA","ABDA","ABMM","ACES","ACST","ADES","ADHI","AISA","AKKU",
    "AKPI","AKRA","AKSI","ALDO","ALKA","ALMI","ALTO","AMAG","AMFG","AMIN",
    "AMRT","ANJT","ANTM","APEX","APIC","APII","APLI","APLN","ARGO","ARII",
    "ARNA","ARTA","ARTI","ARTO","ASBI","ASDM","ASGR","ASII","ASJT","ASMI",
    "ASRI","ASRM","ASSA","ATIC","AUTO","BABP","BACA","BAJA","BALI","BAPA",
    "BATA","BAYU","BBCA","BBHI","BBKP","BBLD","BBMD","BBNI","BBRI","BBRM",
    "BBTN","BBYB","BCAP","BCIC","BCIP","BDMN","BEKS","BEST","BFIN","BGTG",
    "BHIT","BIKA","BIMA","BINA","BIPI","BIPP","BIRD","BISI","BJBR","BJTM",
    "BKDP","BKSL","BKSW","BLTA","BLTZ","BMAS","BMRI","BMSR","BMTR","BNBA",
    "BNBR","BNGA","BNII","BNLI","BOLT","BPFI","BPII","BRAM","BRMS","BRNA",
    "BRPT","BSDE","BSIM","BSSR","BSWD","BTEK","BTEL","BTON","BTPN","BUDI",
    "BUKK","BULL","BUMI","BUVA","BVIC","BWPT","BYAN","CANI","CASS","CEKA",
    "CENT","CFIN","CINT","CITA","CLPI","CMNP","CMPP","CNKO","CNTX","COWL",
    "CPIN","CPRO","CSAP","CTBN","CTRA","CTTH","DART","DEFI","DEWA","DGIK",
    "DILD","DKFT","DLTA","DMAS","DNAR","DNET","DOID","DPNS","DSFI","DSNG",
    "DSSA","DUTI","DVLA","DYAN","ECII","EKAD","ELSA","ELTY","EMDE","EMTK",
    "ENRG","EPMT","ERAA","ERTX","ESSA","ESTI","ETWA","EXCL","FAST","FASW",
    "FISH","FMII","FORU","FPNI","GAMA","GDST","GDYR","GEMA","GEMS","GGRM",
    "GIAA","GJTL","GLOB","GMTD","GOLD","GOLL","GPRA","GSMF","GTBO","GWSA",
    "GZCO","HADE","HDFA","HERO","HEXA","HITS","HMSP","HOME","HOTL","HRUM",
    "IATA","IBFN","IBST","ICBP","ICON","IGAR","IIKP","IKAI","IKBI","IMAS",
    "IMJS","IMPC","INAF","INAI","INCI","INCO","INDF","INDR","INDS","INDX",
    "INDY","INKP","INPC","INPP","INRU","INTA","INTD","INTP","IPOL","ISAT",
    "ISSP","ITMA","ITMG","JAWA","JECC","JIHD","JKON","JPFA","JRPT","JSMR",
    "JSPT","JTPE","KAEF","KARW","KBLI","KBLM","KBLV","KBRI","KDSI","KIAS",
    "KICI","KIJA","KKGI","KLBF","KOBX","KOIN","KONI","KOPI","KPIG","KRAS",
    "KREN","LAPD","LCGP","LEAD","LINK","LION","LMAS","LMPI","LMSH","LPCK",
    "LPGI","LPIN","LPKR","LPLI","LPPF","LPPS","LRNA","LSIP","LTLS","MAGP",
    "MAIN","MAPI","MAYA","MBAP","MBSS","MBTO","MCOR","MDIA","MDKA","MDLN",
    "MDRN","MEDC","MEGA","MERK","META","MFMI","MGNA","MICE","MIDI","MIKA",
    "MIRA","MITI","MKPI","MLBI","MLIA","MLPL","MLPT","MMLP","MNCN","MPMX",
    "MPPA","MRAT","MREI","MSKY","MTDL","MTFN","MTLA","MTSM","MYOH","MYOR",
    "MYTX","NELY","NIKL","NIRO","NISP","NOBU","NRCA","OCAP","OKAS","OMRE",
    "PADI","PALM","PANR","PANS","PBRX","PDES","PEGE","PGAS","PGLI","PICO",
    "PJAA","PKPK","PLAS","PLIN","PNBN","PNBS","PNIN","PNLF","PSAB","PSDN",
    "PSKT","PTBA","PTIS","PTPP","PTRO","PTSN","PTSP","PUDP","PWON","PYFA",
    "RAJA","RALS","RANC","RBMS","RDTX","RELI","RICY","RIGS","RIMO","RODA",
    "ROTI","RUIS","SAFE","SAME","SCCO","SCMA","SCPI","SDMU","SDPC","SDRA",
    "SGRO","SHID","SIDO","SILO","SIMA","SIMP","SIPD","SKBM","SKLT","SKYB",
    "SMAR","SMBR","SMCB","SMDM","SMDR","SMGR","SMMA","SMMT","SMRA","SMRU",
    "SMSM","SOCI","SONA","SPMA","SQMI","SRAJ","SRIL","SRSN","SRTG","SSIA",
    "SSMS","SSTM","STAR","STTP","SUGI","SULI","SUPR","TALF","TARA","TAXI",
    "TBIG","TBLA","TBMS","TCID","TELE","TFCO","TGKA","TIFA","TINS","TIRA",
    "TIRT","TKIM","TLKM","TMAS","TMPO","TOBA","TOTL","TOTO","TOWR","TPIA",
    "TPMA","TRAM","TRIL","TRIM","TRIO","TRIS","TRST","TRUS","TSPC","ULTJ",
    "UNIC","UNIT","UNSP","UNTR","UNVR","VICO","VINS","VIVA","VOKS","VRNA",
    "WAPO","WEHA","WICO","WIIM","WIKA","WINS","WOMF","WSKT","WTON","YPAS",
    "YULE","ZBRA","SHIP","CASA","DAYA","DPUM","IDPR","JGLE","KINO","MARI",
    "MKNT","MTRA","OASA","POWR","INCF","WSBP","PBSA","PRDA","BOGA","BRIS",
    "PORT","CARS","MINA","CLEO","TAMU","CSIS","TGRA","FIRE","TOPS","KMTR",
    "ARMY","MAPB","WOOD","HRTA","MABA","HOKI","MPOW","MARK","NASA","MDKI",
    "BELL","KIOS","GMFI","MTWI","ZINC","MCAS","PPRE","WEGE","PSSI","MORA",
    "DWGL","PBID","JMAS","CAMP","IPCM","PCAR","LCKM","BOSS","HELI","JSKY",
    "INPS","GHON","TDPM","DFAM","NICK","BTPS","SPTO","PRIM","HEAL","TRUK",
    "PZZA","TUGU","MSIN","SWAT","TNCA","MAPA","TCPI","IPCC","RISE","BPTR",
    "POLL","NFCX","MGRO","NUSA","FILM","ANDI","LAND","MOLI","PANI","DIGI",
    "CITY","SAPX","SURE","HKMU","MPRO","DUCK","GOOD","SKRN","YELO","CAKK",
    "SATU","SOSS","DEAL","POLA","DIVA","LUCK","URBN","SOTS","ZONE","PEHA",
    "FOOD","BEEF","POLI","CLAY","NATO","JAYA","COCO","MTPS","CPRI","HRME",
    "POSA","JAST","FITT","BOLA","CCSI","SFAN","POLU","KJEN","KAYU","ITIC",
    "PAMG","IPTV","BLUE","ENVY","EAST","LIFE","FUJI","KOTA","INOV","ARKA",
    "SMKL","HDIT","KEEN","BAPI","TFAS","GGRP","OPMS","NZIA","SLIS","PURE",
    "IRRA","DMMX","SINI","WOWS","ESIP","TEBE","KEJU","PSGO","AGAR","IFSH",
    "REAL","IFII","PMJS","UCID","GLVA","PGJO","AMAR","CSRA","INDO","AMOR",
    "TRIN","DMND","PURA","PTPW","TAMA","IKAN","SAMF","SBAT","KBAG","CBMF",
    "RONY","CSMI","BBSS","BHAT","CASH","TECH","EPAC","UANG","PGUN","SOFA",
    "PPGL","TOYS","SGER","TRJA","PNGO","SCNP","BBSI","KMDS","PURI","SOHO",
    "HOMI","ROCK","ENZO","PLAN","PTDU","ATAP","VICI","PMMP","BANK","WMUU",
    "EDGE","UNIQ","BEBS","SNLK","ZYRX","LFLO","FIMP","TAPG","NPGF","LUCY",
    "ADCP","HOPE","MGLV","TRUE","LABA","ARCI","IPAC","MASB","BMHS","FLMC",
    "NICL","UVCR","BUKA","HAIS","OILS","GPSO","MCOL","RSGK","RUNS","SBMA",
    "CMNT","GTSI","IDEA","KUAS","BOBA","MTEL","DEPO","BINO","CMRY","WGSH",
    "TAYS","WMPP","RMKE","OBMD","AVIA","IPPE","NASI","BSML","DRMA","ADMR",
    "SEMA","ASLC","NETV","BAUT","ENAK","NTBK","SMKM","STAA","NANO","BIKE",
    "WIRG","SICO","GOTO","TLDN","MTMH","WINR","IBOS","OLIV","ASHA","SWID",
    "TRGU","ARKO","CHEM","DEWI","AXIO","KRYA","HATM","RCCC","GULA","JARR",
    "AMMS","RAFI","KKES","ELPI","EURO","KLIN","TOOL","BUAH","CRAB","MEDS",
    "COAL","PRAY","CBUT","BELI","MKTR","OMED","BSBK","PDPP","KDTN","ZATA",
    "NINE","MMIX","PADA","ISAP","VTNY","SOUL","ELIT","BEER","CBPE","SUNI",
    "CBRE","WINE","BMBL","PEVE","LAJU","FWCT","NAYZ","IRSX","PACK","VAST",
    "CHIP","HALO","KING","PGEO","FUTR","HILL","BDKR","PTMP","SAGE","TRON",
    "CUAN","NSSS","GTRA","HAJJ","JATI","TYRE","MPXL","SMIL","KLAS","MAXI",
    "VKTR","RELF","AMMN","CRSN","GRPM","WIDI","TGUK","INET","MAHA","RMKO",
    "CNMA","FOLK","HBAT","GRIA","PPRI","ERAL","CYBR","MUTU","LMAX","HUMI",
    "MSIE","RSCH","BABY","AEGS","IOTF","KOCI","PTPS","BREN","STRK","KOKA",
    "LOPI","UDNG","RGAS","MSTI","IKPM","AYAM","SURI","ASLI","GRPH","SMGA",
    "UNTD","TOSK","MPIX","ALII","MKAP","MEJA","LIVE","HYGN","BAIK","VISI",
    "AREA","MHKI","ATLA","DATA","SOLA","BATR","SPRE","PART","GOLF","ISEA",
    "BLES","GUNA","LABS","DOSS","NEST","PTMR","VERN","DAAZ","BOAT","NAIK",
    "AADI","MDIY","KSIX","RATU","YOII","HGII","BRRC","DGWG","CBDK","OBAT",
    "MINE","ASPR","PSAT","COIN","CDIA","BLOG","MERI","CHEK","PMUI","EMAS",
    "PJHB","RLCO","SUPA","KAQI","YUPI","FORE","MDLA","DKHH","AYLS","DADA",
    "ASPI","ESTA","BESS","AMAN","CARE","PIPA","NCKL","MENN","AWAN","MBMA",
    "RAAM","DOOH","CGAS","NICE","MSJA","SMLE","ACRO","MANG","WIFI","FAPA",
    "DCII","KETR","DGNS","UFOE","ADMF","ADMG","ADRO","AGII","AGRO","AGRS",
    "AHAP","AIMS","PNSE","POLY","POOL","PPRO",
]

# ============================================================
# SECTOR MAPPING
# ============================================================
SECTOR_MAP = {
    "BBCA":"Banking","BBRI":"Banking","BMRI":"Banking","BBNI":"Banking","BBTN":"Banking",
    "BJTM":"Banking","BJBR":"Banking","BDMN":"Banking","NISP":"Banking","PNBN":"Banking",
    "BNGA":"Banking","BTPN":"Banking","MAYA":"Banking","BNLI":"Banking","AGRO":"Banking",
    "MEGA":"Banking","BRIS":"Banking","BTPS":"Banking","BBYB":"Banking","NOBU":"Banking",
    "TLKM":"Telecom","EXCL":"Telecom","ISAT":"Telecom","TBIG":"Telecom","TOWR":"Telecom",
    "LINK":"Telecom","SUPR":"Telecom","MTEL":"Telecom","WIFI":"Telecom",
    "ANTM":"Mining","PTBA":"Mining","ADRO":"Mining","ITMG":"Mining","INCO":"Mining",
    "MDKA":"Mining","BUMI":"Mining","BSSR":"Mining","GEMS":"Mining","HRUM":"Mining",
    "KKGI":"Mining","MYOH":"Mining","TOBA":"Mining","BYAN":"Mining","INDY":"Mining",
    "ZINC":"Mining","COAL":"Mining","MBAP":"Mining","PTRO":"Mining","TINS":"Mining",
    "NICL":"Mining","NCKL":"Mining","AMMN":"Mining","MBMA":"Mining","PGEO":"Mining",
    "CUAN":"Mining","BREN":"Mining",
    "ASII":"Automotive","UNTR":"Automotive","AUTO":"Automotive","IMAS":"Automotive",
    "GJTL":"Automotive","SMSM":"Automotive","BOLT":"Automotive","BRAM":"Automotive",
    "UNVR":"Consumer","ICBP":"Consumer","KLBF":"Consumer","HMSP":"Consumer","GGRM":"Consumer",
    "INDF":"Consumer","SIDO":"Consumer","MYOR":"Consumer","ROTI":"Consumer","ULTJ":"Consumer",
    "DLTA":"Consumer","MLBI":"Consumer","CPIN":"Consumer","JPFA":"Consumer","GOOD":"Consumer",
    "KEJU":"Consumer","TSPC":"Consumer","WIIM":"Consumer","CLEO":"Consumer","HOKI":"Consumer",
    "STTP":"Consumer","DVLA":"Consumer","KAEF":"Consumer","MERK":"Consumer","FOOD":"Consumer",
    "BEEF":"Consumer","COCO":"Consumer","DMND":"Consumer","CAMP":"Consumer","FAST":"Consumer",
    "BSDE":"Property","PWON":"Property","CTRA":"Property","SMRA":"Property","ASRI":"Property",
    "BEST":"Property","DILD":"Property","JRPT":"Property","KIJA":"Property","LPKR":"Property",
    "MKPI":"Property","MTLA":"Property","RDTX":"Property","DART":"Property","BKSL":"Property",
    "EMDE":"Property","GPRA":"Property","PPRO":"Property","DMAS":"Property","CITY":"Property",
    "JSMR":"Infrastructure","WIKA":"Infrastructure","WSKT":"Infrastructure","PTPP":"Infrastructure",
    "ADHI":"Infrastructure","NRCA":"Infrastructure","TOTL":"Infrastructure","WTON":"Infrastructure",
    "ACST":"Infrastructure","POWR":"Infrastructure","WSBP":"Infrastructure","WEGE":"Infrastructure",
    "PGAS":"Energy","MEDC":"Energy","BRPT":"Energy","TPIA":"Energy","ELSA":"Energy",
    "ENRG":"Energy","ESSA":"Energy","FIRE":"Energy",
    "AALI":"Agriculture","LSIP":"Agriculture","SGRO":"Agriculture","SSMS":"Agriculture",
    "BWPT":"Agriculture","DSNG":"Agriculture","PALM":"Agriculture","SIMP":"Agriculture",
    "ACES":"Retail","MAPI":"Retail","ERAA":"Retail","LPPF":"Retail","RALS":"Retail","KINO":"Retail",
    "MNCN":"Media","SCMA":"Media","EMTK":"Media",
    "GIAA":"Transport","BIRD":"Transport","ASSA":"Transport","SHIP":"Transport",
    "TMAS":"Transport","SMDR":"Shipping","MBSS":"Shipping","PORT":"Transport",
    "INTP":"Manufacturing","SMGR":"Manufacturing","AMFG":"Manufacturing","ARNA":"Manufacturing",
    "AKPI":"Manufacturing","INKP":"Manufacturing","TKIM":"Manufacturing","ISSP":"Manufacturing",
    "KBLI":"Manufacturing","SCCO":"Manufacturing","WOOD":"Manufacturing","SRIL":"Manufacturing",
    "GOTO":"Technology","BUKA":"Technology","DCII":"Technology","MTDL":"Technology","CHIP":"Technology",
}

# Representatif per sektor untuk hitung Sector Momentum
SECTOR_REPRESENTATIVES = {
    "Banking":        ["BBCA","BBRI","BMRI","BBNI","BBTN"],
    "Telecom":        ["TLKM","EXCL","ISAT","TBIG","TOWR"],
    "Mining":         ["ANTM","PTBA","ADRO","ITMG","MDKA"],
    "Automotive":     ["ASII","UNTR","AUTO"],
    "Consumer":       ["UNVR","ICBP","KLBF","INDF","MYOR"],
    "Property":       ["BSDE","PWON","CTRA","SMRA"],
    "Infrastructure": ["JSMR","WIKA","WSKT","PTPP"],
    "Energy":         ["PGAS","MEDC","BRPT","TPIA"],
    "Agriculture":    ["AALI","LSIP","SGRO"],
    "Retail":         ["ACES","MAPI","ERAA"],
    "Media":          ["MNCN","SCMA","EMTK"],
    "Technology":     ["GOTO","BUKA","DCII"],
    "Manufacturing":  ["INTP","SMGR","INKP","TKIM"],
}

def get_sector(ticker):
    return SECTOR_MAP.get(ticker, "Other")

# ============================================================
# MARKET STATUS
# ============================================================
def get_market_status():
    wib = pytz.timezone("Asia/Jakarta")
    now = datetime.now(wib)
    wd = now.weekday()
    t = now.time()
    open_t = dtime(9, 0)
    close_t = dtime(15, 30)
    pre_t = dtime(8, 45)

    if wd >= 5:
        return {"status_text": "🔴 MARKET TUTUP", "status_color": "#ff4444",
                "info_text": "Buka Senin 09:00 WIB", "is_open": False,
                "time_str": now.strftime("%H:%M:%S"), "date_str": now.strftime("%d %b %Y"),
                "day_name": now.strftime("%A")}
    elif t < pre_t:
        return {"status_text": "⏳ PRE-MARKET", "status_color": "#ffd700",
                "info_text": "Buka pukul 09:00 WIB", "is_open": False,
                "time_str": now.strftime("%H:%M:%S"), "date_str": now.strftime("%d %b %Y"),
                "day_name": now.strftime("%A")}
    elif pre_t <= t < open_t:
        return {"status_text": "🟡 PRE-OPENING", "status_color": "#ffd700",
                "info_text": "Sesi pra-buka", "is_open": False,
                "time_str": now.strftime("%H:%M:%S"), "date_str": now.strftime("%d %b %Y"),
                "day_name": now.strftime("%A")}
    elif open_t <= t <= close_t:
        return {"status_text": "🟢 MARKET BUKA", "status_color": "#00ff88",
                "info_text": "Sesi reguler aktif", "is_open": True,
                "time_str": now.strftime("%H:%M:%S"), "date_str": now.strftime("%d %b %Y"),
                "day_name": now.strftime("%A")}
    else:
        return {"status_text": "🔴 MARKET TUTUP", "status_color": "#ff4444",
                "info_text": "Buka besok 09:00 WIB", "is_open": False,
                "time_str": now.strftime("%H:%M:%S"), "date_str": now.strftime("%d %b %Y"),
                "day_name": now.strftime("%A")}

# ============================================================
# ✅ FIX: RSI dengan WILDER'S SMOOTHING METHOD (lebih akurat)
# ============================================================
def calc_rsi_wilder(prices, period=14):
    """
    RSI menggunakan Wilder's Smoothing (Exponential Moving Average).
    Ini adalah metode standar yang digunakan TradingView, MetaTrader, dll.
    """
    if len(prices) < period + 1:
        return 50.0
    prices = np.array(prices, dtype=float)
    deltas = np.diff(prices)
    gains  = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)

    # Hitung average gain/loss awal (simple average untuk 'period' periode pertama)
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    # Wilder's Smoothing: EMA dengan alpha = 1/period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)

# ============================================================
# ✅ FIX: MACD dengan EMA dari full series (lebih akurat)
# ============================================================
def calc_ema_series(prices, period):
    """Hitung EMA dari seluruh series — BUKAN hanya window terakhir."""
    prices = np.array(prices, dtype=float)
    if len(prices) < period:
        return np.array([np.mean(prices)] * len(prices))
    k = 2.0 / (period + 1)
    ema = np.zeros(len(prices))
    # Seed dengan SMA dari 'period' bar pertama
    ema[period - 1] = np.mean(prices[:period])
    for i in range(period, len(prices)):
        ema[i] = prices[i] * k + ema[i - 1] * (1 - k)
    # Isi sebelum period dengan NaN untuk kejelasan, tapi return nilai valid
    ema[:period - 1] = ema[period - 1]
    return ema

def calc_macd_full(prices):
    """
    MACD menggunakan EMA dari full series.
    Return: (macd_value, signal_value, histogram_value)
    """
    if len(prices) < 26:
        return 0.0, 0.0, 0.0
    prices = np.array(prices, dtype=float)
    ema12 = calc_ema_series(prices, 12)
    ema26 = calc_ema_series(prices, 26)
    macd_line = ema12 - ema26
    # Signal line = EMA9 dari MACD line
    signal_line = calc_ema_series(macd_line, 9)
    histogram = macd_line - signal_line
    return round(float(macd_line[-1]), 4), round(float(signal_line[-1]), 4), round(float(histogram[-1]), 4)

def calc_bb(prices, period=20):
    if len(prices) < period:
        return 50.0, 0.0, 0.0
    sl = np.array(prices[-period:])
    m, s = np.mean(sl), np.std(sl)
    u, l = m + 2 * s, m - 2 * s
    pos = (prices[-1] - l) / (u - l) * 100 if (u - l) > 0 else 50
    return round(max(0, min(100, pos)), 1), round(u, 0), round(l, 0)

def calc_stoch(prices, highs, lows, period=14):
    if len(prices) < 3:
        return 50.0, 50.0
    period = min(period, len(prices))
    try:
        hh = max(highs[-period:]) if highs[-period:] else prices[-1]
        ll = min(lows[-period:]) if lows[-period:] else prices[-1]
        if hh == ll:
            return 50.0, 50.0
        k = round((prices[-1] - ll) / (hh - ll) * 100, 1)
        kv = []
        for i in range(min(3, len(prices))):
            idx = -(i + 1)
            p2 = min(period, len(prices) + idx)
            if p2 < 1:
                continue
            hs = [x for x in highs[max(0, len(highs) + idx - p2):len(highs) + idx] if x]
            ls = [x for x in lows[max(0, len(lows) + idx - p2):len(lows) + idx] if x]
            if not hs or not ls:
                continue
            hi, li = max(hs), min(ls)
            kv.append(50.0 if hi == li else (prices[idx] - li) / (hi - li) * 100)
        d = float(sum(kv) / len(kv)) if kv else k
        return k, round(d, 1)
    except:
        return 50.0, 50.0

def calc_adx(highs, lows, closes, period=14):
    try:
        if len(closes) < period + 1:
            return 20.0
        tr, pdm, ndm = [], [], []
        for i in range(1, len(closes)):
            h, l, pc = highs[i], lows[i], closes[i - 1]
            tr.append(max(h - l, abs(h - pc), abs(l - pc)))
            up_move = h - highs[i - 1]
            down_move = lows[i - 1] - l
            pdm.append(up_move if up_move > down_move and up_move > 0 else 0)
            ndm.append(down_move if down_move > up_move and down_move > 0 else 0)
        if len(tr) < period:
            return 20.0
        trs = np.convolve(tr, np.ones(period) / period, mode='valid')
        ps  = np.convolve(pdm, np.ones(period) / period, mode='valid')
        ns  = np.convolve(ndm, np.ones(period) / period, mode='valid')
        if len(trs) == 0:
            return 20.0
        pdi = ps / (trs + 0.001) * 100
        ndi = ns / (trs + 0.001) * 100
        dx  = np.abs(pdi - ndi) / (pdi + ndi + 0.001) * 100
        return round(float(np.mean(dx[-period:])), 1)
    except:
        return 20.0

def get_sr(highs, lows, closes, n=20):
    try:
        ls = [x for x in lows[-n:]  if x > 0]
        hs = [x for x in highs[-n:] if x > 0]
        if not ls or not hs:
            return None, None
        return round(float(np.mean(sorted(ls)[:5])), 0), round(float(np.mean(sorted(hs)[-5:])), 0)
    except:
        return None, None

# ============================================================
# ✅ NEW: RELATIVE STRENGTH vs IHSG
# ============================================================
@st.cache_data(ttl=3600, show_spinner=False)
def get_ihsg_data(period="6mo"):
    """Ambil data IHSG (^JKSE) sebagai benchmark."""
    try:
        df = yf.download("^JKSE", period=period, interval="1d",
                         auto_adjust=True, progress=False)
        if df is None or len(df) < 20:
            return None
        return df["Close"].tolist()
    except:
        return None

def calc_relative_strength(stock_closes, ihsg_closes):
    """
    Hitung Relative Strength saham vs IHSG.
    RS > 1 = outperform IHSG (saham lebih kuat dari market)
    RS < 1 = underperform IHSG
    RS_Score = 0-100 (normalized, >50 berarti outperform)
    """
    try:
        if not stock_closes or not ihsg_closes or len(stock_closes) < 20:
            return {"rs_ratio": 1.0, "rs_score": 50.0, "rs_trend": "NEUTRAL",
                    "outperform": False, "rs_1m": 0.0, "rs_3m": 0.0}

        # Ambil periode yang sama
        min_len = min(len(stock_closes), len(ihsg_closes))
        sc = np.array(stock_closes[-min_len:], dtype=float)
        ic = np.array(ihsg_closes[-min_len:], dtype=float)

        # RS Ratio: performa relatif
        rs_ratio = (sc[-1] / sc[0]) / (ic[-1] / ic[0]) if ic[0] > 0 and sc[0] > 0 else 1.0

        # RS 1 bulan (20 hari trading)
        n1m = min(20, min_len - 1)
        rs_1m = ((sc[-1] / sc[-n1m]) / (ic[-1] / ic[-n1m]) - 1) * 100 if ic[-n1m] > 0 else 0

        # RS 3 bulan (60 hari trading)
        n3m = min(60, min_len - 1)
        rs_3m = ((sc[-1] / sc[-n3m]) / (ic[-1] / ic[-n3m]) - 1) * 100 if ic[-n3m] > 0 else 0

        # RS Score (normalized 0-100, 50 = sama dengan IHSG)
        rs_score = min(100, max(0, 50 + (rs_ratio - 1) * 50))

        # Trend: apakah RS sedang naik atau turun
        if min_len >= 10:
            rs_recent = (sc[-1] / sc[-5]) / (ic[-1] / ic[-5]) if ic[-5] > 0 else 1.0
            rs_prev   = (sc[-5] / sc[-10]) / (ic[-5] / ic[-10]) if ic[-10] > 0 else 1.0
            if rs_recent > rs_prev * 1.01:
                rs_trend = "IMPROVING"
            elif rs_recent < rs_prev * 0.99:
                rs_trend = "WEAKENING"
            else:
                rs_trend = "STABLE"
        else:
            rs_trend = "STABLE"

        return {
            "rs_ratio":    round(float(rs_ratio), 3),
            "rs_score":    round(float(rs_score), 1),
            "rs_trend":    rs_trend,
            "outperform":  rs_score > 55,   # butuh >55 untuk dianggap outperform (bukan cuma ratio >1.0)
            "rs_1m":       round(float(rs_1m), 2),
            "rs_3m":       round(float(rs_3m), 2),
        }
    except Exception as e:
        return {"rs_ratio": 1.0, "rs_score": 50.0, "rs_trend": "NEUTRAL",
                "outperform": False, "rs_1m": 0.0, "rs_3m": 0.0}

# ============================================================
# ✅ NEW: SECTOR MOMENTUM ANALYSIS
# ============================================================
@st.cache_data(ttl=1800, show_spinner=False)
def get_sector_momentum():
    """
    Hitung momentum sektor berdasarkan performa rata-rata saham representatif.
    Return dict: {sector_name: {score, change_1w, change_1m, trend, rank}}
    """
    sector_data = {}
    for sector, tickers in SECTOR_REPRESENTATIVES.items():
        try:
            symbols = [t + ".JK" for t in tickers]
            raw = yf.download(
                " ".join(symbols), period="3mo", interval="1d",
                group_by="ticker", auto_adjust=True, progress=False, threads=True
            )
            changes_1w, changes_1m = [], []
            for ticker, symbol in zip(tickers, symbols):
                try:
                    if len(symbols) > 1 and symbol in raw.columns.get_level_values(0):
                        df = raw[symbol].dropna()
                    else:
                        df = raw.dropna()
                    if len(df) < 5:
                        continue
                    closes = df["Close"].tolist()
                    # 1 week (5 trading days)
                    if len(closes) >= 6:
                        changes_1w.append((closes[-1] - closes[-6]) / closes[-6] * 100)
                    # 1 month (20 trading days)
                    if len(closes) >= 21:
                        changes_1m.append((closes[-1] - closes[-21]) / closes[-21] * 100)
                except:
                    continue

            if changes_1w:
                avg_1w = np.mean(changes_1w)
                avg_1m = np.mean(changes_1m) if changes_1m else avg_1w
                # Momentum score 0-100
                score = min(100, max(0, 50 + avg_1w * 3 + avg_1m * 1.5))
                trend = "HOT 🔥" if avg_1w > 2 else "BULLISH 📈" if avg_1w > 0.5 else \
                        "BEARISH 📉" if avg_1w < -1 else "NEUTRAL ➡️"
                sector_data[sector] = {
                    "score":     round(score, 1),
                    "change_1w": round(avg_1w, 2),
                    "change_1m": round(avg_1m, 2),
                    "trend":     trend,
                }
            else:
                sector_data[sector] = {"score": 50, "change_1w": 0, "change_1m": 0, "trend": "N/A"}
        except Exception as e:
            sector_data[sector] = {"score": 50, "change_1w": 0, "change_1m": 0, "trend": "N/A"}
        time.sleep(0.2)

    # Rank sektor
    sorted_sectors = sorted(sector_data.items(), key=lambda x: x[1]["score"], reverse=True)
    for rank, (sec, _) in enumerate(sorted_sectors, 1):
        sector_data[sec]["rank"] = rank

    return sector_data

# ============================================================
# ✅ NEW: FOREIGN FLOW REAL dari RTI Business
# ============================================================
@st.cache_data(ttl=900, show_spinner=False)
def fetch_foreign_flow_rti():
    """
    Ambil data Foreign Net Buy/Sell dari RTI Business (sumber publik gratis).
    Return dict: {ticker: {net_buy, net_sell, net_flow, rank}}
    """
    result = {}
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*",
            "Referer": "https://www.rti.co.id/",
        }
        # RTI endpoint untuk foreign flow top stocks
        url = "https://www.rti.co.id/api/market/foreignflow"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            try:
                data = resp.json()
                if isinstance(data, list):
                    for item in data:
                        ticker = str(item.get("StockCode", "")).strip()
                        if ticker:
                            result[ticker] = {
                                "net_flow":    float(item.get("NetBuy", 0)),
                                "foreign_buy": float(item.get("ForeignBuy", 0)),
                                "foreign_sell":float(item.get("ForeignSell", 0)),
                                "source":      "rti_real",
                            }
                    if result:
                        return result
            except:
                pass

        # Fallback: IDX API
        url2 = "https://idx.co.id/api/v1/StockData/GetForeignFlow"
        resp2 = requests.get(url2, headers=headers, timeout=10)
        if resp2.status_code == 200:
            try:
                data2 = resp2.json()
                stocks = data2.get("ResultData", {}).get("StockList", [])
                for item in stocks:
                    ticker = str(item.get("StockCode","")).strip()
                    if ticker:
                        result[ticker] = {
                            "net_flow":    float(item.get("NetBuy", 0)),
                            "foreign_buy": float(item.get("ForeignBuy", 0)),
                            "foreign_sell":float(item.get("ForeignSell", 0)),
                            "source":      "idx_api",
                        }
                if result:
                    return result
            except:
                pass

    except Exception as e:
        pass

    return {}  # kosong = gunakan fallback estimasi

def analyze_foreign_flow(ticker, closes, highs, lows, volumes, rti_data=None):
    """
    Analisis Foreign Flow.
    Priority: data real dari RTI/IDX → estimasi volume-based.
    """
    default = {
        "net_foreign_flow": 0, "foreign_buy": 0, "foreign_sell": 0,
        "flow_status": "N/A", "flow_color": "#8b949e", "flow_emoji": "❓",
        "buy_trend": "N/A", "sell_trend": "N/A", "flow_strength": 50.0,
        "foreign_ratio": 0.0, "est_foreign_ownership": 0.0,
        "signals": [], "score_adj": 0, "divergence": False, "data_source": "none",
    }

    try:
        if len(closes) < 5:
            return default

        # ── Gunakan data real jika tersedia ──
        if rti_data and ticker in rti_data:
            rd = rti_data[ticker]
            net = rd["net_flow"]
            fb  = rd["foreign_buy"]
            fs  = rd["foreign_sell"]
            data_source = rd.get("source", "real")
        else:
            # ── Estimasi dari volume & price action ──
            data_source = "estimated"
            foreign_buy_vol, foreign_sell_vol = [], []
            for i in range(1, len(closes)):
                price_change = (closes[i] - closes[i-1]) / max(closes[i-1], 0.001)
                vol_ratio    = volumes[i] / max(np.mean(volumes[max(0,i-10):i]), 1)
                if vol_ratio > 1.5 and abs(price_change) > 0.015:
                    if price_change > 0: foreign_buy_vol.append(volumes[i] * 0.4)
                    else:                foreign_sell_vol.append(volumes[i] * 0.4)
                elif vol_ratio > 1.2 and abs(price_change) > 0.008:
                    if price_change > 0: foreign_buy_vol.append(volumes[i] * 0.25)
                    else:                foreign_sell_vol.append(volumes[i] * 0.25)
            fb  = sum(foreign_buy_vol[-10:])  if foreign_buy_vol  else 0
            fs  = sum(foreign_sell_vol[-10:]) if foreign_sell_vol else 0
            net = fb - fs

        if net > 0:
            flow_status = "NET BUY";  flow_color = "#00ff88"; flow_emoji = "🟢"
        elif net < 0:
            flow_status = "NET SELL"; flow_color = "#ff4444"; flow_emoji = "🔴"
        else:
            flow_status = "NEUTRAL";  flow_color = "#ffd700"; flow_emoji = "🟡"

        total_vol     = sum(volumes[-10:]) if volumes else 1
        foreign_ratio = (fb + fs) / max(total_vol, 1) * 100
        flow_strength = min(100, max(0, 50 + (net / max(total_vol, 1) * 200)))

        signals   = []
        score_adj = 0
        if data_source != "estimated":
            signals.append(f"📡 Data Real ({data_source.upper()})")

        if net > 0:
            score_adj += 18; signals.append("✅ Foreign Net Buy")
        elif net < 0:
            score_adj -= 15; signals.append("🔴 Foreign Net Sell")

        price_trend = closes[-1] > closes[-5] if len(closes) >= 5 else True
        divergence  = (not price_trend) and (net > 0)
        if divergence:
            score_adj += 15; signals.append("⚡ Bullish Divergence (Price↓ Foreign↑)")
        elif price_trend and net < 0:
            score_adj -= 12; signals.append("⚠️ Bearish Divergence (Price↑ Foreign↓)")

        big_cap = ["BBCA","BBRI","BMRI","BBNI","TLKM","ASII","UNVR","GOTO","ANTM","ADRO"]
        if ticker in big_cap:
            flow_strength = min(100, flow_strength * 1.15)

        rng = np.random.default_rng(sum(ord(c) for c in ticker))
        est_ownership = (round(float(rng.uniform(35, 65)), 1) if ticker in big_cap
                         else round(float(rng.uniform(15, 40)), 1))

        return {
            "net_foreign_flow":      round(net, 0),
            "foreign_buy":           round(fb, 0),
            "foreign_sell":          round(fs, 0),
            "flow_status":           flow_status,
            "flow_color":            flow_color,
            "flow_emoji":            flow_emoji,
            "buy_trend":             "N/A",
            "sell_trend":            "N/A",
            "flow_strength":         round(flow_strength, 1),
            "foreign_ratio":         round(foreign_ratio, 2),
            "est_foreign_ownership": est_ownership,
            "signals":               signals,
            "score_adj":             score_adj,
            "divergence":            divergence,
            "data_source":           data_source,
        }
    except Exception as e:
        return default

# ============================================================
# BANDARMOLOGI
# ============================================================
def calc_cmf(highs, lows, closes, volumes, period=20):
    try:
        n = min(period, len(closes))
        mf_vol = []
        for i in range(-n, 0):
            h, l, c, v = highs[i], lows[i], closes[i], volumes[i]
            hl = h - l
            mf_vol.append(0 if hl == 0 else ((c - l) - (h - c)) / hl * v)
        vol_sum = sum(volumes[-n:])
        return round(sum(mf_vol) / vol_sum, 4) if vol_sum > 0 else 0
    except:
        return 0

def calc_vwap(highs, lows, closes, volumes):
    try:
        typical = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
        tp_vol  = [t * v for t, v in zip(typical, volumes)]
        cum_vol = np.cumsum(volumes)
        cum_tpv = np.cumsum(tp_vol)
        vwap    = cum_tpv / (cum_vol + 0.001)
        return float(vwap[-1])
    except:
        return closes[-1] if closes else 0

def calc_obv_trend(closes, volumes):
    try:
        obv, obvs = 0, []
        for i in range(len(closes)):
            if i == 0: obv += volumes[i]
            elif closes[i] > closes[i-1]: obv += volumes[i]
            elif closes[i] < closes[i-1]: obv -= volumes[i]
            obvs.append(obv)
        if len(obvs) < 5: return "FLAT"
        recent = obvs[-5:]
        if recent[-1] > recent[0] * 1.01:   return "UP"
        elif recent[-1] < recent[0] * 0.99: return "DOWN"
        return "FLAT"
    except:
        return "FLAT"

def analyze_bandarmologi(closes, highs, lows, volumes):
    try:
        cmf         = calc_cmf(highs, lows, closes, volumes)
        vwap        = calc_vwap(highs, lows, closes, volumes)
        obv_trend   = calc_obv_trend(closes, volumes)
        above_vwap  = closes[-1] > vwap
        vol_ratio   = volumes[-1] / max(np.mean(volumes[-20:]), 1)

        ad, ads = 0, []
        for i in range(len(closes)):
            h, l, c, v = highs[i], lows[i], closes[i], volumes[i]
            hl = h - l
            ad += ((c - l) - (h - c)) / (hl + 0.001) * v
            ads.append(ad)
        ad_trend = ("UP" if len(ads) >= 5 and ads[-1] > ads[-5] * 1.005 else
                    "DOWN" if len(ads) >= 5 and ads[-1] < ads[-5] * 0.995 else "FLAT")

        signals, score = [], 0
        if cmf > 0.1:   score += 25; signals.append("✅ CMF Akumulasi Kuat")
        elif cmf > 0.05:score += 15; signals.append("✅ CMF Akumulasi")
        elif cmf < -0.1: score -= 20; signals.append("🔴 CMF Distribusi Kuat")
        elif cmf < -0.05:score -= 10; signals.append("🔴 CMF Distribusi")

        if above_vwap:        score += 15; signals.append("✅ Di Atas VWAP")
        else:                 score -= 10; signals.append("🔴 Di Bawah VWAP")
        if ad_trend == "UP":  score += 20; signals.append("✅ A/D Line Naik")
        elif ad_trend == "DOWN": score -= 15; signals.append("🔴 A/D Line Turun")
        if obv_trend == "UP": score += 15; signals.append("✅ OBV Naik")
        elif obv_trend == "DOWN": score -= 10; signals.append("🔴 OBV Turun")
        if vol_ratio > 2 and cmf > 0: score += 10; signals.append("✅ Volume Spike + CMF+")

        price_trend = closes[-1] > closes[-5] if len(closes) >= 5 else True
        if not price_trend and ad_trend == "UP":
            score += 15; signals.append("⚡ Divergence Bullish (Akumulasi Tersembunyi!)")

        bandar_strength = min(100, max(0, 50 + score))
        if bandar_strength >= 70:
            fase = "🐋 AKUMULASI AKTIF"; fase_color = "#00ff88"; fase_emoji = "🐋"
        elif bandar_strength >= 55:
            fase = "📈 RE-AKUMULASI";   fase_color = "#7dff6b"; fase_emoji = "📈"
        elif bandar_strength >= 45:
            fase = "➡️ SIDEWAYS/MARKUP";fase_color = "#ffd700"; fase_emoji = "➡️"
        elif bandar_strength >= 30:
            fase = "📉 DISTRIBUSI";     fase_color = "#ff9944"; fase_emoji = "📉"
        else:
            fase = "🔴 DISTRIBUSI AKTIF"; fase_color = "#ff4444"; fase_emoji = "🔴"

        return {
            "cmf": cmf, "vwap": vwap, "above_vwap": above_vwap,
            "obv_trend": obv_trend, "ad_trend": ad_trend,
            "bandar_strength": bandar_strength, "fase": fase,
            "fase_color": fase_color, "fase_emoji": fase_emoji,
            "signals": signals, "vol_ratio": round(vol_ratio, 2),
            "score_adj": round(score / 5),
        }
    except:
        return {
            "cmf": 0, "vwap": 0, "above_vwap": False, "obv_trend": "FLAT", "ad_trend": "FLAT",
            "bandar_strength": 50, "fase": "N/A", "fase_color": "#8b949e", "fase_emoji": "❓",
            "signals": [], "vol_ratio": 1, "score_adj": 0
        }

# ============================================================
# CHART PATTERN RECOGNITION
# ============================================================
def detect_patterns(closes, highs, lows, opens):
    patterns = []
    if len(closes) < 5:
        return patterns

    c, h, l, o   = closes[-1], highs[-1], lows[-1], opens[-1]
    pc, ph, pl, po = closes[-2], highs[-2], lows[-2], opens[-2]
    body     = abs(c - o)
    tr       = h - l + 0.001
    up_shad  = h - max(c, o)
    lo_shad  = min(c, o) - l

    if lo_shad > 2 * body and up_shad < 0.3 * body and c > o:
        patterns.append({"name": "🔨 Hammer", "signal": "BULLISH", "confidence": 75,
                          "description": "Hammer setelah downtrend → potensi reversal"})
    if up_shad > 2 * body and lo_shad < 0.3 * body and c > o:
        patterns.append({"name": "🔨 Inv. Hammer", "signal": "BULLISH", "confidence": 65,
                          "description": "Inverted Hammer di area support"})
    if body < 0.1 * tr:
        patterns.append({"name": "➕ Doji", "signal": "NEUTRAL", "confidence": 60,
                          "description": "Doji menandakan keraguan pasar"})
    if pc < po and c > o and c > po and o < pc:
        patterns.append({"name": "🟢 Bull Engulfing", "signal": "BULLISH", "confidence": 80,
                          "description": "Bullish engulfing setelah downtrend"})
    if pc > po and c < o and c < po and o > pc:
        patterns.append({"name": "🔴 Bear Engulfing", "signal": "BEARISH", "confidence": 80,
                          "description": "Bearish engulfing setelah uptrend"})
    if up_shad > 2 * body and lo_shad < 0.1 * tr and c < o:
        patterns.append({"name": "💫 Shooting Star", "signal": "BEARISH", "confidence": 70,
                          "description": "Shooting Star di puncak uptrend"})

    if len(closes) >= 3:
        o2, c2 = opens[-3], closes[-3]
        if c2 < o2 and body < 0.3 * (ph - pl) and c > o and c > (o2 + c2) / 2:
            patterns.append({"name": "⭐ Morning Star", "signal": "BULLISH", "confidence": 85,
                              "description": "Morning Star: reversal bullish kuat"})

    if len(closes) >= 20:
        n        = min(40, len(closes))
        cs       = closes[-n:]
        hs_slice = highs[-n:]
        ls_slice = lows[-n:]
        mid      = n // 2

        low1 = min(ls_slice[:mid]); low2 = min(ls_slice[mid:])
        if abs(low1 - low2) / max(low1, 0.001) < 0.03 and c > np.mean(cs) * 1.02:
            patterns.append({"name": "📈 Double Bottom", "signal": "BULLISH", "confidence": 78,
                              "description": "Double Bottom di area support",
                              "price_levels": {"support": low1, "target": c * 1.1}})

        high1 = max(hs_slice[:mid]); high2 = max(hs_slice[mid:])
        if abs(high1 - high2) / max(high1, 0.001) < 0.03 and c < np.mean(cs) * 0.98:
            patterns.append({"name": "📉 Double Top", "signal": "BEARISH", "confidence": 78,
                              "description": "Double Top di area resistance",
                              "price_levels": {"resistance": high1, "target": c * 0.9}})

        first_half_chg  = (cs[mid] - cs[0]) / max(cs[0], 0.001) * 100
        second_half_std = np.std(cs[mid:]) / max(np.mean(cs[mid:]), 0.001) * 100
        if first_half_chg > 5 and second_half_std < 2 and c > cs[mid]:
            patterns.append({"name": "🚩 Bull Flag", "signal": "BULLISH", "confidence": 72,
                              "description": "Bull Flag: konsolidasi setelah uptrend"})

        highs_flat  = np.std(hs_slice[-10:]) / max(np.mean(hs_slice[-10:]), 0.001) < 0.02
        lows_rising = ls_slice[-1] > ls_slice[-10] if len(ls_slice) >= 10 else False
        if highs_flat and lows_rising:
            patterns.append({"name": "📐 Ascending Triangle", "signal": "BULLISH", "confidence": 70,
                              "description": "Ascending Triangle: resistance datar, support naik"})

    return patterns

# ============================================================
# RISK MANAGER
# ============================================================
def get_trade_plan(price, atr, support, resistance, modal=10_000_000,
                   adx=0, bandar_fase="", bandar_strength=50, cmf=0):
    try:
        sl = round(max(price - atr * 1.5, support * 0.99, price * 0.94) / 10) * 10
        risk_pct = round((price - sl) / price * 100, 1)

        tp_multiplier = 2.0 if adx > 40 else 1.8 if adx > 25 else 1.5
        if bandar_fase and "AKUMULASI" in bandar_fase.upper(): tp_multiplier *= 1.2
        if cmf > 0.1: tp_multiplier *= 1.15

        tp1 = round(price * (1 + risk_pct / 100 * tp_multiplier) / 10) * 10
        tp2 = round(price * (1 + risk_pct / 100 * tp_multiplier * 2) / 10) * 10
        tp3 = round(price * (1 + risk_pct / 100 * tp_multiplier * 3.5) / 10) * 10

        if resistance and resistance > price:
            tp1 = round(min(tp1, resistance * 0.99) / 10) * 10

        tp1_pct = round((tp1 - price) / price * 100, 1)
        tp2_pct = round((tp2 - price) / price * 100, 1)
        tp3_pct = round((tp3 - price) / price * 100, 1)

        max_loss_per_lembar = price - sl
        max_total_loss      = modal * 0.02
        max_lembar          = int(max_total_loss / max(max_loss_per_lembar, 1))
        max_lot             = max(1, max_lembar // 100)

        if adx > 40 and "AKUMULASI" in bandar_fase.upper():
            adj_note = "ADX kuat + Akumulasi Bandar → TP diperbesar"
        elif adx > 40:
            adj_note = "ADX kuat → TP diperbesar"
        elif "AKUMULASI" in bandar_fase.upper():
            adj_note = "Akumulasi Bandar → TP diperbesar"
        elif cmf < -0.05:
            adj_note = "⚠️ CMF negatif → risiko tinggi, kurangi lot"
        else:
            adj_note = "Standar (tidak ada penyesuaian)"

        return {
            "sl":       {"recommended": sl, "risk_pct": risk_pct, "value": price - sl},
            "tp":       {"tp1": tp1, "tp1_pct": tp1_pct, "tp2": tp2, "tp2_pct": tp2_pct,
                         "tp3": tp3, "tp3_pct": tp3_pct,
                         "rr":  round(tp2_pct / max(risk_pct, 0.1), 1)},
            "position": {"lot": max_lot, "lembar": max_lot * 100,
                         "max_loss":       round(max_lot * 100 * max_loss_per_lembar),
                         "required_modal": round(max_lot * 100 * price)},
            "adjustment_note": adj_note,
        }
    except:
        sl = round(price * 0.95 / 10) * 10
        return {
            "sl":       {"recommended": sl, "risk_pct": 5, "value": price - sl},
            "tp":       {"tp1": round(price * 1.07 / 10) * 10, "tp1_pct": 7,
                         "tp2": round(price * 1.15 / 10) * 10, "tp2_pct": 15,
                         "tp3": round(price * 1.25 / 10) * 10, "tp3_pct": 25, "rr": 3.0},
            "position": {"lot": 1, "lembar": 100,
                         "max_loss": price * 5, "required_modal": price * 100},
            "adjustment_note": "Fallback (error dalam kalkulasi)",
        }

# ============================================================
# ✅ ENHANCED SCORING ENGINE dengan RS vs IHSG + Sector Momentum
# ============================================================
def score_stock(data, hist=None, ihsg_closes=None, sector_momentum=None, rti_data=None):
    price    = data.get("price", 0)
    change   = data.get("change", 0)
    volume   = data.get("volume", 0)
    avg_vol  = data.get("avg_volume", 1) or 1
    high     = data.get("high", price)
    low      = data.get("low", price)
    open_    = data.get("open", price)
    ma50     = data.get("ma50", price)
    ma200    = data.get("ma200", price)
    high52w  = data.get("high52w", price * 1.5)
    low52w   = data.get("low52w", price * 0.5)

    vol_ratio    = round(volume / avg_vol, 2) if avg_vol > 0 else 1.0
    value_traded = volume * price
    is_liquid    = value_traded > 500_000_000

    if hist and len(hist["close"]) > 5:
        closes   = hist["close"]
        opens_   = hist["open"]
        highs_   = hist["high"]
        lows_    = hist["low"]
        volumes_ = hist.get("volume", [volume])
    else:
        closes   = [low52w, price * 0.93, price * 0.97, open_, price]
        opens_   = closes[:]
        highs_   = [x * 1.02 for x in closes]
        lows_    = [x * 0.98 for x in closes]
        volumes_ = [avg_vol] * len(closes)

    # ✅ RSI Wilder's Smoothing
    rsi = calc_rsi_wilder(closes)

    # ✅ MACD Full Series
    macd_val, macd_signal, macd_hist = calc_macd_full(closes)

    bb_pos, bb_upper, bb_lower = calc_bb(closes)
    stoch_k, stoch_d           = calc_stoch(closes, highs_, lows_)
    adx                        = calc_adx(highs_, lows_, closes)
    support, resistance        = get_sr(highs_, lows_, closes)
    patterns                   = detect_patterns(closes, highs_, lows_, opens_)
    bandar                     = analyze_bandarmologi(closes, highs_, lows_, volumes_)
    foreign                    = analyze_foreign_flow(
                                     data.get("ticker", ""), closes, highs_, lows_,
                                     volumes_, rti_data
                                 )

    # ✅ Relative Strength vs IHSG
    rs_data = calc_relative_strength(closes, ihsg_closes) if ihsg_closes else {
        "rs_ratio": 1.0, "rs_score": 50.0, "rs_trend": "STABLE",
        "outperform": False, "rs_1m": 0.0, "rs_3m": 0.0
    }

    atr = (np.mean([highs_[i] - lows_[i] for i in range(-14, 0)])
           if len(closes) >= 14 else price * 0.03)

    above_ma50   = price > ma50   if ma50  > 0 else False
    above_ma200  = price > ma200  if ma200 > 0 else False
    golden_cross = (ma50 > ma200) if (ma50 > 0 and ma200 > 0) else False
    death_cross  = (ma50 < ma200 * 0.98) if (ma50 > 0 and ma200 > 0) else False

    range52w = high52w - low52w
    pos52w   = round((price - low52w) / range52w * 100, 1) if range52w > 0 else 50

    near_support    = support    and abs(price - support)    / price < 0.025
    near_resistance = resistance and abs(price - resistance) / price < 0.025
    vol_trend_up    = (len(volumes_) >= 3 and volumes_[-1] > volumes_[-2] > volumes_[-3])

    # Wyckoff phase
    if pos52w < 25 and vol_ratio > 1.5 and rsi < 50:
        wyckoff = "Accumulation"
    elif pos52w < 35 and change > 0 and vol_ratio > 1.2:
        wyckoff = "Re-Accumulation"
    elif above_ma50 and above_ma200 and change > 0:
        wyckoff = "Markup"
    elif pos52w > 80 and vol_ratio > 1.5 and change < 0:
        wyckoff = "Distribution"
    elif change < -2 and vol_ratio > 1.5:
        wyckoff = "Markdown"
    else:
        wyckoff = "Sideways"

    # ✅ Sector Momentum Score
    sector      = data.get("sector", "Other")
    sec_data    = sector_momentum.get(sector, {}) if sector_momentum else {}
    sec_score   = sec_data.get("score", 50)
    sec_change  = sec_data.get("change_1w", 0)
    sec_rank    = sec_data.get("rank", 7)

    score, signals, confirmations = 0, [], 0
    disqualified      = False
    disqualify_reason = []

    # ============================================================
    # LAYER 1 — HARD DISQUALIFIERS
    # Saham yang kena satu saja langsung AVOID, tidak dihitung lebih lanjut
    # ============================================================

    # 1a. Penny stock / harga tidak layak trading
    if price < 100:
        disqualified = True
        disqualify_reason.append(f"🚫 Harga Rp{price:.0f} terlalu rendah (<100)")
    elif price < 200:
        score -= 25
        signals.append("⚠️ Harga Rendah <200")

    # 1b. Tidak likuid — value traded < 500jt/hari
    if not is_liquid:
        disqualified = True
        disqualify_reason.append("🚫 Tidak Likuid (<Rp500jt/hari)")

    # 1c. Volume sangat sepi — tidak ada partisipan
    if vol_ratio < 0.3:
        disqualified = True
        disqualify_reason.append(f"🚫 Volume Mati ({vol_ratio:.2f}x avg)")

    # 1d. Death cross aktif + downtrend kuat
    if death_cross and change < -3 and rsi < 35:
        disqualified = True
        disqualify_reason.append("🚫 Death Cross + Downtrend Kuat")

    # 1e. Distribusi bandar + foreign net sell bersamaan
    if (bandar.get("bandar_strength", 50) < 25 and
            foreign.get("score_adj", 0) < -10):
        disqualified = True
        disqualify_reason.append("🚫 Bandar + Foreign Distribusi Serentak")

    # 1f. Wyckoff Markdown + RSI tidak oversold (masih bisa turun lebih)
    if wyckoff == "Markdown" and rsi > 40:
        disqualified = True
        disqualify_reason.append("🚫 Wyckoff Markdown, RSI belum oversold")

    # Jika kena hard disqualifier → score 0, rating AVOID, stop scoring
    if disqualified:
        final_score = 0
        rating   = "AVOID"; category = "AVOID"; cat_color = "#ff4444"
        trade_plan = get_trade_plan(
            price, atr, support or price * 0.95, resistance or price * 1.1,
            modal=st.session_state.get('modal', 10_000_000),
            adx=adx, bandar_fase=bandar.get("fase",""),
            bandar_strength=bandar.get("bandar_strength", 50),
            cmf=bandar.get("cmf", 0)
        )
        return {
            **data,
            "ticker": data.get("ticker",""), "close": price,
            "vol_ratio": vol_ratio, "is_liquid": is_liquid, "atr": round(atr,0),
            "rsi": rsi, "bb_pos": bb_pos, "bb_upper": bb_upper, "bb_lower": bb_lower,
            "macd": macd_val, "macd_signal": macd_signal, "macd_hist": macd_hist,
            "stoch_k": stoch_k, "stoch_d": stoch_d, "adx": adx,
            "patterns": patterns, "support": support, "resistance": resistance,
            "above_ma50": above_ma50, "above_ma200": above_ma200,
            "golden_cross": golden_cross, "death_cross": death_cross,
            "pos52w": pos52w, "wyckoff": wyckoff, "confirmations": 0,
            "vol_trend_up": vol_trend_up, "near_support": near_support,
            "bandar": bandar, "bandar_adj": 0,
            "bandar_fase": bandar.get("fase",""), "bandar_fase_color": bandar.get("fase_color","#ff4444"),
            "bandar_strength": bandar.get("bandar_strength",50), "cmf": bandar.get("cmf",0),
            "foreign": foreign, "foreign_adj": 0,
            "foreign_flow_status": foreign.get("flow_status",""),
            "foreign_flow_strength": foreign.get("flow_strength",50),
            "net_foreign_flow": foreign.get("net_foreign_flow",0),
            "foreign_data_source": foreign.get("data_source","estimated"),
            "rs_data": rs_data, "rs_score": rs_data.get("rs_score",50),
            "rs_ratio": rs_data.get("rs_ratio",1.0), "rs_trend": rs_data.get("rs_trend","STABLE"),
            "rs_outperform": rs_data.get("outperform",False),
            "rs_1m": rs_data.get("rs_1m",0), "rs_3m": rs_data.get("rs_3m",0),
            "sec_score": sec_score, "sec_rank": sec_rank, "sec_change": sec_change,
            "score": 0, "rating": "AVOID", "category": "AVOID", "cat_color": "#ff4444",
            "signals": disqualify_reason[:4],
            "disqualified": True, "disqualify_reason": disqualify_reason,
            "trade_plan": trade_plan,
            "df": pd.DataFrame({
                "Close": closes, "Open": opens_, "High": highs_, "Low": lows_, "Volume": volumes_
            }) if hist else None,
        }

    # ============================================================
    # LAYER 2 — QUALITY GATE (Minimum requirement sebelum scoring)
    # Saham harus lolos minimal 2 dari 4 gate ini untuk bisa dapat score tinggi
    # ============================================================
    quality_gates_passed = 0
    quality_gate_details = []

    # Gate A: Likuiditas memadai (sudah lolos hard disqualifier, cek lebih ketat)
    value_traded = volume * price
    if value_traded > 5_000_000_000:        # > 5 milyar/hari = sangat likuid
        quality_gates_passed += 1; quality_gate_details.append("✅ Sangat Likuid (>5M)")
    elif value_traded > 1_000_000_000:      # > 1 milyar = cukup likuid
        quality_gates_passed += 1; quality_gate_details.append("✅ Likuid (>1M)")

    # Gate B: Tren teknikal tidak berlawanan
    tech_ok = not death_cross and wyckoff not in ["Distribution","Markdown"]
    if tech_ok:
        quality_gates_passed += 1; quality_gate_details.append("✅ Tren Teknikal Bersih")

    # Gate C: Bandar tidak distribusi aktif
    if bandar.get("bandar_strength", 50) >= 40:
        quality_gates_passed += 1; quality_gate_details.append("✅ Bandar Netral/Akumulasi")

    # Gate D: Harga tidak di zona distribusi parah (>90% 52W high + RSI overbought)
    price_zone_ok = not (pos52w > 88 and rsi > 68)
    if price_zone_ok:
        quality_gates_passed += 1; quality_gate_details.append("✅ Zona Harga Aman")

    if quality_gates_passed < 2:
        # Kurangi score signifikan, tapi tidak di-disqualify
        score -= 35
        signals.append(f"⚠️ Quality Gate: {quality_gates_passed}/4")

    # ============================================================
    # LAYER 3 — WEIGHTED SCORING
    # Setiap indikator diberi bobot. Indikator "high conviction" bobotnya lebih besar.
    # ============================================================

    # ── GROUP A: MOMENTUM & TREND (bobot tinggi) ────────────────

    # RSI Wilder
    if 28 <= rsi <= 42:
        score += 22; signals.append("RSI Sweet Spot"); confirmations += 1
    elif rsi < 28:
        score += 16; signals.append("RSI Oversold ⚡"); confirmations += 1
    elif rsi > 72:
        score -= 18
    elif 42 < rsi <= 58:
        score += 8

    # MACD Full Series — salah satu konfirmasi terpenting
    if macd_val > 0 and macd_hist > 0:
        score += 20; signals.append("MACD Bull Cross 🎯"); confirmations += 1
    elif macd_val > 0 and macd_hist < 0:
        # MACD positif tapi histogram menyusut = momentum mulai lemah
        score += 7; signals.append("MACD Positif (melemah)")
    elif macd_val < 0 and macd_hist > 0:
        # MACD negatif tapi histogram naik = awal reversal
        score += 12; signals.append("MACD Reversal Early"); confirmations += 1
    elif macd_val < 0 and macd_hist < 0:
        score -= 12

    # ADX — kekuatan trend
    if adx > 40:
        score += 14; signals.append(f"ADX Kuat {adx:.0f}")
        confirmations += 1
    elif adx > 25:
        score += 8; signals.append(f"ADX Trend {adx:.0f}")
    elif adx < 15:
        score -= 8  # sideways choppy, tidak bagus untuk trading arah

    # Moving Averages
    if above_ma50 and above_ma200:
        score += 12; signals.append("Above MA50 & MA200"); confirmations += 1
    elif above_ma50:
        score += 6; signals.append("Above MA50")
    elif not above_ma50 and not above_ma200:
        score -= 8  # di bawah kedua MA = lemah

    if golden_cross:
        score += 10; signals.append("✨ Golden Cross"); confirmations += 1
    if death_cross:
        score -= 15  # sudah lolos hard disqualifier tapi tetap dikurangi

    # ── GROUP B: OVERSOLD / ENTRY ZONE (bobot sedang) ───────────

    # Bollinger Bands
    if bb_pos < 8:
        score += 20; signals.append("BB Extreme Lower 📉"); confirmations += 1
    elif bb_pos < 20:
        score += 13; signals.append("Near BB Lower"); confirmations += 1
    elif bb_pos > 92:
        score -= 14  # overbought ekstrem

    # Stochastic
    if stoch_k < 20 and stoch_d < 20:
        score += 15; signals.append("Stoch Oversold"); confirmations += 1
    elif stoch_k < 20:
        score += 8; signals.append("Stoch %K Oversold")
    elif stoch_k > 20 and stoch_k > stoch_d and stoch_d < 35:
        score += 10; signals.append("Stoch Cross Up ↗"); confirmations += 1
    elif stoch_k > 80 and stoch_d > 80:
        score -= 10  # overbought keduanya

    # 52-Week Position
    if pos52w < 12:
        score += 17; signals.append("Near 52W Low 🎯"); confirmations += 1
    elif pos52w < 22:
        score += 10; signals.append("52W Low Zone")
    elif pos52w > 95:
        score -= 12  # sangat dekat 52W high, risiko distribusi

    # Support / Resistance
    if near_support:
        score += 14; signals.append("At Key Support 🎯"); confirmations += 1
    if near_resistance:
        score -= 10  # tepat di resistance = risiko gagal breakout

    # ── GROUP C: VOLUME & MOMENTUM (bobot sedang-tinggi) ────────

    if vol_ratio > 5:
        score += 22; signals.append("🔥 Volume 5x EXTREME!"); confirmations += 1
    elif vol_ratio > 3:
        score += 16; signals.append("🔥 Volume 3x+"); confirmations += 1
    elif vol_ratio > 2:
        score += 10; signals.append("Volume 2x Surge"); confirmations += 1
    elif vol_ratio > 1.5:
        score += 5; signals.append("Volume Above Avg")
    elif vol_ratio < 0.5:
        score -= 12  # volume mati = tidak ada minat

    if vol_trend_up:
        score += 6; signals.append("Volume Trend Naik ↗")

    # Momentum harga
    if change > 1.5 and vol_ratio > 2:
        score += 14; signals.append("⚡ Breakout!"); confirmations += 1
    elif change > 0.5 and vol_ratio > 1.5:
        score += 7; signals.append("Momentum Up")
    elif change < -8:
        score -= 12  # crash hari ini
    elif change < -5 and rsi < 32:
        score += 6; signals.append("Dip Buy Setup")  # hanya kalau RSI sudah sangat oversold

    # ── GROUP D: WYCKOFF & MARKET STRUCTURE (bobot tinggi) ──────

    if wyckoff == "Accumulation":
        score += 22; signals.append("Wyckoff Accum 🏦"); confirmations += 1
    elif wyckoff == "Re-Accumulation":
        score += 17; signals.append("Wyckoff Re-Accum ↗"); confirmations += 1
    elif wyckoff == "Markup":
        score += 11; signals.append("Wyckoff Markup")
    elif wyckoff == "Distribution":
        score -= 22
    elif wyckoff == "Markdown":
        score -= 15

    # ── GROUP E: CHART PATTERNS ─────────────────────────────────

    bull_pats = [p for p in patterns if p["signal"] == "BULLISH"]
    bear_pats = [p for p in patterns if p["signal"] == "BEARISH"]

    # Bobot pattern berdasarkan confidence
    for p in bull_pats[:2]:
        conf_bonus = round(p.get("confidence", 65) / 10)
        score += conf_bonus; signals.append(p["name"]); confirmations += 1
    for p in bear_pats[:2]:
        conf_penalty = round(p.get("confidence", 65) / 12)
        score -= conf_penalty

    # ── GROUP F: SMART MONEY (bobot sangat tinggi) ───────────────

    # Bandarmologi
    bandar_adj = bandar.get("score_adj", 0)
    score += bandar_adj
    bandar_str = bandar.get("bandar_strength", 50)

    if bandar_str >= 70:
        score += 10; confirmations += 1  # bonus extra untuk akumulasi kuat
        signals.append(f"🐋 Bandar Akumulasi ({bandar_str}/100)")
    elif bandar_str >= 55:
        signals.append(f"🐋 Bandar Netral+ ({bandar_str}/100)")
    elif bandar_str < 35:
        score -= 10  # distribusi aktif, extra penalty
        signals.append(f"🔴 Bandar Distribusi ({bandar_str}/100)")

    if bandar.get("ad_trend") == "UP" and change < 0:
        score += 10; signals.append("🐋 A/D Divergence Bullish!"); confirmations += 1
    elif bandar.get("ad_trend") == "DOWN" and change > 0:
        score -= 8; signals.append("⚠️ A/D Divergence Bearish")

    # Foreign Flow — diberi bobot lebih besar karena smart money
    foreign_adj = foreign.get("score_adj", 0)
    score += foreign_adj

    if foreign_adj >= 15:
        score += 8; confirmations += 1  # extra bonus foreign net buy kuat
        signals.append(f"🌏 Foreign Strong Buy")
    elif foreign_adj >= 10:
        confirmations += 1
    elif foreign_adj <= -12:
        score -= 8  # extra penalty foreign sell kuat

    if foreign.get("divergence"):
        score += 12; signals.append("🌏 Foreign Divergence Bullish!"); confirmations += 1

    # ── GROUP G: RELATIVE STRENGTH vs IHSG (bobot tinggi) ───────

    rs_score_val = rs_data.get("rs_score", 50)
    rs_trend     = rs_data.get("rs_trend", "STABLE")

    if rs_score_val > 68 and rs_trend == "IMPROVING":
        score += 20; signals.append("⭐ RS Outperform IHSG+"); confirmations += 1
    elif rs_score_val > 60 and rs_trend == "IMPROVING":
        score += 14; signals.append("⭐ RS Outperform IHSG ↗"); confirmations += 1
    elif rs_score_val > 58:
        score += 8; signals.append("⭐ RS Outperform IHSG")
    elif rs_score_val < 30 and rs_trend == "WEAKENING":
        score -= 20; signals.append("⚠️ RS Sangat Lemah vs IHSG")
    elif rs_score_val < 40:
        score -= 10; signals.append("⚠️ RS Lemah vs IHSG")
    elif 40 <= rs_score_val < 48:
        score -= 4  # sedikit underperform

    # ── GROUP H: SECTOR MOMENTUM ────────────────────────────────

    if sec_rank <= 2 and sec_change > 1.5:
        score += 15; signals.append(f"🏭 Sektor #1-2 HOT 🔥"); confirmations += 1
    elif sec_rank <= 4 and sec_change > 0.5:
        score += 9; signals.append(f"🏭 Sektor Bullish (#{sec_rank})")
    elif sec_rank <= 6 and sec_change > 0:
        score += 4
    elif sec_rank >= 11 or sec_change < -2:
        score -= 12; signals.append(f"🏭 Sektor Lemah (#{sec_rank})")
    elif sec_rank >= 8 or sec_change < -0.5:
        score -= 6

    # ============================================================
    # LAYER 4 — CONFIRMATION MULTIPLIER
    # Semakin banyak konfirmasi independen, semakin reliable sinyalnya
    # ============================================================
    if confirmations >= 7:
        score += 20; signals.append(f"✅ {confirmations} Konfirmasi KUAT!")
    elif confirmations >= 5:
        score += 13; signals.append(f"✅ {confirmations} Konfirmasi")
    elif confirmations >= 3:
        score += 6; signals.append(f"✅ {confirmations} Konfirmasi")
    elif confirmations == 2:
        score -= 5   # 2 konfirmasi saja terlalu lemah
    elif confirmations <= 1:
        score -= 18  # hampir tidak ada konfirmasi = hindari

    # ============================================================
    # LAYER 5 — CONFLICT PENALTY
    # Kalau ada sinyal yang saling bertentangan, trustworthiness turun
    # ============================================================
    # RSI overbought tapi di BB lower = sinyal konflik
    if rsi > 65 and bb_pos < 25:
        score -= 8

    # Volume spike tapi harga turun = distribusi, bukan akumulasi
    if vol_ratio > 3 and change < -2:
        score -= 10; signals.append("⚠️ Vol Spike + Harga Turun")

    # MACD bull cross tapi bandar distribusi = konflik
    if macd_val > 0 and macd_hist > 0 and bandar_str < 35:
        score -= 10

    # RS bagus tapi death cross = konflik
    if rs_score_val > 60 and death_cross:
        score -= 8

    # ============================================================
    # NORMALISASI FINAL ke 0–100
    # Raw score range kira-kira -150 s/d +250 → normalize ke 0-100
    # ============================================================
    final_score = min(100, max(0, round((score + 80) / 3.3)))

    # ── Rating ditentukan oleh KOMBINASI score + konfirmasi ──────
    # Rating tinggi butuh KEDUANYA: score tinggi DAN banyak konfirmasi
    if final_score >= 82 and confirmations >= 6:
        rating = "🔥 SUPER BUY"; category = "🔥 SUPER BUY"; cat_color = "#00ffcc"
    elif final_score >= 72 and confirmations >= 5:
        rating = "🔥 SUPER BUY"; category = "🔥 SUPER BUY"; cat_color = "#00ffcc"
    elif final_score >= 65 and confirmations >= 4:
        rating = "STRONG BUY";   category = "STRONG BUY";   cat_color = "#00ff88"
    elif final_score >= 55 and confirmations >= 3:
        rating = "BUY";          category = "BUY";          cat_color = "#7dff6b"
    elif final_score >= 42:
        rating = "WATCH";        category = "WATCH";        cat_color = "#ffd700"
    elif final_score >= 28:
        rating = "NEUTRAL";      category = "NEUTRAL";      cat_color = "#ff9944"
    else:
        rating = "AVOID";        category = "AVOID";        cat_color = "#ff4444"

    # Extra: turunkan rating jika quality gate tidak cukup
    if quality_gates_passed < 2 and rating in ["🔥 SUPER BUY", "STRONG BUY", "BUY"]:
        rating = "WATCH"; category = "WATCH"; cat_color = "#ffd700"
        signals.append("⚠️ Rating diturunkan (Quality Gate)")

    rs_score = rs_score_val

    trade_plan = get_trade_plan(
        price, atr, support or price * 0.95, resistance or price * 1.1,
        modal=st.session_state.get('modal', 10_000_000),
        adx=adx, bandar_fase=bandar.get("fase",""),
        bandar_strength=bandar.get("bandar_strength", 50),
        cmf=bandar.get("cmf", 0)
    )

    return {
        **data,
        "ticker":               data.get("ticker", ""),
        "close":                price,
        "vol_ratio":            vol_ratio,
        "is_liquid":            is_liquid,
        "atr":                  round(atr, 0),
        "rsi":                  rsi,
        "bb_pos":               bb_pos,
        "bb_upper":             bb_upper,
        "bb_lower":             bb_lower,
        "macd":                 macd_val,
        "macd_signal":          macd_signal,
        "macd_hist":            macd_hist,
        "stoch_k":              stoch_k,
        "stoch_d":              stoch_d,
        "adx":                  adx,
        "patterns":             patterns,
        "support":              support,
        "resistance":           resistance,
        "above_ma50":           above_ma50,
        "above_ma200":          above_ma200,
        "golden_cross":         golden_cross,
        "death_cross":          death_cross,
        "pos52w":               pos52w,
        "wyckoff":              wyckoff,
        "confirmations":        confirmations,
        "vol_trend_up":         vol_trend_up,
        "near_support":         near_support,
        "bandar":               bandar,
        "bandar_adj":           bandar_adj,
        "bandar_fase":          bandar.get("fase", ""),
        "bandar_fase_color":    bandar.get("fase_color", "#8b949e"),
        "bandar_strength":      bandar.get("bandar_strength", 50),
        "cmf":                  bandar.get("cmf", 0),
        "foreign":              foreign,
        "foreign_adj":          foreign_adj,
        "foreign_flow_status":  foreign.get("flow_status", ""),
        "foreign_flow_strength":foreign.get("flow_strength", 50),
        "net_foreign_flow":     foreign.get("net_foreign_flow", 0),
        "foreign_data_source":  foreign.get("data_source", "estimated"),
        # ✅ NEW
        "rs_data":              rs_data,
        "rs_score":             rs_score,
        "rs_ratio":             rs_data.get("rs_ratio", 1.0),
        "rs_trend":             rs_trend,
        "rs_outperform":        rs_data.get("outperform", False),
        "rs_1m":                rs_data.get("rs_1m", 0),
        "rs_3m":                rs_data.get("rs_3m", 0),
        "sec_score":            sec_score,
        "sec_rank":             sec_rank,
        "sec_change":           sec_change,
        "score":                final_score,
        "rating":               rating,
        "category":             category,
        "cat_color":            cat_color,
        "signals":              signals[:8],
        "disqualified":         False,
        "disqualify_reason":    [],
        "quality_gates":        quality_gates_passed,
        "trade_plan":           trade_plan,
        "df": pd.DataFrame({
            "Close":  closes, "Open":  opens_,
            "High":   highs_, "Low":   lows_, "Volume": volumes_
        }) if hist else None,
    }

# ============================================================
# FETCH DATA dari Yahoo Finance
# ============================================================
@st.cache_data(ttl=300, show_spinner=False)
def fetch_batch(tickers_list, _ihsg_closes=None, _sector_momentum=None, _rti_data=None):
    results = []
    try:
        yf_symbols = [t + ".JK" for t in tickers_list]
        raw = yf.download(
            " ".join(yf_symbols), period="6mo", interval="1d",
            group_by="ticker", auto_adjust=True, progress=False, threads=True
        )
        for ticker, symbol in zip(tickers_list, yf_symbols):
            try:
                if len(yf_symbols) > 1 and symbol in raw.columns.get_level_values(0):
                    df = raw[symbol]
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                else:
                    df = raw
                df = df.dropna()
                if df is None or len(df) < 5:
                    results.append(make_fallback(ticker, _ihsg_closes, _sector_momentum, _rti_data)); continue

                closes   = df["Close"].tolist()
                opens_   = df["Open"].tolist()
                highs_   = df["High"].tolist()
                lows_    = df["Low"].tolist()
                volumes_ = df["Volume"].tolist()

                price      = closes[-1]
                prev_close = closes[-2]
                change     = round((price - prev_close) / prev_close * 100, 2)
                volume     = int(volumes_[-1])
                avg_vol    = int(np.mean(volumes_[-20:]))
                ma50       = float(np.mean(closes[-50:]))  if len(closes) >= 50  else float(np.mean(closes))
                ma200      = float(np.mean(closes[-200:])) if len(closes) >= 200 else float(np.mean(closes))

                stock_data = {
                    "ticker": ticker, "name": ticker, "source": "live",
                    "price": price, "prev_close": prev_close, "change": change,
                    "volume": volume, "avg_volume": avg_vol,
                    "open": opens_[-1], "high": highs_[-1], "low": lows_[-1],
                    "high52w": max(highs_), "low52w": min(lows_),
                    "ma50": ma50, "ma200": ma200, "sector": get_sector(ticker)
                }
                hist = {"close": closes, "open": opens_, "high": highs_, "low": lows_, "volume": volumes_}
                r = score_stock(stock_data, hist, _ihsg_closes, _sector_momentum, _rti_data)

                if "chart_data" not in st.session_state:
                    st.session_state["chart_data"] = {}
                st.session_state["chart_data"][ticker] = df
                results.append(r)
            except Exception as e:
                results.append(make_fallback(ticker, _ihsg_closes, _sector_momentum, _rti_data))
    except Exception as e:
        for t in tickers_list:
            results.append(make_fallback(t, _ihsg_closes, _sector_momentum, _rti_data))
    return results

def make_fallback(ticker, ihsg_closes=None, sector_momentum=None, rti_data=None):
    seed  = sum(ord(c) for c in ticker)
    rng   = np.random.default_rng(seed)
    price = round(rng.uniform(200, 6000) / 10) * 10
    change= round(rng.uniform(-6, 8), 2)
    n     = 120
    prices   = [price * (1 + rng.uniform(-0.02, 0.02)) for _ in range(n)]
    prices[-1] = price
    highs_   = [p * rng.uniform(1.001, 1.03)  for p in prices]
    lows_    = [p * rng.uniform(0.97, 0.999)  for p in prices]
    volumes_ = [int(rng.uniform(500_000, 10_000_000)) for _ in range(n)]

    stock_data = {
        "ticker": ticker, "name": ticker, "source": "simulated",
        "price": price, "prev_close": round(price / (1 + change / 100) / 10) * 10,
        "change": change, "volume": volumes_[-1],
        "avg_volume": int(np.mean(volumes_[-20:])),
        "open": price, "high": highs_[-1], "low": lows_[-1],
        "high52w": max(highs_), "low52w": min(lows_),
        "ma50": float(np.mean(prices[-50:])), "ma200": float(np.mean(prices)),
        "sector": get_sector(ticker)
    }
    hist = {"close": prices, "open": prices[:], "high": highs_, "low": lows_, "volume": volumes_}
    return score_stock(stock_data, hist, ihsg_closes, sector_momentum, rti_data)

# ============================================================
# AI ANALYSIS dengan Groq
# ============================================================
def get_ai_analysis(stock, api_key):
    try:
        b   = stock.get("bandar", {})
        f   = stock.get("foreign", {})
        tp  = stock.get("trade_plan", {})
        rs  = stock.get("rs_data", {})
        pats = ", ".join([p["name"] for p in stock.get("patterns", [])[:3]]) or "Tidak ada"
        sec_rank  = stock.get("sec_rank", 7)
        sec_score = stock.get("sec_score", 50)

        prompt = f"""Kamu adalah expert trader saham Indonesia spesialis SCALPING & DAY TRADING IDX.
Saham: {stock['ticker']} | Sektor: {stock['sector']} (Rank #{sec_rank}/13, Score:{sec_score:.0f})
Harga: Rp {stock['price']:,.0f} | Change: {stock['change']}%
Volume: {stock['vol_ratio']}x rata-rata | Likuid: {'Ya' if stock.get('is_liquid') else 'Tidak'}
RSI (Wilder): {stock['rsi']} | MACD: {stock['macd']:.4f} (hist:{stock['macd_hist']:.4f})
Stoch K/D: {stock['stoch_k']}/{stock['stoch_d']} | ADX: {stock['adx']}
BB Position: {stock['bb_pos']}% | Support: {stock.get('support','N/A')} | Resistance: {stock.get('resistance','N/A')}
MA50: {'Di atas' if stock['above_ma50'] else 'Di bawah'} | MA200: {'Di atas' if stock['above_ma200'] else 'Di bawah'}
52W Position: {stock['pos52w']}% | Wyckoff: {stock['wyckoff']}
Bandarmologi: {b.get('fase','N/A')} | CMF: {b.get('cmf',0):.3f} | VWAP: {'Di atas' if b.get('above_vwap') else 'Di bawah'}
A/D Line: {b.get('ad_trend','N/A')} | OBV: {b.get('obv_trend','N/A')} | Bandar Strength: {b.get('bandar_strength',50)}/100
Foreign Flow: {f.get('flow_status','N/A')} | Net Flow: Rp {stock.get('net_foreign_flow',0):,.0f} | Source: {f.get('data_source','est')}
Relative Strength vs IHSG: {rs.get('rs_score',50):.1f}/100 | RS 1M: {rs.get('rs_1m',0):+.2f}% | Trend: {rs.get('rs_trend','N/A')}
Chart Pattern: {pats}
Sinyal: {', '.join(stock['signals'][:5])}
AI Score: {stock['score']}/100 ({stock['rating']}) | Konfirmasi: {stock['confirmations']}/10
Trade Plan: Entry Rp {stock['price']:,.0f} | SL Rp {tp.get('sl',{}).get('recommended',0):,.0f} | TP1 Rp {tp.get('tp',{}).get('tp1',0):,.0f} | TP2 Rp {tp.get('tp',{}).get('tp2',0):,.0f}

Berikan analisa TAJAM untuk scalping/day trade besok dalam Bahasa Indonesia dengan format MARKDOWN:

## 🔍 VERDICT
[1 kalimat tegas apakah layak beli/hindari]

## 📊 TEKNIKAL
- [RSI Wilder + MACD interpretation]
- [Bandarmologi & Foreign Flow]
- [Relative Strength vs IHSG]

## 🏭 SEKTOR
[kondisi sektor dan implikasinya]

## 💰 RENCANA ENTRY
- **Entry:** Rp X (kondisi: ...)
- **TP1:** Rp X (+Y%)
- **TP2:** Rp X (+Z%)
- **Stop Loss:** Rp X (-W%)
- **Risk/Reward:** 1:X

## ⚠️ RISIKO
[1-2 risiko spesifik]

## ⏱️ TIPS SCALPING
[timing masuk yang ideal]
"""
        models_to_try = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        errors = []
        for model in models_to_try:
            try:
                resp = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": model,
                          "messages": [{"role": "user", "content": prompt}],
                          "max_tokens": 1000, "temperature": 0.7},
                    timeout=30
                )
                d = resp.json()
                if "choices" in d:
                    return d["choices"][0]["message"]["content"]
                err_msg = d.get("error", {}).get("message", str(d.get("error", "")))
                errors.append(f"{model}: {err_msg[:80]}")
                if "invalid_api_key" in str(d.get("error", "")) or resp.status_code == 401:
                    return "⚠️ API Key Groq tidak valid! Daftar gratis di console.groq.com"
            except Exception as e:
                errors.append(f"{model}: {str(e)[:60]}")
        return "⚠️ Gagal: " + " | ".join(errors)
    except Exception as e:
        return f"⚠️ Error: {e}"

# ============================================================
# ✅ IMPROVED BACKTEST ENGINE
# Entry = OPEN hari berikutnya (realistis), bukan close sinyal
# ============================================================
def run_backtest(ticker, days=60, hold_days=10):
    try:
        df = yf.download(ticker + ".JK", period="1y", interval="1d",
                         auto_adjust=True, progress=False)
        if df is None or len(df) < days + 20:
            return None
        df = df.dropna()
        closes = df["Close"].tolist()
        opens  = df["Open"].tolist()
        highs  = df["High"].tolist()
        lows   = df["Low"].tolist()
        vols   = df["Volume"].tolist()
        dates  = df.index.tolist()

        trades = []
        i = 30
        while i < len(closes) - hold_days - 1:
            rsi    = calc_rsi_wilder(closes[:i + 1])
            macd_v, _, macd_h = calc_macd_full(closes[:i + 1])
            bb_pos, _, _ = calc_bb(closes[:i + 1])
            vol_ratio = vols[i] / max(np.mean(vols[max(0, i - 20):i]), 1)

            if rsi < 40 and macd_v > 0 and bb_pos < 35 and vol_ratio > 1.3:
                # ✅ Entry di OPEN hari BERIKUTNYA (realistis!)
                entry_idx  = i + 1
                entry      = opens[entry_idx]
                entry_date = dates[entry_idx]
                sl         = entry * 0.95
                tp1        = entry * 1.07
                tp2        = entry * 1.15
                outcome    = "TIMEOUT"
                exit_price = closes[min(entry_idx + hold_days, len(closes) - 1)]
                exit_date  = dates[min(entry_idx + hold_days, len(dates) - 1)]
                days_held  = hold_days

                for j in range(entry_idx + 1, min(entry_idx + hold_days + 1, len(closes))):
                    if closes[j] >= tp2:
                        outcome = "TP2"; exit_price = tp2; exit_date = dates[j]; days_held = j - entry_idx; break
                    elif closes[j] >= tp1:
                        outcome = "TP1"; exit_price = tp1; exit_date = dates[j]; days_held = j - entry_idx; break
                    elif lows[j] <= sl:
                        outcome = "SL";  exit_price = sl;  exit_date = dates[j]; days_held = j - entry_idx; break

                trades.append({
                    "entry_date": entry_date, "exit_date":  exit_date,
                    "entry": entry, "exit_price": exit_price,
                    "outcome": outcome,
                    "pnl_pct": round((exit_price - entry) / entry * 100, 2),
                    "days_held": days_held, "rsi": round(rsi, 1),
                })
                i = entry_idx + days_held + 1
            else:
                i += 1

        if not trades:
            return None

        wins   = [t for t in trades if t["pnl_pct"] > 0]
        losses = [t for t in trades if t["pnl_pct"] <= 0]
        win_rate = round(len(wins) / len(trades) * 100, 1)
        avg_win  = round(np.mean([t["pnl_pct"] for t in wins]),   2) if wins   else 0
        avg_loss = round(np.mean([t["pnl_pct"] for t in losses]), 2) if losses else 0
        profit_f = round(abs(avg_win * len(wins)) / max(abs(avg_loss * len(losses)), 0.01), 2)

        return {
            "ticker": ticker, "total_trades": len(trades),
            "win_count": len(wins), "loss_count": len(losses),
            "win_rate": win_rate,
            "avg_pnl":  round(np.mean([t["pnl_pct"] for t in trades]), 2),
            "avg_win": avg_win, "avg_loss": avg_loss,
            "avg_days_held": round(np.mean([t["days_held"] for t in trades]), 1),
            "best":    round(max(t["pnl_pct"] for t in trades), 2),
            "worst":   round(min(t["pnl_pct"] for t in trades), 2),
            "profit_factor": profit_f,
            "tp_hit":  sum(1 for t in trades if "TP" in t["outcome"]),
            "sl_hit":  sum(1 for t in trades if t["outcome"] == "SL"),
            "trades":  trades[-20:],
            "entry_method": "Next Day Open (Realistic)",
        }
    except Exception as e:
        print(f"Backtest error: {e}")
        return None

def create_backtest_chart(bt_result):
    if not bt_result or not bt_result.get("trades"):
        return go.Figure()
    trades = bt_result["trades"]
    fig = make_subplots(rows=2, cols=1,
                        subplot_titles=("Equity Curve", "Trade Distribution"),
                        row_heights=[0.6, 0.4], vertical_spacing=0.1)
    equity = [100]
    dates  = [trades[0]["entry_date"]]
    for t in trades:
        equity.append(equity[-1] * (1 + t["pnl_pct"] / 100))
        dates.append(t["exit_date"])
    fig.add_trace(go.Scatter(x=dates, y=equity[1:], mode="lines", name="Equity",
                             line=dict(color="#00ff88", width=2)), row=1, col=1)
    pnls   = [t["pnl_pct"] for t in trades]
    colors = ["#00ff88" if p > 0 else "#ff4444" for p in pnls]
    fig.add_trace(go.Bar(x=list(range(len(trades))), y=pnls, marker_color=colors,
                         name="P&L per Trade",
                         text=[f"{p:+.1f}%" for p in pnls], textposition="outside"), row=2, col=1)
    fig.update_layout(height=480, paper_bgcolor="#070711", plot_bgcolor="#0d0d1a",
                      font=dict(color="#7a84a8", family="JetBrains Mono", size=10),
                      showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
    for r in [1, 2]:
        fig.update_xaxes(gridcolor="#1e1e36", zeroline=False, row=r, col=1)
        fig.update_yaxes(gridcolor="#1e1e36", zeroline=False, row=r, col=1)
    fig.update_yaxes(title_text="Equity", row=1, col=1)
    fig.update_xaxes(title_text="Trade #", row=2, col=1)
    return fig

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def parse_tickers(raw_text):
    tickers = [t.strip().upper() for t in raw_text.replace("\n", ",").split(",") if t.strip()]
    return list(dict.fromkeys(tickers))

def fmt_price(p):
    return f"Rp {p:,.0f}"

def rating_icon(rating):
    return {"🔥 SUPER BUY": "🔥", "STRONG BUY": "🟢", "BUY": "🟩",
            "WATCH": "🟡", "NEUTRAL": "🟠", "AVOID": "🔴"}.get(rating, "⚪")

def metric_card(col, label, value, color="#e0e8ff"):
    with col:
        st.markdown(f"""
        <div class='metric-box'>
            <div class='metric-label'>{label}</div>
            <div class='metric-val' style='color:{color}'>{value}</div>
        </div>
        """, unsafe_allow_html=True)

def create_chart(df, ticker, trade_plan, timeframe="3 Bulan"):
    if df is None or len(df) < 10:
        return None
    df = df.tail(60).copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    closes  = df["Close"].tolist()
    opens_  = df["Open"].tolist()
    highs_  = df["High"].tolist()
    lows_   = df["Low"].tolist()
    volumes = df["Volume"].tolist()
    dates   = df.index.tolist()

    ma20 = [float(np.mean(closes[max(0, i - 20):i + 1])) for i in range(len(closes))]
    ma50 = [float(np.mean(closes[max(0, i - 50):i + 1])) for i in range(len(closes))]
    # ✅ RSI Wilder di chart
    rsi_values = [calc_rsi_wilder(closes[:i + 1]) for i in range(len(closes))]
    vol_colors = ["rgba(0,232,122,0.45)" if c >= o else "rgba(255,61,90,0.45)"
                  for c, o in zip(closes, opens_)]

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03,
                        row_heights=[0.55, 0.15, 0.30],
                        subplot_titles=("", "VOLUME", "RSI (14) — Wilder's"))

    fig.add_trace(go.Candlestick(
        x=dates, open=opens_, high=highs_, low=lows_, close=closes, name=ticker,
        increasing_line_color="#00e87a", decreasing_line_color="#ff3d5a",
        increasing_fillcolor="rgba(0,232,122,0.3)", decreasing_fillcolor="rgba(255,61,90,0.3)",
        increasing_line_width=1.2, decreasing_line_width=1.2, showlegend=False
    ), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=ma20, name="MA20",
                             line=dict(color="#f5c842", width=1.3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=dates, y=ma50, name="MA50",
                             line=dict(color="#00c8ff", width=1.3, dash="dot")), row=1, col=1)
    fig.add_trace(go.Bar(x=dates, y=volumes, marker_color=vol_colors,
                         opacity=0.7, showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=dates, y=rsi_values, name="RSI",
                             line=dict(color="#9b6dff", width=1.5), showlegend=False), row=3, col=1)

    for rsi_lvl, rsi_col in [(70, "#ff3d5a"), (30, "#00e87a")]:
        fig.add_shape(type="line", x0=0, x1=1, xref="paper",
                      y0=rsi_lvl, y1=rsi_lvl, yref="y3",
                      line=dict(color=rsi_col, width=1, dash="dash"))
    fig.add_shape(type="rect", x0=0, x1=1, xref="paper", y0=0, y1=30, yref="y3",
                  fillcolor="rgba(0,232,122,0.04)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=0, x1=1, xref="paper", y0=70, y1=100, yref="y3",
                  fillcolor="rgba(255,61,90,0.04)", line=dict(width=0), layer="below")

    entry_price = closes[-1]
    fig.add_shape(type="line", x0=0, x1=1, xref="paper",
                  y0=entry_price, y1=entry_price, yref="y",
                  line=dict(color="rgba(255,255,255,0.5)", width=1, dash="dot"))
    fig.add_annotation(x=1.01, y=entry_price, xref="paper", yref="y",
                       text=f"ENTRY<br>{entry_price:,.0f}", showarrow=False, xanchor="left",
                       font=dict(color="#cccccc", size=9, family="JetBrains Mono"),
                       bgcolor="rgba(7,7,17,0.85)", bordercolor="#444466", borderwidth=1, borderpad=4)

    if trade_plan:
        price_now = closes[-1]
        levels = [
            (trade_plan.get("sl", {}).get("recommended"), "#ff3d5a", "SL ▼"),
            (trade_plan.get("tp", {}).get("tp1"),          "#f5c842", "TP1 ▲"),
            (trade_plan.get("tp", {}).get("tp2"),          "#00e87a", "TP2 ▲"),
        ]
        for level, color, label in levels:
            if not level or level <= 0: continue
            pct = (level - price_now) / price_now * 100
            fig.add_shape(type="line", x0=0, x1=1, xref="paper",
                          y0=level, y1=level, yref="y",
                          line=dict(color=color, width=1.5, dash="dash"))
            fig.add_annotation(x=1.01, y=level, xref="paper", yref="y",
                               text=f"{label}<br>{level:,.0f} ({pct:+.1f}%)",
                               showarrow=False, xanchor="left",
                               font=dict(color=color, size=9, family="JetBrains Mono"),
                               bgcolor="rgba(7,7,17,0.85)", bordercolor=color, borderwidth=1, borderpad=4)

    fig.update_layout(
        paper_bgcolor="#070711", plot_bgcolor="#0d0d1a",
        font=dict(color="#7a84a8", size=10, family="JetBrains Mono"),
        margin=dict(l=10, r=90, t=28, b=10), height=480,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.4,
                    font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified", xaxis_rangeslider_visible=False
    )
    axis_style = dict(gridcolor="#1a1a2e", showgrid=True,
                      tickfont=dict(size=9, family="JetBrains Mono"),
                      zeroline=False, linecolor="#1e1e36", showline=True)
    for r in [1, 2, 3]:
        fig.update_xaxes(**axis_style, row=r, col=1)
        fig.update_yaxes(**axis_style, row=r, col=1)
    for ann in fig.layout.annotations:
        ann.font = dict(size=9, color="#3a3f5c", family="JetBrains Mono")
    return fig

def export_to_csv(stocks_list):
    rows = []
    for s in stocks_list:
        tp = s.get("trade_plan", {})
        b  = s.get("bandar", {})
        f  = s.get("foreign", {})
        rows.append({
            "Tanggal":         datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Ticker":          s.get("ticker", ""),
            "Sektor":          s.get("sector", ""),
            "Score":           s.get("score", 0),
            "Rating":          s.get("rating", ""),
            "Konfirmasi":      s.get("confirmations", 0),
            "Harga":           s.get("price", 0),
            "Change%":         s.get("change", 0),
            "Volume_Ratio":    s.get("vol_ratio", 0),
            "RSI_Wilder":      s.get("rsi", 0),
            "MACD":            s.get("macd", 0),
            "MACD_Hist":       s.get("macd_hist", 0),
            "ADX":             s.get("adx", 0),
            "BB_Pos":          s.get("bb_pos", 0),
            "Wyckoff":         s.get("wyckoff", ""),
            "Bandar_Fase":     b.get("fase", ""),
            "CMF":             round(b.get("cmf", 0), 4),
            "Bandar_Strength": b.get("bandar_strength", 50),
            "Foreign_Status":  f.get("flow_status", ""),
            "Foreign_Source":  s.get("foreign_data_source","estimated"),
            "Net_Foreign_Flow":s.get("net_foreign_flow", 0),
            "RS_Score":        s.get("rs_score", 50),
            "RS_vs_IHSG":      s.get("rs_ratio", 1.0),
            "RS_1M_pct":       s.get("rs_1m", 0),
            "RS_3M_pct":       s.get("rs_3m", 0),
            "Sector_Rank":     s.get("sec_rank", 7),
            "Sector_Score":    s.get("sec_score", 50),
            "Entry":           s.get("price", 0),
            "SL":              tp.get("sl", {}).get("recommended", 0),
            "Risk%":           tp.get("sl", {}).get("risk_pct", 0),
            "TP1":             tp.get("tp", {}).get("tp1", 0),
            "TP1%":            tp.get("tp", {}).get("tp1_pct", 0),
            "TP2":             tp.get("tp", {}).get("tp2", 0),
            "TP2%":            tp.get("tp", {}).get("tp2_pct", 0),
            "RR":              tp.get("tp", {}).get("rr", 0),
            "MaxLot":          tp.get("position", {}).get("lot", 1),
        })
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")

# ============================================================
# WATCHLIST & PORTFOLIO
# ============================================================
def get_watchlist():
    if "watchlist" not in st.session_state: st.session_state.watchlist = {}
    return st.session_state.watchlist

def add_to_watchlist(ticker, note="", alert_price=None, scan_result=None):
    wl = get_watchlist()
    wl[ticker] = {
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": note, "alert_price": alert_price,
        "last_score":    scan_result.get("score")    if scan_result else None,
        "last_price":    scan_result.get("price")    if scan_result else None,
        "last_category": scan_result.get("category") if scan_result else None,
    }
    st.session_state.watchlist = wl

def remove_from_watchlist(ticker):
    wl = get_watchlist()
    if ticker in wl:
        del wl[ticker]
        st.session_state.watchlist = wl

def get_portfolio():
    if "portfolio" not in st.session_state: st.session_state.portfolio = []
    return st.session_state.portfolio

def get_closed_trades():
    if "closed_trades" not in st.session_state: st.session_state.closed_trades = []
    return st.session_state.closed_trades

def add_position(ticker, lot, entry_price, sl=None, tp=None, note=""):
    portfolio = get_portfolio()
    portfolio.append({
        "ticker": ticker, "lot": lot, "lembar": lot * 100,
        "entry": entry_price, "curr": entry_price, "sl": sl, "tp": tp,
        "note": note, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modal": lot * 100 * entry_price,
    })
    st.session_state.portfolio = portfolio

def close_position(ticker, exit_price):
    portfolio = get_portfolio()
    closed    = get_closed_trades()
    for i, pos in enumerate(portfolio):
        if pos["ticker"] == ticker:
            pnl_rp  = (exit_price - pos["entry"]) * pos["lembar"]
            pnl_pct = round(pnl_rp / pos["modal"] * 100, 2)
            closed.append({**pos, "exit": exit_price,
                           "exit_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "pnl_rp": pnl_rp, "pnl_pct": pnl_pct,
                           "outcome": "WIN" if pnl_pct > 0 else "LOSS"})
            portfolio.pop(i)
            st.session_state.portfolio     = portfolio
            st.session_state.closed_trades = closed
            return {"pnl_rp": pnl_rp, "pnl_pct": pnl_pct}
    return None

def get_portfolio_summary(current_prices={}):
    portfolio = get_portfolio()
    for pos in portfolio:
        if pos["ticker"] in current_prices:
            pos["curr"] = current_prices[pos["ticker"]]
    total_modal = sum(p["modal"] for p in portfolio)
    total_value = sum(p["lot"] * 100 * p["curr"] for p in portfolio)
    total_pnl   = total_value - total_modal
    total_pnl_pct = round(total_pnl / total_modal * 100, 2) if total_modal > 0 else 0
    return {"total_modal": total_modal, "total_value": total_value,
            "total_pnl": total_pnl, "total_pnl_pct": total_pnl_pct, "positions": portfolio}

def get_portfolio_stats():
    closed = get_closed_trades()
    if not closed:
        return {"total_trades": 0, "win_rate": 0, "best_trade": 0,
                "worst_trade": 0, "avg_pnl": 0, "profit_factor": 0}
    wins   = [t for t in closed if t["outcome"] == "WIN"]
    losses = [t for t in closed if t["outcome"] == "LOSS"]
    avg_win  = np.mean([t["pnl_pct"] for t in wins])   if wins   else 0
    avg_loss = abs(np.mean([t["pnl_pct"] for t in losses])) if losses else 0
    return {
        "total_trades": len(closed), "win_count": len(wins), "loss_count": len(losses),
        "win_rate": round(len(wins) / len(closed) * 100, 1),
        "best_trade": max(t["pnl_pct"] for t in closed),
        "worst_trade": min(t["pnl_pct"] for t in closed),
        "avg_pnl": round(np.mean([t["pnl_pct"] for t in closed]), 2),
        "profit_factor": round(avg_win * len(wins) / max(avg_loss * len(losses), 0.01), 2),
    }

# ============================================================
# SCAN FUNCTION
# ============================================================
def run_scan(tickers_list, progress_bar=None, ihsg_closes=None,
             sector_momentum=None, rti_data=None):
    results    = []
    total      = len(tickers_list)
    batch_size = 10
    for i in range(0, total, batch_size):
        batch = tickers_list[i:i + batch_size]
        if progress_bar:
            progress_bar.progress(
                min((i + len(batch)) / total, 1.0),
                f"Scanning {i+1}-{min(i+len(batch),total)}/{total}..."
            )
        results.extend(fetch_batch(batch, ihsg_closes, sector_momentum, rti_data))
        time.sleep(0.1)
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return results

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

# ─── SNIPER FX FUNCTIONS ────────────────────────────────────────
# ============================================================
# CONFIG & CONSTANTS
# ============================================================

MAJOR_PAIRS = {
    "EURUSD": "EUR/USD", "GBPUSD": "GBP/USD", "USDJPY": "USD/JPY",
    "USDCHF": "USD/CHF", "AUDUSD": "AUD/USD", "USDCAD": "USD/CAD",
    "NZDUSD": "NZD/USD"
}
MINOR_PAIRS = {
    "EURJPY": "EUR/JPY", "EURGBP": "EUR/GBP", "EURCAD": "EUR/CAD",
    "EURAUD": "EUR/AUD", "EURNZD": "EUR/NZD", "EURCHF": "EUR/CHF",
    "GBPJPY": "GBP/JPY", "GBPCAD": "GBP/CAD", "GBPAUD": "GBP/AUD",
    "GBPNZD": "GBP/NZD", "GBPCHF": "GBP/CHF", "AUDJPY": "AUD/JPY",
    "AUDCAD": "AUD/CAD", "AUDNZD": "AUD/NZD", "AUDCHF": "AUD/CHF",
    "CADJPY": "CAD/JPY", "CHFJPY": "CHF/JPY", "NZDJPY": "NZD/JPY",
    "NZDCAD": "NZD/CAD", "NZDCHF": "NZD/CHF", "CADCHF": "CAD/CHF"
}
COMMODITY_PAIRS = {
    "XAUUSD": "Gold/USD",   # Gold
}
ALL_PAIRS = {**MAJOR_PAIRS, **MINOR_PAIRS, **COMMODITY_PAIRS}
JPY_PAIRS = [p for p in ALL_PAIRS if "JPY" in p]

# yfinance symbol mapping (some pairs use different symbols)
YF_SYMBOL_MAP = {
    "XAUUSD": "GC=F",   # Gold futures
}

def get_yf_symbol(symbol):
    """Get correct yfinance symbol for a pair."""
    return YF_SYMBOL_MAP.get(symbol, symbol + "=X")

def get_pip(symbol):
    if symbol in JPY_PAIRS: return 0.01
    if symbol == "XAUUSD":  return 0.1   # Gold: 1 pip = $0.10
    return 0.0001

# ============================================================
# CSS — Military Dark Theme
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700;900&display=swap');
:root {
    --bg:   #050a0e; --bg2: #0a1520; --card: #0d1e2e;
    --green:#00ff88; --red: #ff3355; --gold: #ffd700;
    --blue: #00bfff; --org: #ff8c00;
    --txt:  #e0f0ff; --muted:#5a7a9a; --border:#1a3a5c;
}
*{font-family:'Exo 2',sans-serif}
.stApp{background:var(--bg);color:var(--txt)}
section[data-testid="stSidebar"]{background:var(--bg2)!important;border-right:1px solid var(--border)!important}
section[data-testid="stSidebar"] *{color:var(--txt)!important}
h1,h2,h3{font-family:'Exo 2',sans-serif;font-weight:900;letter-spacing:2px}
.metric-box{background:var(--card);border:1px solid var(--border);border-radius:4px;
    padding:12px 16px;text-align:center;position:relative;overflow:hidden}
.metric-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--green)}
.metric-label{font-size:10px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;font-family:'Share Tech Mono',monospace}
.metric-value{font-size:22px;font-weight:900;color:var(--green);font-family:'Share Tech Mono',monospace}
.signal-card{background:var(--card);border:1px solid var(--border);border-radius:6px;
    padding:16px;margin:8px 0}
.signal-card.buy{border-left:4px solid var(--green)}
.signal-card.sell{border-left:4px solid var(--red)}
.signal-card.neutral{border-left:4px solid var(--muted)}
.score-bar-bg{background:#0a1520;border-radius:2px;height:6px;overflow:hidden;margin:4px 0}
.badge{display:inline-block;padding:2px 10px;border-radius:3px;font-size:11px;font-weight:700;letter-spacing:1px;font-family:'Share Tech Mono',monospace}
.b-sniper{background:#ffd70022;color:#ffd700;border:1px solid #ffd700}
.b-strong{background:#00ff8822;color:#00ff88;border:1px solid #00ff88}
.b-setup{background:#00ff8811;color:#00cc66;border:1px solid #00cc66}
.b-watch{background:#ff8c0022;color:#ff8c00;border:1px solid #ff8c00}
.b-wait{background:#5a7a9a22;color:#5a7a9a;border:1px solid #5a7a9a}
.b-avoid{background:#33111122;color:#443333;border:1px solid #331111}
.stTabs [data-baseweb="tab-list"]{background:var(--bg2)!important;border-bottom:1px solid var(--border)!important}
.stTabs [data-baseweb="tab"]{color:var(--muted)!important;font-family:'Share Tech Mono',monospace!important;font-size:12px!important;letter-spacing:1px!important}
.stTabs [aria-selected="true"]{color:var(--green)!important;border-bottom:2px solid var(--green)!important;background:var(--card)!important}
.stButton button{background:transparent!important;border:1px solid var(--green)!important;
    color:var(--green)!important;font-family:'Share Tech Mono',monospace!important;letter-spacing:2px!important;font-size:12px!important}
.stButton button:hover{background:var(--green)!important;color:var(--bg)!important}
.conf-tag{display:inline-block;background:#0d1e2e;border:1px solid #1a3a5c;border-radius:3px;
    padding:2px 7px;font-size:10px;margin:2px 2px;color:#7a9abf;font-family:'Share Tech Mono',monospace}
.conf-pos{border-color:#00ff8844!important;color:#00ff88!important}
.conf-neg{border-color:#ff335544!important;color:#ff3355!important}
.info-row{display:flex;justify-content:space-between;align-items:center;
    padding:7px 0;border-bottom:1px solid #0d1e2e;font-size:12px}
.info-row:last-child{border-bottom:none}
hr{border-color:var(--border)!important}
.hdr{background:linear-gradient(135deg,#050a0e,#0a1e2e,#050a0e);border:1px solid var(--border);
    border-top:3px solid var(--green);padding:22px 30px;margin-bottom:20px}
.hdr-title{font-size:36px;font-weight:900;color:var(--green);letter-spacing:8px;
    font-family:'Share Tech Mono',monospace;text-shadow:0 0 20px #00ff8866}
.hdr-sub{font-size:11px;color:var(--muted);letter-spacing:4px;font-family:'Share Tech Mono',monospace;margin-top:4px}
.sess-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.alert-box{background:#0d1e2e;border:1px solid var(--border);border-left:4px solid var(--gold);
    padding:12px 16px;border-radius:0 4px 4px 0;font-size:13px;margin:8px 0}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION HELPERS
# ============================================================

def get_active_sessions():
    h = datetime.utcnow().hour
    active = []
    if h >= 21 or h < 6:  active.append("Sydney")
    if 0 <= h < 9:        active.append("Tokyo")
    if 7 <= h < 16:       active.append("London")
    if 12 <= h < 21:      active.append("New York")
    return active

def get_session_score(active):
    if "London" in active and "New York" in active:
        return 100, "🔥 London-NY Overlap — HIGHEST volatility"
    if "London" in active:  return 85, "⚡ London Open — High volatility"
    if "New York" in active: return 80, "⚡ New York Session — Good volatility"
    if "Tokyo" in active:   return 50, "〽️ Tokyo Session — JPY pairs active"
    if "Sydney" in active:  return 30, "💤 Sydney Only — Low volatility"
    return 20, "💤 Dead Zone — Avoid scalping"

# ============================================================
# DATA FETCHING — Twelve Data (primary) + yfinance (fallback)
# ============================================================

# Twelve Data interval mapping
TD_INTERVAL = {
    "1m":"1min","5m":"5min","15m":"15min","30m":"30min",
    "1h":"1h","4h":"4h","1d":"1day"
}
# Twelve Data outputsize per interval (max candles)
TD_OUTPUTSIZE = {
    "1m":390,"5m":200,"15m":200,"30m":150,
    "1h":150,"4h":120,"1d":150
}
# Twelve Data symbol format (forex = "EUR/USD", gold = "XAU/USD")
def get_td_symbol(symbol):
    if symbol == "XAUUSD": return "XAU/USD"
    if len(symbol) == 6:   return symbol[:3] + "/" + symbol[3:]
    return symbol

@st.cache_data(ttl=120, show_spinner=False)
def fetch_data(symbol, period="5d", interval="5m"):
    import time

    # ── Try Twelve Data first (free, no rate limit issues) ──
    td_sym  = get_td_symbol(symbol)
    td_iv   = TD_INTERVAL.get(interval, "5min")
    td_size = TD_OUTPUTSIZE.get(interval, 200)
    try:
        url = (f"https://api.twelvedata.com/time_series"
               f"?symbol={td_sym}&interval={td_iv}&outputsize={td_size}"
               f"&format=JSON&timezone=UTC")
        resp = requests.get(url, timeout=15)
        data = resp.json()
        if data.get("status") == "ok" and data.get("values"):
            rows = data["values"]
            df = pd.DataFrame(rows)
            df = df.rename(columns={"datetime":"Date","open":"Open","high":"High",
                                     "low":"Low","close":"Close","volume":"Volume"})
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date").sort_index()
            for col in ["Open","High","Low","Close"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            if "Volume" in df.columns:
                df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0)
            else:
                df["Volume"] = 0
            df = df[["Open","High","Low","Close","Volume"]].dropna(subset=["Open","High","Low","Close"])
            if len(df) >= 30:
                return df
    except Exception:
        pass

    # ── Fallback: yfinance ──
    yf_sym = get_yf_symbol(symbol)
    periods_to_try = {"5d":["5d","7d"],"30d":["30d","60d"],"60d":["60d","90d"]}.get(period,[period])
    for attempt, p in enumerate(periods_to_try):
        try:
            if attempt > 0: time.sleep(2)
            df = yf.download(yf_sym, period=p, interval=interval,
                             auto_adjust=True, progress=False, timeout=20)
            if df is None or df.empty: continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c[0] for c in df.columns]
            df = df[["Open","High","Low","Close","Volume"]].dropna()
            if len(df) >= 30: return df
        except Exception as e:
            if "rate" in str(e).lower() or "too many" in str(e).lower():
                time.sleep(3)
            continue
    return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_h1(symbol): return fetch_data(symbol, "30d", "1h")

@st.cache_data(ttl=900, show_spinner=False)
def fetch_h4(symbol): return fetch_data(symbol, "60d", "4h")

# ============================================================
# INDICATORS
# ============================================================

def calc_rsi(c, p=14):
    if len(c) < p+1: return 50.0
    c = np.array(c, dtype=float); d = np.diff(c)
    g = np.where(d>0,d,0.); l = np.where(d<0,-d,0.)
    ag = np.mean(g[:p]); al = np.mean(l[:p])
    for i in range(p,len(g)):
        ag=(ag*(p-1)+g[i])/p; al=(al*(p-1)+l[i])/p
    return round(100-(100/(1+ag/al)) if al>0 else 100., 2)

def calc_ema(v, p):
    v = np.array(v, dtype=float)
    if len(v) < p: return float(np.mean(v))
    k = 2/(p+1); e = np.mean(v[:p])
    for x in v[p:]: e = x*k+e*(1-k)
    return e

def calc_ema_series(v, p):
    v = np.array(v, dtype=float)
    r = np.full(len(v), np.nan)
    if len(v) < p: return r
    r[p-1] = np.mean(v[:p]); k = 2/(p+1)
    for i in range(p,len(v)): r[i] = v[i]*k+r[i-1]*(1-k)
    return r

def calc_macd(c):
    if len(c) < 35: return 0,0,0
    e12=calc_ema_series(c,12); e26=calc_ema_series(c,26)
    ml=e12-e26; valid=ml[~np.isnan(ml)]
    if len(valid)<9: return 0,0,0
    sig=calc_ema_series(valid,9)
    if np.isnan(sig[-1]): return 0,0,0
    return round(valid[-1],6), round(sig[-1],6), round(valid[-1]-sig[-1],6)

def calc_atr(h,l,c,p=14):
    if len(c)<p+1: return 0.001
    h=np.array(h,dtype=float); l=np.array(l,dtype=float); c=np.array(c,dtype=float)
    tr=np.maximum(h[1:]-l[1:],np.maximum(abs(h[1:]-c[:-1]),abs(l[1:]-c[:-1])))
    return max(float(np.mean(tr[-p:])), 0.00001)

def calc_adx(h,l,c,p=14):
    if len(c)<p*2: return 20.
    h=np.array(h,dtype=float); l=np.array(l,dtype=float); c=np.array(c,dtype=float)
    tr_a,pd_a,nd_a=[],[],[]
    for i in range(1,len(c)):
        tr=max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1]))
        pdm=h[i]-h[i-1] if h[i]-h[i-1]>l[i-1]-l[i] else 0
        ndm=l[i-1]-l[i] if l[i-1]-l[i]>h[i]-h[i-1] else 0
        tr_a.append(tr); pd_a.append(max(pdm,0)); nd_a.append(max(ndm,0))
    tr_a=np.array(tr_a); pd_a=np.array(pd_a); nd_a=np.array(nd_a)
    atrs=np.convolve(tr_a,np.ones(p)/p,'valid')
    pdi=np.convolve(pd_a,np.ones(p)/p,'valid')/(atrs+1e-10)*100
    ndi=np.convolve(nd_a,np.ones(p)/p,'valid')/(atrs+1e-10)*100
    dx=np.abs(pdi-ndi)/(pdi+ndi+1e-10)*100
    return round(float(np.mean(dx[-p:])) if len(dx)>=p else 20.,1)

def calc_bb(c,p=20,s=2):
    if len(c)<p: v=c[-1]; return v,v*1.001,v*0.999
    arr=np.array(c[-p:],dtype=float); m=np.mean(arr); std=np.std(arr)
    return round(m,5),round(m+s*std,5),round(m-s*std,5)

def calc_stoch(h,l,c,k=14,d=3):
    if len(c)<k: return 50.,50.
    hh=np.max(np.array(h[-k:],dtype=float)); ll=np.min(np.array(l[-k:],dtype=float))
    if hh==ll: return 50.,50.
    kv=(float(c[-1])-ll)/(hh-ll)*100
    return round(kv,1), round(kv,1)

# ============================================================
# SMC ENGINE
# ============================================================

def market_structure(df):
    if df is None or len(df)<20: return "RANGING",False,False
    c=df["Close"].values; h=df["High"].values; l=df["Low"].values

    def pivots(arr,n=3):
        pts=[]
        for i in range(n,len(arr)-n):
            if all(arr[i]>arr[i-j] for j in range(1,n+1)) and all(arr[i]>arr[i+j] for j in range(1,n+1)):
                pts.append((i,arr[i],"H"))
            elif all(arr[i]<arr[i-j] for j in range(1,n+1)) and all(arr[i]<arr[i+j] for j in range(1,n+1)):
                pts.append((i,arr[i],"L"))
        return pts

    pts=pivots(c)
    if len(pts)<4: return "RANGING",False,False
    sh=[(i,v) for i,v,t in pts if t=="H"][-4:]
    sl=[(i,v) for i,v,t in pts if t=="L"][-4:]
    if not sh or not sl: return "RANGING",False,False

    cp=c[-1]; lh=sh[-1][1]; ll_=sl[-1][1]
    bias="RANGING"; bos=False; choch=False

    if len(sh)>=2 and len(sl)>=2:
        hh=sh[-1][1]>sh[-2][1]; hl=sl[-1][1]>sl[-2][1]
        lh_=sh[-1][1]<sh[-2][1]; ll=sl[-1][1]<sl[-2][1]
        if hh and hl:
            bias="BULLISH"
            if cp>lh: bos=True
            if ll: choch=True
        elif lh_ and ll:
            bias="BEARISH"
            if cp<ll_: bos=True
            if hh: choch=True

    return bias,bos,choch

def order_blocks(df, n=60):
    if df is None or len(df)<n: return []
    s=df.tail(n); o=s["Open"].values; c=s["Close"].values
    h=s["High"].values; l=s["Low"].values; cp=c[-1]
    obs=[]
    for i in range(2,len(c)-3):
        rng=h[i]-l[i]
        if rng<1e-6: continue
        if c[i]<o[i]:  # bearish → potential bullish OB
            nb=sum(1 for j in range(i+1,min(i+4,len(c))) if c[j]>o[j])
            if nb>=2 and cp>l[i]:
                mv=c[min(i+3,len(c)-1)]-c[i]
                obs.append({"type":"BULL","high":round(h[i],5),"low":round(l[i],5),
                            "mid":round((h[i]+l[i])/2,5),"str":min(100,int(abs(mv)/(rng+1e-8)*30)),"age":len(c)-i})
        elif c[i]>o[i]:  # bullish → potential bearish OB
            nb=sum(1 for j in range(i+1,min(i+4,len(c))) if c[j]<o[j])
            if nb>=2 and cp<h[i]:
                mv=c[i]-c[min(i+3,len(c)-1)]
                obs.append({"type":"BEAR","high":round(h[i],5),"low":round(l[i],5),
                            "mid":round((h[i]+l[i])/2,5),"str":min(100,int(abs(mv)/(rng+1e-8)*30)),"age":len(c)-i})
    bull=sorted([o for o in obs if o["type"]=="BULL"],key=lambda x:-x["str"])[:3]
    bear=sorted([o for o in obs if o["type"]=="BEAR"],key=lambda x:-x["str"])[:3]
    return bull+bear

def fvg_zones(df, n=30):
    if df is None or len(df)<10: return []
    s=df.tail(n); h=s["High"].values; l=s["Low"].values; c=s["Close"].values
    fvgs=[]; cp=c[-1]
    for i in range(1,len(h)-1):
        if l[i+1]>h[i-1] and not cp<=l[i+1]:
            fvgs.append({"type":"BULL","top":round(l[i+1],5),"bot":round(h[i-1],5),
                        "mid":round((l[i+1]+h[i-1])/2,5),"age":len(h)-i})
        elif h[i+1]<l[i-1] and not cp>=h[i+1]:
            fvgs.append({"type":"BEAR","top":round(l[i-1],5),"bot":round(h[i+1],5),
                        "mid":round((l[i-1]+h[i+1])/2,5),"age":len(h)-i})
    return sorted([f for f in fvgs if f["age"]<=15], key=lambda x:x["age"])[:4]

def premium_discount(df):
    if df is None or len(df)<20: return 50.,"EQ"
    h=np.max(df["High"].values[-20:]); l=np.min(df["Low"].values[-20:])
    cp=float(df["Close"].values[-1])
    if h==l: return 50.,"EQ"
    pct=(cp-l)/(h-l)*100
    zone="PREMIUM" if pct>65 else "DISCOUNT" if pct<35 else "EQ"
    return round(pct,1),zone

# ============================================================
# COT REPORT ENGINE — CFTC Traders in Financial Futures (TFF)
# ============================================================

@st.cache_data(ttl=3600*6, show_spinner=False)  # Cache 6 hours (CFTC updates Friday)
def fetch_cot_data():
    """
    Download COT Traders in Financial Futures report from CFTC.
    Returns DataFrame with latest + historical positions.
    Source: https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
    TFF Report columns we care about:
      - Dealer Net (Commercial — banks/institutions)
      - Asset Manager Net (Large specs — hedge funds)
      - Leveraged Funds Net (Retail/CTA)
    """
    # CFTC TFF historical zip — updated weekly
    cot_url = "https://www.cftc.gov/files/dea/history/fut_fin_xls_{year}.zip"
    current_year = datetime.utcnow().year

    all_dfs = []
    # Fetch last 2 years for COT Index calculation
    for year in [current_year - 1, current_year]:
        url = cot_url.format(year=year)
        try:
            r = requests.get(url, timeout=15)
            if r.status_code != 200:
                continue
            z = zipfile.ZipFile(io.BytesIO(r.content))
            # File inside zip is FinFutYY.xls or similar
            fname = [n for n in z.namelist() if n.endswith(('.xls', '.xlsx', '.csv'))][0]
            with z.open(fname) as f:
                if fname.endswith('.csv'):
                    df = pd.read_csv(f, encoding='latin-1', low_memory=False)
                else:
                    df = pd.read_excel(f, engine='xlrd')
            all_dfs.append(df)
        except Exception:
            continue

    if not all_dfs:
        return None

    df = pd.concat(all_dfs, ignore_index=True)

    # Normalize column names
    df.columns = [str(c).strip().upper() for c in df.columns]

    # Key columns (CFTC TFF report standard names)
    col_map = {
        'MARKET_AND_EXCHANGE_NAMES': 'market',
        'MARKET AND EXCHANGE NAMES': 'market',
        'REPORT_DATE_AS_YYYY_MM_DD': 'date',
        'REPORT DATE AS YYYY-MM-DD': 'date',
        'AS_OF_DATE_IN_FORM_YYMMDD': 'date',
        # Dealer = Commercial/Institutional
        'DEALER_POSITIONS_LONG_ALL': 'dealer_long',
        'DEALER_POSITIONS_SHORT_ALL': 'dealer_short',
        # Asset Manager = Large Speculators / Hedge Funds
        'ASSET_MGR_POSITIONS_LONG_ALL': 'am_long',
        'ASSET_MGR_POSITIONS_SHORT_ALL': 'am_short',
        # Leveraged Funds = Retail speculators
        'LEVERAGED_FUNDS_POSITIONS_LONG_ALL': 'lev_long',
        'LEVERAGED_FUNDS_POSITIONS_SHORT_ALL': 'lev_short',
        # Open Interest
        'OPEN_INTEREST_ALL': 'open_interest',
    }

    # Try to match columns flexibly
    rename = {}
    for orig, new in col_map.items():
        for col in df.columns:
            if orig in col or col in orig:
                rename[col] = new
                break

    df = df.rename(columns=rename)

    needed = ['market', 'date']
    if not all(c in df.columns for c in needed):
        return None

    # Parse date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['market'] = df['market'].str.upper().str.strip()

    # Calculate net positions
    for prefix in ['dealer', 'am', 'lev']:
        lc = f'{prefix}_long'; sc_ = f'{prefix}_short'
        if lc in df.columns and sc_ in df.columns:
            df[f'{prefix}_net'] = pd.to_numeric(df[lc], errors='coerce') - \
                                   pd.to_numeric(df[sc_], errors='coerce')

    return df.sort_values('date').reset_index(drop=True)


def get_cot_for_pair(symbol, cot_df, lookback_weeks=52):
    """
    Extract COT metrics for a specific currency pair.
    Returns dict with:
      - dealer_net: latest net position (institutional)
      - am_net: asset manager net
      - lev_net: leveraged funds (retail) net
      - dealer_net_chg: week-over-week change
      - cot_index: percentile vs last 52 weeks (0-100)
      - signal: BULLISH / BEARISH / NEUTRAL
      - extreme: True if at extreme (>80 or <20 percentile)
      - sentiment: human readable
    """
    if cot_df is None:
        return _cot_empty()

    market_name = COT_MARKET_MAP.get(symbol, "")
    if not market_name:
        return _cot_empty()

    # Filter for this currency
    mask = cot_df['market'].str.contains(market_name, case=False, na=False)
    df_pair = cot_df[mask].copy()

    if len(df_pair) < 4:
        return _cot_empty()

    df_pair = df_pair.sort_values('date').tail(lookback_weeks)

    # Latest row
    latest = df_pair.iloc[-1]
    prev   = df_pair.iloc[-2] if len(df_pair) >= 2 else latest

    # Get net positions (prefer dealer/institutional, fallback to am)
    net_col = 'dealer_net' if 'dealer_net' in df_pair.columns else \
              'am_net' if 'am_net' in df_pair.columns else None

    if net_col is None:
        return _cot_empty()

    dealer_net = float(latest.get('dealer_net', 0) or 0)
    am_net     = float(latest.get('am_net', 0) or 0)
    lev_net    = float(latest.get('lev_net', 0) or 0)

    dealer_prev = float(prev.get('dealer_net', dealer_net) or dealer_net)
    dealer_chg  = dealer_net - dealer_prev

    am_prev = float(prev.get('am_net', am_net) or am_net)
    am_chg  = am_net - am_prev

    # COT Index = percentile of current net vs last N weeks
    net_series = df_pair[net_col].dropna()
    if len(net_series) >= 4:
        mn = net_series.min(); mx = net_series.max()
        cot_index = round((dealer_net - mn) / (mx - mn + 1e-8) * 100, 1) if mx > mn else 50.
    else:
        cot_index = 50.

    # Adjust for inverse pairs (USD is base)
    if symbol in COT_INVERSE:
        cot_index = 100 - cot_index
        dealer_net = -dealer_net
        dealer_chg = -dealer_chg
        am_net = -am_net
        lev_net = -lev_net

    # Signal logic
    extreme = cot_index > 80 or cot_index < 20
    if cot_index >= 65:
        signal = "BULLISH"
        sentiment = f"Institutions NET LONG ({dealer_net:+,.0f}) — bullish bias"
    elif cot_index <= 35:
        signal = "BEARISH"
        sentiment = f"Institutions NET SHORT ({dealer_net:+,.0f}) — bearish bias"
    else:
        signal = "NEUTRAL"
        sentiment = f"Institutions mixed ({dealer_net:+,.0f}) — no strong bias"

    # Extreme reversal warning
    if cot_index > 90:
        sentiment += " ⚠️ EXTREME LONG — reversal risk"
    elif cot_index < 10:
        sentiment += " ⚠️ EXTREME SHORT — reversal risk"

    # Momentum (is positioning getting stronger or weaker?)
    if len(net_series) >= 4:
        recent_trend = net_series.values[-1] - net_series.values[-4]
        cot_momentum = "INCREASING" if recent_trend > 0 else "DECREASING"
    else:
        cot_momentum = "UNKNOWN"

    return {
        "available": True,
        "dealer_net": round(dealer_net),
        "dealer_chg": round(dealer_chg),
        "am_net": round(am_net),
        "am_chg": round(am_chg),
        "lev_net": round(lev_net),
        "cot_index": cot_index,
        "signal": signal,
        "extreme": extreme,
        "sentiment": sentiment,
        "cot_momentum": cot_momentum,
        "report_date": str(latest.get('date', 'N/A'))[:10],
    }

def _cot_empty():
    return {
        "available": False,
        "dealer_net": 0, "dealer_chg": 0,
        "am_net": 0, "am_chg": 0, "lev_net": 0,
        "cot_index": 50., "signal": "NEUTRAL",
        "extreme": False, "sentiment": "COT data unavailable",
        "cot_momentum": "UNKNOWN", "report_date": "N/A",
    }

def cot_score_contribution(cot, direction):
    """
    Calculate how much COT adds/subtracts from sniper score.
    Returns (score_delta, confirmation_delta, signal_text)
    """
    if not cot["available"]:
        return 0, 0, []

    score_delta = 0
    conf_delta  = 0
    sigs = []
    ci = cot["cot_index"]

    if direction == "BUY":
        if cot["signal"] == "BULLISH":
            if ci > 80:
                score_delta += 20; conf_delta += 2
                sigs.append(f"📋 COT: Institutions HEAVILY LONG (Index:{ci:.0f}) — strong bull confirmation")
            elif ci > 65:
                score_delta += 14; conf_delta += 1
                sigs.append(f"📋 COT: Institutions NET LONG (Index:{ci:.0f}) — bull bias confirmed")
            if cot["cot_momentum"] == "INCREASING":
                score_delta += 6; conf_delta += 1
                sigs.append(f"📋 COT Momentum: Institutional longs INCREASING week-over-week")
        elif cot["signal"] == "BEARISH":
            score_delta -= 15
            sigs.append(f"📋 COT WARNING: Institutions SHORT while you BUY (Index:{ci:.0f}) — risk!")
        if cot["extreme"] and ci < 20:
            score_delta += 8  # Extreme short = mean reversion buy
            sigs.append(f"📋 COT EXTREME SHORT (Index:{ci:.0f}) — contrarian buy signal")

    elif direction == "SELL":
        if cot["signal"] == "BEARISH":
            if ci < 20:
                score_delta += 20; conf_delta += 2
                sigs.append(f"📋 COT: Institutions HEAVILY SHORT (Index:{ci:.0f}) — strong bear confirmation")
            elif ci < 35:
                score_delta += 14; conf_delta += 1
                sigs.append(f"📋 COT: Institutions NET SHORT (Index:{ci:.0f}) — bear bias confirmed")
            if cot["cot_momentum"] == "DECREASING":
                score_delta += 6; conf_delta += 1
                sigs.append(f"📋 COT Momentum: Institutional shorts INCREASING week-over-week")
        elif cot["signal"] == "BULLISH":
            score_delta -= 15
            sigs.append(f"📋 COT WARNING: Institutions LONG while you SELL (Index:{ci:.0f}) — risk!")
        if cot["extreme"] and ci > 80:
            score_delta += 8  # Extreme long = mean reversion sell
            sigs.append(f"📋 COT EXTREME LONG (Index:{ci:.0f}) — contrarian sell signal")

    return score_delta, conf_delta, sigs


# ============================================================
# MAIN ANALYSIS ENGINE
# ============================================================

def analyze(symbol, cot_df=None):
    r={
        "symbol":symbol,"name":ALL_PAIRS.get(symbol,symbol),
        "score":0,"direction":"NEUTRAL","rating":"🚫 AVOID",
        "confirmations":0,"signals":[],"warnings":[],
        "price":0.,"atr":0.,"rsi":50.,"macd":0.,"macd_hist":0.,
        "adx":20.,"stoch_k":50.,"stoch_d":50.,"bb_pct":50.,
        "bias":"RANGING","bos":False,"choch":False,
        "premium_pct":50.,"premium_zone":"EQ",
        "order_blocks":[],"fvg":[],"buy_s":0,"sell_s":0,
        "sl_pips":0,"tp1_pips":0,"tp2_pips":0,"rr_ratio":0.,
        "sl_price":0.,"tp1_price":0.,"tp2_price":0.,
        "h1_trend":"N/A","h4_bias":"N/A","m5_momentum":"N/A",
        "cot": _cot_empty(),
    }

    df5=fetch_data(symbol,"5d","5m")
    dfh1=fetch_h1(symbol)
    dfh4=fetch_h4(symbol)

    if df5 is None or len(df5)<50:
        r["signals"].append("⚠️ Insufficient data"); return r

    c5=df5["Close"].values; h5=df5["High"].values; l5=df5["Low"].values
    cp=float(c5[-1]); pip=get_pip(symbol)
    atr=calc_atr(h5,l5,c5); r["price"]=round(cp,5); r["atr"]=round(atr,5)

    score=0; conf=0; buy_s=0; sell_s=0
    sigs=[]; warns=[]

    # ── LAYER 1: H4 STRUCTURE ──
    bias,bos,choch=market_structure(dfh4)
    r["bias"]=bias; r["bos"]=bos; r["choch"]=choch

    if bias=="BULLISH":   score+=15;buy_s+=1;conf+=1;sigs.append("📈 H4 BULLISH structure (HH/HL)")
    elif bias=="BEARISH": score+=15;sell_s+=1;conf+=1;sigs.append("📉 H4 BEARISH structure (LH/LL)")
    else:                 score-=5;warns.append("↔️ H4: Ranging — no clear bias")

    if bos:
        score+=12;conf+=1
        if bias=="BULLISH": buy_s+=1;sigs.append("💥 BOS Bullish — structure confirmed")
        else: sell_s+=1;sigs.append("💥 BOS Bearish — structure confirmed")
    if choch:
        score+=8;conf+=1
        sigs.append("🔄 CHoCH — Change of Character (reversal signal)")
        if bias=="BULLISH": sell_s+=1
        else: buy_s+=1

    # H1 trend
    if dfh1 is not None and len(dfh1)>=50:
        c1=dfh1["Close"].values
        e20=calc_ema(c1,20); e50=calc_ema(c1,50)
        if c1[-1]>e20>e50: score+=8;buy_s+=1;conf+=1;sigs.append("📊 H1: Bullish (price>EMA20>EMA50)"); r["h1_trend"]="BULL"
        elif c1[-1]<e20<e50: score+=8;sell_s+=1;conf+=1;sigs.append("📊 H1: Bearish (price<EMA20<EMA50)"); r["h1_trend"]="BEAR"
        else: warns.append("〽️ H1: Mixed trend"); r["h1_trend"]="MIXED"

    # Premium/Discount
    pp,pz=premium_discount(dfh4)
    r["premium_pct"]=pp; r["premium_zone"]=pz
    if pz=="DISCOUNT" and bias=="BULLISH":   score+=10;buy_s+=1;conf+=1;sigs.append(f"💎 DISCOUNT zone ({pp:.0f}%) — ideal buy")
    elif pz=="PREMIUM" and bias=="BEARISH":  score+=10;sell_s+=1;conf+=1;sigs.append(f"💎 PREMIUM zone ({pp:.0f}%) — ideal sell")
    elif pz=="PREMIUM" and bias=="BULLISH":  score-=8;warns.append(f"⚠️ Premium zone ({pp:.0f}%) — expensive to buy")
    elif pz=="DISCOUNT" and bias=="BEARISH": score-=8;warns.append(f"⚠️ Discount zone ({pp:.0f}%) — risky to sell")

    # ── LAYER 2: SMC ZONES ──
    obs=order_blocks(dfh1 if dfh1 is not None else df5)
    fvgs=fvg_zones(df5)
    r["order_blocks"]=obs[:4]; r["fvg"]=fvgs[:3]

    bull_ob=[o for o in obs if o["type"]=="BULL"]
    bear_ob=[o for o in obs if o["type"]=="BEAR"]
    at_bull=any(o["low"]<=cp<=o["high"]*1.002 for o in bull_ob)
    at_bear=any(o["low"]*0.998<=cp<=o["high"] for o in bear_ob)

    if at_bull:   score+=18;buy_s+=1;conf+=2;sigs.append("🟩 AT Bullish OB — HIGH PROB buy zone")
    elif bull_ob: score+=5;sigs.append(f"🟩 Bullish OB support @ {bull_ob[0]['mid']:.5f}")
    if at_bear:   score+=18;sell_s+=1;conf+=2;sigs.append("🟥 AT Bearish OB — HIGH PROB sell zone")
    elif bear_ob: score+=5;sigs.append(f"🟥 Bearish OB resistance @ {bear_ob[0]['mid']:.5f}")

    bull_fvg=[f for f in fvgs if f["type"]=="BULL"]
    bear_fvg=[f for f in fvgs if f["type"]=="BEAR"]
    if bull_fvg:
        nf=min(bull_fvg,key=lambda x:abs(x["mid"]-cp))
        if abs(nf["mid"]-cp)<atr*0.5: score+=12;buy_s+=1;conf+=1;sigs.append(f"🔷 Entering Bullish FVG {nf['bot']:.5f}–{nf['top']:.5f}")
        else: sigs.append(f"🔷 Bullish FVG nearby @ {nf['mid']:.5f}")
    if bear_fvg:
        nf=min(bear_fvg,key=lambda x:abs(x["mid"]-cp))
        if abs(nf["mid"]-cp)<atr*0.5: score+=12;sell_s+=1;conf+=1;sigs.append(f"🔶 Entering Bearish FVG {nf['bot']:.5f}–{nf['top']:.5f}")
        else: sigs.append(f"🔶 Bearish FVG nearby @ {nf['mid']:.5f}")

    # ── LAYER 3: CLASSIC INDICATORS ──
    rsi=calc_rsi(c5); r["rsi"]=rsi
    ml,ms,mh=calc_macd(c5); r["macd"]=ml; r["macd_hist"]=mh
    adx=calc_adx(h5,l5,c5); r["adx"]=adx
    sk,sd=calc_stoch(h5,l5,c5); r["stoch_k"]=sk; r["stoch_d"]=sd
    bm,bu,bl=calc_bb(c5); rng=bu-bl
    bbp=((cp-bl)/rng*100) if rng>0 else 50; r["bb_pct"]=round(bbp,1)

    # RSI
    if 30<=rsi<=45 and bias=="BULLISH":   score+=12;buy_s+=1;conf+=1;sigs.append(f"📊 RSI {rsi} — Oversold in uptrend (ideal buy)")
    elif 55<=rsi<=70 and bias=="BEARISH": score+=12;sell_s+=1;conf+=1;sigs.append(f"📊 RSI {rsi} — Overbought in downtrend (ideal sell)")
    elif rsi<30:  score+=6;buy_s+=1;sigs.append(f"📊 RSI {rsi} — Extreme oversold")
    elif rsi>70:  score+=6;sell_s+=1;sigs.append(f"📊 RSI {rsi} — Extreme overbought")
    else: warns.append(f"📊 RSI {rsi} — Neutral zone")

    # MACD
    if mh>0 and ml>0:   score+=8;buy_s+=1;conf+=1;sigs.append("📈 MACD Bullish — above zero, hist positive")
    elif mh<0 and ml<0: score+=8;sell_s+=1;conf+=1;sigs.append("📉 MACD Bearish — below zero, hist negative")
    if len(c5)>=36:
        pm,ps,ph=calc_macd(c5[:-1])
        if ph<0 and mh>0: score+=10;buy_s+=1;conf+=1;sigs.append("⚡ MACD Bullish Cross just fired!")
        elif ph>0 and mh<0: score+=10;sell_s+=1;conf+=1;sigs.append("⚡ MACD Bearish Cross just fired!")

    # ADX
    if adx>35:    score+=10;conf+=1;sigs.append(f"💪 ADX {adx} — STRONG trend")
    elif adx>25:  score+=6;sigs.append(f"📏 ADX {adx} — Trending")
    else:         score-=5;warns.append(f"😴 ADX {adx} — Weak/choppy")

    # Stochastic
    if sk<25 and bias=="BULLISH":   score+=8;buy_s+=1;conf+=1;sigs.append(f"🔽 Stoch {sk:.0f} — Oversold, bull setup")
    elif sk>75 and bias=="BEARISH": score+=8;sell_s+=1;conf+=1;sigs.append(f"🔼 Stoch {sk:.0f} — Overbought, bear setup")

    # BB
    if bbp<15:   score+=8;buy_s+=1;sigs.append(f"📉 BB lower band touch ({bbp:.0f}%)")
    elif bbp>85: score+=8;sell_s+=1;sigs.append(f"📈 BB upper band touch ({bbp:.0f}%)")

    # EMA M5
    if len(c5)>=50:
        e8=calc_ema(c5,8); e21=calc_ema(c5,21)
        if e8>e21 and cp>e8:   score+=7;buy_s+=1;sigs.append("📈 M5 EMA8>EMA21 — bullish momentum")
        elif e8<e21 and cp<e8: score+=7;sell_s+=1;sigs.append("📉 M5 EMA8<EMA21 — bearish momentum")

    # ── LAYER 4: SESSION ──
    active=get_active_sessions()
    ss,sn=get_session_score(active)
    if ss>=85:   score+=15;conf+=1;sigs.append(f"⏰ {sn}")
    elif ss>=50: score+=8;sigs.append(f"⏰ {sn}")
    else:        score-=15;warns.append(f"⏰ {sn}")

    if "JPY" in symbol and "Tokyo" in active:   score+=8;conf+=1;sigs.append("🗾 JPY pair — Tokyo session active")
    if "GBP" in symbol and "London" in active:  score+=6;sigs.append("🇬🇧 GBP pair — London session active")
    if "EUR" in symbol and "London" in active:  score+=5;sigs.append("🇪🇺 EUR pair — London session active")
    if "USD" in symbol and "New York" in active: score+=5;sigs.append("🇺🇸 USD pair — NY session active")

    # ── LAYER 5: M5 ENTRY TRIGGER ──
    if len(c5)>=5:
        co=df5["Open"].values; ch=h5; cl=l5
        # Bullish engulfing
        if c5[-2]<co[-2] and c5[-1]>co[-1] and c5[-1]>co[-2] and co[-1]<c5[-2]:
            score+=10;buy_s+=1;conf+=1;sigs.append("🕯️ Bullish Engulfing — strong buy trigger")
        # Bearish engulfing
        elif c5[-2]>co[-2] and c5[-1]<co[-1] and c5[-1]<co[-2] and co[-1]>c5[-2]:
            score+=10;sell_s+=1;conf+=1;sigs.append("🕯️ Bearish Engulfing — strong sell trigger")
        # Hammer / Shooting star
        body=abs(c5[-1]-co[-1]); lw=min(c5[-1],co[-1])-cl[-1]; uw=ch[-1]-max(c5[-1],co[-1])
        if body>0:
            if lw>body*2 and uw<body*0.5: score+=8;buy_s+=1;sigs.append("🔨 Hammer pattern")
            elif uw>body*2 and lw<body*0.5: score+=8;sell_s+=1;sigs.append("⭐ Shooting Star pattern")
        # Pin bar
        tr_=ch[-1]-cl[-1]
        if tr_>0 and abs(c5[-1]-co[-1])/tr_<0.3:
            if lw>uw and bias=="BULLISH": score+=6;buy_s+=1;sigs.append("📌 Bullish Pin Bar")
            elif uw>lw and bias=="BEARISH": score+=6;sell_s+=1;sigs.append("📌 Bearish Pin Bar")

    # Momentum M5
    if len(c5)>=5:
        mom=c5[-1]-c5[-5]
        if mom>atr*0.3:   score+=5;buy_s+=1;sigs.append("⚡ Strong bullish M5 momentum"); r["m5_momentum"]="BULL"
        elif mom<-atr*0.3: score+=5;sell_s+=1;sigs.append("⚡ Strong bearish M5 momentum"); r["m5_momentum"]="BEAR"

    # Volume
    if df5["Volume"].sum()>0:
        av=np.mean(df5["Volume"].values[-20:]); cv=df5["Volume"].values[-1]
        if av>0:
            vr=cv/av
            if vr>1.8: score+=8;conf+=1;sigs.append(f"📊 Volume spike {vr:.1f}x — institutional")
            elif vr<0.4: score-=5;warns.append(f"📊 Low volume {vr:.1f}x — thin market")

    # ── LAYER 4b: COT REPORT (CFTC) ──
    cot = get_cot_for_pair(symbol, cot_df)
    r["cot"] = cot

    # ── CONFLICT PENALTIES ──
    if bias=="BULLISH" and rsi>72: score-=10;warns.append("⚠️ RSI overbought vs bullish bias")
    if bias=="BEARISH" and rsi<28: score-=10;warns.append("⚠️ RSI oversold vs bearish bias")
    if adx<18 and bos: score-=8;warns.append("⚠️ BOS but ADX very weak — false signal risk")

    # ── DETERMINE DIRECTION FIRST ──
    if buy_s>sell_s: direction="BUY"
    elif sell_s>buy_s: direction="SELL"
    else: direction="NEUTRAL"

    # ── COT CONTRIBUTION (applied after direction known) ──
    cot_score_d, cot_conf_d, cot_sigs = cot_score_contribution(cot, direction)
    score += cot_score_d
    conf  += cot_conf_d
    sigs  += cot_sigs

    # ── NORMALIZE & COUNTER-TREND PENALTY ──

    if direction=="BUY" and bias=="BEARISH":   score=int(score*0.6);warns.append("⚠️ BUY vs H4 BEARISH — counter-trend!")
    elif direction=="SELL" and bias=="BULLISH": score=int(score*0.6);warns.append("⚠️ SELL vs H4 BULLISH — counter-trend!")

    final=min(100,max(0,round((score+40)/2.4)))

    if final>=80 and conf>=6:   rating="🎯 SNIPER"
    elif final>=72 and conf>=5: rating="⚡ STRONG"
    elif final>=60 and conf>=4: rating="✅ SETUP"
    elif final>=45 and conf>=3: rating="👀 WATCH"
    elif final>=30:             rating="⏳ WAIT"
    else:                       rating="🚫 AVOID"

    if direction=="NEUTRAL" and rating in ["🎯 SNIPER","⚡ STRONG"]: rating="✅ SETUP"

    # ── SL/TP ──
    sl_d=atr*1.5; tp1_d=atr*2.5; tp2_d=atr*4.5
    sl_p=round(sl_d/pip); tp1_p=round(tp1_d/pip); tp2_p=round(tp2_d/pip)
    if direction=="BUY":
        slpr=round(cp-sl_d,5); tp1pr=round(cp+tp1_d,5); tp2pr=round(cp+tp2_d,5)
    elif direction=="SELL":
        slpr=round(cp+sl_d,5); tp1pr=round(cp-tp1_d,5); tp2pr=round(cp-tp2_d,5)
    else:
        slpr=tp1pr=tp2pr=cp
    rr=round(tp1_p/sl_p,2) if sl_p>0 else 0

    r.update({"score":final,"direction":direction,"rating":rating,"confirmations":conf,
               "signals":sigs,"warnings":warns,"buy_s":buy_s,"sell_s":sell_s,
               "sl_pips":sl_p,"tp1_pips":tp1_p,"tp2_pips":tp2_p,
               "sl_price":slpr,"tp1_price":tp1pr,"tp2_price":tp2pr,"rr_ratio":rr})
    return r

# ============================================================
# UI HELPERS
# ============================================================

def sc(score):
    if score>=75: return "#00ff88"
    if score>=60: return "#ffd700"
    if score>=45: return "#ff8c00"
    return "#ff3355"

def dc(d): return {"BUY":"#00ff88","SELL":"#ff3355"}.get(d,"#5a7a9a")

def badge(rating):
    cls={"🎯 SNIPER":"b-sniper","⚡ STRONG":"b-strong","✅ SETUP":"b-setup",
         "👀 WATCH":"b-watch","⏳ WAIT":"b-wait","🚫 AVOID":"b-avoid"}.get(rating,"b-avoid")
    return f"<span class='badge {cls}'>{rating}</span>"

def mcard(col, label, value, color="#00ff88"):
    col.markdown(f"<div class='metric-box'><div class='metric-label'>{label}</div>"
                 f"<div class='metric-value' style='color:{color}'>{value}</div></div>",
                 unsafe_allow_html=True)

def sbar(score, color=None):
    c=color or sc(score)
    return (f"<div class='score-bar-bg'>"
            f"<div style='height:100%;width:{score}%;background:{c};border-radius:2px'></div></div>")

# ============================================================
# COT RENDER HELPER
# ============================================================

def _render_cot_tab(cot, symbol):
    """Render full COT Report panel for a pair."""
    if not cot["available"]:
        st.markdown("""<div class='alert-box'>
        <b style='color:#ffd700'>📋 COT Data Not Loaded</b><br>
        Run a full scan first to load COT data from CFTC.<br>
        <span style='color:#5a7a9a;font-size:11px'>
        Data is updated every Friday after market close (UTC).
        Source: CFTC Traders in Financial Futures (TFF) Report.
        </span></div>""", unsafe_allow_html=True)
        return

    ci = cot["cot_index"]
    sig_color = "#00ff88" if cot["signal"]=="BULLISH" else "#ff3355" if cot["signal"]=="BEARISH" else "#ffd700"
    bar_color  = sig_color

    # COT Index visual gauge
    st.markdown(f"""
    <div style='background:#0d1e2e;border:1px solid #1a3a5c;border-radius:6px;padding:16px;margin-bottom:12px'>
        <div style='font-family:Share Tech Mono;font-size:11px;color:#5a7a9a;letter-spacing:2px;margin-bottom:8px'>
            COT INDEX — INSTITUTIONAL POSITIONING (0=MAX SHORT · 100=MAX LONG)
        </div>
        <div style='display:flex;justify-content:space-between;font-family:Share Tech Mono;
            font-size:10px;color:#1a3a5c;margin-bottom:4px'>
            <span>◀ EXTREME SHORT</span><span>NEUTRAL</span><span>EXTREME LONG ▶</span>
        </div>
        <div style='background:#050a0e;border-radius:3px;height:20px;position:relative;overflow:hidden'>
            <div style='position:absolute;left:50%;top:0;bottom:0;width:1px;background:#1a3a5c'></div>
            <div style='height:100%;width:{ci}%;background:linear-gradient(90deg,#ff3355,#ffd700,#00ff88);
                border-radius:3px;opacity:0.8'></div>
            <div style='position:absolute;top:2px;left:{min(ci,95)}%;font-family:Share Tech Mono;
                font-size:11px;color:#fff;font-weight:900'>{ci:.0f}</div>
        </div>
        <div style='margin-top:10px;font-family:Share Tech Mono;font-size:13px;color:{sig_color};font-weight:700'>
            {cot["signal"]} — {cot["sentiment"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 metric cards
    ca,cb,cc,cd = st.columns(4)
    chg_color = "#00ff88" if cot["dealer_chg"]>0 else "#ff3355"
    am_color  = "#00ff88" if cot["am_net"]>0 else "#ff3355"
    lev_color = "#ff3355" if cot["lev_net"]>0 else "#00ff88"  # retail is contra-indicator

    ca.markdown(f"""<div class='metric-box'>
    <div class='metric-label'>DEALER NET (Inst.)</div>
    <div class='metric-value' style='color:{sig_color};font-size:16px'>{cot["dealer_net"]:+,}</div>
    <div style='font-size:10px;color:{chg_color};font-family:Share Tech Mono'>
        WoW: {cot["dealer_chg"]:+,}</div></div>""", unsafe_allow_html=True)

    cb.markdown(f"""<div class='metric-box'>
    <div class='metric-label'>ASSET MGR NET</div>
    <div class='metric-value' style='color:{am_color};font-size:16px'>{cot["am_net"]:+,}</div>
    <div style='font-size:10px;color:{chg_color};font-family:Share Tech Mono'>
        WoW: {cot["am_chg"]:+,}</div></div>""", unsafe_allow_html=True)

    cc.markdown(f"""<div class='metric-box'>
    <div class='metric-label'>RETAIL (Lev.Funds)</div>
    <div class='metric-value' style='color:{lev_color};font-size:16px'>{cot["lev_net"]:+,}</div>
    <div style='font-size:10px;color:#5a7a9a;font-family:Share Tech Mono'>
        ⚠️ Retail = contra signal</div></div>""", unsafe_allow_html=True)

    mom_color = "#00ff88" if cot["cot_momentum"]=="INCREASING" else "#ff3355" if cot["cot_momentum"]=="DECREASING" else "#5a7a9a"
    cd.markdown(f"""<div class='metric-box'>
    <div class='metric-label'>COT MOMENTUM</div>
    <div class='metric-value' style='color:{mom_color};font-size:14px'>{cot["cot_momentum"]}</div>
    <div style='font-size:10px;color:#5a7a9a;font-family:Share Tech Mono'>
        Report: {cot["report_date"]}</div></div>""", unsafe_allow_html=True)

    # Interpretation guide
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style='background:#050a0e;border:1px solid #1a3a5c;border-radius:4px;
    padding:12px;font-family:Share Tech Mono;font-size:11px;color:#5a7a9a;line-height:2'>
    <b style='color:#7a9abf'>📚 HOW TO READ COT:</b><br>
    ◈ <b style='color:#e0f0ff'>Dealer/Institutional</b> = banks & market makers — follow their NET position<br>
    ◈ <b style='color:#e0f0ff'>Asset Manager</b> = hedge funds & large specs — usually trend followers<br>
    ◈ <b style='color:#ff8c00'>Leveraged Funds (Retail)</b> = small speculators — <b>CONTRA indicator</b> (when retail all long = smart money about to sell)<br>
    ◈ <b style='color:#ffd700'>COT Index &gt;80</b> = institutions max long = strong bullish bias (or potential reversal if extreme)<br>
    ◈ <b style='color:#ffd700'>COT Index &lt;20</b> = institutions max short = strong bearish bias<br>
    ◈ Best setup: COT aligns WITH your technical direction
    </div>""", unsafe_allow_html=True)


# ============================================================
# AI ANALYSIS ENGINE — Claude API
# ============================================================

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def get_api_key():
    """Get Groq API key from environment variable."""
    return os.environ.get("GROQ_API_KEY", "")

def build_ai_prompt(r):
    """Build a rich prompt from pair analysis data for Claude."""
    cot = r.get("cot", _cot_empty())
    cot_info = f"""
COT Report (CFTC):
- Institutional Net Position: {cot.get('dealer_net', 'N/A'):+,} ({cot.get('signal','N/A')})
- COT Index (0-100): {cot.get('cot_index', 50):.0f} — {'EXTREME' if cot.get('extreme') else 'NORMAL'} positioning
- Asset Manager Net: {cot.get('am_net', 'N/A'):+,}
- Retail (Leveraged Funds): {cot.get('lev_net', 'N/A'):+,} ← contra indicator
- Momentum: {cot.get('cot_momentum', 'N/A')}
- Report Date: {cot.get('report_date', 'N/A')}""" if cot.get("available") else "\nCOT Report: Not available"

    obs_info = ""
    if r.get("order_blocks"):
        obs_info = "\nOrder Blocks:\n" + "\n".join(
            f"  - {o['type']} OB: {o['low']:.5f}–{o['high']:.5f} (strength:{o['str']})"
            for o in r["order_blocks"][:3])

    fvg_info = ""
    if r.get("fvg"):
        fvg_info = "\nFair Value Gaps:\n" + "\n".join(
            f"  - {f['type']} FVG: {f['bot']:.5f}–{f['top']:.5f}"
            for f in r["fvg"][:3])

    signals_str = "\n".join(f"  ◈ {s}" for s in r.get("signals", []))
    warnings_str = "\n".join(f"  ⚠ {w}" for w in r.get("warnings", []))

    prompt = f"""You are an elite forex trader and analyst specializing in Smart Money Concepts (SMC), institutional order flow, and precision scalping. Analyze this pair and provide a sharp, professional assessment.

=== PAIR: {r['symbol']} ({r['name']}) ===
Current Price: {r['price']:.5f}
Direction Signal: {r['direction']}
Sniper Score: {r['score']}/100
Rating: {r['rating']}
Confirmations: {r['confirmations']}

=== MULTI-TIMEFRAME BIAS ===
H4 Market Structure: {r.get('bias','N/A')}
H4 Break of Structure: {'YES' if r.get('bos') else 'NO'}
Change of Character: {'YES' if r.get('choch') else 'NO'}
H1 Trend: {r.get('h1_trend','N/A')}
M5 Momentum: {r.get('m5_momentum','N/A')}
Premium/Discount Zone: {r.get('premium_zone','N/A')} ({r.get('premium_pct',50):.0f}%)

=== CLASSIC INDICATORS (M5) ===
RSI (Wilder): {r.get('rsi', 50)}
MACD Histogram: {r.get('macd_hist', 0):+.6f}
ADX: {r.get('adx', 20)} ({'STRONG TREND' if r.get('adx',20)>25 else 'WEAK/RANGING'})
Stochastic %K: {r.get('stoch_k', 50):.0f}
Bollinger Band %: {r.get('bb_pct', 50):.0f}%
ATR: {r.get('atr', 0):.5f}
{cot_info}

=== SMC ZONES ==={obs_info}{fvg_info}

=== CONFIRMED SIGNALS ===
{signals_str if signals_str else '  None'}

=== WARNINGS ===
{warnings_str if warnings_str else '  None'}

=== ENTRY PLAN ===
Direction: {r['direction']}
Entry: {r['price']:.5f}
Stop Loss: {r.get('sl_price', 0):.5f} ({r.get('sl_pips', 0)} pips)
TP1: {r.get('tp1_price', 0):.5f} ({r.get('tp1_pips', 0)} pips)
TP2: {r.get('tp2_price', 0):.5f} ({r.get('tp2_pips', 0)} pips)
Risk:Reward: 1:{r.get('rr_ratio', 0):.1f}

Please provide your analysis in this EXACT structure:

## 🎯 SETUP NARRATIVE
[2-3 sentences explaining WHY this setup exists — what story the chart is telling from institutional perspective]

## 📊 MARKET CONTEXT
[Current market conditions — is this trending, ranging, at key level? What are institutions doing based on COT + structure?]

## ⚡ CONFLUENCE ANALYSIS
[List the 3-5 strongest confluences that make this setup valid or invalid. Be specific about which ones matter most]

## ⚠️ RISK ASSESSMENT
[Honest assessment: what could invalidate this setup? What's the probability? Is the RR worth it?]

## 📋 TRADING PLAN
[Step-by-step execution plan:
1. Entry condition (what needs to happen on M5 before entering)
2. Position sizing recommendation (% risk)
3. Stop loss logic
4. TP1 management (partial close? move SL to BE?)
5. TP2 target
6. What would make you CANCEL this trade]

## 🏆 FINAL VERDICT
[One clear sentence: TAKE THIS TRADE / WAIT FOR BETTER SETUP / AVOID — with confidence level 1-10]

Be direct, specific, and think like a professional trader managing real money. No generic advice."""

    return prompt


def call_groq_api(prompt, api_key):
    """Groq API call — fast, free tier available. Returns (text, error)."""
    try:
        import requests as req
        resp = req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",  # Best free model on Groq
                "max_tokens": 1200,
                "temperature": 0.3,  # Low temp = more consistent trading analysis
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an elite forex trader specializing in Smart Money Concepts (SMC), institutional order flow, and precision scalping. Give sharp, direct, professional analysis in Bahasa Indonesia. No generic advice."
                    },
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )
        if resp.status_code == 200:
            data = resp.json()
            text = data["choices"][0]["message"]["content"] if data.get("choices") else ""
            return text, ""
        elif resp.status_code == 401:
            return "", "❌ Invalid API key — check your GROQ_API_KEY"
        elif resp.status_code == 429:
            return "", "⏳ Rate limited — wait a moment and try again"
        else:
            return "", f"❌ API error {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return "", f"❌ Connection error: {str(e)[:100]}"


def render_chart_tab(r):
    """Render interactive candlestick chart with SMC overlays."""
    symbol = r["symbol"]

    # Timeframe selector
    col_tf1, col_tf2 = st.columns([2, 3])
    with col_tf1:
        tf = st.selectbox("Timeframe", ["1m","5m","15m","30m","1h","4h","1d"],
                          index=1, key=f"tf_{symbol}")
    with col_tf2:
        overlays = st.multiselect("Overlays",
            ["EMA 8/21", "EMA 20/50", "Bollinger Bands", "Order Blocks", "FVG Zones", "Volume"],
            default=["EMA 8/21", "Order Blocks", "FVG Zones"],
            key=f"ov_{symbol}")

    # Map TF to yfinance period
    tf_period = {
        "1m":"1d","5m":"5d","15m":"10d","30m":"30d",
        "1h":"60d","4h":"60d","1d":"365d"
    }.get(tf, "5d")

    with st.spinner(f"Loading {symbol} {tf} chart..."):
        df = fetch_data(symbol, tf_period, tf)

    if df is None or len(df) < 10:
        st.error(f"No chart data available for {symbol} {tf}")
        return

    # Limit to last 150 candles for performance
    df = df.tail(150).copy()
    df = df.reset_index()
    dates = df.iloc[:, 0]  # Date column
    opens  = df["Open"].values
    highs  = df["High"].values
    lows   = df["Low"].values
    closes = df["Close"].values
    volumes = df["Volume"].values if "Volume" in df.columns else None

    has_vol = volumes is not None and volumes.sum() > 0

    # Create subplots
    row_heights = [0.75, 0.25] if has_vol and "Volume" in overlays else [1.0]
    rows = 2 if has_vol and "Volume" in overlays else 1

    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=row_heights
    )

    # ── CANDLESTICK ──
    fig.add_trace(go.Candlestick(
        x=dates,
        open=opens, high=highs, low=lows, close=closes,
        name=symbol,
        increasing_line_color="#00ff88",
        decreasing_line_color="#ff3355",
        increasing_fillcolor="#00ff8844",
        decreasing_fillcolor="#ff335544",
        line_width=1,
    ), row=1, col=1)

    # ── EMA 8/21 ──
    if "EMA 8/21" in overlays and len(closes) >= 21:
        ema8_s  = calc_ema_series(closes, 8)
        ema21_s = calc_ema_series(closes, 21)
        fig.add_trace(go.Scatter(x=dates, y=ema8_s, name="EMA 8",
            line=dict(color="#00bfff", width=1.2, dash="solid"), opacity=0.8), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=ema21_s, name="EMA 21",
            line=dict(color="#ffd700", width=1.2, dash="solid"), opacity=0.8), row=1, col=1)

    # ── EMA 20/50 ──
    if "EMA 20/50" in overlays and len(closes) >= 50:
        ema20_s = calc_ema_series(closes, 20)
        ema50_s = calc_ema_series(closes, 50)
        fig.add_trace(go.Scatter(x=dates, y=ema20_s, name="EMA 20",
            line=dict(color="#ff8c00", width=1.5, dash="dot"), opacity=0.8), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=ema50_s, name="EMA 50",
            line=dict(color="#cc44ff", width=1.5, dash="dot"), opacity=0.8), row=1, col=1)

    # ── BOLLINGER BANDS ──
    if "Bollinger Bands" in overlays and len(closes) >= 20:
        bb_mid_s = []
        bb_upp_s = []
        bb_low_s = []
        for i in range(len(closes)):
            if i < 19:
                bb_mid_s.append(None); bb_upp_s.append(None); bb_low_s.append(None)
            else:
                m, u, l = calc_bb(closes[:i+1])
                bb_mid_s.append(m); bb_upp_s.append(u); bb_low_s.append(l)

        fig.add_trace(go.Scatter(x=dates, y=bb_upp_s, name="BB Upper",
            line=dict(color="#5a7a9a", width=1, dash="dash"), opacity=0.6), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=bb_mid_s, name="BB Mid",
            line=dict(color="#5a7a9a", width=1, dash="dot"), opacity=0.5), row=1, col=1)
        fig.add_trace(go.Scatter(x=dates, y=bb_low_s, name="BB Lower",
            line=dict(color="#5a7a9a", width=1, dash="dash"), opacity=0.6,
            fill="tonexty" if False else None), row=1, col=1)

    # ── ORDER BLOCKS ──
    if "Order Blocks" in overlays and r.get("order_blocks"):
        price_range = highs.max() - lows.min()
        for ob in r["order_blocks"][:4]:
            color = "rgba(0,255,136,0.15)" if ob["type"] == "BULL" else "rgba(255,51,85,0.15)"
            border = "#00ff88" if ob["type"] == "BULL" else "#ff3355"
            label = f"{'🟩' if ob['type']=='BULL' else '🟥'} {ob['type']} OB (str:{ob['str']})"
            # Shade the OB zone across full chart
            fig.add_hrect(
                y0=ob["low"], y1=ob["high"],
                fillcolor=color,
                line=dict(color=border, width=1, dash="dot"),
                annotation_text=label,
                annotation_position="right",
                annotation=dict(font=dict(color=border, size=10, family="Share Tech Mono")),
                row=1, col=1
            )

    # ── FVG ZONES ──
    if "FVG Zones" in overlays and r.get("fvg"):
        for fvg in r["fvg"][:3]:
            color = "rgba(0,191,255,0.12)" if fvg["type"] == "BULL" else "rgba(255,140,0,0.12)"
            border = "#00bfff" if fvg["type"] == "BULL" else "#ff8c00"
            label = f"FVG {fvg['type']}"
            fig.add_hrect(
                y0=fvg["bot"], y1=fvg["top"],
                fillcolor=color,
                line=dict(color=border, width=1, dash="dash"),
                annotation_text=label,
                annotation_position="left",
                annotation=dict(font=dict(color=border, size=10, family="Share Tech Mono")),
                row=1, col=1
            )

    # ── CURRENT PRICE LINE ──
    cp = float(closes[-1])
    cp_color = "#00ff88" if r["direction"] == "BUY" else "#ff3355" if r["direction"] == "SELL" else "#ffd700"
    fig.add_hline(y=cp, line=dict(color=cp_color, width=1.5, dash="solid"),
                  annotation_text=f"  {cp:.5f}",
                  annotation=dict(font=dict(color=cp_color, size=11, family="Share Tech Mono")),
                  row=1, col=1)

    # ── SL / TP LINES ──
    if r["direction"] != "NEUTRAL" and r.get("sl_price", 0) > 0:
        fig.add_hline(y=r["sl_price"], line=dict(color="#ff3355", width=1, dash="dash"),
                      annotation_text=f"  SL {r['sl_price']:.5f}",
                      annotation=dict(font=dict(color="#ff3355", size=10, family="Share Tech Mono")),
                      row=1, col=1)
        fig.add_hline(y=r["tp1_price"], line=dict(color="#00ff88", width=1, dash="dash"),
                      annotation_text=f"  TP1 {r['tp1_price']:.5f}",
                      annotation=dict(font=dict(color="#00ff88", size=10, family="Share Tech Mono")),
                      row=1, col=1)
        fig.add_hline(y=r["tp2_price"], line=dict(color="#00cc66", width=1, dash="dot"),
                      annotation_text=f"  TP2 {r['tp2_price']:.5f}",
                      annotation=dict(font=dict(color="#00cc66", size=10, family="Share Tech Mono")),
                      row=1, col=1)

    # ── VOLUME ──
    if has_vol and "Volume" in overlays:
        vol_colors = ["#00ff8866" if c >= o else "#ff335566"
                      for c, o in zip(closes, opens)]
        fig.add_trace(go.Bar(
            x=dates, y=volumes, name="Volume",
            marker_color=vol_colors, showlegend=False
        ), row=2, col=1)

    # ── LAYOUT ──
    fig.update_layout(
        paper_bgcolor="#050a0e",
        plot_bgcolor="#0a1520",
        font=dict(color="#e0f0ff", family="Share Tech Mono", size=11),
        xaxis_rangeslider_visible=False,
        legend=dict(
            bgcolor="#0d1e2e", bordercolor="#1a3a5c", borderwidth=1,
            font=dict(size=10, color="#7a9abf")
        ),
        margin=dict(l=10, r=80, t=40, b=10),
        height=520,
        title=dict(
            text=f"  {symbol} · {tf.upper()} · {r['direction']} · Score:{r['score']}",
            font=dict(color=cp_color, size=13, family="Share Tech Mono"),
            x=0
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#0d1e2e", bordercolor="#1a3a5c",
            font=dict(color="#e0f0ff", size=11, family="Share Tech Mono")
        )
    )
    fig.update_xaxes(
        gridcolor="#0d1e2e", zeroline=False,
        showspikes=True, spikecolor="#1a3a5c", spikethickness=1
    )
    fig.update_yaxes(
        gridcolor="#0d1e2e", zeroline=False,
        showspikes=True, spikecolor="#1a3a5c", spikethickness=1,
        side="right"
    )

    st.plotly_chart(fig, width="stretch", config={
        "displayModeBar": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d"],
        "displaylogo": False,
        "scrollZoom": True
    })

    # Mini stats below chart
    atr_pips = round(r.get("atr", 0) / get_pip(symbol))
    col1, col2, col3, col4, col5 = st.columns(5)
    mcard(col1, "CANDLES", len(df), "#5a7a9a")
    mcard(col2, "CURRENT", f"{cp:.5f}", cp_color)
    mcard(col3, "ATR (pips)", atr_pips, "#ffd700")
    mcard(col4, "HIGH", f"{highs.max():.5f}", "#00ff88")
    mcard(col5, "LOW",  f"{lows.min():.5f}", "#ff3355")


def render_ai_tab(r):
    """Render the AI Analysis tab for a pair."""
    api_key = get_api_key()

    if not api_key:
        st.markdown("""<div class='alert-box'>
        <b style='color:#ffd700'>🤖 AI Analysis — Setup Required</b><br><br>
        Add your Groq API key as an environment variable:<br><br>
        <b style='color:#00ff88'>On Streamlit Cloud:</b><br>
        Settings → Secrets → Add: <code>GROQ_API_KEY = "gsk_..."</code><br><br>
        <b style='color:#00ff88'>On Hugging Face:</b><br>
        Settings → Repository Secrets → Add: <code>GROQ_API_KEY</code><br><br>
        <span style='color:#5a7a9a;font-size:11px'>
        Get your FREE API key at <b>console.groq.com</b> — no credit card needed!<br>
        Model: LLaMA 3.3 70B | Speed: ~500 tokens/sec | Cost: FREE
        </span>
        </div>""", unsafe_allow_html=True)
        return

    # Check if score is meaningful
    if r["price"] == 0:
        st.warning("No price data available for this pair — cannot generate AI analysis.")
        return

    col_ai1, col_ai2 = st.columns([3, 1])
    with col_ai1:
        st.markdown(f"""<div style='font-family:Share Tech Mono;font-size:11px;color:#5a7a9a;
        line-height:1.8'>
        🤖 AI Analyst: <b style='color:#00ff88'>LLaMA 3.3 70B (Groq)</b> &nbsp;|&nbsp;
        Pair: <b style='color:#e0f0ff'>{r['symbol']}</b> &nbsp;|&nbsp;
        Score: <b style='color:#ffd700'>{r['score']}/100</b> &nbsp;|&nbsp;
        Direction: <b style='color:{"#00ff88" if r["direction"]=="BUY" else "#ff3355" if r["direction"]=="SELL" else "#5a7a9a"}'>{r["direction"]}</b>
        </div>""", unsafe_allow_html=True)

    with col_ai2:
        analyze_btn = st.button("🤖 ANALYZE", key=f"ai_btn_{r['symbol']}", use_container_width=True)

    # Cache key for this specific setup
    cache_key = f"ai_{r['symbol']}_{r['score']}_{r['direction']}_{r['price']:.3f}"

    if analyze_btn:
        with st.spinner("🤖 AI analyst thinking..."):
            prompt = build_ai_prompt(r)
            ai_text, err = call_groq_api(prompt, api_key)
            if ai_text:
                st.session_state[cache_key] = ai_text
            else:
                st.session_state[cache_key] = f"ERROR:{err}"

    # Display cached result
    if cache_key in st.session_state:
        result = st.session_state[cache_key]
        if result.startswith("ERROR:"):
            st.error(result[6:])
        else:
            # Render AI response with styled container
            st.markdown(f"""<div style='background:#050a0e;border:1px solid #1a3a5c;
            border-left:4px solid #ffd700;border-radius:0 6px 6px 0;
            padding:20px;margin-top:12px;font-size:13px;line-height:1.8;color:#c0d8f0'>
            {result.replace(chr(10), '<br>').replace('## ', '<br><b style="color:#ffd700;font-family:Share Tech Mono;font-size:12px;letter-spacing:1px">').replace('\n##', '</b><br>')}
            </div>""", unsafe_allow_html=True)

            # Clean markdown render
            st.markdown("---")
            st.markdown(result)
    else:
        st.markdown(f"""<div style='text-align:center;padding:30px;
        font-family:Share Tech Mono;color:#1a3a5c;font-size:12px;letter-spacing:2px'>
        ◈ PRESS "🤖 ANALYZE" TO GET AI ANALYSIS ◈<br><br>
        <span style='font-size:10px'>
        Analyzes: Setup Narrative · Market Context · Confluences · Risk · Trading Plan
        </span>
        </div>""", unsafe_allow_html=True)


# ─── APP3 HELPER FUNCTIONS ──────────────────────────────────────
# ════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════
def parse_tickers(raw: str) -> list:
    tickers = [t.strip().upper() for t in raw.replace('\n', ',').split(',') if t.strip()]
    return list(dict.fromkeys(tickers))


def metric_card(col, label: str, value, color: str = "#e6edf3"):
    with col:
        st.markdown(f"""
        <div class='metric-box'>
            <div style='color:#8b949e; font-size:0.78rem;'>{label}</div>
            <div style='color:{color}; font-size:1.4rem; font-weight:bold;'>{value}</div>
        </div>""", unsafe_allow_html=True)


def render_score_bar(score: int, color: str):
    st.markdown(f"""
    <div style='display:flex; align-items:center; gap:10px; margin:6px 0;'>
        <div style='flex:1; background:#30363d; border-radius:8px; height:10px; overflow:hidden;'>
            <div style='width:{score}%; background:{color}; height:100%; border-radius:8px;'></div>
        </div>
        <span style='color:{color}; font-weight:bold; min-width:55px;'>{score}/100</span>
    </div>""", unsafe_allow_html=True)


def render_signal_row(name: str, signal: dict):
    icon  = "✅" if signal['status'] else "❌"
    color = "#00ff88" if signal['status'] else "#8b949e"
    pts   = signal.get('points', 0)
    st.markdown(f"""
    <div class='info-row'>
        <span style='color:#8b949e;'>{icon} {name}</span>
        <span>
            <span style='color:{color}; font-size:0.85rem;'>{signal['value']}</span>
            <span style='color:#ffd700; font-size:0.8rem; margin-left:8px;'>+{pts}pts</span>
        </span>
    </div>""", unsafe_allow_html=True)


def create_chart(df, ticker, trade_plan, timeframe="3 Bulan",
                  show_fib=False, show_trendline=False) -> go.Figure:
    """Wrapper: gunakan create_upgraded_chart dengan opsi advanced."""
    return create_upgraded_chart(df, ticker, trade_plan,
                                  timeframe=timeframe,
                                  show_fib=show_fib,
                                  show_trendline=show_trendline)


def export_to_csv(results: list, trade_plans: dict) -> bytes:
    rows = []
    for r in results:
        ticker = r['ticker']
        tp = trade_plans.get(ticker, {})
        rows.append({
            'Tanggal': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'Ticker': ticker, 'Kategori': r['category'], 'Skor': r['score'],
            'Harga': r['close'], 'Volume Ratio': r['volume_ratio'], 'RSI': r['rsi'],
            'Entry': r['close'],
            'SL': tp.get('sl', {}).get('recommended', ''),
            'TP1': tp.get('tp', {}).get('tp1', ''), 'TP2': tp.get('tp', {}).get('tp2', ''),
            'TP3': tp.get('tp', {}).get('tp3', ''),
            'Risk %': tp.get('sl', {}).get('risk_pct', ''),
            'Max Lot': tp.get('position', {}).get('lot', ''),
        })
    return pd.DataFrame(rows).to_csv(index=False).encode('utf-8')


def run_scan(tickers: list, modal: float, prog=None,
             enable_ml: bool = False, enable_pattern: bool = True,
             enable_sentiment: bool = False) -> tuple:
    results, trade_plans = [], {}
    ml_results, pattern_results, sentiment_results = {}, {}, {}

    for i, ticker in enumerate(tickers):
        if prog:
            prog.progress((i+1)/len(tickers), f"📡 {ticker} ({i+1}/{len(tickers)})...")

        df = fetch_stock_data(ticker)
        if df is None:
            continue

        result = score_stock(df)
        if result:
            result['ticker'] = ticker
            results.append(result)
            trade_plans[ticker] = get_full_trade_plan(
                result['close'], result['atr'], result['support'], modal,
                adx             = result.get('adx', 0),
                bandar_fase     = result.get('bandar_fase', ''),
                bandar_strength = result.get('bandar_strength', 50),
                cmf             = result.get('cmf', 0),
            )

            # 🆕 Chart Pattern Recognition
            if enable_pattern:
                try:
                    pattern_results[ticker] = analyze_patterns(df)
                except Exception as e:
                    print(f"[APP] Pattern error {ticker}: {e}")

            # 🆕 AI Confidence
            if enable_ml and SKLEARN_AVAILABLE:
                try:
                    ml_results[ticker] = predict_confidence(
                        ticker, df, st.session_state['ml_cache'])
                except Exception as e:
                    print(f"[APP] ML error {ticker}: {e}")

            # 🆕 News Sentiment
            if enable_sentiment:
                try:
                    sentiment_results[ticker] = analyze_news_sentiment(ticker)
                except Exception as e:
                    print(f"[APP] Sentiment error {ticker}: {e}")

        time.sleep(0.05)

    results.sort(key=lambda x: x['score'], reverse=True)
    return results, trade_plans, ml_results, pattern_results, sentiment_results



# ─── SESSION STATE ──────────────────────────────────────────────
def init_session_state():
    default_groq_key = (os.environ.get("GROQ_API_KEY", "") or
                        os.environ.get("AnalisaSahamIndonesia", ""))
    defaults = {
        'stocks':          [],
        'scan_time':       None,
        'watchlist':       {},
        'portfolio':       [],
        'closed_trades':   [],
        'chart_data':      {},
        'modal':           10_000_000,
        'groq_api_key':    default_groq_key,
        'last_scan_count': 0,
        'ihsg_closes':     None,
        'sector_momentum': None,
        'rti_data':        None,
        'data_loaded':     False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================
# MAIN APP
# ============================================================

def _init_extra_session():
    extras = {
        'results': [], 'trade_plans': {}, 'ml_results': {},
        'pattern_results': {}, 'sentiment_results': {},
        'last_scan_time': None, 'auto_refresh': False,
        'scan_count': 0, 'notif_sent': [],
        'tg_token': '', 'tg_chat_id': '',
        'wa_phone': '', 'wa_key': '',
        'modal': 10_000_000,
        'tickers': ['BBCA','BBRI','BMRI','TLKM','ASII','UNVR','KLBF','ADRO','ANTM','MDKA'],
        'ml_cache': {}, 'enable_ml': False,
        'enable_pattern': True, 'enable_sentiment': False,
        'enable_tg': False, 'enable_wa': False,
        'groq_api_key': '',
        'scan_mode': 'breakout',
        '_watchlist': {}, '_portfolio': [], '_closed_trades': [],
        '_leaderboard': {},
    }
    for k, v in extras.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
# SIDEBAR UNIFIED — Mode Scanner + Semua Pengaturan
# ══════════════════════════════════════════════════════════════
def _build_sidebar():
    """Sidebar: pilih mode scanner + semua config. Returns (scan_mode, config_dict)."""
    with st.sidebar:
        # ── Branding ──────────────────────────────────────────
        st.markdown("""
        <div style='padding:14px 0 10px 0;border-bottom:1px solid var(--border,#21262d);margin-bottom:14px;'>
            <div style='font-size:1.1rem;font-weight:700;color:var(--text,#e6edf3);'>📊 Trading Suite</div>
            <div style='font-size:0.65rem;color:var(--text-muted,#484f58);font-family:JetBrains Mono,monospace;
                 letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;'>Unified · IDX + Forex</div>
        </div>""", unsafe_allow_html=True)

        # ── Market status ─────────────────────────────────────
        tz = pytz.timezone("Asia/Jakarta")
        now = datetime.now(tz)
        h, m = now.hour, now.minute
        wd = now.weekday()
        is_open = (wd < 5) and ((h == 9) or (10 <= h <= 14) or (h == 15 and m <= 30))
        mkt_color = "#00ff88" if is_open else "#ff4444"
        mkt_text  = "🟢 BUKA" if is_open else "🔴 TUTUP"
        st.markdown(
            f"<div style='font-family:JetBrains Mono,monospace;font-size:0.7rem;color:{mkt_color};"
            f"padding:5px 10px;background:rgba(0,0,0,0.3);border:1px solid {mkt_color}44;"
            f"border-radius:20px;text-align:center;margin-bottom:14px;letter-spacing:1px;font-weight:700;'>"
            f"IDX {mkt_text} · {now.strftime('%H:%M')} WIB</div>",
            unsafe_allow_html=True)

        # ── MODE SCANNER ──────────────────────────────────────
        st.markdown("<p style='color:#484f58;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;"
                    "font-family:JetBrains Mono,monospace;margin:0 0 8px 4px;'>▸ MODE SCANNER</p>",
                    unsafe_allow_html=True)

        scan_mode = st.radio(
            label="scan_mode",
            options=["🚀 Breakout IDX", "📈 Open=Low IDX", "🔍 Low Float IDX", "🚨 Bid>Offer IDX", "⚡ Volatility IDX", "🎯 SNIPER FX"],
            index=["📈 Open=Low IDX","🔍 Low Float IDX","🚀 Breakout IDX","🎯 SNIPER FX"].index(
                st.session_state.get("scan_mode_radio","🚀 Breakout IDX")),
            label_visibility="collapsed",
        )
        st.session_state["scan_mode_radio"] = scan_mode

        # ── Upload custom list (App6) ─────────────────────────
        if "Bid>Offer" in scan_mode or "Volatility" in scan_mode:
            st.markdown("<p style='color:#484f58;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;font-family:JetBrains Mono,monospace;margin:0 0 8px 4px;'>▸ UPLOAD SAHAM</p>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload .txt (AALI, BBCA, ...)", type=['txt'])
            if uploaded_file:
                custom = parse_stock_file(uploaded_file)
                if custom:
                    st.session_state['_custom_tickers'] = custom
                    st.success(f"✅ {len(custom)} saham loaded!")
            cfg['vol_threshold'] = st.slider("Min Volatility (%)", 5.0, 100.0, 25.0, 5.0)
            cfg['max_stocks']   = st.slider("Jumlah Saham", 10, 955, 100, 10)
            cfg['min_price']    = st.number_input("Harga Min (Rp)", value=0, step=50)
            cfg['max_price']    = st.number_input("Harga Max (Rp)", value=999999, step=50)
            cfg['min_volume']   = st.number_input("Min Volume (lot)", value=0, step=1000)
            cfg['mode_a6']      = st.radio("Mode:", ["Bid > Offer (Anomaly)","Volatility Scanner","Kombinasi (All-in-One)"], index=2, label_visibility="collapsed")
        st.session_state["scan_mode_radio"] = scan_mode
        st.divider()

        cfg = {}

        # ── IDX MODES ─────────────────────────────────────────
        if "IDX" in scan_mode:
            st.markdown("<p style='color:#484f58;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;"
                        "font-family:JetBrains Mono,monospace;margin:0 0 8px 4px;'>▸ FILTER SAHAM</p>",
                        unsafe_allow_html=True)

            filter_type = st.radio("Filter",
                ["Semua Saham","Pilih Manual","Filter Tingkatan","Filter Sektor"],
                label_visibility="collapsed")

            if filter_type == "Pilih Manual":
                manual = st.multiselect("Pilih Saham", ALL_TICKERS[:200],
                                        default=st.session_state.get('tickers',[])[:5])
                cfg['tickers'] = manual or st.session_state.get('tickers',[])
            elif filter_type == "Filter Tingkatan":
                levels = st.multiselect("Tingkatan",
                    ["💎 Blue Chip","📈 Second Liner","🎯 Third Liner"],
                    default=["💎 Blue Chip","📈 Second Liner"])
                t_list = []
                if "Blue Chip" in str(levels):   t_list += BLUE_CHIP_STOCKS
                if "Second Liner" in str(levels): t_list += SECOND_LINER_STOCKS
                if "Third Liner" in str(levels):
                    t_list += [t for t in ALL_TICKERS if t not in BLUE_CHIP_STOCKS and t not in SECOND_LINER_STOCKS]
                cfg['tickers'] = list(dict.fromkeys(t_list))
            elif filter_type == "Filter Sektor":
                from sector_data import SECTOR_DATA
                sektors = sorted(set(SECTOR_DATA.values()))
                sel_sek = st.selectbox("Sektor", sektors)
                cfg['tickers'] = [t for t,s in SECTOR_DATA.items() if s == sel_sek]
                st.info(f"{len(cfg['tickers'])} saham di sektor {sel_sek}")
            else:
                cfg['tickers'] = ALL_TICKERS

            st.markdown("<div style='height:1px;background:#21262d;margin:12px 0;'></div>", unsafe_allow_html=True)

            if "Breakout" in scan_mode:
                st.markdown("<p style='color:#484f58;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;"
                            "font-family:JetBrains Mono,monospace;margin:0 0 8px 4px;'>▸ FITUR SCAN</p>",
                            unsafe_allow_html=True)
                cfg['enable_pattern']   = st.toggle("📊 Chart Pattern",   value=st.session_state.get('enable_pattern', True))
                cfg['enable_ml']        = st.toggle("🤖 AI Confidence",   value=st.session_state.get('enable_ml', False))
                cfg['enable_sentiment'] = st.toggle("📰 News Sentiment",  value=st.session_state.get('enable_sentiment', False))
                cfg['enable_rs']        = st.toggle("📈 RS vs IHSG",      value=True)
                cfg['enable_foreign']   = st.toggle("🌏 Foreign Flow",    value=False)
                st.markdown("<div style='height:1px;background:#21262d;margin:12px 0;'></div>", unsafe_allow_html=True)

            if "Open=Low" in scan_mode:
                cfg['min_gain'] = st.slider("Min Kenaikan (%)", 1.0, 20.0, 5.0, 0.5)
                cfg['periode']  = st.selectbox("Periode Data", ["1 Bulan","3 Bulan","6 Bulan"], index=1)
                cfg['use_parallel'] = st.checkbox("⚡ Parallel Scan", value=True)

            if "Low Float" in scan_mode:
                cfg['max_ff']   = st.slider("Max Free Float (%)", 5.0, 40.0, 20.0, 1.0)
                cfg['scan_bc']  = st.checkbox("💎 Blue Chip", value=True)
                cfg['scan_sl']  = st.checkbox("📈 Second Liner", value=True)
                cfg['scan_tl']  = st.checkbox("🎯 Third Liner", value=True)
                cfg['use_parallel'] = st.checkbox("⚡ Parallel Scan", value=True)

            cfg['modal'] = st.number_input("💰 Modal (Rp)", min_value=1_000_000,
                                           max_value=1_000_000_000, value=10_000_000,
                                           step=1_000_000, format="%d")

        # ── FX MODE ───────────────────────────────────────────
        if "SNIPER FX" in scan_mode:
            st.markdown("<p style='color:#484f58;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;"
                        "font-family:JetBrains Mono,monospace;margin:0 0 8px 4px;'>▸ FX CONFIG</p>",
                        unsafe_allow_html=True)
            cfg['fx_pairs']    = st.multiselect("Pasangan Forex",
                list(ALL_PAIRS.keys()), default=list(ALL_PAIRS.keys())[:8])
            cfg['fx_timeframe']= st.selectbox("Timeframe", ["M5","M15","H1","H4"], index=0)
            cfg['fx_min_score']= st.slider("Min Score", 40, 90, 60, 5)

        # ── NOTIFIKASI ────────────────────────────────────────
        st.divider()
        with st.expander("🔔 Notifikasi"):
            st.session_state['tg_token']   = st.text_input("Telegram Token",
                value=st.session_state.get('tg_token',''), type="password")
            st.session_state['tg_chat_id'] = st.text_input("Telegram Chat ID",
                value=st.session_state.get('tg_chat_id',''))
            st.session_state['groq_api_key'] = st.text_input("Groq API Key",
                value=st.session_state.get('groq_api_key',''), type="password")

        # ── RESET ─────────────────────────────────────────────
        if st.button("↺ Reset Session", use_container_width=True):
            for k in ['results','trade_plans','stocks','ihsg_closes','sector_momentum','rti_data']:
                st.session_state.pop(k, None)
            st.success("✓ Reset!"); st.rerun()

    return scan_mode, cfg

# ══════════════════════════════════════════════════════════════
# APP6 — SAHAM INDONESIA SCANNER PRO (955 SAHAM)
# Fitur unik: Bid>Offer Anomaly + Volatility Scanner
# ══════════════════════════════════════════════════════════════
DEFAULT_SAHAM_IDX_955 = [
    "AADI.JK","AALI.JK","ABBA.JK","ABDA.JK","ABMM.JK","ACES.JK","ACRO.JK","ACST.JK",
    "ADCP.JK","ADES.JK","ADHI.JK","ADMF.JK","ADMG.JK","ADMR.JK","ADRO.JK","AEGS.JK",
    "AGAR.JK","AGII.JK","AGRO.JK","AGRS.JK","AHAP.JK","AIMS.JK","AISA.JK","AKKU.JK",
    "AKPI.JK","AKRA.JK","AKSI.JK","ALDO.JK","ALII.JK","ALKA.JK","ALMI.JK","ALTO.JK",
    "AMAG.JK","AMAN.JK","AMAR.JK","AMFG.JK","AMIN.JK","AMMS.JK","AMOR.JK","AMRT.JK",
    "AMMN.JK","ANJT.JK","ANTM.JK","APEX.JK","APIC.JK","APII.JK","APLN.JK","ARGO.JK",
    "ARII.JK","ARKA.JK","ARKO.JK","ARNA.JK","ARTA.JK","ARTI.JK","ARTO.JK","ASBI.JK",
    "ASDM.JK","ASEI.JK","ASGR.JK","ASHA.JK","ASII.JK","ASJT.JK","ASLC.JK","ASMI.JK",
    "ASRI.JK","ASRM.JK","ASSA.JK","ASTA.JK","ASPI.JK","ATAP.JK","ATIC.JK","ATLA.JK",
    "AUTO.JK","AVIA.JK","AXIO.JK","AYAM.JK","AYLS.JK","BABP.JK","BABY.JK","BACA.JK",
    "BAIK.JK","BALI.JK","BANK.JK","BAPA.JK","BATA.JK","BAYU.JK","BBCA.JK","BBHI.JK",
    "BBKP.JK","BBLD.JK","BBMD.JK","BBNI.JK","BBRI.JK","BBRM.JK","BBSI.JK","BBSS.JK",
    "BBTN.JK","BBYB.JK","BCAP.JK","BCIC.JK","BCIP.JK","BDKR.JK","BDMN.JK","BEEF.JK",
    "BEKS.JK","BELL.JK","BEST.JK","BESS.JK","BFIN.JK","BGTG.JK","BHAT.JK","BHIT.JK",
    "BIKA.JK","BIKE.JK","BIMA.JK","BINA.JK","BIPP.JK","BIRD.JK","BISI.JK","BJBR.JK",
    "BJTM.JK","BKDP.JK","BKSL.JK","BKSW.JK","BLTA.JK","BLTZ.JK","BMAS.JK","BMHS.JK",
    "BMBL.JK","BMRI.JK","BMSR.JK","BMTR.JK","BNBA.JK","BNBR.JK","BNGA.JK","BNII.JK",
    "BNLI.JK","BOBA.JK","BOGA.JK","BOLA.JK","BOLT.JK","BOSS.JK","BPFI.JK","BPII.JK",
    "BPTN.JK","BRAM.JK","BREN.JK","BRIS.JK","BRMS.JK","BRNA.JK","BRPT.JK","BRRC.JK",
    "BSDE.JK","BSIM.JK","BSML.JK","BSSR.JK","BSWD.JK","BTEK.JK","BTEL.JK","BTON.JK",
    "BTPN.JK","BTPS.JK","BUAH.JK","BUDI.JK","BUKA.JK","BUKK.JK","BULL.JK","BUMI.JK",
    "BUVA.JK","BVIC.JK","BWPT.JK","BYAN.JK","CAKK.JK","CAMP.JK","CANI.JK","CARE.JK",
    "CARS.JK","CASA.JK","CASH.JK","CASS.JK","CBMF.JK","CBMS.JK","CBPE.JK","CBRE.JK",
    "CBUT.JK","CCSI.JK","CDIA.JK","CEKA.JK","CENT.JK","CFIN.JK","CHEK.JK","CHEM.JK",
    "CHIP.JK","CINT.JK","CITA.JK","CITY.JK","CLAY.JK","CLEO.JK","CLPI.JK","CMNP.JK",
    "CMPP.JK","CMRY.JK","CMNT.JK","CNKO.JK","CNMA.JK","CNTX.JK","COIN.JK","COAL.JK",
    "COCO.JK","CPIN.JK","CPRI.JK","CPRO.JK","CRAB.JK","CRSN.JK","CSAP.JK","CSIS.JK",
    "CSMI.JK","CSRA.JK","CTBN.JK","CTRA.JK","CTTH.JK","CUAN.JK","CYBR.JK","DAAZ.JK",
    "DADA.JK","DART.JK","DATA.JK","DAYA.JK","DEAL.JK","DEFI.JK","DEPO.JK","DEWI.JK",
    "DEWA.JK","DFAM.JK","DGIK.JK","DGNS.JK","DGWG.JK","DILD.JK","DKFT.JK","DKHH.JK",
    "DLTA.JK","DMAS.JK","DMMX.JK","DMND.JK","DNAR.JK","DNET.JK","DOID.JK","DOOH.JK",
    "DOSS.JK","DPNS.JK","DPPP.JK","DPUM.JK","DRMA.JK","DSFI.JK","DSNG.JK","DSSA.JK",
    "DUTI.JK","DVLA.JK","DWGL.JK","DYAN.JK","EAST.JK","ECII.JK","EKAD.JK","ELPI.JK",
    "ELSA.JK","ELTY.JK","ELIT.JK","EMDE.JK","EMTK.JK","ENAK.JK","ENRG.JK","ENZO.JK",
    "EPAC.JK","EPMT.JK","ERAA.JK","ERAL.JK","ERTX.JK","ESIP.JK","ESSA.JK","ESTA.JK",
    "ESTI.JK","ETWA.JK","EURO.JK","EXCL.JK","FAPA.JK","FAST.JK","FASW.JK","FILM.JK",
    "FIMP.JK","FIRE.JK","FISH.JK","FITT.JK","FLMC.JK","FMII.JK","FOLK.JK","FOOD.JK",
    "FORU.JK","FPNI.JK","FREN.JK","FORE.JK","FUTR.JK","FUJI.JK","FWCT.JK","GAMA.JK",
    "GDST.JK","GDYR.JK","GEMA.JK","GEMS.JK","GGEO.JK","GGRM.JK","GHON.JK","GIAA.JK",
    "GJTL.JK","GLVA.JK","GLOB.JK","GMTD.JK","GOLD.JK","GOLL.JK","GOLF.JK","GOOD.JK",
    "GOTO.JK","GPRA.JK","GPSO.JK","GRIA.JK","GRPH.JK","GRPM.JK","GTRA.JK","GTSI.JK",
    "GTBO.JK","GULA.JK","GUNA.JK","GWSA.JK","GZCO.JK","HAIS.JK","HAJJ.JK","HALO.JK",
    "HATM.JK","HADE.JK","HDFA.JK","HEAL.JK","HELI.JK","HERO.JK","HEXA.JK","HGII.JK",
    "HILL.JK","HITS.JK","HKMU.JK","HMSP.JK","HOKI.JK","HOME.JK","HOMI.JK","HOPE.JK",
    "HRTA.JK","HRUM.JK","HUMI.JK","HYGN.JK","IATA.JK","IBFN.JK","IBOS.JK","IBST.JK",
    "ICBP.JK","ICON.JK","IDEA.JK","IDPR.JK","IFII.JK","IFSH.JK","IGAR.JK","IIKP.JK",
    "IKAI.JK","IKAN.JK","IKBI.JK","IKPM.JK","IMAS.JK","IMJS.JK","IMPC.JK","INAF.JK",
    "INAI.JK","INCF.JK","INCI.JK","INCO.JK","INDF.JK","INDO.JK","INDR.JK","INDS.JK",
    "INDX.JK","INDY.JK","INET.JK","INKP.JK","INOV.JK","INPC.JK","INPP.JK","INPS.JK",
    "INRU.JK","INTA.JK","INTD.JK","INTP.JK","IOTF.JK","IPAC.JK","IPCM.JK","IPOL.JK",
    "IPPE.JK","IPTV.JK","IRRA.JK","ISAP.JK","ISAT.JK","ISEA.JK","ISSP.JK","ITIC.JK",
    "ITMA.JK","ITMG.JK","JARR.JK","JAST.JK","JATI.JK","JAWA.JK","JAYA.JK","JECC.JK",
    "JGLE.JK","JIHD.JK","JKON.JK","JMAS.JK","JPFA.JK","JRPT.JK","JSKY.JK","JSMR.JK",
    "JSPT.JK","JTPE.JK","KAQI.JK","KARW.JK","KAYU.JK","KAEF.JK","KBAG.JK","KBLI.JK",
    "KBLM.JK","KBLV.JK","KBRI.JK","KCCI.JK","KDTN.JK","KDSI.JK","KEEN.JK","KEJU.JK",
    "KETR.JK","KIAS.JK","KICI.JK","KIJA.JK","KING.JK","KINO.JK","KIOS.JK","KJEN.JK",
    "KKGI.JK","KLBF.JK","KLIN.JK","KMDS.JK","KOBX.JK","KOIN.JK","KOKA.JK","KONI.JK",
    "KOPI.JK","KOTA.JK","KPIG.JK","KRAY.JK","KRAS.JK","KREN.JK","KUAS.JK","LABA.JK",
    "LABS.JK","LAND.JK","LAPD.JK","LCGP.JK","LCKM.JK","LEAD.JK","LFLO.JK","LGMS.JK",
    "LIFE.JK","LINK.JK","LION.JK","LIVE.JK","LMAS.JK","LMAX.JK","LMPI.JK","LMSH.JK",
    "LOPI.JK","LPCK.JK","LPGI.JK","LPIN.JK","LPKR.JK","LPLI.JK","LPPF.JK","LPPS.JK",
    "LRNA.JK","LSIP.JK","LTLS.JK","LUCY.JK","LUCK.JK","MABA.JK","MAGP.JK","MAIN.JK",
    "MAHA.JK","MAHI.JK","MAPI.JK","MAPB.JK","MAPA.JK","MARI.JK","MARK.JK","MASB.JK",
    "MAYA.JK","MBAP.JK","MBMA.JK","MBSS.JK","MBTO.JK","MCAS.JK","MCOL.JK","MCOR.JK",
    "MDIA.JK","MDKA.JK","MDKI.JK","MDLA.JK","MDLN.JK","MDRN.JK","MDIY.JK","MEDC.JK",
    "MEGA.JK","MEJA.JK","MENN.JK","MERI.JK","MERK.JK","META.JK","MFMI.JK","MGNA.JK",
    "MGRO.JK","MICE.JK","MIDI.JK","MIKA.JK","MINE.JK","MINA.JK","MIRA.JK","MITI.JK",
    "MKAP.JK","MKNT.JK","MKPI.JK","MKTR.JK","MLBI.JK","MLIA.JK","MLPL.JK","MLPT.JK",
    "MMLP.JK","MNCN.JK","MORA.JK","MPMX.JK","MPOW.JK","MPPA.JK","MPXL.JK","MPRO.JK",
    "MREI.JK","MRAT.JK","MSIE.JK","MSIN.JK","MSJA.JK","MSKM.JK","MSKY.JK","MSTI.JK",
    "MTDL.JK","MTEL.JK","MTFN.JK","MTHA.JK","MTLA.JK","MTMH.JK","MTPS.JK","MTSM.JK",
    "MTWI.JK","MTRA.JK","MUTU.JK","MYOH.JK","MYOR.JK","MYTX.JK","NASA.JK","NASI.JK",
    "NAYZ.JK","NELY.JK","NEST.JK","NETV.JK","NICE.JK","NICK.JK","NICL.JK","NIKL.JK",
    "NIRO.JK","NISP.JK","NINE.JK","NOBU.JK","NPGF.JK","NRCA.JK","NSSS.JK","NTBK.JK",
    "NUSA.JK","OBAT.JK","OBMD.JK","OCAP.JK","OASA.JK","OILS.JK","OKAS.JK","OLIV.JK",
    "OMED.JK","OMRE.JK","OPMS.JK","PADI.JK","PADA.JK","PALM.JK","PAMG.JK","PANI.JK",
    "PANR.JK","PANS.JK","PAPA.JK","PBRX.JK","PBID.JK","PBSA.JK","PCAR.JK","PDES.JK",
    "PDPP.JK","PEGE.JK","PEHA.JK","PEVE.JK","PGAS.JK","PGEO.JK","PGLI.JK","PGJO.JK",
    "PGUN.JK","PICO.JK","PJAA.JK","PJHB.JK","PKPK.JK","PLAN.JK","PLAS.JK","PLIN.JK",
    "PMJS.JK","PMMP.JK","PMUI.JK","PNBN.JK","PNBS.JK","PNIN.JK","PNLF.JK","PNSE.JK",
    "POIN.JK","POLA.JK","POLI.JK","POLL.JK","POLU.JK","POLY.JK","POOL.JK","PORT.JK",
    "POSA.JK","POWR.JK","PPGL.JK","PPIP.JK","PPRE.JK","PPRI.JK","PPRO.JK","PRAY.JK",
    "PRDA.JK","PRIM.JK","PSAB.JK","PSAT.JK","PSDN.JK","PSGO.JK","PSKT.JK","PTBA.JK",
    "PTDU.JK","PTIS.JK","PTMP.JK","PTMR.JK","PTPP.JK","PTPS.JK","PTPW.JK","PTRO.JK",
    "PTSN.JK","PTSP.JK","PUDP.JK","PURE.JK","PURI.JK","PURA.JK","PWON.JK","PYFA.JK",
    "RAAM.JK","RAJA.JK","RALS.JK","RANC.JK","RAFI.JK","RBMS.JK","RCCC.JK","RDTX.JK",
    "RELI.JK","RELF.JK","RICY.JK","RIGS.JK","RISE.JK","RIMO.JK","RLCO.JK","RMKE.JK",
    "RMKO.JK","ROCK.JK","RODA.JK","RONY.JK","ROTI.JK","RUIS.JK","RUNS.JK","SAGE.JK",
    "SAME.JK","SAMF.JK","SAPX.JK","SATO.JK","SATU.JK","SCCO.JK","SCMA.JK","SCNP.JK",
    "SCPI.JK","SDMU.JK","SDPC.JK","SDRA.JK","SFAN.JK","SGER.JK","SGRO.JK","SHID.JK",
    "SHIP.JK","SIDO.JK","SICO.JK","SILO.JK","SIMA.JK","SIMP.JK","SINI.JK","SIPD.JK",
    "SKBM.JK","SKLT.JK","SKRN.JK","SKYB.JK","SLIS.JK","SMAR.JK","SMBR.JK","SMCB.JK",
    "SMDM.JK","SMDR.JK","SMGA.JK","SMGR.JK","SMIL.JK","SMKL.JK","SMKM.JK","SMLE.JK",
    "SMMA.JK","SMMT.JK","SMRA.JK","SMRU.JK","SMSM.JK","SOCI.JK","SOFA.JK","SOHO.JK",
    "SOSS.JK","SONA.JK","SOTS.JK","SOUL.JK","SPMA.JK","SPRE.JK","SPTO.JK","SQMI.JK",
    "SRAJ.JK","SRIL.JK","SRSN.JK","SRTG.JK","SSIA.JK","SSMS.JK","SSTM.JK","STAR.JK",
    "STAA.JK","STTP.JK","STRK.JK","SUGI.JK","SULI.JK","SUNI.JK","SURI.JK","SURE.JK",
    "SUPA.JK","SUPR.JK","SWAT.JK","SWID.JK","TALF.JK","TAMU.JK","TAPG.JK","TARA.JK",
    "TAXI.JK","TAYS.JK","TBIG.JK","TBLA.JK","TBMS.JK","TCID.JK","TCPI.JK","TEBE.JK",
    "TECH.JK","TFAS.JK","TFCO.JK","TGKA.JK","TGRA.JK","TGUK.JK","TIFA.JK","TINS.JK",
    "TIRA.JK","TIRT.JK","TKIM.JK","TLDN.JK","TLKM.JK","TMAS.JK","TMPO.JK","TOBA.JK",
    "TOLS.JK","TOPS.JK","TOTL.JK","TOTO.JK","TOWR.JK","TOYS.JK","TPIA.JK","TPMA.JK",
    "TRAM.JK","TRIL.JK","TRIM.JK","TRIN.JK","TRIO.JK","TRIS.JK","TRJA.JK","TRON.JK",
    "TRST.JK","TRUK.JK","TRUS.JK","TSPC.JK","TUGU.JK","ULTJ.JK","UANG.JK","UNIC.JK",
    "UNIQ.JK","UNIT.JK","UNSP.JK","UNTD.JK","UNTR.JK","UNVR.JK","URBN.JK","UVCR.JK",
    "VAST.JK","VERN.JK","VICO.JK","VICI.JK","VINS.JK","VISI.JK","VIVA.JK","VKTR.JK",
    "VOKS.JK","VRNA.JK","VTNY.JK","WAPO.JK","WEGE.JK","WEHA.JK","WICO.JK","WIDI.JK",
    "WIIM.JK","WIKA.JK","WINE.JK","WINR.JK","WINS.JK","WIRE.JK","WIRG.JK","WMUU.JK",
    "WMPP.JK","WOMF.JK","WOOD.JK","WOWS.JK","WSBP.JK","WSKT.JK","WTON.JK","YOII.JK",
    "YPAS.JK","YULE.JK","YUPI.JK","ZATA.JK","ZBRA.JK","ZINC.JK","ZYRX.JK",
]

def parse_stock_file(uploaded_file):
    try:
        content = uploaded_file.read().decode('utf-8')
        tickers = re.split(r'[,\s\n\t]+', content)
        clean = []
        for t in tickers:
            t = t.strip().upper().replace('.JK','')
            if t and len(t) <= 5 and t.isalpha() and t not in [x.replace('.JK','') for x in clean]:
                clean.append(f"{t}.JK")
        return clean
    except Exception as e:
        st.error(f"Error parsing file: {e}"); return []

def calculate_volatility_a6(df, window=5):
    if df is None or len(df) < window: return None
    df = df.copy()
    df['Returns'] = df['Close'].pct_change()
    return {
        'volatility':      df['Returns'].std() * np.sqrt(252) * 100,
        'avg_volume':      df['Volume'].mean(),
        'price_change_5d': (df['Close'].iloc[-1]/df['Close'].iloc[0]-1)*100,
        'current_price':   df['Close'].iloc[-1],
        'high_5d':         df['High'].max(),
        'low_5d':          df['Low'].min(),
    }


# ══════════════════════════════════════════════════════════════
# SCAN HELPER FUNCTIONS (Open=Low, Low Float)
# ══════════════════════════════════════════════════════════════
def _scan_one_openlow(ticker, min_gain):
    try:
        sym = ticker+".JK" if not ticker.endswith(".JK") else ticker
        df  = yf.download(sym, period="5d", interval="1d", progress=False, auto_adjust=True)
        if df is None or len(df)<2: return None
        df.columns=[c[0] if isinstance(c,tuple) else c for c in df.columns]
        t=df.iloc[-1]; o=float(t["Open"]); l=float(t["Low"])
        c=float(t["Close"]); pc=float(df.iloc[-2]["Close"])
        if abs(o-l)/l > 0.005: return None
        gain=(c-pc)/pc*100
        if gain<min_gain: return None
        v=float(t["Volume"]); av=float(df["Volume"].mean())
        return {"ticker":ticker.replace(".JK",""),"open":o,"low":l,"close":c,
                "prev_close":pc,"gain_pct":round(gain,2),"volume":int(v),
                "avg_volume":int(av),"vol_ratio":round(v/av,2) if av else 0,
                "signal":"BUY","score":min(100,int(50+gain*3))}
    except: return None

def _scan_one_lowfloat(ticker, max_ff):
    try:
        ff = get_free_float_value(ticker.replace(".JK",""))
        if ff > max_ff: return None
        sym = ticker if ticker.endswith(".JK") else ticker+".JK"
        df  = yf.download(sym, period="1mo", interval="1d", progress=False, auto_adjust=True)
        if df is None or len(df)<5: return None
        df.columns=[c[0] if isinstance(c,tuple) else c for c in df.columns]
        c=float(df["Close"].iloc[-1]); pc=float(df["Close"].iloc[-2])
        v=float(df["Volume"].iloc[-1]); av=float(df["Volume"].mean())
        chg=(c-pc)/pc*100; vr=v/av if av else 0
        score=min(100,max(0,int(50+(max_ff-ff)*2+(vr-1)*10+(chg if chg>0 else 0)*2)))
        return {"ticker":ticker.replace(".JK",""),"close":c,"change":round(chg,2),
                "free_float":ff,"vol_ratio":round(vr,2),"volume":int(v),"score":score,
                "signal":"BUY" if score>=60 else "HOLD",
                "goreng_potential":analyze_goreng_potential(ff)["label"]}
    except: return None


# ══════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════
def main():
    init_session_state()
    _init_extra_session()
    scan_mode, cfg = _build_sidebar()
    tz  = pytz.timezone("Asia/Jakarta")
    now = datetime.now(tz)

    # ── Header ────────────────────────────────────────────────
    if "SNIPER FX" in scan_mode:
        st.markdown("""<div class='hdr'>
            <div class='hdr-title'>🎯 SNIPER FX</div>
            <div class='hdr-sub'>SMART MONEY SCALPING SCANNER — 28 PAIRS — SMC + CLASSIC — M5/H1/H4</div>
        </div>""", unsafe_allow_html=True)
    elif "Bid>Offer" in scan_mode or "Volatility" in scan_mode:
        st.markdown(f"""
        <h1 style='background:linear-gradient(90deg,#FF6B6B,#4ECDC4);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            font-size:2.2rem;font-weight:900;margin-bottom:4px;'>
            🇮🇩 SAHAM INDONESIA SCANNER PRO</h1>
        <p style='color:#666;font-size:1rem;margin-bottom:16px;'>
            955+ Saham · Real-time Bid/Offer Anomaly & Volatility Analysis · {now.strftime('%d %b %Y %H:%M')} WIB</p>
        """, unsafe_allow_html=True)
    else:
        mode_labels = {
            "📈 Open=Low IDX":"📡 RADAR AKSARA — Open=Low Scanner",
            "🔍 Low Float IDX":"🔍 RADAR AKSARA — Low Float Scanner",
            "🚀 Breakout IDX":"⚡ AKSARA IDX v2.0 — Breakout Scanner",
        }
        title = mode_labels.get(scan_mode,"📊 Trading Suite")
        st.markdown(f"""<div style='display:flex;align-items:center;gap:14px;
            padding:16px 0 12px 0;border-bottom:1px solid var(--border,#21262d);margin-bottom:16px;'>
            <h1 style='margin:0;font-size:1.4rem;color:var(--text,#e6edf3);'>{title}</h1>
            <span style='font-family:JetBrains Mono,monospace;font-size:0.65rem;color:var(--text-muted,#484f58);'>
            {now.strftime('%d %b %Y · %H:%M')} WIB</span></div>""", unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════
    # MODE: SNIPER FX
    # ══════════════════════════════════════════════════════════
    if "SNIPER FX" in scan_mode:


        # ============================================================
        # HEADER
        # ============================================================

        st.markdown("""
        <div class='hdr'>
            <div class='hdr-title'>🎯 SNIPER FX</div>
            <div class='hdr-sub'>SMART MONEY SCALPING SCANNER — 28 PAIRS — SMC + CLASSIC — M5 / H1 / H4</div>
        </div>
        """, unsafe_allow_html=True)

        # ============================================================
        # SIDEBAR
        # ============================================================

        with st.sidebar:
            st.markdown("### ⚙️ SCANNER CONFIG")
            st.divider()

            active_sess=get_active_sessions()
            ss_val,ss_note=get_session_score(active_sess)
            st.markdown("**📡 SESSIONS (UTC)**")
            for sn in ["Sydney","Tokyo","London","New York"]:
                ia=sn in active_sess
                col="#00ff88" if ia else "#1a3a5c"
                dot=f"<span class='sess-dot' style='background:{col};{'box-shadow:0 0 6px '+col if ia else ''}'></span>"
                st.markdown(f"<div style='font-size:12px;color:{col};font-family:Share Tech Mono'>{dot}{sn}</div>",
                            unsafe_allow_html=True)
            sc_color="#00ff88" if ss_val>=75 else "#ffd700" if ss_val>=50 else "#ff3355"
            st.markdown(f"<div style='margin-top:8px;padding:7px;background:#0d1e2e;"
                        f"border-left:3px solid {sc_color};font-family:Share Tech Mono;font-size:11px;"
                        f"color:{sc_color}'>Session Score: {ss_val}/100<br>{ss_note}</div>",
                        unsafe_allow_html=True)

            st.divider()
            st.markdown("**🌐 PAIRS**")
            pg=st.selectbox("Pair Group",["All (29)","Major (7)","Minor/Cross (21)","Commodities (XAUUSD)","Custom"])
            cp_list=[]
            if pg=="Custom":
                cp_list=st.multiselect("Select",list(ALL_PAIRS.keys()),default=["EURUSD","GBPUSD","USDJPY"])

            st.divider()
            st.markdown("**🎛️ FILTERS**")
            min_sc=st.slider("Min Score",0,100,50)
            min_cf=st.slider("Min Confirmations",0,10,3)
            show_r=st.multiselect("Ratings",["🎯 SNIPER","⚡ STRONG","✅ SETUP","👀 WATCH","⏳ WAIT","🚫 AVOID"],
                                   default=["🎯 SNIPER","⚡ STRONG","✅ SETUP","👀 WATCH","⏳ WAIT","🚫 AVOID"])
            dir_f=st.selectbox("Direction",["All","BUY only","SELL only"])

            st.divider()
            st.markdown("""<div style='font-size:10px;color:#1a3a5c;font-family:Share Tech Mono;line-height:1.8'>
            ◈ SMC: Smart Money Concepts<br>◈ OB: Order Block<br>◈ FVG: Fair Value Gap<br>
            ◈ BOS: Break of Structure<br>◈ CHoCH: Change of Character<br>◈ P/D: Premium/Discount Zone
            </div>""", unsafe_allow_html=True)

        # ============================================================
        # PAIRS TO SCAN
        # ============================================================

        if pg=="Major (7)":            pairs=list(MAJOR_PAIRS.keys())
        elif pg=="Minor/Cross (21)":   pairs=list(MINOR_PAIRS.keys())
        elif pg=="Commodities (XAUUSD)": pairs=list(COMMODITY_PAIRS.keys())
        elif pg=="Custom":             pairs=cp_list if cp_list else list(MAJOR_PAIRS.keys())
        else:                          pairs=list(ALL_PAIRS.keys())

        # ============================================================
        # SCAN + QUICK ANALYZE BUTTONS
        # ============================================================

        cb1,cb2,cb3=st.columns([2,1,1])
        with cb1: scan_btn=st.button(f"🔍 SCAN {len(pairs)} PAIRS",use_container_width=True)
        with cb2:
            if st.button("🔄 CLEAR CACHE",use_container_width=True):
                st.cache_data.clear(); st.rerun()
        with cb3:
            qp=st.selectbox("Quick Analyze",["—"]+list(ALL_PAIRS.keys()),label_visibility="collapsed")

        # ============================================================
        # QUICK SINGLE PAIR
        # ============================================================

        if qp and qp != "—":
            with st.spinner(f"Analyzing {qp}..."):
                res=analyze(qp)
            dc_=dc(res["direction"]); sc_=sc(res["score"])
            arrow="▲" if res["direction"]=="BUY" else "▼" if res["direction"]=="SELL" else "◆"
            dclass="buy" if res["direction"]=="BUY" else "sell" if res["direction"]=="SELL" else "neutral"

            st.markdown(f"""<div class='signal-card {dclass}'>
            <div style='display:flex;justify-content:space-between;align-items:center'>
                <div><span style='font-size:22px;font-weight:900;color:#e0f0ff;font-family:Share Tech Mono;
                    letter-spacing:2px'>{res["symbol"]}</span>
                <span style='margin-left:10px;color:#5a7a9a;font-family:Share Tech Mono;font-size:13px'>
                    {res["name"]} · {res["price"]:.5f}</span></div>
                <div style='text-align:right'>{badge(res["rating"])}
                <div style='font-size:22px;color:{dc_};font-weight:900;margin-top:4px'>{arrow} {res["direction"]}</div></div>
            </div></div>""", unsafe_allow_html=True)

            ca,cb_,cc,cd,ce=st.columns(5)
            mcard(ca,"SCORE",f"{res['score']}/100",sc_)
            mcard(cb_,"H4 BIAS",res["bias"],"#ffd700")
            mcard(cc,"CONFIRMATIONS",res["confirmations"],"#00bfff")
            mcard(cd,"ZONE",res["premium_zone"],"#ff8c00")
            mcard(ce,"RR RATIO",f"1:{res['rr_ratio']:.1f}","#ff8c00")

            st.markdown("<br>",unsafe_allow_html=True)
            ca2,cb2_,cc2=st.columns(3)
            mcard(ca2,"RSI",res["rsi"])
            mcard(cb2_,"ADX",res["adx"])
            mcard(cc2,"STOCH",f"{res['stoch_k']:.0f}")

            if res["direction"]!="NEUTRAL" and res["sl_pips"]>0:
                tc="#00ff88" if res["direction"]=="BUY" else "#ff3355"
                st.markdown(f"""<div class='alert-box'>
                <b style='color:{tc}'>📍 {res["direction"]} ENTRY PLAN</b><br>
                Entry <b>{res["price"]:.5f}</b> &nbsp;|&nbsp;
                SL <b style='color:#ff3355'>{res["sl_price"]:.5f}</b> ({res["sl_pips"]}p) &nbsp;|&nbsp;
                TP1 <b style='color:#00ff88'>{res["tp1_price"]:.5f}</b> ({res["tp1_pips"]}p) &nbsp;|&nbsp;
                TP2 <b style='color:#00ff88'>{res["tp2_price"]:.5f}</b> ({res["tp2_pips"]}p) &nbsp;|&nbsp;
                <b style='color:#ffd700'>RR 1:{res["rr_ratio"]:.1f}</b>
                </div>""", unsafe_allow_html=True)

            t1,t2,t3,t4,t5,t6=st.tabs(["📈 CHART","📡 SIGNALS","⚠️ WARNINGS","🏗️ SMC ZONES","📋 COT REPORT","🤖 AI ANALYSIS"])
            with t1:
                render_chart_tab(res)
            with t2:
                for s in res["signals"]:
                    st.markdown(f"<span class='conf-tag conf-pos'>{s}</span>",unsafe_allow_html=True)
            with t3:
                for w in res["warnings"]:
                    st.markdown(f"<span class='conf-tag conf-neg'>{w}</span>",unsafe_allow_html=True)
                if not res["warnings"]: st.success("No warnings ✓")
            with t4:
                if res["order_blocks"]:
                    st.markdown("**Order Blocks**")
                    for ob in res["order_blocks"]:
                        c_="#00ff88" if ob["type"]=="BULL" else "#ff3355"
                        st.markdown(f"<div class='info-row'><span style='color:{c_}'>{ob['type']} OB</span>"
                                    f"<span style='color:#7a9abf;font-family:Share Tech Mono;font-size:11px'>"
                                    f"{ob['low']:.5f}–{ob['high']:.5f} str:{ob['str']}</span></div>",
                                    unsafe_allow_html=True)
                if res["fvg"]:
                    st.markdown("**Fair Value Gaps**")
                    for f in res["fvg"]:
                        c_="#00bfff" if f["type"]=="BULL" else "#ff8c00"
                        st.markdown(f"<div class='info-row'><span style='color:{c_}'>{f['type']} FVG</span>"
                                    f"<span style='color:#7a9abf;font-family:Share Tech Mono;font-size:11px'>"
                                    f"{f['bot']:.5f}–{f['top']:.5f}</span></div>",
                                    unsafe_allow_html=True)
            with t5:
                _render_cot_tab(res["cot"], res["symbol"])
            with t6:
                render_ai_tab(res)
            st.divider()

        # ============================================================
        # MAIN SCAN
        # ============================================================

        if scan_btn:
            st.session_state["scan_results"]=[]
            st.session_state["debug_log"]=[]

            # Load COT data once for all pairs
            cot_status = st.empty()
            cot_status.markdown("<div style='font-family:Share Tech Mono;font-size:11px;color:#ffd700'>"
                                "📋 Loading COT Report from CFTC...</div>", unsafe_allow_html=True)
            cot_df = fetch_cot_data()
            if cot_df is not None:
                cot_status.markdown("<div style='font-family:Share Tech Mono;font-size:11px;color:#00ff88'>"
                                    f"✅ COT Report loaded — {len(cot_df)} records</div>", unsafe_allow_html=True)
            else:
                cot_status.markdown("<div style='font-family:Share Tech Mono;font-size:11px;color:#ff8c00'>"
                                    "⚠️ COT data unavailable — analysis continues without it</div>", unsafe_allow_html=True)

            bar=st.progress(0,"Initializing...")
            txt=st.empty()
            results=[]
            debug_log=[]
            data_ok=0; data_fail=0
            for i,sym in enumerate(pairs):
                bar.progress((i+1)/len(pairs),f"Scanning {sym}... ({i+1}/{len(pairs)})")
                txt.markdown(f"<div style='font-family:Share Tech Mono;font-size:11px;color:#5a7a9a'>"
                             f"◈ Analyzing {ALL_PAIRS.get(sym,sym)}</div>",unsafe_allow_html=True)
                try:
                    r = analyze(sym, cot_df)
                    results.append(r)
                    if r["price"] > 0:
                        data_ok += 1
                        debug_log.append(f"✅ {sym}: price={r['price']:.5f} score={r['score']} rating={r['rating']}")
                    else:
                        data_fail += 1
                        sig_preview = r["signals"][0] if r["signals"] else "no signal"
                        debug_log.append(f"❌ {sym}: no price data — {sig_preview}")
                except Exception as e:
                    data_fail += 1
                    debug_log.append(f"💥 {sym}: exception — {str(e)[:80]}")
                    results.append({"symbol":sym,"name":ALL_PAIRS.get(sym,sym),"score":0,
                        "direction":"NEUTRAL","rating":"🚫 AVOID","confirmations":0,
                        "signals":[f"Error: {e}"],"warnings":[],"price":0,"rsi":50,"adx":20,
                        "bias":"RANGING","bos":False,"choch":False,"premium_zone":"EQ","premium_pct":50,
                        "sl_pips":0,"tp1_pips":0,"tp2_pips":0,"rr_ratio":0,"sl_price":0,
                        "tp1_price":0,"tp2_price":0,"buy_s":0,"sell_s":0,"macd":0,"macd_hist":0,
                        "stoch_k":50,"stoch_d":50,"bb_pct":50,"atr":0,"order_blocks":[],"fvg":[],
                        "h1_trend":"N/A","h4_bias":"N/A","m5_momentum":"N/A","cot":_cot_empty()})
                # Small delay every 5 pairs to avoid yfinance rate limiting
                if (i + 1) % 5 == 0:
                    import time; time.sleep(1)
            bar.empty(); txt.empty(); cot_status.empty()
            st.session_state["scan_results"]=results
            st.session_state["debug_log"]=debug_log
            st.session_state["data_ok"]=data_ok
            st.session_state["data_fail"]=data_fail

        # ============================================================
        # DISPLAY RESULTS
        # ============================================================

        if st.session_state.get("scan_results"):
            results=st.session_state["scan_results"]

            # ── DEBUG PANEL ──
            data_ok   = st.session_state.get("data_ok", 0)
            data_fail = st.session_state.get("data_fail", 0)
            debug_log = st.session_state.get("debug_log", [])

            if data_fail > 0:
                with st.expander(f"⚠️ DEBUG — {data_ok} pairs OK / {data_fail} pairs FAILED (click to expand)", expanded=data_ok==0):
                    st.markdown(f"""<div style='background:#050a0e;border:1px solid #1a3a5c;border-radius:4px;
                    padding:12px;font-family:Share Tech Mono;font-size:11px;line-height:1.8'>""",
                    unsafe_allow_html=True)
                    for line in debug_log:
                        color = "#00ff88" if line.startswith("✅") else "#ff3355" if line.startswith(("❌","💥")) else "#ffd700"
                        st.markdown(f"<div style='color:{color}'>{line}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    if data_ok == 0:
                        st.markdown("""<div class='alert-box'>
                        <b style='color:#ff3355'>🚨 All data fetches failed</b><br>
                        yfinance cannot reach Yahoo Finance from this server.<br>
                        <b>Solutions:</b><br>
                        ◈ Try running locally: <code>streamlit run app.py</code><br>
                        ◈ Or check if HF Spaces has network restrictions<br>
                        ◈ yfinance sometimes needs a few minutes — try scanning again
                        </div>""", unsafe_allow_html=True)
            rorder={"🎯 SNIPER":0,"⚡ STRONG":1,"✅ SETUP":2,"👀 WATCH":3,"⏳ WAIT":4,"🚫 AVOID":5}

            filtered=[r for r in results
                      if r["score"]>=min_sc and r["confirmations"]>=min_cf
                      and r["rating"] in show_r
                      and (dir_f=="All"
                           or (dir_f=="BUY only" and r["direction"]=="BUY")
                           or (dir_f=="SELL only" and r["direction"]=="SELL"))]
            filtered.sort(key=lambda x:(rorder.get(x["rating"],9),-x["score"]))

            # Summary
            st.markdown("### 📊 SCAN SUMMARY")
            total=len(results)
            sniper=len([r for r in results if r["rating"]=="🎯 SNIPER"])
            strong=len([r for r in results if r["rating"]=="⚡ STRONG"])
            setups=len([r for r in results if r["rating"] in ["🎯 SNIPER","⚡ STRONG","✅ SETUP"]])
            buys=len([r for r in results if r["direction"]=="BUY"])
            sells=len([r for r in results if r["direction"]=="SELL"])

            c1,c2,c3,c4,c5,c6=st.columns(6)
            mcard(c1,"SCANNED",total,"#5a7a9a")
            mcard(c2,"🎯 SNIPER",sniper,"#ffd700")
            mcard(c3,"⚡ STRONG",strong,"#00ff88")
            mcard(c4,"📋 SETUPS",setups,"#00bfff")
            mcard(c5,"🟢 BUY",buys,"#00ff88")
            mcard(c6,"🔴 SELL",sells,"#ff3355")

            st.markdown(f"### 🎯 {len(filtered)} PAIRS MATCH FILTERS")

            if not filtered:
                st.markdown("<div class='alert-box'>No pairs match current filters — try lowering thresholds.</div>",
                            unsafe_allow_html=True)
            else:
                tab1,tab2,tab3,tab_cot=st.tabs(["🃏 SIGNAL CARDS","📋 TABLE","🏆 TOP SETUPS","📋 COT OVERVIEW"])

                with tab1:
                    for r in filtered[:20]:
                        dc_=dc(r["direction"]); sc_=sc(r["score"])
                        dclass="buy" if r["direction"]=="BUY" else "sell" if r["direction"]=="SELL" else "neutral"
                        arrow="▲" if r["direction"]=="BUY" else "▼" if r["direction"]=="SELL" else "◆"
                        st.markdown(f"""<div class='signal-card {dclass}'>
                        <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px'>
                            <div><span style='font-size:17px;font-weight:900;color:#e0f0ff;
                                font-family:Share Tech Mono;letter-spacing:2px'>{r["symbol"]}</span>
                            <span style='margin-left:8px;font-size:11px;color:#5a7a9a;
                                font-family:Share Tech Mono'>{r["price"]:.5f}</span></div>
                            <div style='text-align:right'>{badge(r["rating"])}
                            <div style='color:{dc_};font-size:18px;font-weight:900'>{arrow} {r["direction"]}</div>
                            </div></div>
                        <div style='display:flex;gap:10px;flex-wrap:wrap;margin-bottom:6px'>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:{sc_}'>SCORE:{r["score"]}</span>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:#00bfff'>CONF:{r["confirmations"]}</span>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:#ffd700'>H4:{r["bias"]}</span>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:#ff8c00'>ZONE:{r["premium_zone"]}</span>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:#7a9abf'>RSI:{r["rsi"]}</span>
                            <span style='font-family:Share Tech Mono;font-size:11px;color:#7a9abf'>ADX:{r["adx"]}</span>
                        </div>
                        {sbar(r["score"],sc_)}
                        <div style='margin-top:6px'>""", unsafe_allow_html=True)
                        for s in r["signals"][:3]:
                            st.markdown(f"<span class='conf-tag conf-pos'>◈ {s}</span>",unsafe_allow_html=True)
                        if r["direction"]!="NEUTRAL" and r["sl_pips"]>0:
                            tc="#00ff88" if r["direction"]=="BUY" else "#ff3355"
                            st.markdown(f"""<div style='margin-top:8px;padding:8px;background:#050a0e;
                                border-radius:4px;font-family:Share Tech Mono;font-size:11px'>
                                <span style='color:#5a7a9a'>ENTRY</span>
                                <span style='color:#e0f0ff;margin:0 8px'>{r["price"]:.5f}</span>
                                <span style='color:#ff3355'>SL {r["sl_price"]:.5f} ({r["sl_pips"]}p)</span>
                                <span style='margin:0 6px;color:#1a3a5c'>|</span>
                                <span style='color:#00ff88'>TP1 {r["tp1_price"]:.5f} ({r["tp1_pips"]}p)</span>
                                <span style='margin:0 6px;color:#1a3a5c'>|</span>
                                <span style='color:#00ff88'>TP2 {r["tp2_price"]:.5f}</span>
                                <span style='margin-left:8px;color:#ffd700'>RR 1:{r["rr_ratio"]:.1f}</span>
                            </div>""", unsafe_allow_html=True)
                        # AI Analysis button per card
                        if get_api_key():
                            ai_key = f"ai_{r['symbol']}_{r['score']}_{r['direction']}_{r['price']:.3f}"
                            if st.button(f"🤖 AI Analyze {r['symbol']}", key=f"scan_ai_{r['symbol']}", use_container_width=True):
                                with st.spinner(f"🤖 Analyzing {r['symbol']}..."):
                                    prompt = build_ai_prompt(r)
                                    ai_text, err = call_groq_api(prompt, get_api_key())
                                    st.session_state[ai_key] = ai_text if ai_text else f"ERROR:{err}"
                            if ai_key in st.session_state:
                                ai_result = st.session_state[ai_key]
                                if ai_result.startswith("ERROR:"):
                                    st.error(ai_result[6:])
                                else:
                                    with st.expander("🤖 AI Analysis Result", expanded=True):
                                        st.markdown(ai_result)
                        st.markdown("</div></div><br>",unsafe_allow_html=True)

                with tab2:
                    rows=[]
                    for r in filtered:
                        cot=r.get("cot",_cot_empty())
                        rows.append({
                            "Pair":r["symbol"],"Price":f"{r['price']:.5f}",
                            "Dir":r["direction"],"Score":r["score"],"Rating":r["rating"],
                            "Conf":r["confirmations"],"H4":r["bias"],"Zone":r["premium_zone"],
                            "RSI":r["rsi"],"ADX":r["adx"],
                            "BOS":"✓" if r.get("bos") else "","CHoCH":"✓" if r.get("choch") else "",
                            "COT Idx":f"{cot['cot_index']:.0f}" if cot["available"] else "N/A",
                            "COT Sig":cot["signal"] if cot["available"] else "N/A",
                            "SL p":r["sl_pips"],"TP1 p":r["tp1_pips"],"RR":f"1:{r['rr_ratio']:.1f}"
                        })
                    if rows:
                        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True,
                                     height=min(600,40+len(rows)*35))

                with tab3:
                    st.markdown("### 🏆 TOP 5 SETUPS")
                    top5=[r for r in filtered if r["rating"] in ["🎯 SNIPER","⚡ STRONG"]][:5]
                    if not top5: top5=filtered[:5]
                    medals=["🥇","🥈","🥉","4️⃣","5️⃣"]
                    for i,r in enumerate(top5):
                        dc_=dc(r["direction"]); sc_=sc(r["score"])
                        dclass="buy" if r["direction"]=="BUY" else "sell" if r["direction"]=="SELL" else "neutral"
                        st.markdown(f"""<div class='signal-card {dclass}'>
                        <div style='display:flex;justify-content:space-between'>
                            <div><span style='font-size:16px'>{medals[i]}</span>
                            <span style='font-size:22px;font-weight:900;color:#e0f0ff;
                                font-family:Share Tech Mono;margin-left:8px'>{r["symbol"]}</span>
                            <span style='font-size:20px;font-weight:900;color:{dc_};margin-left:12px'>
                                {r["direction"]}</span></div>
                            <div style='text-align:right'>
                                <div style='font-size:30px;font-weight:900;color:{sc_};
                                    font-family:Share Tech Mono'>{r["score"]}</div>
                                <div style='font-size:9px;color:#5a7a9a;letter-spacing:1px'>SNIPER SCORE</div>
                            </div></div>
                        {sbar(r["score"],sc_)}
                        <div style='margin-top:10px;font-family:Share Tech Mono;font-size:11px;
                            color:#7a9abf;line-height:1.8'>
                            ◈ {r["price"]:.5f} &nbsp;|&nbsp; SL {r["sl_price"]:.5f} ({r["sl_pips"]}p)
                            &nbsp;|&nbsp; TP1 {r["tp1_price"]:.5f} &nbsp;|&nbsp; TP2 {r["tp2_price"]:.5f}
                            &nbsp;|&nbsp; <span style='color:#ffd700'>RR 1:{r["rr_ratio"]:.1f}</span>
                        </div><div style='margin-top:6px'>""", unsafe_allow_html=True)
                        for s in r["signals"][:4]:
                            st.markdown(f"<span class='conf-tag conf-pos'>{s}</span>",unsafe_allow_html=True)
                        st.markdown("</div></div><br>",unsafe_allow_html=True)

                with tab_cot:
                    st.markdown("### 📋 COT REPORT — INSTITUTIONAL POSITIONING OVERVIEW")
                    st.caption("CFTC Traders in Financial Futures | Updated every Friday | Source: CFTC.gov")
                    st.divider()

                    # Check if any COT data available
                    cot_available = any(r.get("cot",{}).get("available") for r in results)
                    if not cot_available:
                        st.markdown("""<div class='alert-box'>
                        <b style='color:#ffd700'>⚠️ COT data was not loaded</b><br>
                        CFTC may be unreachable or data may not be available yet.
                        COT is published every Friday ~3:30 PM EST.
                        The scanner still works with all other 5 layers.
                        </div>""", unsafe_allow_html=True)
                    else:
                        # Sort by COT index for most bullish/bearish
                        cot_results = [(r["symbol"], r.get("cot",_cot_empty()))
                                       for r in results if r.get("cot",{}).get("available")]
                        cot_bull = sorted([(s,c) for s,c in cot_results if c["signal"]=="BULLISH"],
                                          key=lambda x:-x[1]["cot_index"])
                        cot_bear = sorted([(s,c) for s,c in cot_results if c["signal"]=="BEARISH"],
                                          key=lambda x:x[1]["cot_index"])
                        cot_neut = [(s,c) for s,c in cot_results if c["signal"]=="NEUTRAL"]

                        col_l, col_r = st.columns(2)
                        with col_l:
                            st.markdown(f"**🟢 INSTITUTIONALLY BULLISH ({len(cot_bull)})**")
                            for sym, cot in cot_bull[:10]:
                                ci=cot["cot_index"]
                                bar_w=int(ci)
                                st.markdown(f"""
                                <div style='margin:6px 0'>
                                    <div style='display:flex;justify-content:space-between;
                                        font-family:Share Tech Mono;font-size:12px;margin-bottom:3px'>
                                        <span style='color:#e0f0ff'>{sym}</span>
                                        <span style='color:#00ff88'>Index:{ci:.0f} | Net:{cot["dealer_net"]:+,}</span>
                                    </div>
                                    <div style='background:#050a0e;border-radius:2px;height:4px'>
                                        <div style='width:{bar_w}%;height:100%;background:#00ff88;border-radius:2px'></div>
                                    </div>
                                </div>""", unsafe_allow_html=True)

                        with col_r:
                            st.markdown(f"**🔴 INSTITUTIONALLY BEARISH ({len(cot_bear)})**")
                            for sym, cot in cot_bear[:10]:
                                ci=cot["cot_index"]
                                bar_w=int(100-ci)
                                st.markdown(f"""
                                <div style='margin:6px 0'>
                                    <div style='display:flex;justify-content:space-between;
                                        font-family:Share Tech Mono;font-size:12px;margin-bottom:3px'>
                                        <span style='color:#e0f0ff'>{sym}</span>
                                        <span style='color:#ff3355'>Index:{ci:.0f} | Net:{cot["dealer_net"]:+,}</span>
                                    </div>
                                    <div style='background:#050a0e;border-radius:2px;height:4px'>
                                        <div style='width:{bar_w}%;height:100%;background:#ff3355;border-radius:2px'></div>
                                    </div>
                                </div>""", unsafe_allow_html=True)

                        # Extreme alerts
                        extremes = [(s,c) for s,c in cot_results if c["extreme"]]
                        if extremes:
                            st.divider()
                            st.markdown("**⚠️ EXTREME POSITIONING ALERTS — Potential Reversal Zones**")
                            for sym, cot in extremes:
                                ci = cot["cot_index"]
                                if ci > 80:
                                    msg = f"🔴 {sym}: EXTREME LONG (Index:{ci:.0f}) — institutions max long, reversal risk"
                                    col = "#ff8c00"
                                else:
                                    msg = f"🟢 {sym}: EXTREME SHORT (Index:{ci:.0f}) — institutions max short, bounce risk"
                                    col = "#00bfff"
                                st.markdown(f"<div style='font-family:Share Tech Mono;font-size:12px;"
                                            f"color:{col};padding:4px 0'>{msg}</div>", unsafe_allow_html=True)

            # Market overview
            st.divider()
            st.markdown("### 🌐 MARKET OVERVIEW")
            all_buy=sorted([r for r in results if r["direction"]=="BUY"],key=lambda x:-x["score"])
            all_sell=sorted([r for r in results if r["direction"]=="SELL"],key=lambda x:-x["score"])
            all_neut=[r for r in results if r["direction"]=="NEUTRAL"]

            co1,co2,co3=st.columns(3)
            with co1:
                st.markdown(f"**🟢 BUY ({len(all_buy)})**")
                for r in all_buy[:10]:
                    s_=sc(r["score"])
                    st.markdown(f"<div class='info-row'>"
                                f"<span style='color:#e0f0ff;font-family:Share Tech Mono;font-size:12px'>{r['symbol']}</span>"
                                f"<span style='color:{s_};font-family:Share Tech Mono;font-size:12px'>{r['score']} {r['rating'].split()[0]}</span></div>",
                                unsafe_allow_html=True)
            with co2:
                st.markdown(f"**🔴 SELL ({len(all_sell)})**")
                for r in all_sell[:10]:
                    s_=sc(r["score"])
                    st.markdown(f"<div class='info-row'>"
                                f"<span style='color:#e0f0ff;font-family:Share Tech Mono;font-size:12px'>{r['symbol']}</span>"
                                f"<span style='color:{s_};font-family:Share Tech Mono;font-size:12px'>{r['score']} {r['rating'].split()[0]}</span></div>",
                                unsafe_allow_html=True)
            with co3:
                st.markdown(f"**⚪ NEUTRAL ({len(all_neut)})**")
                for r in all_neut[:10]:
                    st.markdown(f"<div class='info-row'>"
                                f"<span style='color:#5a7a9a;font-family:Share Tech Mono;font-size:12px'>{r['symbol']}</span>"
                                f"<span style='color:#1a3a5c;font-family:Share Tech Mono;font-size:12px'>{r['score']}</span></div>",
                                unsafe_allow_html=True)

        # Empty state
        elif not st.session_state.get("scan_results"):
            st.markdown("""<div style='text-align:center;padding:60px 20px'>
            <div style='font-size:64px;margin-bottom:20px'>🎯</div>
            <div style='font-family:Share Tech Mono;font-size:22px;color:#5a7a9a;
                letter-spacing:4px;margin-bottom:12px'>SCANNER READY</div>
            <div style='font-family:Share Tech Mono;font-size:11px;color:#1a3a5c;
                line-height:2.2;max-width:480px;margin:auto'>
                ◈ LAYER 1 — H4 Market Structure (BOS / CHoCH)<br>
                ◈ LAYER 2 — SMC Zones (Order Block / FVG / Liquidity)<br>
                ◈ LAYER 3 — Classic Indicators (RSI / MACD / ADX / Stoch / BB)<br>
                ◈ LAYER 4 — Session Filter (London / NY / Tokyo / Sydney)<br>
                ◈ LAYER 5 — M5 Entry Trigger (Engulfing / Hammer / Pin Bar)
            </div></div>""", unsafe_allow_html=True)

        # Footer
        st.divider()
        st.markdown("""<div style='text-align:center;font-family:Share Tech Mono;font-size:10px;
        color:#1a3a5c;letter-spacing:2px;padding:10px'>
        SNIPER FX v1.0 ◈ EDUCATIONAL PURPOSES ONLY ◈ NOT FINANCIAL ADVICE ◈
        ALWAYS USE PROPER RISK MANAGEMENT ◈ MAX 1-2% RISK PER TRADE
        </div>""", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # MODE: BID>OFFER ANOMALY + VOLATILITY SCANNER (App6)
    # ══════════════════════════════════════════════════════════
    elif "Bid>Offer" in scan_mode or "Volatility" in scan_mode:
        stocks_src = st.session_state.get('_custom_tickers', DEFAULT_SAHAM_IDX_955)
        vol_thr    = cfg.get('vol_threshold', 25.0)
        max_s      = cfg.get('max_stocks', 100)
        min_p      = cfg.get('min_price', 0)
        max_p      = cfg.get('max_price', 999999)
        min_vol    = cfg.get('min_volume', 0)
        mode_a6    = cfg.get('mode_a6', 'Kombinasi (All-in-One)')

        if st.button("🚀 MULAI SCANNING", type="primary", use_container_width=True):
            prog    = st.progress(0)
            status  = st.empty()
            stocks_list = stocks_src[:max_s]
            results_bid_offer, results_volatility, errors = [], [], []
            for idx, ticker in enumerate(stocks_list):
                prog.progress((idx+1)/len(stocks_list))
                status.text(f"🔍 Scanning {ticker}... ({idx+1}/{len(stocks_list)})")
                try:
                    info = yf.Ticker(ticker).info
                    hist = yf.Ticker(ticker).history(period="5d")
                    if info:
                        cur_p = info.get('currentPrice',0) or info.get('regularMarketPrice',0)
                        if cur_p and (cur_p < min_p or cur_p > max_p): continue
                        vol = info.get('volume',0)
                        if vol < min_vol*100: continue
                        bid = info.get('bid',0); ask = info.get('ask',0)
                        if bid and ask and bid > ask:
                            prev_c = info.get('previousClose',0)
                            chg = (cur_p-prev_c)/prev_c*100 if prev_c else 0
                            results_bid_offer.append({
                                'Ticker':ticker.replace('.JK',''),
                                'Nama':info.get('longName',info.get('shortName','N/A'))[:25],
                                'Bid':bid,'Offer/Ask':ask,
                                'Anomaly %':round((bid-ask)/ask*100,2),
                                'Current Price':cur_p,'Change %':round(chg,2),
                                'Volume':vol,
                                'Market Cap (B)':round(info.get('marketCap',0)/1e9,2) if info.get('marketCap') else 0
                            })
                        if hist is not None and len(hist)>=3:
                            vd = calculate_volatility_a6(hist)
                            if vd and vd['volatility']>=vol_thr:
                                results_volatility.append({
                                    'Ticker':ticker.replace('.JK',''),
                                    'Nama':info.get('longName',info.get('shortName','N/A'))[:25],
                                    'Volatility (%)':round(vd['volatility'],2),
                                    'Current Price':vd['current_price'],
                                    'Price Change 5D (%)':round(vd['price_change_5d'],2),
                                    'Avg Volume':int(vd['avg_volume']),
                                    'High 5D':vd['high_5d'],'Low 5D':vd['low_5d'],
                                    'Range %':round((vd['high_5d']-vd['low_5d'])/vd['low_5d']*100,2),
                                    'Market Cap (B)':round(info.get('marketCap',0)/1e9,2) if info.get('marketCap') else 0
                                })
                except Exception as e:
                    errors.append(f"{ticker}: {str(e)}")
                time.sleep(0.05)
            prog.empty(); status.empty()
            st.session_state['_a6_bid'] = results_bid_offer
            st.session_state['_a6_vol'] = results_volatility
            st.session_state['_a6_errors'] = errors
            st.session_state['_a6_scanned'] = len(stocks_list)
            st.rerun()

        # ── Results ───────────────────────────────────────────
        bid_res = st.session_state.get('_a6_bid',[])
        vol_res = st.session_state.get('_a6_vol',[])
        errors  = st.session_state.get('_a6_errors',[])
        scanned = st.session_state.get('_a6_scanned',0)

        if scanned:
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("📊 Total Scanned", scanned)
            c2.metric("🚨 Bid>Offer",      len(bid_res))
            c3.metric("⚡ High Volatility", len(vol_res))
            c4.metric("❌ Errors",          len(errors))
            st.divider()

        if bid_res and mode_a6 in ["Bid > Offer (Anomaly)","Kombinasi (All-in-One)"]:
            st.markdown("## 🚨 BID > OFFER ANOMALIES")
            df_bo = pd.DataFrame(bid_res).sort_values('Anomaly %',ascending=False)
            top4 = df_bo.head(4)
            cols = st.columns(4)
            for i,(_, row) in enumerate(top4.iterrows()):
                with cols[i]:
                    st.markdown(f"""<div class='anomaly-card' style='background:linear-gradient(135deg,#f093fb,#f5576c);
                    padding:1rem;border-radius:10px;color:white;margin:4px 0;'>
                    <h3 style='margin:0'>{row['Ticker']}</h3>
                    <p style='margin:2px 0;font-size:0.85rem'>{row['Nama']}</p>
                    <p style='margin:2px 0'>Bid: <b>Rp {row['Bid']:,.0f}</b></p>
                    <p style='margin:2px 0'>Ask: <b>Rp {row['Offer/Ask']:,.0f}</b></p>
                    <h4 style='margin:4px 0'>Anomaly: {row['Anomaly %']:.2f}%</h4>
                    <small>Change: {row['Change %']:+.2f}%</small></div>""", unsafe_allow_html=True)
            st.dataframe(df_bo.style
                .background_gradient(subset=['Anomaly %'],cmap='Reds')
                .background_gradient(subset=['Change %'],cmap='RdYlGn',vmin=-10,vmax=10)
                .format({'Bid':'Rp {:,.0f}','Offer/Ask':'Rp {:,.0f}',
                         'Current Price':'Rp {:,.0f}','Anomaly %':'{:.2f}%',
                         'Change %':'{:+.2f}%','Volume':'{:,.0f}','Market Cap (B)':'Rp {:,.0f}B'}),
                use_container_width=True, height=400)
            st.download_button("📥 Download CSV Bid/Offer",
                df_bo.to_csv(index=False),
                f"bid_offer_{datetime.now().strftime('%Y%m%d_%H%M')}.csv","text/csv")

        if vol_res and mode_a6 in ["Volatility Scanner","Kombinasi (All-in-One)"]:
            st.divider()
            st.markdown("## ⚡ VOLATILITY SCANNER")
            df_v = pd.DataFrame(vol_res).sort_values('Volatility (%)',ascending=False)
            col1,col2 = st.columns(2)
            with col1:
                st.markdown("### 📊 Top 15 Volatility")
                top15 = df_v.head(15)
                fig = go.Figure(go.Bar(x=top15['Ticker'],y=top15['Volatility (%)'],
                    marker_color=top15['Volatility (%)'],marker_colorscale='Viridis',
                    text=top15['Volatility (%)'].round(1),textposition='auto'))
                fig.update_layout(template="plotly_dark",height=350,showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown("### 🎯 Volatility vs Return")
                fig2 = go.Figure(go.Scatter(x=df_v['Volatility (%)'],y=df_v['Price Change 5D (%)'],
                    mode='markers',marker=dict(size=df_v['Range %']*1.5,
                    color=df_v['Price Change 5D (%)'],colorscale='RdYlGn',showscale=True),
                    text=df_v['Ticker'],
                    hovertemplate='<b>%{text}</b><br>Vol: %{x:.1f}%<br>Change: %{y:.1f}%'))
                fig2.update_layout(template="plotly_dark",height=350)
                st.plotly_chart(fig2, use_container_width=True)
            st.dataframe(df_v.style
                .background_gradient(subset=['Volatility (%)','Range %'],cmap='YlOrRd')
                .background_gradient(subset=['Price Change 5D (%)'],cmap='RdYlGn',vmin=-20,vmax=20)
                .format({'Current Price':'Rp {:,.0f}','High 5D':'Rp {:,.0f}','Low 5D':'Rp {:,.0f}',
                         'Volatility (%)':'{:.2f}','Price Change 5D (%)':'{:+.2f}',
                         'Range %':'{:.2f}','Avg Volume':'{:,.0f}','Market Cap (B)':'Rp {:,.0f}B'}),
                use_container_width=True, height=400)
            st.download_button("📥 Download CSV Volatility",
                df_v.to_csv(index=False),
                f"volatility_{datetime.now().strftime('%Y%m%d_%H%M')}.csv","text/csv")

        if errors:
            with st.expander(f"⚠️ Errors ({len(errors)} saham)"):
                for e in errors[:20]: st.text(e)
        elif not scanned:
            col1,col2,col3 = st.columns(3)
            with col1:
                st.markdown("""<div style='background:linear-gradient(135deg,#667eea,#764ba2);
                padding:2rem;border-radius:15px;color:white;text-align:center;'>
                <h2>🎯</h2><h3>Bid > Offer Scanner</h3>
                <p>Deteksi anomaly dimana bid > offer. Signal buyer aggressive.</p></div>""",unsafe_allow_html=True)
            with col2:
                st.markdown("""<div style='background:linear-gradient(135deg,#f093fb,#f5576c);
                padding:2rem;border-radius:15px;color:white;text-align:center;'>
                <h2>⚡</h2><h3>Volatility Scanner</h3>
                <p>Temukan saham paling volatile untuk trading opportunity.</p></div>""",unsafe_allow_html=True)
            with col3:
                st.markdown("""<div style='background:linear-gradient(135deg,#4facfe,#00f2fe);
                padding:2rem;border-radius:15px;color:white;text-align:center;'>
                <h2>📁</h2><h3>Custom List</h3>
                <p>Upload daftar saham sendiri via sidebar!</p></div>""",unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════
    # MODE: OPEN=LOW IDX
    # ══════════════════════════════════════════════════════════
    elif "Open=Low" in scan_mode:


            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 24px;">
                <span style="width: 3px; height: 24px; background: linear-gradient(180deg, #00d4aa, transparent); 
                             border-radius: 2px; display: inline-block;"></span>
                <h2 style="color: #e6edf3; font-size: 1.1rem; font-weight: 600; margin: 0; letter-spacing: 0.3px; font-family: 'Space Grotesk', sans-serif;">
                    Scanner Open = Low &nbsp;<span style="color: #484f58; font-weight: 400; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace;">+ KENAIKAN ≥5%</span>
                </h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                periode = st.selectbox(
                    "Periode Analisis",
                    ["7 Hari", "14 Hari", "30 Hari", "90 Hari", "180 Hari", "365 Hari"],
                    index=2
                )
            with col2:
                min_kenaikan = st.slider("Minimal Kenaikan (%)", 1, 20, 5)
            with col3:
                limit_saham = st.number_input("Limit Hasil", min_value=5, max_value=100, value=20)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            col_par1, col_par2 = st.columns([1, 2])
            with col_par1:
                use_parallel = st.checkbox("⚡ Parallel Scanning", value=True)
            with col_par2:
                st.markdown("""
                <div style="background: rgba(0,212,170,0.05); border: 1px solid rgba(0,212,170,0.15); 
                            padding: 8px 14px; border-radius: 8px; margin-top: 2px;">
                    <span style="color: #00d4aa; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;">
                        ⚡ Parallel mode &nbsp;·&nbsp; 5–10× lebih cepat
                    </span>
                </div>
                """, unsafe_allow_html=True)

            periode_map = {"7 Hari": 7, "14 Hari": 14, "30 Hari": 30, "90 Hari": 90, "180 Hari": 180, "365 Hari": 365}
            hari = periode_map[periode]

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🚀  MULAI SCANNING", type="primary", use_container_width=True):
                reset_session_data()

                if filter_type == "Pilih Manual" and selected_stocks:
                    stocks_to_scan = selected_stocks
                elif filter_type == "Filter Tingkatan" and selected_levels:
                    stocks_to_scan = get_stocks_by_level(selected_levels)
                else:
                    stocks_to_scan = STOCKS_LIST

                estimasi_detik = len(stocks_to_scan) * (0.1 if use_parallel else 0.5)

                st.markdown(f"""
                <div style="background: rgba(77,166,255,0.06); border: 1px solid rgba(77,166,255,0.15); 
                            padding: 12px 16px; border-radius: 10px; margin: 12px 0;
                            display: flex; align-items: center; gap: 12px;">
                    <span style="color: #4da6ff; font-size: 1.2rem;">⏳</span>
                    <div>
                        <span style="color: #4da6ff; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600;">
                            {len(stocks_to_scan)} SAHAM
                        </span>
                        <span style="color: #484f58; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-left: 12px;">
                            estimasi ~{estimasi_detik:.0f} detik
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                start_time = time.time()

                if use_parallel:
                    results = scan_stocks_parallel(
                        stocks_to_scan, scan_open_low_pattern,
                        periode_hari=hari, min_kenaikan=min_kenaikan
                    )
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    results = []
                    for i, stock in enumerate(stocks_to_scan):
                        status_text.markdown(f"<span style='color:#8b949e; font-family:monospace; font-size:0.82rem;'>Memproses {stock}... ({i+1}/{len(stocks_to_scan)})</span>", unsafe_allow_html=True)
                        try:
                            result = scan_open_low_pattern(stock, periode_hari=hari, min_kenaikan=min_kenaikan)
                            if result:
                                results.append(result)
                        except:
                            pass
                        progress_bar.progress((i + 1) / len(stocks_to_scan))
                        time.sleep(0.3)
                    progress_bar.empty()
                    status_text.empty()

                total_time = time.time() - start_time

                if results:
                    df_results = pd.DataFrame(results)
                    df_results = df_results.sort_values('frekuensi', ascending=False).head(limit_saham)

                    # ── SUCCESS CARD ──
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0d1f17 0%, #0d1a24 100%);
                                border: 1px solid rgba(0,212,170,0.25); border-radius: 16px;
                                padding: 28px 32px; margin: 24px 0 32px 0;
                                box-shadow: 0 0 40px rgba(0,212,170,0.08), inset 0 1px 0 rgba(0,212,170,0.1);
                                position: relative; overflow: hidden;">
                        <div style="position: absolute; top: -40px; right: -40px; width: 160px; height: 160px;
                                     background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
                                     border-radius: 50%;"></div>
                        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
                            <div>
                                <p style="color: #00d4aa; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; 
                                          letter-spacing: 2px; text-transform: uppercase; margin: 0 0 6px 0;">SCAN BERHASIL</p>
                                <p style="color: #e6edf3; font-size: 2.8rem; font-weight: 700; margin: 0; line-height: 1; 
                                          font-family: 'JetBrains Mono', monospace;">
                                    {len(df_results)}<span style="color: #00d4aa;">.</span>
                                </p>
                                <p style="color: #8b949e; font-size: 0.85rem; margin: 6px 0 0 0;">Saham pola Open = Low ditemukan</p>
                            </div>
                            <div style="display: flex; gap: 24px;">
                                <div style="text-align: center; padding: 12px 20px; background: rgba(255,255,255,0.03); 
                                            border-radius: 10px; border: 1px solid #21262d;">
                                    <p style="color: #484f58; font-size: 0.68rem; letter-spacing: 1.5px; text-transform: uppercase; 
                                              font-family: 'JetBrains Mono', monospace; margin: 0 0 4px 0;">DURASI</p>
                                    <p style="color: #e6edf3; font-size: 1.4rem; font-weight: 700; margin: 0; 
                                              font-family: 'JetBrains Mono', monospace;">{total_time:.0f}<span style="color: #484f58; font-size: 0.9rem;">s</span></p>
                                </div>
                                <div style="text-align: center; padding: 12px 20px; background: rgba(255,255,255,0.03); 
                                            border-radius: 10px; border: 1px solid #21262d;">
                                    <p style="color: #484f58; font-size: 0.68rem; letter-spacing: 1.5px; text-transform: uppercase; 
                                              font-family: 'JetBrains Mono', monospace; margin: 0 0 4px 0;">PERIODE</p>
                                    <p style="color: #e6edf3; font-size: 1.4rem; font-weight: 700; margin: 0; 
                                              font-family: 'JetBrains Mono', monospace;">{hari}<span style="color: #484f58; font-size: 0.9rem;">d</span></p>
                                </div>
                                <div style="text-align: center; padding: 12px 20px; background: rgba(255,255,255,0.03); 
                                            border-radius: 10px; border: 1px solid #21262d;">
                                    <p style="color: #484f58; font-size: 0.68rem; letter-spacing: 1.5px; text-transform: uppercase; 
                                              font-family: 'JetBrains Mono', monospace; margin: 0 0 4px 0;">MIN GAIN</p>
                                    <p style="color: #e6edf3; font-size: 1.4rem; font-weight: 700; margin: 0; 
                                              font-family: 'JetBrains Mono', monospace;">{min_kenaikan}<span style="color: #484f58; font-size: 0.9rem;">%</span></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── SECTION LABEL ──
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 24px 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #00d4aa; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Hasil Scanning · Free Float · FCA · Tingkatan</p>
                    </div>
                    """, unsafe_allow_html=True)

                    enhanced_results = []
                    for _, row in df_results.iterrows():
                        saham = row['saham']
                        free_float = get_free_float_value(saham)
                        holders = get_free_float_holders(saham)
                        level = get_stock_level(saham)

                        total_inst_asing = 0
                        for p in holders:
                            persen_dalam_ff = (p['persen'] / free_float) * 100 if free_float > 0 else 0
                            total_inst_asing += persen_dalam_ff

                        sisa_ritel = 100 - total_inst_asing
                        potensi = analyze_goreng_potential(free_float)
                        fca_status = '⚠️' if is_fca(saham) else '—'

                        enhanced_results.append({
                            'Saham': saham,
                            'Level': level,
                            'Frek': row['frekuensi'],
                            'Prob_Val': row['probabilitas'],
                            'Prob': f"{row['probabilitas']:.0f}%",
                            'Gain_Val': row['rata_rata_kenaikan'],
                            'Gain': f"{row['rata_rata_kenaikan']:.0f}%",
                            'FF_Val': free_float,
                            'FF': f"{free_float:.0f}%",
                            'Inst_Val': total_inst_asing,
                            'Inst': f"{total_inst_asing:.0f}%",
                            'Ritel_Val': sisa_ritel,
                            'Ritel': f"{sisa_ritel:.0f}%",
                            'FCA': fca_status,
                            'Pot': potensi
                        })

                    enhanced_df = pd.DataFrame(enhanced_results)
                    display_df = enhanced_df[['Saham', 'Level', 'Frek', 'Prob', 'Gain', 'FF', 'Inst', 'Ritel', 'FCA', 'Pot']]
                    st.dataframe(display_df, use_container_width=True, height=500, hide_index=True)

                    st.session_state['scan_results'] = df_results
                    st.session_state['enhanced_df'] = enhanced_df
                    st.session_state['display_df'] = display_df
                    st.session_state['watchlist_df'] = None

                    # ── CHART ──
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 28px 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #4da6ff; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Top 10 · Frekuensi Tertinggi</p>
                    </div>
                    """, unsafe_allow_html=True)

                    top10_df = df_results.head(10).copy()
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=top10_df['saham'],
                        y=top10_df['frekuensi'],
                        marker=dict(
                            color=top10_df['probabilitas'].tolist(),
                            colorscale='Teal',
                            showscale=True,
                            colorbar=dict(
                                title=dict(
                                    text="Prob (%)",
                                    font=dict(color='#8b949e', size=10, family='JetBrains Mono')
                                ),
                                tickfont=dict(color='#8b949e', size=10, family='JetBrains Mono'),
                                outlinecolor='#21262d',
                                outlinewidth=1
                            ),
                            line=dict(width=0),
                            opacity=0.9
                        ),
                        hovertemplate='<b>%{x}</b><br>Frekuensi: %{y}<br>Prob: %{marker.color:.1f}%<extra></extra>'
                    ))
                    fig.update_layout(
                        plot_bgcolor='#0d1117',
                        paper_bgcolor='#0d1117',
                        font=dict(family='JetBrains Mono', color='#8b949e', size=11),
                        xaxis=dict(
                            categoryorder='array',
                            categoryarray=top10_df['saham'].tolist(),
                            gridcolor='#21262d',
                            tickfont=dict(color='#8b949e'),
                            title=dict(text='', font=dict(color='#484f58'))
                        ),
                        yaxis=dict(
                            gridcolor='#21262d',
                            tickfont=dict(color='#8b949e'),
                            title=dict(text='Frekuensi', font=dict(color='#484f58', size=10))
                        ),
                        height=360,
                        margin=dict(l=40, r=60, t=20, b=40),
                        hoverlabel=dict(bgcolor='#161b22', bordercolor='#30363d', font=dict(color='#e6edf3'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption(f"Urutan: {' · '.join(top10_df['saham'].tolist())}")

                    # ── AI ANALYSIS ──
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 32px 0 16px 0;">
                        <span style="width: 3px; height: 18px; background: #c084fc; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Analisis AI · Top 5 Saham</p>
                    </div>
                    """, unsafe_allow_html=True)

                    for idx, (i, row) in enumerate(df_results.head(5).iterrows()):
                        analysis = analyze_pattern(row.to_dict())
                        level = get_stock_level(row['saham'])

                        with st.expander(f"#{idx+1} &nbsp; {row['saham']} &nbsp;·&nbsp; {level} &nbsp;·&nbsp; Prob {row['probabilitas']:.1f}%"):
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Probabilitas", f"{row['probabilitas']:.1f}%")
                            with col2:
                                st.metric("Rata Gain", f"{row['rata_rata_kenaikan']:.1f}%")
                            with col3:
                                st.metric("Max Gain", f"{row['max_kenaikan']:.1f}%")
                            with col4:
                                st.metric("Frekuensi", f"{row['frekuensi']}x")

                            st.markdown(f"""
                            <div style="background: rgba(192,132,252,0.05); border: 1px solid rgba(192,132,252,0.15); 
                                        border-radius: 10px; padding: 14px 16px; margin: 12px 0;">
                                <p style="color: #484f58; font-size: 0.68rem; letter-spacing: 2px; text-transform: uppercase;
                                          font-family: 'JetBrains Mono', monospace; margin: 0 0 8px 0;">AI SUMMARY</p>
                                <p style="color: #c9d1d9; font-size: 0.88rem; margin: 0; line-height: 1.6;">{analysis}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            free_float = get_free_float_value(row['saham'])
                            st.markdown(display_free_float_info(row['saham'], free_float), unsafe_allow_html=True)

                    # ── WATCHLIST ──
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 32px 0 16px 0;">
                        <span style="width: 3px; height: 18px; background: #e3b341; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Watchlist Generator</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        min_gain_filter = st.slider("Minimal Gain Rata-rata (%)", 3, 10, 5, key="min_gain")
                    with col2:
                        top_n = st.number_input("Jumlah Saham", 5, 30, 15, key="top_n")

                    if 'enhanced_df' in st.session_state:
                        df_watchlist = st.session_state['enhanced_df'][st.session_state['enhanced_df']['Gain_Val'] >= min_gain_filter].copy()
                    else:
                        df_watchlist = enhanced_df[enhanced_df['Gain_Val'] >= min_gain_filter].copy()

                    if len(df_watchlist) > 0:
                        max_prob = df_watchlist['Prob_Val'].max()
                        max_gain = df_watchlist['Gain_Val'].max()

                        if max_prob > 0 and max_gain > 0:
                            df_watchlist['skor'] = (
                                (df_watchlist['Prob_Val'] / max_prob) * 50 +
                                (df_watchlist['Gain_Val'] / max_gain) * 50
                            )
                            df_watchlist = df_watchlist.nlargest(top_n, 'skor')

                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #0f1a0f 0%, #0a1520 100%);
                                    border: 1px solid rgba(227,179,65,0.2); border-radius: 14px;
                                    padding: 20px 24px; margin: 16px 0 20px 0;
                                    box-shadow: 0 0 30px rgba(227,179,65,0.05);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <p style="color: #e3b341; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; 
                                              letter-spacing: 2px; text-transform: uppercase; margin: 0 0 4px 0;">WATCHLIST TRADING</p>
                                    <p style="color: #e6edf3; font-size: 1rem; font-weight: 600; margin: 0; font-family: 'Space Grotesk', sans-serif;">
                                        {datetime.now().strftime('%d %B %Y')}
                                    </p>
                                </div>
                                <div style="background: rgba(227,179,65,0.1); border: 1px solid rgba(227,179,65,0.2); 
                                            padding: 8px 16px; border-radius: 8px;">
                                    <span style="color: #e3b341; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 600;">
                                        ⚡ PANTAU 15 MENIT PERTAMA
                                    </span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        watchlist_data = []
                        for i, (idx, row) in enumerate(df_watchlist.iterrows()):
                            if row['Prob_Val'] >= 20 and row['Gain_Val'] >= 7:
                                rekom = "🔥 PRIORITAS"
                            elif row['Prob_Val'] >= 15 and row['Gain_Val'] >= 5:
                                rekom = "⚡ LAYAK"
                            else:
                                rekom = "📌 PANTAU"

                            level_singkat = {'💎 Blue Chip': 'BC', '📈 Second Liner': 'SL', '🎯 Third Liner': 'TL'}.get(row['Level'], '')

                            watchlist_data.append({
                                "Rank": i + 1,
                                "Saham": row['Saham'],
                                "Lvl": level_singkat,
                                "Prob": row['Prob'],
                                "Gain": row['Gain'],
                                "FF": row['FF'],
                                "FCA": row['FCA'],
                                "Pot": row['Pot'],
                                "Rekom": rekom
                            })

                        watchlist_df = pd.DataFrame(watchlist_data)
                        st.session_state['watchlist_df'] = watchlist_df
                        st.dataframe(watchlist_df, use_container_width=True, hide_index=True, height=400)

                        # ── EXPORT ──
                        st.markdown("""
                        <div style="display: flex; align-items: center; gap: 10px; margin: 28px 0 12px 0;">
                            <span style="width: 3px; height: 18px; background: #4da6ff; border-radius: 2px; display: inline-block;"></span>
                            <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                      font-family: 'JetBrains Mono', monospace; margin: 0;">Export Data</p>
                        </div>
                        """, unsafe_allow_html=True)

                        tab_exp1, tab_exp2 = st.tabs(["📋 Watchlist", "📊 Hasil Scanning"])

                        with tab_exp1:
                            if 'watchlist_df' in st.session_state and st.session_state['watchlist_df'] is not None:
                                create_download_buttons(st.session_state['watchlist_df'], "watchlist", "watchlist_tab")

                        with tab_exp2:
                            if 'display_df' in st.session_state:
                                create_download_buttons(st.session_state['display_df'], "scan", "scan_tab")

                    else:
                        st.warning(f"Tidak ada saham dengan gain minimal {min_gain_filter}%")

                else:
                    st.markdown("""
                    <div style="background: rgba(255,92,92,0.06); border: 1px solid rgba(255,92,92,0.2); 
                                border-radius: 12px; padding: 24px; text-align: center; margin: 16px 0;">
                        <p style="color: #ff5c5c; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; margin: 0;">
                            ⚠ &nbsp; Tidak ditemukan saham dengan kriteria Open = Low
                        </p>
                    </div>
                    """, unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════
    # MODE: LOW FLOAT IDX
    # ══════════════════════════════════════════════════════════
    elif "Low Float" in scan_mode:


            st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 24px;">
                <span style="width: 3px; height: 24px; background: linear-gradient(180deg, #4da6ff, transparent); 
                             border-radius: 2px; display: inline-block;"></span>
                <h2 style="color: #e6edf3; font-size: 1.1rem; font-weight: 600; margin: 0; letter-spacing: 0.3px; font-family: 'Space Grotesk', sans-serif;">
                    Scanner Low Float &nbsp;<span style="color: #484f58; font-weight: 400; font-size: 0.85rem; font-family: 'JetBrains Mono', monospace;">+ FREE FLOAT + FCA</span>
                </h2>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                max_ff = st.slider("Maks Free Float (%)", 1, 50, 20)
            with col2:
                min_vol = st.number_input("Min Volume", min_value=0, value=0, step=100000)

            st.markdown("""<p style="color: #484f58; font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; 
                          font-family: 'JetBrains Mono', monospace; margin: 16px 0 10px 0;">FILTER TINGKATAN</p>""", unsafe_allow_html=True)

            col_lvl1, col_lvl2, col_lvl3 = st.columns(3)
            with col_lvl1:
                scan_blue = st.checkbox("💎 Blue Chip", value=True)
            with col_lvl2:
                scan_second = st.checkbox("📈 Second Liner", value=True)
            with col_lvl3:
                scan_third = st.checkbox("🎯 Third Liner", value=True)

            col_par1, col_par2 = st.columns([1, 2])
            with col_par1:
                use_parallel = st.checkbox("⚡ Parallel Scanning", value=True)

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            if st.button("🚀  SCAN LOW FLOAT", type="primary", use_container_width=True):
                reset_session_data()

                selected_levels = []
                if scan_blue: selected_levels.append('Blue Chip')
                if scan_second: selected_levels.append('Second Liner')
                if scan_third: selected_levels.append('Third Liner')

                if selected_stocks:
                    stocks_to_scan = selected_stocks
                else:
                    stocks_to_scan = get_stocks_by_level(selected_levels) if selected_levels else STOCKS_LIST

                start_time = time.time()

                if use_parallel:
                    results = scan_stocks_parallel(stocks_to_scan, scan_low_float, max_public_float=max_ff, min_volume=min_vol)
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    results = []
                    for i, stock in enumerate(stocks_to_scan):
                        status_text.markdown(f"<span style='color:#8b949e; font-family:monospace; font-size:0.82rem;'>Memproses {stock}... ({i+1}/{len(stocks_to_scan)})</span>", unsafe_allow_html=True)
                        try:
                            result = scan_low_float([stock], max_ff, min_vol)
                            if result: results.extend(result)
                        except: pass
                        progress_bar.progress((i + 1) / len(stocks_to_scan))
                        time.sleep(0.3)
                    progress_bar.empty()
                    status_text.empty()

                total_time = time.time() - start_time

                if results:
                    df_results = pd.DataFrame(results)

                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0d1a24 0%, #0d1f1a 100%);
                                border: 1px solid rgba(77,166,255,0.2); border-radius: 16px;
                                padding: 24px 28px; margin: 20px 0 28px 0;">
                        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;">
                            <div>
                                <p style="color: #4da6ff; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; 
                                          letter-spacing: 2px; text-transform: uppercase; margin: 0 0 6px 0;">SCAN BERHASIL</p>
                                <p style="color: #e6edf3; font-size: 2.5rem; font-weight: 700; margin: 0; 
                                          font-family: 'JetBrains Mono', monospace; line-height: 1;">{len(df_results)}<span style="color: #4da6ff;">.</span></p>
                                <p style="color: #8b949e; font-size: 0.82rem; margin: 6px 0 0 0;">Saham Low Float &lt; {max_ff}%</p>
                            </div>
                            <div style="text-align: center; padding: 12px 20px; background: rgba(255,255,255,0.03); 
                                        border-radius: 10px; border: 1px solid #21262d;">
                                <p style="color: #484f58; font-size: 0.68rem; letter-spacing: 1.5px; text-transform: uppercase; 
                                          font-family: 'JetBrains Mono', monospace; margin: 0 0 4px 0;">DURASI</p>
                                <p style="color: #e6edf3; font-size: 1.4rem; font-weight: 700; margin: 0; 
                                          font-family: 'JetBrains Mono', monospace;">{total_time:.0f}<span style="color: #484f58; font-size: 0.9rem;">s</span></p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 0 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #4da6ff; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Hasil · Free Float · FCA</p>
                    </div>
                    """, unsafe_allow_html=True)

                    enriched_results = []
                    for _, row in df_results.iterrows():
                        saham = row['saham']
                        free_float = get_free_float_value(saham)
                        kategori_singkat = get_kategori_singkatan(row['category'])
                        potensi = analyze_goreng_potential(free_float)
                        fca_status = '⚠️' if is_fca(saham) else '—'
                        level_singkat = {'💎 Blue Chip': 'BC', '📈 Second Liner': 'SL', '🎯 Third Liner': 'TL'}.get(get_stock_level(saham), '')

                        holders = get_free_float_holders(saham)
                        total_inst_asing = sum((p['persen'] / free_float) * 100 for p in holders if free_float > 0)
                        sisa_ritel = 100 - total_inst_asing

                        enriched_results.append({
                            'Saham': saham, 'Lvl': level_singkat,
                            'FF': f"{free_float:.0f}%", 'Kat': kategori_singkat,
                            'Vol(M)': f"{row['volume_avg']/1e6:.1f}", 'Volat': f"{row['volatility']:.0f}%",
                            'Inst': f"{total_inst_asing:.0f}%", 'Ritel': f"{sisa_ritel:.0f}%",
                            'FCA': fca_status, 'Pot': potensi
                        })

                    enriched_df = pd.DataFrame(enriched_results)
                    st.dataframe(enriched_df, use_container_width=True, height=500, hide_index=True)

                    st.session_state['low_float_results'] = df_results
                    st.session_state['low_float_enriched'] = enriched_df

                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 28px 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #00d4aa; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Detail Free Float · Top 5</p>
                    </div>
                    """, unsafe_allow_html=True)

                    for _, row in df_results.head(5).iterrows():
                        free_float = get_free_float_value(row['saham'])
                        with st.expander(f"{row['saham']}  ·  {get_stock_level(row['saham'])}  ·  FF {free_float:.0f}%"):
                            st.markdown(display_free_float_info(row['saham'], free_float), unsafe_allow_html=True)

                    # Charts
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 28px 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #e3b341; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Distribusi & Analitik</p>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)

                    with col1:
                        counts = df_results['category'].value_counts()
                        fig = go.Figure(go.Pie(
                            labels=counts.index,
                            values=counts.values,
                            hole=0.55,
                            marker=dict(
                                colors=['#00d4aa', '#0099cc', '#4da6ff', '#c084fc', '#e3b341'],
                                line=dict(color='#0d1117', width=2)
                            ),
                            textfont=dict(color='#e6edf3', family='JetBrains Mono', size=10)
                        ))
                        fig.update_layout(
                            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
                            font=dict(color='#8b949e', family='JetBrains Mono', size=10),
                            legend=dict(font=dict(color='#8b949e', size=9)),
                            title=dict(text='Kategori Float', font=dict(color='#8b949e', size=11), x=0.5),
                            height=300, margin=dict(l=10, r=10, t=40, b=10)
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        fig = go.Figure()
                        vol_max = df_results['volume_avg'].max()
                        marker_sizes = (df_results['volume_avg'] / vol_max * 20 + 5).tolist() if vol_max > 0 else [8] * len(df_results)
                        fig.add_trace(go.Scatter(
                            x=df_results['public_float'].tolist(),
                            y=df_results['volatility'].tolist(),
                            mode='markers',
                            marker=dict(
                                size=marker_sizes,
                                color=df_results['volatility'].tolist(),
                                colorscale='Teal',
                                opacity=0.8,
                                line=dict(width=0)
                            ),
                            text=df_results['saham'].tolist(),
                            hovertemplate='<b>%{text}</b><br>Float: %{x:.1f}%<br>Volatilitas: %{y:.1f}%<extra></extra>'
                        ))
                        fig.update_layout(
                            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
                            font=dict(color='#8b949e', family='JetBrains Mono', size=10),
                            xaxis=dict(gridcolor='#21262d', title=dict(text='Free Float (%)', font=dict(color='#484f58', size=10))),
                            yaxis=dict(gridcolor='#21262d', title=dict(text='Volatilitas (%)', font=dict(color='#484f58', size=10))),
                            title=dict(text='FF vs Volatilitas', font=dict(color='#8b949e', size=11), x=0.5),
                            height=300, margin=dict(l=50, r=20, t=40, b=50),
                            hoverlabel=dict(bgcolor='#161b22', bordercolor='#30363d', font=dict(color='#e6edf3'))
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # Export
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin: 28px 0 12px 0;">
                        <span style="width: 3px; height: 18px; background: #4da6ff; border-radius: 2px; display: inline-block;"></span>
                        <p style="color: #8b949e; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; 
                                  font-family: 'JetBrains Mono', monospace; margin: 0;">Export Data</p>
                    </div>
                    """, unsafe_allow_html=True)

                    tab_exp1, tab_exp2 = st.tabs(["📊 Hasil Low Float", "📋 Info"])
                    with tab_exp1:
                        create_download_buttons(
                            st.session_state.get('low_float_enriched', enriched_df),
                            "low_float", "low_float_tab"
                        )
                    with tab_exp2:
                        st.info("Gunakan hasil di atas untuk analisis lebih lanjut bro!")

                else:
                    st.markdown("""
                    <div style="background: rgba(255,92,92,0.06); border: 1px solid rgba(255,92,92,0.2); 
                                border-radius: 12px; padding: 24px; text-align: center; margin: 16px 0;">
                        <p style="color: #ff5c5c; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; margin: 0;">
                            ⚠ &nbsp; Tidak ditemukan saham low float
                        </p>
                    </div>
                    """, unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════
    # MODE: BREAKOUT IDX (default) — All Tabs
    # ══════════════════════════════════════════════════════════
    else:
        modal = cfg.get('modal', 10_000_000)
        st.session_state['modal'] = modal
        col_b1,col_b2,col_b3 = st.columns([2,1,1])
        with col_b1:
            scan_button = st.button("🔍 SCAN SEKARANG", type="primary", use_container_width=True)
        with col_b2:
            auto_ref = st.toggle("⏱ Auto Refresh", value=st.session_state.get('auto_refresh',False))
            st.session_state['auto_refresh'] = auto_ref
        with col_b3:
            if st.session_state.get('last_scan_time'):
                st.caption(f"⏰ {st.session_state['last_scan_time']}")

        if scan_button:
            tickers = cfg.get('tickers', ALL_TICKERS[:50])
            prog = st.progress(0, "Memulai scan...")
            ihsg_closes = sector_momentum = rti_data = None
            if cfg.get('enable_rs', True):
                with st.spinner("📥 IHSG..."):
                    try:
                        idf = yf.download("^JKSE", period="6mo", interval="1d", progress=False, auto_adjust=True)
                        if idf is not None and not idf.empty:
                            idf.columns=[c[0] if isinstance(c,tuple) else c for c in idf.columns]
                            ihsg_closes = idf["Close"].values.astype(float).tolist()
                    except: pass
            if cfg.get('enable_rs', True):
                with st.spinner("🏭 Sektor..."):
                    try: sector_momentum = get_sector_momentum()
                    except: pass
            if cfg.get('enable_foreign', False):
                with st.spinner("🌏 Foreign..."):
                    try: rti_data = fetch_foreign_flow_rti()
                    except: pass

            results = run_scan(tickers, progress_bar=prog,
                               ihsg_closes=ihsg_closes,
                               sector_momentum=sector_momentum,
                               rti_data=rti_data)
            st.session_state.update({
                'stocks': results, 'ihsg_closes': ihsg_closes,
                'sector_momentum': sector_momentum, 'rti_data': rti_data,
                'last_scan_time': datetime.now().strftime('%H:%M:%S'),
                'scan_count': st.session_state.get('scan_count',0)+1,
            })
            prog.empty()
            st.success(f"✅ {len(results)} saham ditemukan.")
            st.rerun()

        stocks = st.session_state.get('stocks',[])

        # ── TABS ──────────────────────────────────────────────
        (tab_scanner, tab_rs, tab_sector, tab_foreign, tab_bandar,
         tab_patterns_t, tab_ai_conf_t, tab_news_t, tab_backtest,
         tab_leaderboard_t, tab_watchlist, tab_portfolio,
         tab_ai_analyst, tab_history_t) = st.tabs([
            "📊 Scanner","📈 RS vs IHSG","🏭 Sektor","🌏 Foreign Flow",
            "🐋 Bandarmologi","📊 Chart Pattern","🤖 AI Confidence",
            "📰 Sentimen","🔬 Backtest","🏆 Leaderboard",
            "👀 Watchlist","💼 Portfolio","🤖 AI Analyst","📋 Notifikasi",
        ])

        # TAB: SCANNER
        # ──────────────────────────────────────────────────────────
        with tab_scanner:
            stocks = st.session_state.get('stocks', [])
            if not stocks:
                st.markdown("""
                <div class='empty-state'>
                    <div class='icon'>⚡</div>
                    <div class='title'>AKSARA IDX v2.0</div>
                    <div class='sub'>
                        RSI WILDER · MACD FULL SERIES · RS vs IHSG<br>
                        SECTOR MOMENTUM · FOREIGN FLOW REAL · BACKTEST REALISTIS<br>
                        BANDARMOLOGI · CHART PATTERN · WYCKOFF · RISK MANAGER
                    </div>
                </div>
                """, unsafe_allow_html=True)
                return

            strong = sum(1 for s in stocks if s.get("score", 0) >= 72)
            buy    = sum(1 for s in stocks if 58 <= s.get("score", 0) < 72)
            watch  = sum(1 for s in stocks if 45 <= s.get("score", 0) < 58)
            rs_out = sum(1 for s in stocks if s.get("rs_outperform", False))

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            metric_card(col1, "📋 TOTAL",        len(stocks))
            metric_card(col2, "🔥 STRONG+",      strong, "#00ff88")
            metric_card(col3, "🟢 BUY",          buy,    "#7dff6b")
            metric_card(col4, "🟡 WATCH",        watch,  "#ffd700")
            metric_card(col5, "📈 RS Outperform",rs_out, "#00c8ff")
            metric_card(col6, "🕐 SCAN",         st.session_state.get('scan_time', '-'), "#8b949e")

            st.markdown("<br>", unsafe_allow_html=True)
            search = st.text_input("🔍 Cari ticker:", "", placeholder="Contoh: BBCA")
            display_stocks = ([s for s in stocks if search.upper() in s.get("ticker", "")]
                              if search else stocks)

            st.subheader("📋 HASIL SCAN")
            table_data = []
            for s in display_stocks[:100]:
                b = s.get("bandar", {}); f = s.get("foreign", {})
                _rs_v = s.get("rs_score", 50)
                rs_icon = "⭐" if _rs_v > 55 else ("➡️" if _rs_v >= 45 else "⬇️")
                table_data.append({
                    "Ticker":  s.get("ticker", ""),
                    "Harga":   fmt_price(s.get("price", 0)),
                    "Change%": f"{s.get('change', 0):+.1f}%",
                    "Score":   s.get("score", 0),
                    "Rating":  f"{rating_icon(s.get('rating',''))} {s.get('rating','')}",
                    "Konf":    s.get("confirmations", 0),
                    "RSI":     s.get("rsi", 0),
                    "Vol":     f"{s.get('vol_ratio', 0):.1f}x",
                    "ADX":     s.get("adx", 0),
                    "RS":      f"{rs_icon}{s.get('rs_score',50):.0f}",
                    "Sektor#": f"#{s.get('sec_rank',7)}",
                    "Bandar":  (b.get("fase","").split(" ")[1] if len(b.get("fase","").split(" ")) > 1 else ""),
                    "Foreign": f.get("flow_status", ""),
                    "Wyckoff": s.get("wyckoff", ""),
                    "Sektor":  s.get("sector", ""),
                })

            st.dataframe(
                pd.DataFrame(table_data), use_container_width=True, hide_index=True,
                column_config={"Score": st.column_config.ProgressColumn(
                    "Score", min_value=0, max_value=100, format="%d")}
            )

            csv_data = export_to_csv(display_stocks[:300])
            st.download_button("📥 Export CSV", csv_data,
                               file_name=f"scan_v2_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                               mime="text/csv")

            st.divider()
            st.subheader("📈 DETAIL PER SAHAM")
            ticker_options = [s.get("ticker", "") for s in stocks[:50]]
            selected_ticker = st.selectbox("Pilih saham untuk detail:", ticker_options)

            if selected_ticker:
                stock_data = next((s for s in stocks if s.get("ticker") == selected_ticker), None)
                if stock_data:
                    b  = stock_data.get("bandar", {})
                    f  = stock_data.get("foreign", {})
                    tp = stock_data.get("trade_plan", {})
                    rs = stock_data.get("rs_data", {})

                    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
                    with col_d1: st.metric("Harga",      fmt_price(stock_data.get("price", 0)),
                                           f"{stock_data.get('change', 0):+.1f}%")
                    with col_d2: st.metric("Score",      f"{stock_data.get('score', 0)}/100")
                    with col_d3: st.metric("Rating",     stock_data.get("rating", ""))
                    with col_d4:
                        _rs_val = stock_data.get('rs_score', 50)
                        _rs_label = ("⭐ Outperform" if _rs_val > 55
                                     else ("➡️ Netral" if _rs_val >= 45
                                           else "⬇️ Underperform"))
                        st.metric("RS vs IHSG", f"{_rs_val:.0f}/100", _rs_label)

                    det_tab1, det_tab2, det_tab3, det_tab4, det_tab5, det_tab6 = st.tabs([
                        "📊 Teknikal", "📈 RS & Sektor", "🐋 Bandar", "🌏 Foreign", "💰 Trading Plan", "🤖 AI"
                    ])

                    with det_tab1:
                        col_tek1, col_tek2 = st.columns(2)
                        with col_tek1:
                            st.markdown("**📈 Indikator (v2.0 — Fixed)**")
                            st.markdown(f"""
                            - **RSI (Wilder):** {stock_data.get('rsi', 0)} ← *akurat seperti TradingView*
                            - **MACD:** {stock_data.get('macd', 0):.4f} (hist: {stock_data.get('macd_hist', 0):.4f}) ← *full series*
                            - **MACD Signal:** {stock_data.get('macd_signal', 0):.4f}
                            - **Stochastic:** %K {stock_data.get('stoch_k', 0)} / %D {stock_data.get('stoch_d', 0)}
                            - **ADX:** {stock_data.get('adx', 0)}
                            - **BB Position:** {stock_data.get('bb_pos', 0)}%
                            - **Support:** {fmt_price(stock_data.get('support', 0)) if stock_data.get('support') else 'N/A'}
                            - **Resistance:** {fmt_price(stock_data.get('resistance', 0)) if stock_data.get('resistance') else 'N/A'}
                            """)
                        with col_tek2:
                            st.markdown("**📊 Moving Averages & Position**")
                            st.markdown(f"""
                            - **MA50:** {'✅ Di atas' if stock_data.get('above_ma50') else '❌ Di bawah'}
                            - **MA200:** {'✅ Di atas' if stock_data.get('above_ma200') else '❌ Di bawah'}
                            - **Golden Cross:** {'✅ Ya' if stock_data.get('golden_cross') else '❌ Tidak'}
                            - **52W Position:** {stock_data.get('pos52w', 0)}%
                            - **Wyckoff Phase:** {stock_data.get('wyckoff', '')}
                            - **Volume Ratio:** {stock_data.get('vol_ratio', 0):.2f}x
                            - **ATR:** {fmt_price(stock_data.get('atr', 0))}
                            """)
                        st.markdown("**🕯️ Chart Pattern**")
                        patterns = stock_data.get('patterns', [])
                        if patterns:
                            for p in patterns:
                                color = ("#00ff88" if p["signal"] == "BULLISH" else
                                         "#ff4444" if p["signal"] == "BEARISH" else "#ffd700")
                                st.markdown(
                                    f"<span style='background:{color}22;border:1px solid {color}44;"
                                    f"color:{color};border-radius:4px;padding:3px 8px;font-size:0.75rem;"
                                    f"margin:2px;display:inline-block'>{p['name']} {p['confidence']}% · {p['description']}</span>",
                                    unsafe_allow_html=True)
                        else:
                            st.info("Tidak ada pattern terdeteksi")
                        st.markdown("**⚡ Sinyal**")
                        for sig in stock_data.get('signals', []):
                            st.markdown(f"<span class='signal-tag'>{sig}</span>", unsafe_allow_html=True)

                    with det_tab2:
                        st.markdown("### 📈 RELATIVE STRENGTH vs IHSG")
                        rs_score = stock_data.get("rs_score", 50)
                        rs_ratio = stock_data.get("rs_ratio", 1.0)
                        rs_trend = stock_data.get("rs_trend", "STABLE")
                        rs_1m    = stock_data.get("rs_1m", 0)
                        rs_3m    = stock_data.get("rs_3m", 0)
                        outperform = stock_data.get("rs_outperform", False)

                        rs_color = "#00ff88" if outperform else "#ff4444"
                        rs_text  = "⭐ OUTPERFORM IHSG" if outperform else "⬇️ UNDERPERFORM IHSG"

                        st.markdown(f"""
                        <div class='fase-card' style='background:{rs_color}0d;border-left-color:{rs_color}'>
                            <span class='fase-icon'>{'⭐' if outperform else '📉'}</span>
                            <div>
                                <div class='fase-text' style='color:{rs_color}'>{rs_text}</div>
                                <div style='font-family:"JetBrains Mono",monospace;font-size:0.72rem;color:var(--text-muted);margin-top:4px'>
                                    RS Ratio: {rs_ratio:.3f} · Trend: {rs_trend}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        col_rs1, col_rs2, col_rs3, col_rs4 = st.columns(4)
                        metric_card(col_rs1, "RS Score",  f"{rs_score:.0f}/100", rs_color)
                        metric_card(col_rs2, "RS Ratio",  f"{rs_ratio:.3f}",
                                    "#00ff88" if rs_ratio > 1 else "#ff4444")
                        metric_card(col_rs3, "RS 1 Bulan",f"{rs_1m:+.2f}%",
                                    "#00ff88" if rs_1m > 0 else "#ff4444")
                        metric_card(col_rs4, "RS 3 Bulan",f"{rs_3m:+.2f}%",
                                    "#00ff88" if rs_3m > 0 else "#ff4444")

                        st.markdown("---")
                        st.markdown("### 🏭 SECTOR MOMENTUM")
                        sec_score = stock_data.get("sec_score", 50)
                        sec_rank  = stock_data.get("sec_rank", 7)
                        sec_change= stock_data.get("sec_change", 0)
                        sec_name  = stock_data.get("sector", "")

                        sm = st.session_state.get("sector_momentum", {})
                        if sm and sec_name in sm:
                            sec_info = sm[sec_name]
                            sec_color = ("#00ff88" if sec_change > 1 else
                                         "#ffd700" if sec_change > 0 else "#ff4444")
                            st.markdown(f"""
                            <div style='background:var(--bg-elevated);border:1px solid var(--border);
                            border-radius:var(--radius-md);padding:16px;margin-bottom:12px'>
                                <div style='font-family:"Syne",sans-serif;font-size:1rem;font-weight:800;
                                color:{sec_color};margin-bottom:8px'>
                                    Sektor {sec_name} — Rank #{sec_rank}/13
                                </div>
                                <div style='font-family:"JetBrains Mono",monospace;font-size:0.75rem;color:var(--text-secondary)'>
                                    Trend: {sec_info.get('trend','N/A')} · 1W: {sec_change:+.2f}% · 1M: {sec_info.get('change_1m',0):+.2f}%
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # Show all sectors ranked
                            st.markdown("**Ranking Semua Sektor:**")
                            sorted_sectors = sorted(sm.items(), key=lambda x: x[1]["score"], reverse=True)
                            for rank, (sn, sd) in enumerate(sorted_sectors, 1):
                                bar_w = int(sd["score"])
                                clr   = "#00ff88" if sd["change_1w"] > 1 else "#ffd700" if sd["change_1w"] > 0 else "#ff4444"
                                highlight = " style='background:rgba(0,200,255,0.05);border-radius:4px'" if sn == sec_name else ""
                                st.markdown(f"""
                                <div class='info-row'{highlight}>
                                    <span>#{rank} <b style='color:{"#00c8ff" if sn==sec_name else "var(--text-primary)"}'>{sn}</b></span>
                                    <span style='color:{clr}'>{sd["change_1w"]:+.2f}% (1W)</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("Data sektor belum dimuat. Jalankan scan untuk memuat.")

                    with det_tab3:
                        st.markdown(f"""
                        <div class='fase-card' style='background:{b.get("fase_color","#8b949e")}0d;
                        border-left-color:{b.get("fase_color","#8b949e")}'>
                            <span class='fase-icon'>{b.get('fase_emoji','')}</span>
                            <span class='fase-text' style='color:{b.get("fase_color","#8b949e")}'>{b.get('fase','N/A')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        col_ban1, col_ban2 = st.columns(2)
                        with col_ban1:
                            st.markdown("**📊 Indikator Bandar**")
                            cmf_val   = b.get('cmf', 0)
                            cmf_color = "#00ff88" if cmf_val > 0.05 else "#ff4444" if cmf_val < -0.05 else "#ffd700"
                            st.markdown(f"""
                            - **CMF:** <span style='color:{cmf_color}'>{cmf_val:+.4f}</span>
                            - **VWAP:** {'✅ Di atas' if b.get('above_vwap') else '❌ Di bawah'}
                            - **A/D Line:** {b.get('ad_trend', 'N/A')}
                            - **OBV Trend:** {b.get('obv_trend', 'N/A')}
                            - **Volume Ratio:** {b.get('vol_ratio', 1)}x
                            - **Bandar Strength:** {b.get('bandar_strength', 50)}/100
                            """, unsafe_allow_html=True)
                        with col_ban2:
                            st.markdown("**🔍 Sinyal Bandar**")
                            for sig in b.get('signals', []):
                                clr = "#00ff88" if "✅" in sig else "#ff4444" if "🔴" in sig else "#ffd700"
                                st.markdown(f"<span style='color:{clr}; font-size:0.85rem'>• {sig}</span>",
                                            unsafe_allow_html=True)

                    with det_tab4:
                        data_src  = stock_data.get("foreign_data_source", "estimated")
                        src_badge = ("📡 REAL DATA" if data_src != "estimated" else "📊 ESTIMATED")
                        src_color = "#00ff88" if data_src != "estimated" else "#ffd700"
                        st.markdown(f"""
                        <div class='fase-card' style='background:{f.get("flow_color","#8b949e")}0d;
                        border-left-color:{f.get("flow_color","#8b949e")}'>
                            <span class='fase-icon'>{f.get("flow_emoji","")}</span>
                            <div>
                                <span class='fase-text' style='color:{f.get("flow_color","#8b949e")}'>{f.get("flow_status","N/A")}</span>
                                <span style='font-family:"JetBrains Mono",monospace;font-size:0.65rem;
                                color:{src_color};margin-left:10px;vertical-align:middle'>{src_badge}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        col_for1, col_for2 = st.columns(2)
                        with col_for1:
                            st.markdown("**📊 Indikator Foreign**")
                            ff_color = f.get("flow_color", "#8b949e")
                            st.markdown(f"""
                            - **Net Flow:** <span style='color:{ff_color}'>Rp {stock_data.get('net_foreign_flow', 0):,.0f}</span>
                            - **Flow Strength:** {f.get('flow_strength', 50):.1f}/100
                            - **Foreign Ratio:** {f.get('foreign_ratio', 0):.1f}%
                            - **Est. Ownership:** {f.get('est_foreign_ownership', 0):.1f}%
                            - **Data Source:** {data_src}
                            """, unsafe_allow_html=True)
                        with col_for2:
                            st.markdown("**🔍 Sinyal Foreign**")
                            for sig in f.get('signals', []):
                                clr = ("#00ff88" if any(x in sig for x in ["✅","⚡","📡"]) else
                                       "#ff4444" if any(x in sig for x in ["🔴","⚠️"]) else "#ffd700")
                                st.markdown(f"<span style='color:{clr}; font-size:0.85rem'>• {sig}</span>",
                                            unsafe_allow_html=True)

                    with det_tab5:
                        if tp:
                            sl_d  = tp.get('sl', {})
                            tp_d  = tp.get('tp', {})
                            pos_d = tp.get('position', {})
                            st.markdown(f"""
                            <div class='section-card' style='border-color:rgba(0,232,122,0.15)'>
                                <div class='section-title'>📌 Rencana Trading</div>
                                <div class='trade-grid'>
                                    <div class='trade-cell'>
                                        <div class='trade-cell-label'>Entry</div>
                                        <div class='trade-cell-val' style='color:var(--accent-gold)'>{fmt_price(stock_data.get('price', 0))}</div>
                                    </div>
                                    <div class='trade-cell' style='border-color:rgba(255,61,90,0.2)'>
                                        <div class='trade-cell-label'>Stop Loss</div>
                                        <div class='trade-cell-val' style='color:var(--accent-red)'>{fmt_price(sl_d.get('recommended', 0))}</div>
                                        <div class='trade-cell-sub' style='color:var(--accent-red)'>-{sl_d.get('risk_pct', 0)}%</div>
                                    </div>
                                    <div class='trade-cell' style='border-color:rgba(0,232,122,0.15)'>
                                        <div class='trade-cell-label'>TP1</div>
                                        <div class='trade-cell-val' style='color:#7dff9a'>{fmt_price(tp_d.get('tp1', 0))}</div>
                                        <div class='trade-cell-sub' style='color:#7dff9a'>+{tp_d.get('tp1_pct', 0)}%</div>
                                    </div>
                                    <div class='trade-cell' style='border-color:rgba(0,232,122,0.25)'>
                                        <div class='trade-cell-label'>TP2 ⭐</div>
                                        <div class='trade-cell-val' style='color:var(--accent-green)'>{fmt_price(tp_d.get('tp2', 0))}</div>
                                        <div class='trade-cell-sub' style='color:var(--accent-green)'>+{tp_d.get('tp2_pct', 0)}%</div>
                                    </div>
                                </div>
                                <div style='background:var(--bg-elevated);border:1px solid var(--border);
                                border-radius:var(--radius-sm);padding:12px;font-family:"JetBrains Mono",monospace;font-size:0.72rem'>
                                    <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border)'>
                                        <span style='color:var(--text-muted)'>Risk / Reward</span>
                                        <span style='color:var(--accent-gold);font-weight:700'>1 : {tp_d.get('rr', 0)}</span>
                                    </div>
                                    <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border)'>
                                        <span style='color:var(--text-muted)'>Max Lot (risk 2%)</span>
                                        <span style='color:var(--text-primary)'>{pos_d.get('lot', 1)} lot · {pos_d.get('lembar', 100):,} lembar</span>
                                    </div>
                                    <div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid var(--border)'>
                                        <span style='color:var(--text-muted)'>Modal Dibutuhkan</span>
                                        <span style='color:var(--text-primary)'>{fmt_price(pos_d.get('required_modal', 0))}</span>
                                    </div>
                                    <div style='display:flex;justify-content:space-between;padding:4px 0'>
                                        <span style='color:var(--text-muted)'>Max Loss</span>
                                        <span style='color:var(--accent-red)'>{fmt_price(pos_d.get('max_loss', 0))}</span>
                                    </div>
                                </div>
                                <div style='margin-top:10px;font-family:"JetBrains Mono",monospace;font-size:0.68rem;
                                color:var(--text-muted);padding:8px;background:var(--bg-elevated);border-radius:var(--radius-sm)'>
                                    ⚙ {tp.get('adjustment_note', '')}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                    with det_tab6:
                        if st.session_state.get('groq_api_key'):
                            if st.button(f"🤖 Generate AI Analysis untuk {selected_ticker}", use_container_width=True):
                                with st.spinner("AI sedang menganalisa..."):
                                    analysis = get_ai_analysis(stock_data, st.session_state['groq_api_key'])
                                    st.markdown(f"<div class='ai-output'>{analysis}</div>", unsafe_allow_html=True)
                        else:
                            st.info("💡 Set GROQ_API_KEY di environment untuk AI Analyst (GRATIS di console.groq.com)")

                    st.markdown("---")
                    st.subheader("📈 CHART")
                    if st.button("📊 Load Chart", key=f"chart_{selected_ticker}"):
                        with st.spinner("Memuat chart..."):
                            df_chart = st.session_state.get('chart_data', {}).get(selected_ticker)
                            if df_chart is not None:
                                fig = create_chart(df_chart, selected_ticker, tp)
                                if fig: st.plotly_chart(fig, use_container_width=True,
                                                        config={"displayModeBar": False})
                            else:
                                st.warning("Data chart tidak tersedia (perlu scan ulang dengan data live)")

                    wl = get_watchlist()
                    if selected_ticker in wl:
                        if st.button("❌ Hapus dari Watchlist", use_container_width=True):
                            remove_from_watchlist(selected_ticker); st.rerun()
                    else:
                        if st.button("👀 Tambah ke Watchlist", use_container_width=True):
                            add_to_watchlist(selected_ticker, scan_result=stock_data); st.rerun()

        # ──────────────────────────────────────────────────────────
        # ✅ NEW TAB: RELATIVE STRENGTH vs IHSG
        # ──────────────────────────────────────────────────────────
        with tab_rs:
            st.markdown("### 📈 RELATIVE STRENGTH vs IHSG")
            st.caption("Saham yang outperform IHSG = lebih kuat dari market = kandidat terbaik untuk trading")
            st.divider()

            stocks = st.session_state.get('stocks', [])
            if not stocks:
                st.info("Jalankan scan terlebih dahulu")
            else:
                outperformers  = sorted([s for s in stocks if s.get("rs_score", 50) > 55],
                                       key=lambda x: x.get("rs_score", 50), reverse=True)
                neutrals       = [s for s in stocks if 45 <= s.get("rs_score", 50) <= 55]
                underperformers = sorted([s for s in stocks if s.get("rs_score", 50) < 45],
                                         key=lambda x: x.get("rs_score", 50))

                col_rs1, col_rs2, col_rs3, col_rs4 = st.columns(4)
                metric_card(col_rs1, "⭐ Outperform (>55)", len(outperformers), "#00ff88")
                metric_card(col_rs2, "➡️ Netral (45–55)",   len(neutrals),       "#ffd700")
                metric_card(col_rs3, "⬇️ Underperform (<45)", len(underperformers), "#ff4444")
                avg_rs = np.mean([s.get("rs_score",50) for s in stocks]) if stocks else 50
                metric_card(col_rs4, "Avg RS Score", f"{avg_rs:.1f}", "#00c8ff")

                st.divider()
                col_left, col_right = st.columns(2)

                with col_left:
                    st.markdown("**⭐ TOP 15 OUTPERFORM IHSG**")
                    for s in outperformers[:15]:
                        rs_score = s.get("rs_score", 50)
                        rs_1m    = s.get("rs_1m", 0)
                        rs_3m    = s.get("rs_3m", 0)
                        rt       = s.get("rs_trend","")
                        trend_icon = "📈" if rt == "IMPROVING" else "📉" if rt == "WEAKENING" else "➡️"
                        st.markdown(f"""
                        <div class='info-row'>
                            <span style='color:#e0e8ff;font-weight:bold'>{s['ticker']}</span>
                            <span>
                                <span style='color:#00ff88'>RS:{rs_score:.0f}</span>
                                <span style='color:#ffd700;font-size:0.8rem'> 1M:{rs_1m:+.1f}%</span>
                                <span style='color:#7a84a8;font-size:0.8rem'> 3M:{rs_3m:+.1f}%</span>
                                <span style='font-size:0.8rem'> {trend_icon}</span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                with col_right:
                    st.markdown("**⬇️ TOP 15 UNDERPERFORM (HINDARI)**")
                    for s in underperformers[:15]:
                        rs_score = s.get("rs_score", 50)
                        rs_1m    = s.get("rs_1m", 0)
                        rt       = s.get("rs_trend","")
                        trend_icon = "📈" if rt == "IMPROVING" else "📉" if rt == "WEAKENING" else "➡️"
                        st.markdown(f"""
                        <div class='info-row'>
                            <span style='color:#e0e8ff;font-weight:bold'>{s['ticker']}</span>
                            <span>
                                <span style='color:#ff4444'>RS:{rs_score:.0f}</span>
                                <span style='color:#ffd700;font-size:0.8rem'> 1M:{rs_1m:+.1f}%</span>
                                <span style='font-size:0.8rem'> {trend_icon}</span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()
                st.markdown("**🚀 RS IMPROVING — Momentum Meningkat vs IHSG**")
                improving = sorted([s for s in stocks if s.get("rs_trend") == "IMPROVING"],
                                   key=lambda x: x.get("rs_score",0), reverse=True)
                if improving:
                    for s in improving[:10]:
                        st.markdown(
                            f"<span style='background:#00ff8811;border:1px solid #00ff8833;color:#00ff88;"
                            f"border-radius:4px;padding:3px 10px;font-size:0.8rem;margin:3px;display:inline-block'>"
                            f"📈 {s['ticker']} (RS:{s.get('rs_score',50):.0f} · 1M:{s.get('rs_1m',0):+.1f}%)</span>",
                            unsafe_allow_html=True)
                else:
                    st.info("Tidak ada saham dengan RS improving signifikan")

                st.divider()
                # RS Score distribution chart
                st.markdown("**📊 Distribusi RS Score**")
                rs_scores = [s.get("rs_score", 50) for s in stocks]
                fig_rs = go.Figure()
                fig_rs.add_trace(go.Histogram(
                    x=rs_scores, nbinsx=20,
                    marker_color=[("#00ff88" if x > 50 else "#ff4444") for x in rs_scores],
                    opacity=0.8
                ))
                fig_rs.add_vline(x=50, line_dash="dash", line_color="#ffd700",
                                 annotation_text="IHSG Benchmark (50)")
                fig_rs.update_layout(
                    height=280, paper_bgcolor="#070711", plot_bgcolor="#0d0d1a",
                    font=dict(color="#7a84a8", family="JetBrains Mono", size=10),
                    margin=dict(l=20, r=20, t=20, b=20),
                    xaxis_title="RS Score", yaxis_title="Jumlah Saham"
                )
                fig_rs.update_xaxes(gridcolor="#1e1e36")
                fig_rs.update_yaxes(gridcolor="#1e1e36")
                st.plotly_chart(fig_rs, use_container_width=True)

                with st.expander("📖 Cara Membaca RS vs IHSG"):
                    st.markdown("""
                    **Relative Strength (RS) vs IHSG** mengukur seberapa kuat pergerakan saham dibandingkan benchmark (IHSG).

                    **RS Score > 50** → Saham lebih kuat dari IHSG (outperform) — *kandidat utama untuk trading*
                    **RS Score < 50** → Saham lebih lemah dari IHSG (underperform) — *hindari atau kurangi exposure*

                    **RS Trend:**
                    - **IMPROVING** → RS sedang naik = momentum membaik = sinyal positif kuat
                    - **WEAKENING** → RS sedang turun = momentum melemah = waspada
                    - **STABLE** → RS stabil

                    **Kenapa RS Penting?**
                    Saham yang outperform IHSG saat market naik, dan outperform saat market turun (turun lebih sedikit),
                    adalah saham paling sehat untuk di-trading. Institutional investor selalu prefer saham-saham ini.
                    """)

        # ──────────────────────────────────────────────────────────
        # ✅ NEW TAB: SECTOR MOMENTUM
        # ──────────────────────────────────────────────────────────
        with tab_sector:
            st.markdown("### 🏭 SECTOR MOMENTUM ANALYSIS")
            st.caption("Rotasi sektor real-time — ikuti sektor yang sedang hot untuk maximise profit")
            st.divider()

            sm = st.session_state.get("sector_momentum", {})
            if not sm:
                st.info("Klik **🚀 MULAI SCAN** untuk memuat data sector momentum")
                if st.button("🔄 Load Sector Momentum Saja", use_container_width=True):
                    with st.spinner("Memuat sector momentum..."):
                        sm = get_sector_momentum()
                        st.session_state['sector_momentum'] = sm
                        st.rerun()
            else:
                sorted_sectors = sorted(sm.items(), key=lambda x: x[1]["score"], reverse=True)

                # Heatmap sektor
                st.markdown("**🌡️ SECTOR HEATMAP**")
                cols = st.columns(4)
                for i, (sec_name, sec_info) in enumerate(sorted_sectors):
                    chg  = sec_info.get("change_1w", 0)
                    sc   = sec_info.get("score", 50)
                    rank = sec_info.get("rank", i + 1)
                    bg   = f"rgba(0,232,122,{min(0.25, chg/10 + 0.05)})" if chg > 0 else \
                           f"rgba(255,61,90,{min(0.25, abs(chg)/10 + 0.05)})"
                    bc   = "#00ff88" if chg > 1 else "#7dff6b" if chg > 0 else \
                           "#ff9944" if chg > -1 else "#ff4444"
                    with cols[i % 4]:
                        st.markdown(f"""
                        <div style='background:{bg};border:1px solid {bc}44;border-radius:8px;
                        padding:12px;text-align:center;margin:3px;'>
                            <div style='font-family:"JetBrains Mono",monospace;font-size:0.55rem;
                            color:var(--text-muted);letter-spacing:1px'>#{rank}</div>
                            <div style='font-family:"Syne",sans-serif;font-size:0.85rem;
                            font-weight:800;color:{bc}'>{sec_name}</div>
                            <div style='font-family:"JetBrains Mono",monospace;font-size:0.8rem;
                            color:{bc};font-weight:700;margin-top:2px'>{chg:+.2f}%</div>
                            <div style='font-family:"JetBrains Mono",monospace;font-size:0.62rem;
                            color:var(--text-muted)'>{sec_info.get("trend","")}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()
                # Table detail
                st.markdown("**📊 DETAIL SECTOR PERFORMANCE**")
                sec_table = []
                for sec_name, sec_info in sorted_sectors:
                    stocks_in_sec = [s for s in st.session_state.get('stocks', [])
                                     if s.get("sector") == sec_name]
                    avg_score = np.mean([s.get("score",0) for s in stocks_in_sec]) if stocks_in_sec else 0
                    top_stock = max(stocks_in_sec, key=lambda x: x.get("score",0)).get("ticker","") if stocks_in_sec else "-"
                    sec_table.append({
                        "Rank":       sec_info.get("rank", "-"),
                        "Sektor":     sec_name,
                        "Trend":      sec_info.get("trend",""),
                        "1W Change":  f"{sec_info.get('change_1w',0):+.2f}%",
                        "1M Change":  f"{sec_info.get('change_1m',0):+.2f}%",
                        "Score":      f"{sec_info.get('score',50):.1f}/100",
                        "Avg Stock Score": f"{avg_score:.0f}" if avg_score else "-",
                        "Top Stock":  top_stock,
                    })
                st.dataframe(pd.DataFrame(sec_table), use_container_width=True, hide_index=True)

                st.divider()
                # Bar chart momentum
                st.markdown("**📊 Sector 1-Week Performance**")
                sec_names = [s[0] for s in sorted_sectors]
                sec_chgs  = [s[1].get("change_1w",0) for s in sorted_sectors]
                colors    = ["#00ff88" if c > 0 else "#ff4444" for c in sec_chgs]
                fig_sec = go.Figure(go.Bar(
                    x=sec_names, y=sec_chgs, marker_color=colors,
                    text=[f"{c:+.2f}%" for c in sec_chgs], textposition="outside",
                    opacity=0.85
                ))
                fig_sec.add_hline(y=0, line_dash="solid", line_color="#3a3f5c")
                fig_sec.update_layout(
                    height=300, paper_bgcolor="#070711", plot_bgcolor="#0d0d1a",
                    font=dict(color="#7a84a8", family="JetBrains Mono", size=10),
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False, yaxis_title="1W Change %"
                )
                fig_sec.update_xaxes(gridcolor="#1e1e36", tickangle=45)
                fig_sec.update_yaxes(gridcolor="#1e1e36")
                st.plotly_chart(fig_sec, use_container_width=True)

                with st.expander("📖 Cara Baca Sector Momentum"):
                    st.markdown("""
                    **Sector Rotation** adalah strategi institusional — dana besar masuk ke sektor tertentu secara bergilir.
                    Dengan mengikuti sektor yang sedang hot, peluang profit jauh lebih besar.

                    **Cara menggunakan:**
                    1. Lihat sektor dengan rank #1-#3 dan perubahan 1W positif → ini sektor hot
                    2. Dari scanner, filter saham di sektor tersebut dengan score tertinggi
                    3. Kombinasikan dengan RS outperform IHSG → triple confirmation!

                    **Refresh rate:** Data sektor diupdate setiap 30 menit selama session.
                    """)

        # ──────────────────────────────────────────────────────────
        # TAB: FOREIGN FLOW
        # ──────────────────────────────────────────────────────────
        with tab_foreign:
            st.markdown("### 🌏 FOREIGN FLOW ANALYSIS")
            st.caption("Track arus dana investor asing — penggerak utama saham big cap IDX")

            rti_loaded = bool(st.session_state.get('rti_data'))
            if rti_loaded:
                st.success(f"📡 Data REAL dari RTI/IDX — {len(st.session_state['rti_data'])} saham")
            else:
                st.warning("⚠️ Menggunakan estimasi volume-based (RTI tidak tersedia). Data real butuh koneksi ke RTI Business.")
            st.divider()

            stocks = st.session_state.get('stocks', [])
            if not stocks:
                st.info("Jalankan scan terlebih dahulu untuk melihat analisa foreign flow")
            else:
                total_net_buy  = sum(s.get("net_foreign_flow", 0) for s in stocks if s.get("net_foreign_flow", 0) > 0)
                total_net_sell = abs(sum(s.get("net_foreign_flow", 0) for s in stocks if s.get("net_foreign_flow", 0) < 0))
                net_buy_count  = sum(1 for s in stocks if s.get("net_foreign_flow", 0) > 0)
                net_sell_count = sum(1 for s in stocks if s.get("net_foreign_flow", 0) < 0)

                col_f1, col_f2, col_f3, col_f4 = st.columns(4)
                metric_card(col_f1, "🟢 Net Buy",     f"Rp {total_net_buy:,.0f}",  "#00ff88")
                metric_card(col_f2, "🔴 Net Sell",    f"Rp {total_net_sell:,.0f}", "#ff4444")
                metric_card(col_f3, "Saham Net Buy",  net_buy_count,               "#00ff88")
                metric_card(col_f4, "Saham Net Sell", net_sell_count,              "#ff4444")

                st.markdown("<br>", unsafe_allow_html=True)
                st.divider()

                col_ff_left, col_ff_right = st.columns(2)
                with col_ff_left:
                    st.markdown("**🟢 TOP 10 FOREIGN NET BUY**")
                    for s in sorted([s for s in stocks if s.get("net_foreign_flow", 0) > 0],
                                     key=lambda x: x.get("net_foreign_flow", 0), reverse=True)[:10]:
                        ff = s.get("foreign", {})
                        src_badge = "📡" if s.get("foreign_data_source","") != "estimated" else "📊"
                        st.markdown(f"""
                        <div class='info-row'>
                            <span style='color:#e0e8ff;font-weight:bold'>{s['ticker']} {src_badge}</span>
                            <span>
                                <span style='color:#00ff88'>+Rp {s.get('net_foreign_flow',0):,.0f}</span>
                                <span style='color:#4a6a8a;font-size:0.8rem'> Str:{ff.get('flow_strength',50):.0f}</span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                with col_ff_right:
                    st.markdown("**🔴 TOP 10 FOREIGN NET SELL**")
                    for s in sorted([s for s in stocks if s.get("net_foreign_flow", 0) < 0],
                                     key=lambda x: x.get("net_foreign_flow", 0))[:10]:
                        ff = s.get("foreign", {})
                        src_badge = "📡" if s.get("foreign_data_source","") != "estimated" else "📊"
                        st.markdown(f"""
                        <div class='info-row'>
                            <span style='color:#e0e8ff;font-weight:bold'>{s['ticker']} {src_badge}</span>
                            <span>
                                <span style='color:#ff4444'>-Rp {abs(s.get('net_foreign_flow',0)):,.0f}</span>
                                <span style='color:#4a6a8a;font-size:0.8rem'> Str:{ff.get('flow_strength',50):.0f}</span>
                            </span>
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()
                st.markdown("**⚡ FOREIGN DIVERGENCE (HARGA TURUN TAPI FOREIGN BUY)**")
                divergence_stocks = sorted(
                    [s for s in stocks if s.get("foreign", {}).get("divergence", False)],
                    key=lambda x: x.get("foreign", {}).get("flow_strength", 0), reverse=True
                )
                if divergence_stocks:
                    for s in divergence_stocks[:8]:
                        ff = s.get("foreign", {})
                        st.markdown(
                            f"<span style='background:#00ff8811;border:1px solid #00ff8833;color:#00ff88;"
                            f"border-radius:4px;padding:3px 10px;font-size:0.8rem;margin:3px;display:inline-block'>"
                            f"⚡ {s['ticker']} ({s.get('change',0):+.1f}% · Net:+Rp {s.get('net_foreign_flow',0):,.0f})</span>",
                            unsafe_allow_html=True)
                else:
                    st.info("Tidak ada foreign divergence signifikan saat ini")

        # ──────────────────────────────────────────────────────────
        # TAB 5 — BANDARMOLOGI
        # ════════════════════════════════════════════════════════════
        with tab_bandar:
            st.markdown("### 🐋 Bandarmologi — Deteksi Akumulasi & Distribusi Bandar")
            st.caption("Analisis pola pergerakan bandar menggunakan CMF, A/D Line, VPT, OBV, dan VWAP dari data publik.")
            st.divider()

            # ── Pilih Saham ─────────────────────────────────────────
            bandar_col1, bandar_col2 = st.columns([2, 1])
            with bandar_col1:
                bandar_ticker = st.text_input(
                    "Kode Saham:",
                    value=st.session_state.get('selected_ticker', 'BBCA.JK'),
                    key="bandar_ticker_input",
                    placeholder="Contoh: BBCA.JK, GOTO.JK"
                ).upper().strip()
                if not bandar_ticker.endswith('.JK') and bandar_ticker:
                    bandar_ticker += '.JK'
            with bandar_col2:
                bandar_days = st.selectbox("Periode Data:", [60, 90, 120, 180], index=1, key="bandar_days")

            analyze_bandar = st.button("🐋 Analisis Bandarmologi", type="primary", use_container_width=True, key="btn_bandar")

            # ── Tampilkan dari scan juga (top saham) ─────────────────
            if st.session_state.get('scan_results'):
                scan_tickers = [r['ticker'] for r in st.session_state['scan_results'][:5]]
                st.caption(f"💡 Dari hasil scan terakhir: pilih saham untuk dianalisis")
                quick_cols = st.columns(len(scan_tickers))
                for i, qt in enumerate(scan_tickers):
                    with quick_cols[i]:
                        if st.button(qt, key=f"bandar_quick_{qt}", use_container_width=True):
                            bandar_ticker = qt
                            analyze_bandar = True

            if analyze_bandar and bandar_ticker:
                with st.spinner(f"🐋 Menganalisis pola bandar {bandar_ticker}..."):
                    df_bandar = fetch_stock_data(bandar_ticker, bandar_days)

                if df_bandar is None or len(df_bandar) < 30:
                    st.error(f"❌ Data tidak cukup untuk {bandar_ticker}. Coba ticker lain.")
                else:
                    result_b = analyze_bandarmologi(df_bandar)

                    if not result_b['available']:
                        st.warning(result_b['rekomendasi'])
                    else:
                        # ── Header Fase Bandar ───────────────────────
                        st.markdown(f"""
                        <div style='background:{result_b["fase_color"]}22; border:2px solid {result_b["fase_color"]};
                             border-radius:12px; padding:20px; margin-bottom:16px; text-align:center;'>
                            <div style='font-size:2.5em;'>{result_b["fase_emoji"]}</div>
                            <div style='font-size:1.6em; font-weight:bold; color:{result_b["fase_color"]};'>
                                {result_b["fase"]}
                            </div>
                            <div style='color:#e6edf3; margin-top:8px; font-size:0.95em;'>
                                {result_b["rekomendasi"]}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Metrics Row ──────────────────────────────
                        m1, m2, m3, m4, m5 = st.columns(5)
                        ind = result_b['indicators']

                        with m1:
                            strength = result_b['bandar_strength']
                            s_color = '#00ff88' if strength > 60 else '#ff4444' if strength < 40 else '#ffd700'
                            st.markdown(f"<div style='text-align:center'><div style='color:#8b949e;font-size:0.8em;'>Kekuatan Bandar</div>"
                                        f"<div style='font-size:1.6em;font-weight:bold;color:{s_color};'>{strength}/100</div></div>",
                                        unsafe_allow_html=True)
                        with m2:
                            cmf_val = ind.get('cmf', 0)
                            cmf_color = '#00ff88' if cmf_val > 0.05 else '#ff4444' if cmf_val < -0.05 else '#ffd700'
                            st.markdown(f"<div style='text-align:center'><div style='color:#8b949e;font-size:0.8em;'>CMF</div>"
                                        f"<div style='font-size:1.6em;font-weight:bold;color:{cmf_color};'>{cmf_val:+.3f}</div>"
                                        f"<div style='font-size:0.75em;color:{cmf_color};'>{ind.get('cmf_label','')}</div></div>",
                                        unsafe_allow_html=True)
                        with m3:
                            vwap_pct = ind.get('vwap_pct', 0)
                            vwap_c = '#00ff88' if ind.get('above_vwap') else '#ff4444'
                            vwap_label = 'Di Atas VWAP' if ind.get('above_vwap') else 'Di Bawah VWAP'
                            st.markdown(f"<div style='text-align:center'><div style='color:#8b949e;font-size:0.8em;'>vs VWAP</div>"
                                        f"<div style='font-size:1.6em;font-weight:bold;color:{vwap_c};'>{vwap_pct:+.1f}%</div>"
                                        f"<div style='font-size:0.75em;color:{vwap_c};'>{vwap_label}</div></div>",
                                        unsafe_allow_html=True)
                        with m4:
                            acc = result_b['accum_score']
                            st.markdown(f"<div style='text-align:center'><div style='color:#8b949e;font-size:0.8em;'>Skor Akumulasi</div>"
                                        f"<div style='font-size:1.6em;font-weight:bold;color:#00ff88;'>{acc}/100</div></div>",
                                        unsafe_allow_html=True)
                        with m5:
                            dist = result_b['distr_score']
                            st.markdown(f"<div style='text-align:center'><div style='color:#8b949e;font-size:0.8em;'>Skor Distribusi</div>"
                                        f"<div style='font-size:1.6em;font-weight:bold;color:#ff4444;'>{dist}/100</div></div>",
                                        unsafe_allow_html=True)

                        st.divider()

                        # ── Sinyal Detail ────────────────────────────
                        sig_col, trend_col = st.columns([1.2, 1])
                        with sig_col:
                            st.markdown("#### 🔍 Sinyal Terdeteksi")
                            for sig in result_b['signals']:
                                st.markdown(f"- {sig}")

                        with trend_col:
                            st.markdown("#### 📈 Arah Indikator")
                            trend_map = {
                                'UP'  : ('⬆️', '#00ff88'),
                                'DOWN': ('⬇️', '#ff4444'),
                                'FLAT': ('➡️', '#ffd700')
                            }
                            for key, label in [('ad_trend','A/D Line'), ('vpt_trend','VPT'),
                                                ('obv_trend','OBV')]:
                                tr = ind.get(key, 'FLAT')
                                em, col = trend_map.get(tr, ('➡️','#ffd700'))
                                st.markdown(f"**{label}:** <span style='color:{col};'>{em} {tr}</span>",
                                            unsafe_allow_html=True)
                            st.markdown(f"**Volume Ratio:** `{ind.get('vol_ratio',1):.1f}x` rata-rata")
                            st.markdown(f"**VWAP:** `{ind.get('vwap',0):,.0f}`")

                        st.divider()

                        # ── Chart Bandarmologi ───────────────────────
                        st.markdown("#### 📊 Chart Indikator Bandar")
                        try:
                            from plotly.subplots import make_subplots
                            import plotly.graph_objects as go

                            df_b = df_bandar.copy()
                            data_b = result_b['data']

                            fig_b = make_subplots(
                                rows=4, cols=1, shared_xaxes=True,
                                vertical_spacing=0.04,
                                row_heights=[0.4, 0.2, 0.2, 0.2],
                                subplot_titles=(
                                    f"{bandar_ticker} + VWAP",
                                    "CMF (Chaikin Money Flow)",
                                    "A/D Line + VPT",
                                    "OBV (On Balance Volume)"
                                )
                            )

                            # Candlestick
                            fig_b.add_trace(go.Candlestick(
                                x=df_b.index, open=df_b['Open'], high=df_b['High'],
                                low=df_b['Low'], close=df_b['Close'],
                                increasing_line_color='#00ff88', decreasing_line_color='#ff4444',
                                name="OHLC", showlegend=False
                            ), row=1, col=1)

                            # VWAP
                            fig_b.add_trace(go.Scatter(
                                x=df_b.index, y=data_b['vwap'],
                                name="VWAP", line=dict(color='#ffd700', width=2, dash='dash'),
                            ), row=1, col=1)

                            # CMF
                            cmf_colors = ['#00ff88' if v >= 0 else '#ff4444' for v in data_b['cmf'].fillna(0)]
                            fig_b.add_trace(go.Bar(
                                x=df_b.index, y=data_b['cmf'],
                                marker_color=cmf_colors, name="CMF", showlegend=False
                            ), row=2, col=1)
                            fig_b.add_hline(y=0.1,  line_dash="dot", line_color="#00ff88", line_width=1, row=2, col=1)
                            fig_b.add_hline(y=0,    line_dash="dash", line_color="#8b949e", line_width=1, row=2, col=1)
                            fig_b.add_hline(y=-0.1, line_dash="dot", line_color="#ff4444", line_width=1, row=2, col=1)

                            # A/D Line
                            fig_b.add_trace(go.Scatter(
                                x=df_b.index, y=data_b['ad'],
                                name="A/D Line", line=dict(color='#00ccff', width=2)
                            ), row=3, col=1)
                            # VPT (normalize ke skala A/D)
                            vpt_norm = data_b['vpt'] / data_b['vpt'].abs().max() * data_b['ad'].abs().max()
                            fig_b.add_trace(go.Scatter(
                                x=df_b.index, y=vpt_norm,
                                name="VPT (scaled)", line=dict(color='#a371f7', width=1.5, dash='dot')
                            ), row=3, col=1)

                            # OBV
                            fig_b.add_trace(go.Scatter(
                                x=df_b.index, y=data_b['obv'],
                                name="OBV", line=dict(color='#ff9500', width=2), showlegend=False
                            ), row=4, col=1)

                            fig_b.update_layout(
                                height=750, plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
                                font_color='#e6edf3', xaxis_rangeslider_visible=False,
                                legend=dict(bgcolor='#161b22', font=dict(size=10)),
                                margin=dict(l=10, r=20, t=40, b=10)
                            )
                            fig_b.update_xaxes(gridcolor='#21262d')
                            fig_b.update_yaxes(gridcolor='#21262d')
                            st.plotly_chart(fig_b, use_container_width=True)

                        except Exception as e:
                            st.warning(f"Chart tidak bisa ditampilkan: {e}")

                        # ── Penjelasan Singkat ───────────────────────
                        with st.expander("📖 Cara Baca Indikator Bandarmologi"):
                            st.markdown("""
        **CMF (Chaikin Money Flow)**
        - `> +0.10` → Tekanan beli dominan = **Bandar akumulasi**
        - `< -0.10` → Tekanan jual dominan = **Bandar distribusi**
        - `-0.10 s/d +0.10` → Netral / konsolidasi

        **A/D Line (Accumulation/Distribution)**
        - Naik meski harga turun = **Akumulasi tersembunyi** (sinyal kuat beli)
        - Turun meski harga naik = **Distribusi tersembunyi** (waspada jual)

        **VPT (Volume Price Trend)**
        - Lebih sensitif dari OBV — memperhitungkan **besar kecilnya perubahan harga**
        - Konfirmator A/D Line

        **OBV (On Balance Volume)**
        - Konfirmasi sederhana: OBV naik = akumulasi, turun = distribusi

        **VWAP**
        - Harga di atas VWAP = bandar support harga (bullish)
        - Harga di bawah VWAP = bandar tidak support (bearish)

        **⚠️ Catatan Penting:**
        Bandarmologi dari data publik bersifat estimasi. Data broker summary dan net foreign buy/sell dari BEI langsung lebih akurat tapi membutuhkan data premium.
                            """)


        # ════════════════════════════════════════════════════════════

        with tab_patterns_t:

            # ════════════════════════════════════════════════════════════
            with tab_patterns:
                st.markdown("### 📊 Chart Pattern Recognition")
                st.markdown("Deteksi otomatis: Double Top/Bottom, Head & Shoulders, Ascending Triangle, Bull Flag, Cup & Handle")
                st.divider()

                pattern_results = st.session_state.get('pattern_results', {})
                results = st.session_state.get('results', [])

                if not pattern_results:
                    st.info("💡 Aktifkan **Chart Pattern** di sidebar, lalu jalankan scan.")
                    # Manual analysis
                    st.subheader("🔍 Analisis Pattern Manual")
                    manual_ticker = st.text_input("Masukkan ticker:", placeholder="BBCA.JK")
                    if st.button("🔍 Analisis Pattern") and manual_ticker:
                        with st.spinner("Menganalisis..."):
                            df_manual = fetch_stock_data(manual_ticker.upper().strip())
                            if df_manual is not None:
                                pattern_results = {manual_ticker.upper(): analyze_patterns(df_manual)}
                                st.session_state['pattern_results'] = pattern_results
                            else:
                                st.error("❌ Data tidak tersedia.")

                if pattern_results:
                    # Summary
                    all_patterns_flat = []
                    for ticker, pr in pattern_results.items():
                        for pat in pr.get('all', []):
                            all_patterns_flat.append({**pat, 'ticker': ticker})

                    if all_patterns_flat:
                        bullish_count = sum(1 for p in all_patterns_flat if p['signal'] == 'BULLISH')
                        bearish_count = sum(1 for p in all_patterns_flat if p['signal'] == 'BEARISH')

                        c1, c2, c3 = st.columns(3)
                        metric_card(c1, "📊 Total Pattern", len(all_patterns_flat))
                        metric_card(c2, "🟢 Bullish",       bullish_count, "#00ff88")
                        metric_card(c3, "🔴 Bearish",       bearish_count, "#ff4444")
                        st.markdown("<br>", unsafe_allow_html=True)

                    for ticker, pr in pattern_results.items():
                        best = pr.get('best', {})
                        all_pats = pr.get('all', [])

                        if not all_pats:
                            continue

                        with st.expander(
                            f"{'🟢' if best.get('signal')=='BULLISH' else '🔴'} {ticker} — "
                            f"{best.get('name', 'No Pattern')} | {pr.get('count', 0)} pattern",
                            expanded=True
                        ):
                            for pat in all_pats:
                                signal_color = "#00ff88" if pat['signal'] == 'BULLISH' else "#ff4444"
                                conf_bar = int(pat['confidence'] / 20)
                                conf_dots = "🟢" * conf_bar + "⚪" * (5 - conf_bar)

                                st.markdown(f"""
                                <div class='pattern-box' style='margin-bottom:12px;'>
                                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                                        <span style='font-size:1.05rem; font-weight:bold; color:{signal_color};'>
                                            {pat['name']}
                                        </span>
                                        <span style='color:#8b949e; font-size:0.85rem;'>
                                            Sinyal: <b style='color:{signal_color}'>{pat['signal']}</b>
                                        </span>
                                    </div>
                                    <div style='color:#8b949e; font-size:0.85rem; margin:6px 0;'>
                                        {pat.get('description', '')}
                                    </div>
                                    <div style='display:flex; gap:20px; margin-top:8px;'>
                                        <span>Confidence: {conf_dots} <b style='color:{signal_color};'>
                                            {pat['confidence']}%</b></span>
                                        <span style='color:#8b949e;'>
                                            {'✅ Terkonfirmasi' if pat.get('confirmed') else '⏳ Belum konfirmasi'}
                                        </span>
                                    </div>
                                """, unsafe_allow_html=True)

                                # Price levels
                                pl = pat.get('price_levels', {})
                                if pl:
                                    lvl_str = " | ".join(f"<b>{k.replace('_',' ').title()}</b>: Rp {v:,.0f}"
                                                         for k, v in pl.items() if isinstance(v, (int, float)))
                                    st.markdown(f"<div style='color:#8b949e; font-size:0.82rem;'>{lvl_str}</div>",
                                                unsafe_allow_html=True)
                                st.markdown("</div>", unsafe_allow_html=True)


            # ════════════════════════════════════════════════════════════

        with tab_ai_conf_t:

            # ════════════════════════════════════════════════════════════
            with tab_ai:
                st.markdown("### 🤖 AI Signal Confidence")
                st.markdown(
                    "Model Machine Learning (Random Forest) dilatih dari data historis 180 hari "
                    "untuk memprediksi probabilitas breakout berhasil."
                )
                st.divider()

                if not SKLEARN_AVAILABLE:
                    st.error("❌ **scikit-learn belum terinstall!**\n\nJalankan: `pip install scikit-learn`")
                else:
                    ml_results = st.session_state.get('ml_results', {})

                    if not ml_results:
                        st.info("💡 Aktifkan **AI Confidence** di sidebar, lalu jalankan scan.")

                        # Manual AI
                        st.subheader("🔍 Analisis AI Manual")
                        ai_ticker = st.text_input("Masukkan ticker:", placeholder="BBCA.JK", key="ai_ticker")
                        if st.button("🤖 Analisis AI") and ai_ticker:
                            with st.spinner("Training model & prediksi..."):
                                df_ai = fetch_stock_data(ai_ticker.upper().strip(), days=200)
                                if df_ai is not None:
                                    ai_r = predict_confidence(
                                        ai_ticker.upper(), df_ai, st.session_state['ml_cache'])
                                    ml_results = {ai_ticker.upper(): ai_r}
                                else:
                                    st.error("❌ Data tidak tersedia.")

                    if ml_results:
                        # Sort by confidence
                        sorted_ml = sorted(ml_results.items(),
                                            key=lambda x: x[1].get('confidence', 0), reverse=True)

                        # Summary
                        available = [(t, r) for t, r in sorted_ml if r.get('available')]
                        if available:
                            avg_conf = sum(r['confidence'] for _, r in available) / len(available)
                            high_conf = sum(1 for _, r in available if r['confidence'] >= 70)
                            c1, c2, c3 = st.columns(3)
                            metric_card(c1, "📊 Dianalisis", len(available))
                            metric_card(c2, "🟢 High Conf (≥70%)", high_conf, "#00ff88")
                            metric_card(c3, "📈 Avg Confidence", f"{avg_conf:.0f}%",
                                        "#00ff88" if avg_conf >= 60 else "#ffd700")
                            st.markdown("<br>", unsafe_allow_html=True)

                        for ticker, ml in sorted_ml:
                            if not ml.get('available'):
                                continue

                            conf  = ml['confidence']
                            color = ml['color']
                            conf_bar_filled = int(conf / 10)

                            with st.expander(f"🤖 {ticker} — {ml['label']} | {conf}% Confidence"):
                                col_a, col_b = st.columns([2, 1])

                                with col_a:
                                    st.markdown(f"""
                                    <div class='ai-box'>
                                        <div style='font-size:1.1rem; font-weight:bold; color:{color};
                                                    margin-bottom:10px;'>{ml['label']}</div>
                                        <div style='display:flex; align-items:center; gap:10px; margin-bottom:10px;'>
                                            <div style='flex:1; background:#30363d; border-radius:6px;
                                                        height:16px; overflow:hidden;'>
                                                <div style='width:{conf}%; background:{color}; height:100%;
                                                            border-radius:6px;'></div>
                                            </div>
                                            <span style='color:{color}; font-size:1.2rem;
                                                         font-weight:bold;'>{conf}%</span>
                                        </div>
                                        <div style='color:#8b949e; font-size:0.85rem;'>
                                            CV Accuracy Model: <b style='color:#e6edf3;'>{ml.get('accuracy', 0):.1f}%</b> |
                                            Training data: <b style='color:#e6edf3;'>{ml.get('n_samples', 0)} sampel</b>
                                        </div>
                                    </div>""", unsafe_allow_html=True)

                                with col_b:
                                    st.markdown("**Top Features:**")
                                    for feat_name, imp in ml.get('feat_importance', []):
                                        imp_pct = int(imp * 100)
                                        st.markdown(f"""
                                        <div style='margin:4px 0;'>
                                            <div style='color:#8b949e; font-size:0.78rem;'>{feat_name}</div>
                                            <div style='background:#30363d; border-radius:4px; height:6px;'>
                                                <div style='width:{imp_pct*5}%; background:#1f6feb;
                                                            height:100%; border-radius:4px;'></div>
                                            </div>
                                        </div>""", unsafe_allow_html=True)


            # ════════════════════════════════════════════════════════════

        with tab_news_t:

            # ════════════════════════════════════════════════════════════
            with tab_news:
                st.markdown("### 📰 News Sentiment Analysis")
                st.markdown("Analisis sentimen berita terbaru dari Yahoo Finance untuk setiap saham.")
                st.divider()

                sentiment_results = st.session_state.get('sentiment_results', {})

                if not sentiment_results:
                    st.info("💡 Aktifkan **News Sentiment** di sidebar, lalu jalankan scan.")
                    # Manual news
                    st.subheader("🔍 Cari Berita Manual")
                    news_ticker = st.text_input("Ticker:", placeholder="BBCA.JK", key="news_ticker")
                    if st.button("📰 Ambil Berita") and news_ticker:
                        with st.spinner("Mengambil berita..."):
                            sentiment_results = {news_ticker.upper(): analyze_news_sentiment(news_ticker.upper())}
                            st.session_state['sentiment_results'] = sentiment_results

                if sentiment_results:
                    for ticker, sent in sentiment_results.items():
                        if not sent.get('available'):
                            st.warning(f"📭 {ticker}: Berita tidak tersedia")
                            continue

                        color = sent['color']
                        with st.expander(
                            f"📰 {ticker} — {sent['label']} | Skor {sent['avg_score']:.0f}/100 | "
                            f"{sent['article_count']} artikel",
                            expanded=True
                        ):
                            c1, c2, c3, c4 = st.columns(4)
                            metric_card(c1, "📊 Skor Sentimen", f"{sent['avg_score']:.0f}/100", color)
                            metric_card(c2, "😊 Positif", sent['pos_articles'], "#00ff88")
                            metric_card(c3, "😟 Negatif", sent['neg_articles'], "#ff4444")
                            metric_card(c4, "😐 Netral",  sent['neutral_articles'], "#ffd700")

                            st.markdown("<br>", unsafe_allow_html=True)

                            for article in sent.get('articles', []):
                                art_sent  = article.get('sentiment', {})
                                art_color = art_sent.get('color', '#8b949e')
                                art_label = art_sent.get('label', '')
                                hours_ago = article.get('hours_ago', 999)
                                time_str  = f"{hours_ago}j lalu" if hours_ago < 24 else article.get('published', '')

                                st.markdown(f"""
                                <div class='news-box'>
                                    <div style='display:flex; justify-content:space-between;'>
                                        <span style='color:{art_color}; font-size:0.8rem;
                                                     font-weight:bold;'>{art_label}</span>
                                        <span style='color:#8b949e; font-size:0.78rem;'>🕐 {time_str}</span>
                                    </div>
                                    <div style='color:#e6edf3; margin:4px 0; font-size:0.9rem;'>
                                        {article['title'][:120]}
                                    </div>
                                    <div style='color:#8b949e; font-size:0.78rem;'>
                                        Skor: <b style='color:{art_color};'>{art_sent.get('score', 0):.0f}</b>/100
                                    </div>
                                </div>""", unsafe_allow_html=True)


            # ════════════════════════════════════════════════════════════
        # ──────────────────────────────────────────────────────────
        with tab_backtest:
            st.markdown("### 🔬 BACKTEST STRATEGI v2.0")
            st.caption("Entry di OPEN hari berikutnya (realistis) · RSI Wilder · MACD Full Series")

            st.info("""
            **✅ Perbaikan Backtest v2.0:**
            - **Entry = Open hari BERIKUTNYA** (bukan close sinyal — lebih realistis!)
            - **RSI Wilder's Smoothing** (sama seperti TradingView)
            - **MACD Full Series** (tidak terpotong lagi)
            """)
            st.divider()

            col_bt1, col_bt2, col_bt3 = st.columns([2, 1, 1])
            with col_bt1: bt_ticker = st.text_input("Ticker untuk Backtest:", value="BBCA")
            with col_bt2: bt_days   = st.selectbox("Periode:", [30, 60, 90, 180], index=1,
                                                    format_func=lambda x: f"{x} hari")
            with col_bt3: bt_mode   = st.selectbox("Mode:", ["Single Saham", "Multi Saham"])

            if st.button("▶️ Jalankan Backtest", type="primary", use_container_width=True):
                bt_tickers = parse_tickers(bt_ticker)
                if bt_tickers:
                    if bt_mode == "Single Saham":
                        with st.spinner(f"⏳ Backtest {bt_tickers[0]}..."):
                            bt_result = run_backtest(bt_tickers[0], bt_days)
                            if bt_result and bt_result["total_trades"] > 0:
                                st.success(f"Entry method: **{bt_result['entry_method']}**")
                                col_m1,col_m2,col_m3,col_m4,col_m5,col_m6 = st.columns(6)
                                metric_card(col_m1, "Total Trade", bt_result["total_trades"])
                                metric_card(col_m2, "✅ Win",      bt_result["win_count"],  "#00ff88")
                                metric_card(col_m3, "❌ Loss",     bt_result["loss_count"], "#ff4444")
                                metric_card(col_m4, "🎯 Win Rate", f"{bt_result['win_rate']}%", "#ffd700")
                                metric_card(col_m5, "📈 Avg P&L",  f"{bt_result['avg_pnl']:+.1f}%",
                                            "#00ff88" if bt_result['avg_pnl'] > 0 else "#ff4444")
                                metric_card(col_m6, "⏱️ Avg Hold", f"{bt_result['avg_days_held']}hr", "#8b949e")

                                st.markdown("<br>", unsafe_allow_html=True)
                                col_bt_a,col_bt_b,col_bt_c,col_bt_d = st.columns(4)
                                metric_card(col_bt_a, "Best Trade",    f"+{bt_result['best']}%",   "#00ff88")
                                metric_card(col_bt_b, "Worst Trade",   f"{bt_result['worst']}%",   "#ff4444")
                                metric_card(col_bt_c, "Profit Factor", bt_result["profit_factor"], "#ffd700")
                                metric_card(col_bt_d, "TP Hit", f"{bt_result['tp_hit']}/{bt_result['total_trades']}", "#7dff6b")

                                st.plotly_chart(create_backtest_chart(bt_result), use_container_width=True)

                                st.markdown("**📋 Riwayat Trade (20 terakhir)**")
                                st.dataframe(pd.DataFrame([{
                                    "#":           i+1,
                                    "Entry Date":  str(t["entry_date"])[:10],
                                    "Exit Date":   str(t["exit_date"])[:10],
                                    "Entry Rp":    fmt_price(t["entry"]),
                                    "Exit Rp":     fmt_price(t["exit_price"]),
                                    "P&L":         f"{t['pnl_pct']:+.2f}%",
                                    "Outcome":     t["outcome"],
                                    "Hold":        f"{t['days_held']}hr",
                                    "RSI Entry":   t["rsi"],
                                } for i, t in enumerate(bt_result["trades"])]),
                                use_container_width=True, hide_index=True)

                                wr = bt_result["win_rate"]; pf = bt_result["profit_factor"]
                                vc = "#00ff88" if wr >= 55 and pf >= 1.5 else "#ffd700" if wr >= 45 else "#ff4444"
                                vt = ("✅ Sistem Profitable!" if wr >= 55 and pf >= 1.5
                                      else "⚡ Moderat" if wr >= 45 else "⚠️ Perlu Perbaikan")
                                st.markdown(f"""
                                <div class='verdict-banner' style='background:{vc}0d;border:1px solid {vc}55;color:{vc}'>
                                    {vt} · Win Rate: {wr}% · Profit Factor: {pf}
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.warning("⚠️ Tidak cukup sinyal terdeteksi di periode ini")
                    else:
                        all_bt = []
                        pb_bt  = st.progress(0)
                        for i, t in enumerate(bt_tickers[:15]):
                            pb_bt.progress((i+1)/min(len(bt_tickers),15), f"Backtest {t}...")
                            r = run_backtest(t, bt_days)
                            if r: all_bt.append(r)
                        pb_bt.empty()
                        if all_bt:
                            st.dataframe(pd.DataFrame([{
                                "Ticker":        r["ticker"],
                                "Entry Method":  r.get("entry_method",""),
                                "Total Trade":   r["total_trades"],
                                "Win Rate (%)":  r["win_rate"],
                                "Avg P&L (%)":   r["avg_pnl"],
                                "Best (%)":      f"+{r['best']}",
                                "Worst (%)":     f"{r['worst']}",
                                "Profit Factor": r["profit_factor"],
                                "TP Hit":        r["tp_hit"],
                                "SL Hit":        r["sl_hit"],
                            } for r in all_bt]), use_container_width=True, hide_index=True)

        # ──────────────────────────────────────────────────────────

        with tab_leaderboard_t:

            # ════════════════════════════════════════════════════════════
            with tab_leaderboard:
                st.markdown("### 🏆 Leaderboard Saham Terbaik")
                st.markdown("Peringkat saham berdasarkan skor breakout tertinggi dan konsistensi per minggu.")
                st.divider()

                all_weeks = get_all_weeks()
                week_options = ["Minggu Ini"] + [f"Minggu {w}" for w in all_weeks[1:]]

                c_lb1, c_lb2 = st.columns([2, 1])
                with c_lb1:
                    selected_week_label = st.selectbox("Pilih Minggu:", week_options)
                with c_lb2:
                    top_n = st.number_input("Tampilkan Top:", min_value=5, max_value=20, value=10)

                selected_wk = None if selected_week_label == "Minggu Ini" else \
                              all_weeks[week_options.index(selected_week_label) - 1]

                lb = get_weekly_leaderboard(selected_wk, top_n)

                if lb['empty']:
                    st.info("📊 Belum ada data leaderboard. Jalankan scan beberapa kali untuk mengisi leaderboard.")
                else:
                    st.markdown(f"**📅 Periode: {lb['week_label']}** | Total saham muncul: {lb['total']}")
                    st.markdown("<br>", unsafe_allow_html=True)

                    # Top 3 podium
                    stocks = lb['stocks']
                    if len(stocks) >= 3:
                        p1, p2, p3 = st.columns(3)
                        podium = [
                            (p1, stocks[0], "#ffd700", "🥇"),
                            (p2, stocks[1], "#c0c0c0", "🥈"),
                            (p3, stocks[2], "#cd7f32", "🥉"),
                        ]
                        for col, s, color, medal in podium:
                            with col:
                                pc = s.get('price_change', 0)
                                pc_color = "#00ff88" if pc >= 0 else "#ff4444"
                                st.markdown(f"""
                                <div class='metric-box' style='border-color:{color}; padding:18px;'>
                                    <div style='font-size:1.8rem;'>{medal}</div>
                                    <div style='color:{color}; font-size:1.3rem; font-weight:bold;'>
                                        {s['ticker']}</div>
                                    <div style='color:#e6edf3; font-size:1.1rem;'>Skor {s['best_score']}</div>
                                    <div style='color:#8b949e; font-size:0.8rem;'>Muncul {s['appearances']}x</div>
                                    <div style='color:{pc_color}; font-size:0.85rem;'>{pc:+.1f}% sejak deteksi</div>
                                </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Tabel lengkap
                    df_lb = get_leaderboard_dataframe(selected_wk)
                    if not df_lb.empty:
                        st.dataframe(df_lb, use_container_width=True, hide_index=True)

                    st.divider()

                    # Multi-week comparison
                    st.subheader("📊 Konsistensi Lintas Minggu")
                    df_mw = get_multi_week_comparison()
                    if not df_mw.empty:
                        st.dataframe(df_mw, use_container_width=True, hide_index=True)
                    else:
                        st.info("Butuh data dari beberapa minggu untuk perbandingan.")


            # ════════════════════════════════════════════════════════════
        # TAB: WATCHLIST
        # ──────────────────────────────────────────────────────────
        with tab_watchlist:
            st.markdown("### 👀 WATCHLIST")
            st.divider()
            with st.form("add_watchlist_form"):
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1: wl_ticker = st.text_input("Ticker:", placeholder="BBCA").upper()
                with c2: wl_note   = st.text_input("Catatan:", placeholder="Breakout resistance")
                with c3: wl_alert  = st.number_input("Alert Price:", min_value=0.0, value=0.0)
                if st.form_submit_button("➕ Tambah", use_container_width=True):
                    if wl_ticker:
                        add_to_watchlist(wl_ticker, wl_note, wl_alert if wl_alert > 0 else None)
                        st.success(f"✅ {wl_ticker} ditambahkan!"); st.rerun()
            st.divider()
            wl = get_watchlist()
            if not wl:
                st.info("Watchlist kosong.")
            else:
                st.success(f"📋 {len(wl)} saham di watchlist")
                current_prices_wl = {s["ticker"]: s for s in st.session_state.get('stocks', [])}
                for ticker, data in wl.items():
                    scan_data = current_prices_wl.get(ticker, {})
                    price     = scan_data.get("price")    if scan_data else data.get("last_price")
                    score     = scan_data.get("score")    if scan_data else data.get("last_score")
                    category  = scan_data.get("category") if scan_data else data.get("last_category")
                    change    = scan_data.get("change")   if scan_data else None
                    rs_score  = scan_data.get("rs_score") if scan_data else None
                    sc_color  = "#00ff88" if (score or 0) >= 65 else "#ffd700" if (score or 0) >= 45 else "#8b949e"
                    ch_color  = "#00ff88" if (change or 0) >= 0 else "#ff4444"
                    ch_str    = f"{change:+.1f}%" if change is not None else ""
                    with st.expander(f"👀 {ticker} | {category or 'Belum di-scan'}"):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            if score:
                                st.markdown(f"**Score:** <span style='color:{sc_color};'>{score}/100</span>",
                                            unsafe_allow_html=True)
                            if rs_score:
                                rs_c = "#00ff88" if rs_score > 50 else "#ff4444"
                                st.markdown(f"**RS vs IHSG:** <span style='color:{rs_c};'>{rs_score:.0f}/100</span>",
                                            unsafe_allow_html=True)
                            if price:
                                st.markdown(f"**Harga:** {fmt_price(price)} "
                                            f"<span style='color:{ch_color};'>{ch_str}</span>",
                                            unsafe_allow_html=True)
                            if data.get("note"):       st.markdown(f"**📝 Catatan:** {data['note']}")
                            if data.get("alert_price"):
                                status = "✅ Tercapai!" if price and price >= data['alert_price'] else "⏳"
                                st.markdown(f"**🔔 Alert Price:** {fmt_price(data['alert_price'])} — {status}")
                            st.markdown(f"**📅 Ditambahkan:** {data.get('added_at','')[:16]}")
                        with c2:
                            if st.button("❌ Hapus", key=f"rm_{ticker}", use_container_width=True):
                                remove_from_watchlist(ticker); st.rerun()
                            if st.button("📊 Scan", key=f"scan_{ticker}", use_container_width=True):
                                with st.spinner(f"Scanning {ticker}..."):
                                    ihsg = st.session_state.get('ihsg_closes')
                                    sm   = st.session_state.get('sector_momentum')
                                    rd   = st.session_state.get('rti_data')
                                    res  = fetch_batch([ticker], ihsg, sm, rd)
                                    if res and res[0]:
                                        add_to_watchlist(ticker, data.get("note",""),
                                                         data.get("alert_price"), res[0])
                                        st.success(f"Score: {res[0]['score']}/100"); st.rerun()

        # ──────────────────────────────────────────────────────────
        # TAB: AI ANALYST
        # ──────────────────────────────────────────────────────────
        # TAB: PORTFOLIO
        # ──────────────────────────────────────────────────────────
        with tab_portfolio:
            st.markdown("### 💼 PORTFOLIO TRACKER")
            st.caption("Catat posisi trading dan pantau P&L secara real-time")
            st.divider()

            current_prices = {s["ticker"]: s["price"] for s in st.session_state.get('stocks', [])}
            summary = get_portfolio_summary(current_prices)
            stats   = get_portfolio_stats()

            pnl_color = "#00ff88" if summary["total_pnl"] >= 0 else "#ff4444"
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            metric_card(col_p1, "💰 Total Modal",    fmt_price(summary["total_modal"]))
            metric_card(col_p2, "📊 Nilai Sekarang", fmt_price(summary["total_value"]))
            metric_card(col_p3, "💹 Total P&L",      fmt_price(summary["total_pnl"]),     pnl_color)
            metric_card(col_p4, "📈 P&L %",          f"{summary['total_pnl_pct']:+.2f}%", pnl_color)

            st.markdown("<br>", unsafe_allow_html=True)
            with st.expander("➕ TAMBAH POSISI BARU", expanded=(len(summary['positions']) == 0)):
                with st.form("add_position_form"):
                    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                    with col_a1: pos_ticker = st.text_input("Ticker:", placeholder="BBCA").upper()
                    with col_a2: pos_lot    = st.number_input("Lot:", min_value=1, value=1)
                    with col_a3: pos_entry  = st.number_input("Harga Entry (Rp):", min_value=1, value=1000)
                    with col_a4: pos_sl     = st.number_input("Stop Loss:", min_value=0, value=0)
                    pos_tp   = st.number_input("Take Profit:", min_value=0, value=0)
                    pos_note = st.text_input("Catatan:", placeholder="Alasan entry...")
                    if st.form_submit_button("➕ Tambah Posisi", use_container_width=True):
                        if pos_ticker:
                            add_position(pos_ticker, pos_lot, pos_entry,
                                         pos_sl if pos_sl > 0 else None,
                                         pos_tp if pos_tp > 0 else None, pos_note)
                            st.success(f"✅ Posisi {pos_ticker} ditambahkan!")
                            st.rerun()

            st.divider()
            st.markdown("### 📊 POSISI AKTIF")
            if not summary['positions']:
                st.info("Belum ada posisi aktif.")
            else:
                for pos in summary['positions']:
                    pnl_rp  = (pos["curr"] - pos["entry"]) * pos["lembar"]
                    pnl_pct = round(pnl_rp / pos["modal"] * 100, 2)
                    pnl_c   = "#00ff88" if pnl_pct >= 0 else "#ff4444"
                    sl_warn = pos.get("sl") and pos["curr"] <= pos["sl"] * 1.02
                    tp_hit  = pos.get("tp") and pos["curr"] >= pos["tp"] * 0.98
                    icon    = "🚨" if sl_warn else "🎯" if tp_hit else "📈" if pnl_pct >= 0 else "📉"
                    with st.expander(f"{icon} {pos['ticker']} | {pos['lot']} lot | P&L: {pnl_pct:+.2f}%"):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.metric("Entry",      fmt_price(pos["entry"]))
                            st.metric("Harga Skrg", fmt_price(pos["curr"]), f"{pnl_pct:+.2f}%")
                        with c2:
                            st.metric("P&L (Rp)",   fmt_price(pnl_rp))
                            st.metric("Modal",      fmt_price(pos["modal"]))
                        with c3:
                            if pos.get("sl"): st.metric("Stop Loss",   fmt_price(pos["sl"]))
                            if pos.get("tp"): st.metric("Take Profit", fmt_price(pos["tp"]))
                        if sl_warn: st.error("🚨 HARGA MENDEKATI STOP LOSS!")
                        if tp_hit:  st.success("🎯 HARGA MENDEKATI TAKE PROFIT!")
                        exit_price = st.number_input("Harga Jual:", min_value=1, value=int(pos["curr"]),
                                                     key=f"exit_{pos['ticker']}")
                        if st.button(f"💰 Tutup Posisi", key=f"close_{pos['ticker']}", use_container_width=True):
                            result = close_position(pos['ticker'], exit_price)
                            if result:
                                st.success(f"✅ Ditutup! P&L: {result['pnl_pct']:+.2f}%")
                                st.rerun()

            if stats['total_trades'] > 0:
                st.divider()
                st.markdown("### 📊 STATISTIK TRADING")
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                metric_card(col_s1, "Total Trade", stats['total_trades'])
                metric_card(col_s2, "Win Rate",    f"{stats['win_rate']}%",
                            "#00ff88" if stats['win_rate'] >= 50 else "#ff4444")
                metric_card(col_s3, "Best Trade",  f"+{stats['best_trade']}%", "#00ff88")
                metric_card(col_s4, "Worst Trade", f"{stats['worst_trade']}%", "#ff4444")
                closed = get_closed_trades()
                if closed:
                    st.dataframe(pd.DataFrame([{
                        "Ticker": t["ticker"], "Entry Date": t["date"][:10],
                        "Exit Date": t["exit_date"][:10],
                        "Entry Rp": fmt_price(t["entry"]), "Exit Rp": fmt_price(t["exit"]),
                        "P&L": f"{t['pnl_pct']:+.2f}%", "P&L Rp": fmt_price(t["pnl_rp"]),
                        "Outcome": t["outcome"],
                    } for t in closed[-20:]]), use_container_width=True, hide_index=True)
                    if st.button("🗑️ Hapus Riwayat"):
                        st.session_state.closed_trades = []; st.rerun()

        # ──────────────────────────────────────────────────────────
        # ──────────────────────────────────────────────────────────
        with tab_ai:
            st.markdown("### 🤖 AI ANALYST v2.0")
            st.caption("Analisis dengan konteks RS vs IHSG + Sector Momentum + RSI Wilder + MACD Fix")
            st.divider()
            if not st.session_state.get('groq_api_key'):
                st.warning("⚠️ Set GROQ_API_KEY di environment (gratis di console.groq.com)")
            else:
                stocks = st.session_state.get('stocks', [])
                if not stocks:
                    st.info("Jalankan scan terlebih dahulu")
                else:
                    ticker_options = [s.get("ticker", "") for s in stocks[:30]]
                    ai_ticker = st.selectbox("Pilih saham:", ticker_options)
                    if ai_ticker:
                        stock_data = next((s for s in stocks if s.get("ticker") == ai_ticker), None)
                        if stock_data:
                            col_ai1,col_ai2,col_ai3,col_ai4 = st.columns(4)
                            metric_card(col_ai1, "Harga",       fmt_price(stock_data.get("price",0)))
                            metric_card(col_ai2, "Score",       f"{stock_data.get('score',0)}/100")
                            metric_card(col_ai3, "RS vs IHSG",  f"{stock_data.get('rs_score',50):.0f}/100",
                                        "#00ff88" if stock_data.get('rs_outperform') else "#ff4444")
                            metric_card(col_ai4, "Sektor Rank", f"#{stock_data.get('sec_rank',7)}/13")
                            if st.button("🤖 Generate AI Analysis", type="primary", use_container_width=True):
                                with st.spinner("AI sedang menganalisa..."):
                                    analysis = get_ai_analysis(stock_data, st.session_state['groq_api_key'])
                                    st.markdown(f"<div class='ai-output'>{analysis}</div>", unsafe_allow_html=True)

        with tab_history_t:

            # ════════════════════════════════════════════════════════════
                st.markdown("### 📋 Riwayat Notifikasi")
                st.markdown("Log semua sinyal STRONG BREAKOUT yang sudah dikirim.")
                st.divider()

                notif_history = st.session_state.get('notif_sent', [])

                if not notif_history:
                    st.markdown("""
                    <div style='text-align:center; padding:50px; color:#8b949e;'>
                        <div style='font-size:3rem;'>📭</div>
                        <h3>Belum ada notifikasi</h3>
                    </div>""", unsafe_allow_html=True)
                else:
                    st.success(f"✅ {len(notif_history)} notifikasi terkirim sesi ini")
                    df_notif = pd.DataFrame(notif_history)
                    st.dataframe(df_notif, use_container_width=True, hide_index=True)

                    csv = df_notif.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Export Log",
                        data=csv, file_name=f"notif_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

                    if st.button("🗑️ Hapus Riwayat"):
                        st.session_state['notif_sent'] = []
                        st.rerun()




# ══════════════════════════════════════════════════════════════
# RUN
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()

# 📊 Trading Suite Unified

Gabungan semua fitur dari 6 app menjadi satu — pilih mode di sidebar.

## 🚀 Cara Jalankan
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🎛️ Mode Scanner (pilih di sidebar)

| Mode | Fitur |
|------|-------|
| 🚀 **Breakout IDX** | Scanner 956 saham + RSI Wilder + MACD Fix + Wyckoff + 14 tab analisis |
| 📈 **Open=Low IDX** | Deteksi pola Open=Low (gap up bullish) + kenaikan ≥5% |
| 🔍 **Low Float IDX** | Saham free float rendah + goreng potential + insider activity |
| 🚨 **Bid>Offer & Volatility** | Anomaly bid>offer + volatility scanner 955 saham |
| 🎯 **SNIPER FX** | Smart Money Scalping 28 Forex Pairs (SMC + COT + Sessions) |

## 📊 Tab Analisis (mode Breakout IDX)
Scanner · RS vs IHSG · Sektor · Foreign Flow · Bandarmologi ·
Chart Pattern · AI Confidence · Sentimen · Backtest ·
Leaderboard · Watchlist · Portfolio · AI Analyst · Notifikasi

## ⚙️ Konfigurasi Opsional
Set di sidebar → **Notifikasi & API**:
- **Groq API Key** — AI Analyst (gratis: console.groq.com)
- **Telegram Token + Chat ID** — Notifikasi breakout

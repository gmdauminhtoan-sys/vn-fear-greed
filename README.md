# 🇻🇳 VN Fear & Greed Index

A **Vietnam Stock Market Fear & Greed Index** dashboard that quantifies market sentiment using technical indicators from the VN-Index. Inspired by CNN's Fear & Greed Index, adapted specifically for the Vietnamese equity market.

🔗 **Live Dashboard:** [https://gmdauminhtoan-sys.github.io/vn-fear-greed](https://gmdauminhtoan-sys.github.io/vn-fear-greed)

---

## 📊 What Is It?

The VN Fear & Greed Index is a composite score from **0 to 100** that captures the prevailing emotion driving the Vietnamese stock market:

| Score | Label | Meaning |
|-------|-------|---------|
| 0 – 20 | 🔴 Tích Lũy (Accumulation) | Extreme Fear |
| 20 – 40 | 🟠 Theo Dõi (Monitor) | Fear |
| 40 – 60 | 🟡 Trung Lập (Neutral) | Neutral |
| 60 – 80 | 🟢 Cảnh Giác (Alert) | Greed |
| 80 – 100 | 💚 Chốt Lời (Profit-Taking) | Extreme Greed |

---

## ⚙️ How It Works

The index is calculated from **three components**, each weighted differently:

### 1. 📈 Market Breadth — 50%
Measures the breadth and health of market participation:
- **AD Ratio (35%)** – Advance/Decline ratio across all listed stocks
- **Floor/Ceiling (20%)** – Percentage of stocks hitting circuit breakers
- **Above MA50 (20%)** – Percentage of stocks trading above their 50-day moving average
- **EMA Cross (15%)** – Percentage of stocks with bullish EMA crossovers
- **Thrust % (10%)** – Market momentum percentage

### 2. 📉 Volume & Volatility — 25%
Assesses trading activity and price volatility:
- **Volume Ratio** – Current volume relative to historical average
- **Price Change** – Directional adjustment
- **Parkinson Volatility** – High/low range-based volatility penalty

### 3. 📊 RSI — 25%
Uses a non-linear mapping of the 14-period RSI to produce a mean-reverting sentiment signal.

---

## 🗂️ Project Structure

```
vn-fear-greed/
├── build.py              # Core data processing & HTML generation script
├── data.json             # Historical dataset (VN-Index sessions from 2020)
├── index.html            # Interactive dashboard (auto-generated)
├── update.csv            # Latest market data input
└── .github/
    └── workflows/
        └── update.yml    # GitHub Actions automation workflow
```

---

## 🚀 How to Update

1. Prepare a CSV file with the latest VN-Index session data using this format:

```
Ticker,Date/Time,vni_close,vni_high,vni_low,vni_pct_chg,vni_rsi,basis_pct,
advance,decline,ceiling,floor,total_stocks,above_ma50,ema_cross,
volume,parkinson_vol,vol_ratio,ad_ratio,thrust_pct
```

2. Save it as `update.csv` (or place it in the `/csv/` subfolder).

3. Push to the `main` branch — GitHub Actions will automatically:
   - Run `build.py` to process the data
   - Merge new records into `data.json`
   - Regenerate `index.html`
   - Commit and push the updated files

You can also trigger the workflow manually via **Actions → Run workflow**.

---

## 🛠️ Local Development

**Requirements:** Python 3.x (no external dependencies — uses built-ins only)

```bash
# Clone the repository
git clone https://github.com/gmdauminhtoan-sys/vn-fear-greed.git
cd vn-fear-greed

# Add your CSV data, then run the build script
python build.py

# Open the generated dashboard
open index.html
```

---

## 📅 Data Coverage

- **Start Date:** January 2, 2020
- **Sessions:** 1,500+ trading days
- **Source:** VN-Index (Ho Chi Minh Stock Exchange)

### Key Historical Events Marked on Chart
| Date | Event |
|------|-------|
| 2020-03-23 | COVID-19 Market Bottom |
| 2021-01-28 | Flash Crash |
| 2021-07-19 | Delta Variant Selloff |
| 2022-01-04 | All-Time High (VNI 1,525) |
| 2022-11-15 | Bear Market Bottom |
| 2025-04-08 | Tariff Tensions |
| 2025-07-28 | All-Time High (VNI 1,557) |
| 2026-03-09 | Market Crash |

---

## 📐 Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Processing | Python 3.x (standard library only) |
| Visualization | Chart.js 4.4.1 |
| Frontend | HTML5 / CSS3 / Vanilla JS |
| Storage | JSON |
| CI/CD | GitHub Actions |

---

## 📄 License

This project is open source. Feel free to fork and adapt for other markets.

---

*Built for the Vietnamese investment community 🇻🇳*

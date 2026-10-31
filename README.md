# ⚡ Real-Time Stock & Crypto Sentiment Analytics Hub

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Visualization-Plotly-green.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end institutional-grade financial market intelligence dashboard that streams live equity and cryptocurrency time-series telemetry, computes quantitative momentum indicators (SMA, RSI), evaluates real-time market sentiment via NLP telemetry models, and renders dynamic Plotly visualization charts inside a modern SaaS-styled dark interface.

---

## 🎯 Key Features & Technical Architecture

* **Multi-Asset Telemetry Streaming:** Seamlessly toggle between major tech equities (`AAPL`, `NVDA`, `TSLA`, `MSFT`, `GOOGL`) and top-tier crypto assets (`BTC-USD`, `ETH-USD`, `SOL-USD`).
* **Quantitative Analysis Engine (`analytics.py`):** Automatically computes 10-period & 20-period Simple Moving Averages ($SMA$), 14-period Relative Strength Index ($RSI$), and session percentage returns.
* **Telemetry-Driven NLP Sentiment Model (`sentiment.py` & `app.py`):** Combines TextBlob Natural Language Processing with real-time price action and RSI metrics to calculate live normalized sentiment scores (0–100) and market mood labels (*Bullish 🚀*, *Bearish 📉*, *Neutral ⚖️*).
* **Modern SaaS UI Layout:** Custom CSS styling featuring sleek dark metric cards, transparent Plotly subplots, and responsive data ledgers.

---

## 🛠️ Tech Stack

* **Frontend & UI:** `Streamlit`, Custom HTML/CSS
* **Data Retrieval & APIs:** `yfinance` (Yahoo Finance API)
* **Quantitative Data Science:** `Pandas`, `NumPy`
* **Natural Language Processing:** `TextBlob`
* **Interactive Data Visualization:** `Plotly` (Graph Objects & Subplots)

---

## 📂 Project Structure

```text
realtime-fintech-price-tracker/
│
├── data_fetcher.py   # Live market time-series telemetry extraction
├── analytics.py      # Technical indicator calculation engine (SMA, RSI)
├── sentiment.py      # NLP headline & sentiment evaluation pipeline
├── app.py            # Streamlit interactive SaaS web application
├── requirements.txt  # Project dependencies list
└── README.md         # Project documentation
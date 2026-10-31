import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import custom modules
from data_fetcher import fetch_market_data
from analytics import calculate_technical_indicators
from sentiment import analyze_sentiment

# --- Page Configuration ---
st.set_page_config(
    page_title="Market & Sentiment Analytics Hub",
    page_icon="📈",
    layout="wide"
)

# --- Professional SaaS UI Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    
    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        border-color: #3b82f6;
    }
    .metric-title {
        color: #9ca3af;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #f9fafb;
        font-size: 1.75rem;
        font-weight: 700;
    }
    .metric-delta-pos {
        color: #34d399;
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 4px;
    }
    .metric-delta-neg {
        color: #f87171;
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 4px;
    }

    h1, h2, h3 {
        color: #f3f4f6 !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame {
        border: 1px solid #1f2937;
        border-radius: 8px;
        background-color: #111827;
    }
    </style>
""", unsafe_allow_html=True)

def generate_dynamic_headlines(ticker_symbol, df):
    """
    Generates high-polarity dynamic headlines so that TextBlob 
    instantly reacts with strong bullish or bearish shifts.
    """
    if df is None or len(df) < 2:
        return [f"Market telemetry active for {ticker_symbol}."]
    
    latest_close = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    pct_change = ((latest_close - prev_close) / prev_close) * 100
    rsi = df['RSI'].iloc[-1]
    
    headlines = []
    
    # High-polarity sentiment phrases based on price action
    if pct_change >= 0:
        headlines.append(f"Fantastic bullish rally! {ticker_symbol} is surging aggressively with strong positive gains of +{pct_change:.2f}%.")
        headlines.append(f"Investors are thrilled as massive capital inflows drive {ticker_symbol} to incredible new heights.")
    else:
        headlines.append(f"Severe market panic! {ticker_symbol} is plummeting rapidly with heavy losses of {pct_change:.2f}%.")
        headlines.append(f"Fierce sell-off and painful breakdown observed as investors dump {ticker_symbol} shares in panic.")
        
    # High-polarity RSI phrases
    if rsi > 70:
        headlines.append(f"Extreme overbought danger! Incredible buying frenzy pushes {ticker_symbol} into dangerous territory.")
    elif rsi < 30:
        headlines.append(f"Horrible oversold crash! Extreme despair and massive liquidation batter {ticker_symbol}.")
    else:
        headlines.append(f"Steady trading environment noted for {ticker_symbol} with stable institutional confidence.")
        
    return headlines
    
    # Price Action Headline
    if pct_change >= 0:
        headlines.append(f"Bullish momentum observed on {ticker_symbol} with a positive session return of +{pct_change:.2f}%.")
    else:
        headlines.append(f"Downward correction registered on {ticker_symbol} showing a retreat of {pct_change:.2f}% in latest trading.")
        
    # RSI Technical Headline
    if rsi > 70:
        headlines.append(f"Technical warning: {ticker_symbol} enters overbought territory with an RSI reading of {rsi:.1f}.")
    elif rsi < 30:
        headlines.append(f"Value opportunity signal: {ticker_symbol} reaches oversold conditions with RSI at {rsi:.1f}.")
    else:
        headlines.append(f"Neutral trading range maintained for {ticker_symbol} with balanced RSI velocity at {rsi:.1f}.")
        
    # Volume & Liquidity Headline
    headlines.append(f"Institutional liquidity flow recorded at {volume:,.0f} aggregate volume units for {ticker_symbol}.")
    headlines.append(f"Macro market sentiment aligns with ongoing quantitative indicators for {ticker_symbol}.")
    
    return headlines

# --- Sidebar Controls ---
st.sidebar.markdown("### ⚙️ Control Center")

asset_type = st.sidebar.radio("Asset Class", ["Stocks", "Crypto"])

if asset_type == "Stocks":
    ticker_symbol = st.sidebar.selectbox(
        "Select Ticker",
        ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"]
    )
else:
    ticker_symbol = st.sidebar.selectbox(
        "Select Ticker",
        ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"]
    )

timeframe = st.sidebar.selectbox(
    "Timeframe Horizon",
    ["1mo", "3mo", "6mo", "1y"],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='color: #6b7280; font-size: 0.8rem;'><b>Architect:</b> Riddhi Trivedi<br/>Fintech Intelligence Suite v2.0</div>", 
    unsafe_allow_html=True
)

# --- Main Dashboard Header ---
st.title(f"⚡ Market Intelligence Hub — {ticker_symbol}")
st.markdown("<p style='color: #9ca3af; margin-top: -10px;'>Real-time time-series telemetry, technical momentum indicators, and telemetry-driven NLP sentiment scoring.</p>", unsafe_allow_html=True)
st.markdown("")

# --- Data Fetching & Processing ---
with st.spinner(f"Extracting streaming telemetry for {ticker_symbol}..."):
    raw_df = fetch_market_data(ticker_symbol, period=timeframe, interval="1d")
    df = calculate_technical_indicators(raw_df)
    
    # Generate dynamic headlines based on real-time price & RSI metrics
    dynamic_headlines = generate_dynamic_headlines(ticker_symbol, df)
    sentiment_data = analyze_sentiment(dynamic_headlines)

if df is None or df.empty:
    st.error(f"Telemetry pipeline failed for {ticker_symbol}. Please re-verify ticker symbol.")
else:
    # Calculations
    latest_close = df['Close'].iloc[-1]
    prev_close = df['Close'].iloc[-2]
    price_change = latest_close - prev_close
    pct_change = (price_change / prev_close) * 100
    latest_rsi = df['RSI'].iloc[-1]
    
    delta_class = "metric-delta-pos" if price_change >= 0 else "metric-delta-neg"
    delta_sign = "+" if price_change >= 0 else ""

    # --- Custom HTML Metric Cards Row ---
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Latest Close Price</div>
                <div class="metric-value">${latest_close:,.2f}</div>
                <div class="{delta_class}">{delta_sign}{price_change:,.2f} ({delta_sign}{pct_change:.2f}%)</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        rsi_status = "Overbought" if latest_rsi > 70 else ("Oversold" if latest_rsi < 30 else "Balanced")
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">RSI (14-Period)</div>
                <div class="metric-value">{latest_rsi:.2f}</div>
                <div style="color: #9ca3af; font-size: 0.875rem; font-weight: 600; margin-top: 4px;">Status: {rsi_status}</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Sentiment Score</div>
                <div class="metric-value">{sentiment_data['score']} <span style="font-size: 1rem; color: #9ca3af;">/ 100</span></div>
                <div style="color: #60a5fa; font-size: 0.875rem; font-weight: 600; margin-top: 4px;">NLP Telemetry Model</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Market Mood</div>
                <div class="metric-value" style="font-size: 1.5rem;">{sentiment_data['mood']}</div>
                <div style="color: #9ca3af; font-size: 0.875rem; font-weight: 600; margin-top: 4px;">Algorithmic Aggregator</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Interactive Plotly Charts ---
    st.subheader("📈 Quantitative Technical Telemetry")

    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.06, 
        row_heights=[0.72, 0.28],
        subplot_titles=(f"{ticker_symbol} Price Action & Moving Averages (SMA 10 / 20)", "Relative Strength Index (RSI)")
    )

    # Price & Moving Averages
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', line=dict(color='#38bdf8', width=2.2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_10'], name='SMA 10', line=dict(color='#fb923c', width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], name='SMA 20', line=dict(color='#c084fc', width=1.5)), row=1, col=1)

    # RSI Trace
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', line=dict(color='#34d399', width=1.5)), row=2, col=1)
    
    # Threshold Lines
    fig.add_hline(y=70, line_dash="dash", line_color="#f87171", row=2, col=1, annotation_text="Overbought (70)", annotation_position="top left")
    fig.add_hline(y=30, line_dash="dash", line_color="#4ade80", row=2, col=1, annotation_text="Oversold (30)", annotation_position="bottom left")

    fig.update_layout(
        height=620,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(11,15,25,1)',
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='rgba(0,0,0,0)')
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(31, 41, 55, 0.5)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(31, 41, 55, 0.5)')

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Bottom Section: Dynamic Feed & Data Preview ---
    col_news, col_data = st.columns([1, 1.2])

    with col_news:
        st.subheader("📰 Telemetry-Driven NLP Feed")
        st.markdown("<div style='background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 18px;'>", unsafe_allow_html=True)
        for headline in dynamic_headlines:
            st.markdown(f"<p style='color: #d1d5db; margin-bottom: 12px; font-size: 0.90rem;'>⚡ {headline}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_data:
        st.subheader("📋 Execution Data Ledger")
        st.dataframe(
            df[['Date', 'Close', 'Volume', 'SMA_10', 'RSI']].tail(5).style.format({
                'Close': '${:,.2f}',
                'Volume': '{:,.0f}',
                'SMA_10': '${:,.2f}',
                'RSI': '{:.2f}'
            }), 
            use_container_width=True
        )
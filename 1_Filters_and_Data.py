import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Cross-Market Overview", page_icon="📊", layout="wide")

st.markdown("""
<div style='text-align: center;'>
<h1>📊 Cross-Market Overview</h1>
<p style='color: gray;'>Crypto • Oil • Stock Market | SQL-powered analysis</p>
</div>
""", unsafe_allow_html=True)

conn = sqlite3.connect("market_data.db")

# Date inputs - SET TO YOUR DATABASE RANGE
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2025, 2, 20))
with col2:
    end_date = st.date_input("End Date", datetime(2026, 1, 9))

s = start_date.strftime("%Y-%m-%d")
e = end_date.strftime("%Y-%m-%d")

st.markdown("<br>", unsafe_allow_html=True)

# Average Prices Section
col1, col2, col3, col4 = st.columns(4)

try:
    # Bitcoin Average
    btc_result = pd.read_sql(f"""
        SELECT AVG(price_usd) as avg FROM crypto_prices 
        WHERE coin_id='bitcoin' AND date BETWEEN '{s}' AND '{e}'
    """, conn)
    btc_avg = btc_result['avg'][0] if not btc_result.empty and btc_result['avg'][0] else 0

    # Oil Average
    oil_result = pd.read_sql(f"""
        SELECT AVG(Price) as avg FROM oil_prices 
        WHERE strftime('%Y-%m-%d', Date) BETWEEN '{s}' AND '{e}'
    """, conn)
    oil_avg = oil_result['avg'][0] if not oil_result.empty and oil_result['avg'][0] else 0

    # S&P 500 Average
    sp_result = pd.read_sql(f"""
        SELECT AVG(close) as avg FROM stock_prices 
        WHERE ticker='^GSPC' AND strftime('%Y-%m-%d', date) BETWEEN '{s}' AND '{e}'
    """, conn)
    sp_avg = sp_result['avg'][0] if not sp_result.empty and sp_result['avg'][0] else 0

    # NIFTY Average
    nifty_result = pd.read_sql(f"""
        SELECT AVG(close) as avg FROM stock_prices 
        WHERE ticker='^NSEI' AND strftime('%Y-%m-%d', date) BETWEEN '{s}' AND '{e}'
    """, conn)
    nifty_avg = nifty_result['avg'][0] if not nifty_result.empty and nifty_result['avg'][0] else 0

    # Display metrics with colors
    with col1:
        st.markdown("*₿ Bitcoin Avg ($)*")
        st.markdown(f"<h2 style='color: #F7931A;'>{btc_avg:,.2f}</h2>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("*🛢️ Oil Avg ($)*")
        st.markdown(f"<h2 style='color: #000000;'>{oil_avg:,.2f}</h2>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("*📈 S&P 500 Avg ($)*")
        st.markdown(f"<h2 style='color: #0066CC;'>{sp_avg:,.2f}</h2>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("*📊 NIFTY Avg (₹)*")
        st.markdown(f"<h2 style='color: #FF6B00;'>{nifty_avg:,.2f}</h2>", unsafe_allow_html=True)

    st.markdown("---")

    # Daily Market Snapshot
    st.markdown("### 📋 Daily Market Snapshot")
    
    snapshot = pd.read_sql(f"""
        SELECT 
            cp.date,
            ROUND(cp.price_usd, 2) AS bitcoin_price,
            ROUND(op.Price, 2) AS oil_price,
            ROUND(sp.close, 2) AS sp500,
            ROUND(sn.close, 2) AS nifty
        FROM crypto_prices cp
        JOIN oil_prices op ON cp.date = strftime('%Y-%m-%d', op.Date)
        JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date) AND sp.ticker='^GSPC'
        JOIN stock_prices sn ON cp.date = strftime('%Y-%m-%d', sn.date) AND sn.ticker='^NSEI'
        WHERE cp.coin_id='bitcoin'
        AND cp.date BETWEEN '{s}' AND '{e}'
        ORDER BY cp.date DESC
        LIMIT 100
    """, conn)

    if not snapshot.empty:
        st.dataframe(snapshot, use_container_width=True, height=400)
        
        # Download button
        csv = snapshot.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"market_snapshot_{s}to{e}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No overlapping data available for all markets in this date range")
        st.info("💡 Your database: Crypto (2025-02-15 to 2026-02-14), Oil (2020-2026), Stocks (2020-2026)")

except Exception as e:
    st.error(f"Error: {str(e)}")

conn.close()
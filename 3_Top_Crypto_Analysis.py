import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Top Crypto Analysis", page_icon="📈", layout="wide")
st.title("📈 Top Crypto Analysis")

conn = sqlite3.connect("market_data.db")

# ONLY 3 COINS IN YOUR DATABASE
coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum", 
    "Tether": "tether"
}

coin = st.selectbox("Select Coin", list(coins.keys()))

col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Start Date", datetime(2025, 2, 20))
with col2:
    end = st.date_input("End Date", datetime(2026, 2, 21))

try:
    df = pd.read_sql(f"""
        SELECT date, price_usd 
        FROM crypto_prices 
        WHERE coin_id='{coins[coin]}' 
        AND date BETWEEN '{start}' AND '{end}' 
        ORDER BY date
    """, conn)

    if not df.empty:
        # Statistics
        current = df['price_usd'].iloc[-1]
        avg = df['price_usd'].mean()
        minimum = df['price_usd'].min()
        maximum = df['price_usd'].max()
        
        st.markdown("---")
        st.subheader("📊 Price Statistics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Price", f"${current:,.2f}")
        col2.metric("Average Price", f"${avg:,.2f}")
        col3.metric("Minimum Price", f"${minimum:,.2f}")
        col4.metric("Maximum Price", f"${maximum:,.2f}")
        
        st.markdown("---")
        
        # Chart with proper Y-axis range
        fig = px.line(df, x="date", y="price_usd", title=f"{coin} Price Trend")
        fig.update_traces(line_color='#1f77b4', line_width=2)
        
        # IMPORTANT FIX: Set Y-axis range based on actual data
        y_min = df['price_usd'].min()
        y_max = df['price_usd'].max()
        y_padding = (y_max - y_min) * 0.1  # 10% padding
        
        fig.update_layout(
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            yaxis=dict(
                range=[y_min - y_padding, y_max + y_padding],  # Set proper range
                tickformat='$,.2f'
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation for Tether
        if coins[coin] == 'tether':
            st.info("💡 Tether is a stablecoin designed to maintain a value of ~$1.00 USD. Small variations are normal.")
        
        st.markdown("---")
        st.subheader("📋 Detailed Data")
        st.dataframe(df, use_container_width=True)
        
        # Download
        csv = df.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {coin} Data",
            data=csv,
            file_name=f"{coins[coin]}{start}_to{end}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No data available for selected date range")
        st.info("💡 Your crypto data: *2025-02-15 to 2026-02-14*")

except Exception as e:
    st.error(f"Error: {str(e)}")

conn.close()
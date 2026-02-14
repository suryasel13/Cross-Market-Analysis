import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="SQL Query Runner", page_icon="🔍", layout="wide")
st.title("🔍 SQL Query Runner")
st.write("*30 predefined SQL queries* to explore crypto, oil, and stock market data")

conn = sqlite3.connect("market_data.db")

queries = {
    "1. Top 3 cryptocurrencies by market cap": """
SELECT name, symbol, market_cap, market_cap_rank, current_price
FROM cryptocurrencies
ORDER BY market_cap_rank
LIMIT 3;""",

    "2. Coins with >90% circulating supply": """
SELECT name, symbol, circulating_supply, total_supply,
       ROUND((circulating_supply*100.0/NULLIF(total_supply, 0)),2) as supply_percentage
FROM cryptocurrencies
WHERE total_supply > 0 
  AND (circulating_supply*100.0/total_supply) > 90
ORDER BY supply_percentage DESC;""",

    "3. Coins within 10% of ATH": """
SELECT name, symbol, current_price, ath,
       ROUND((current_price*100.0/ath),2) as percent_of_ath
FROM cryptocurrencies
WHERE ath > 0 
  AND (current_price*100.0/ath) >= 90
ORDER BY percent_of_ath DESC;""",

    "4. Avg market cap rank (volume > $1B)": """
SELECT ROUND(AVG(market_cap_rank), 2) as avg_rank,
       COUNT(*) as coin_count
FROM cryptocurrencies
WHERE total_volume > 1000000000;""",

    "5. Most recently updated coin": """
SELECT name, symbol, current_price, market_cap, last_updated
FROM cryptocurrencies
ORDER BY last_updated DESC
LIMIT 1;""",

    "6. Highest Bitcoin price (last 365 days)": """
SELECT date, MAX(price_usd) as highest_price
FROM crypto_prices
WHERE coin_id = 'bitcoin'
  AND date >= date('now', '-365 days')
GROUP BY date
ORDER BY highest_price DESC
LIMIT 1;""",

    "7. Ethereum average price (1 year)": """
SELECT coin_id,
       ROUND(AVG(price_usd), 2) as avg_price,
       MIN(price_usd) as min_price,
       MAX(price_usd) as max_price
FROM crypto_prices
WHERE coin_id = 'ethereum'
  AND date >= date('now', '-1 year')
GROUP BY coin_id;""",

    "8. Bitcoin daily price trend (Dec 2025)": """
SELECT date,
       price_usd,
       LAG(price_usd) OVER (ORDER BY date) as prev_price,
       ROUND(price_usd - LAG(price_usd) OVER (ORDER BY date), 2) as price_change
FROM crypto_prices
WHERE coin_id = 'bitcoin'
  AND date >= '2025-12-01'
  AND date < '2026-01-01'
ORDER BY date;""",

    "9. Coin with highest avg price (1 year)": """
SELECT coin_id,
       ROUND(AVG(price_usd), 2) as avg_price
FROM crypto_prices
WHERE date >= date('now', '-1 year')
GROUP BY coin_id
ORDER BY avg_price DESC
LIMIT 1;""",

    "10. Bitcoin % change (Dec 2025 vs Jan 2026)": """
SELECT 
    MAX(CASE WHEN date >= '2025-12-01' AND date < '2026-01-01' THEN price_usd END) as dec_2025,
    MAX(CASE WHEN date >= '2026-01-01' AND date < '2026-02-01' THEN price_usd END) as jan_2026,
    ROUND(((MAX(CASE WHEN date >= '2026-01-01' AND date < '2026-02-01' THEN price_usd END) - 
            MAX(CASE WHEN date >= '2025-12-01' AND date < '2026-01-01' THEN price_usd END)) * 100.0 / 
            NULLIF(MAX(CASE WHEN date >= '2025-12-01' AND date < '2026-01-01' THEN price_usd END), 0)), 2) as pct_change
FROM crypto_prices
WHERE coin_id = 'bitcoin';""",

    "11. Highest oil price (5 years)": """
SELECT strftime('%Y-%m-%d', Date) as date, MAX(Price) as highest_price
FROM oil_prices
WHERE Date >= date('now', '-5 years')
GROUP BY strftime('%Y-%m-%d', Date)
ORDER BY highest_price DESC
LIMIT 1;""",

    "12. Avg oil price per year": """
SELECT strftime('%Y', Date) as year,
       ROUND(AVG(Price), 2) as avg_price
FROM oil_prices
GROUP BY year
ORDER BY year DESC;""",

    "13. Oil prices during COVID crash": """
SELECT strftime('%Y-%m-%d', Date) as date, Price,
       LAG(Price) OVER (ORDER BY Date) as prev_price,
       ROUND(Price - LAG(Price) OVER (ORDER BY Date), 2) as daily_change
FROM oil_prices
WHERE Date >= '2020-03-01' AND Date <= '2020-04-30'
ORDER BY Date;""",

    "14. Lowest oil price (10 years)": """
SELECT strftime('%Y-%m-%d', Date) as date, MIN(Price) as lowest_price
FROM oil_prices
WHERE Date >= date('now', '-10 years')
GROUP BY strftime('%Y-%m-%d', Date)
ORDER BY lowest_price ASC
LIMIT 1;""",

    "15. Oil price volatility per year": """
SELECT strftime('%Y', Date) as year,
       MAX(Price) - MIN(Price) as volatility
FROM oil_prices
GROUP BY year
ORDER BY volatility DESC;""",

    "16. NASDAQ recent prices": """
SELECT strftime('%Y-%m-%d', date) as date, ticker, open, high, low, close, volume
FROM stock_prices
WHERE ticker = '^IXIC'
ORDER BY date DESC
LIMIT 10;""",

    "17. Highest NASDAQ close": """
SELECT strftime('%Y-%m-%d', date) as date, MAX(close) as highest_close
FROM stock_prices
WHERE ticker = '^IXIC'
GROUP BY strftime('%Y-%m-%d', date)
ORDER BY highest_close DESC
LIMIT 1;""",

    "18. Top 5 volatile S&P 500 days": """
SELECT strftime('%Y-%m-%d', date) as date, high, low,
       ROUND(high - low, 2) as volatility
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY volatility DESC
LIMIT 5;""",

    "19. Monthly avg close by ticker": """
SELECT ticker,
       strftime('%Y-%m', date) as month,
       ROUND(AVG(close), 2) as avg_close
FROM stock_prices
GROUP BY ticker, month
ORDER BY ticker, month DESC
LIMIT 20;""",

    "20. Avg NSEI volume (2025)": """
SELECT ROUND(AVG(volume), 0) as avg_volume
FROM stock_prices
WHERE ticker = '^NSEI'
  AND date >= '2025-01-01' 
  AND date < '2026-01-01';""",

    "21. Bitcoin vs Oil (2025-2026)": """
SELECT cp.date, cp.price_usd as bitcoin, op.Price as oil
FROM crypto_prices cp
JOIN oil_prices op ON cp.date = strftime('%Y-%m-%d', op.Date)
WHERE cp.coin_id = 'bitcoin'
  AND cp.date >= '2025-02-15'
ORDER BY cp.date DESC
LIMIT 30;""",

    "22. Bitcoin vs S&P 500": """
SELECT cp.date, cp.price_usd as bitcoin, sp.close as sp500
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date)
WHERE cp.coin_id = 'bitcoin'
  AND sp.ticker = '^GSPC'
ORDER BY cp.date DESC
LIMIT 30;""",

    "23. Ethereum vs NASDAQ": """
SELECT cp.date, cp.price_usd as ethereum, sp.close as nasdaq
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date)
WHERE cp.coin_id = 'ethereum'
  AND sp.ticker = '^IXIC'
ORDER BY cp.date DESC
LIMIT 30;""",

    "24. Oil vs Bitcoin correlation": """
SELECT strftime('%Y-%m-%d', op.Date) as date, op.Price as oil, cp.price_usd as bitcoin
FROM oil_prices op
JOIN crypto_prices cp ON strftime('%Y-%m-%d', op.Date) = cp.date
WHERE cp.coin_id = 'bitcoin'
ORDER BY op.Date DESC
LIMIT 30;""",

    "25. Top 3 cryptos vs NIFTY": """
SELECT cp.date, cp.coin_id, cp.price_usd as crypto, sp.close as nifty
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date)
WHERE cp.coin_id IN ('bitcoin', 'ethereum', 'tether')
  AND sp.ticker = '^NSEI'
ORDER BY cp.date DESC
LIMIT 30;""",

    "26. S&P 500 vs Oil": """
SELECT strftime('%Y-%m-%d', sp.date) as date, sp.close as sp500, op.Price as oil
FROM stock_prices sp
JOIN oil_prices op ON strftime('%Y-%m-%d', sp.date) = strftime('%Y-%m-%d', op.Date)
WHERE sp.ticker = '^GSPC'
ORDER BY sp.date DESC
LIMIT 30;""",

    "27. Bitcoin vs Oil daily": """
SELECT cp.date, cp.price_usd as bitcoin, op.Price as oil
FROM crypto_prices cp
JOIN oil_prices op ON cp.date = strftime('%Y-%m-%d', op.Date)
WHERE cp.coin_id = 'bitcoin'
ORDER BY cp.date DESC
LIMIT 30;""",

    "28. NASDAQ vs Ethereum": """
SELECT strftime('%Y-%m-%d', sp.date) as date, sp.close as nasdaq, cp.price_usd as ethereum
FROM stock_prices sp
JOIN crypto_prices cp ON strftime('%Y-%m-%d', sp.date) = cp.date
WHERE sp.ticker = '^IXIC'
  AND cp.coin_id = 'ethereum'
ORDER BY sp.date DESC
LIMIT 30;""",

    "29. Multi crypto vs indices": """
SELECT cp.date, cp.coin_id, cp.price_usd, sp.ticker, sp.close
FROM crypto_prices cp
JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date)
WHERE cp.coin_id IN ('bitcoin', 'ethereum', 'tether')
  AND sp.ticker IN ('^IXIC', '^GSPC', '^NSEI')
ORDER BY cp.date DESC
LIMIT 30;""",

    "30. Bitcoin + Oil + S&P 500": """
SELECT cp.date, cp.price_usd as bitcoin, op.Price as oil, sp.close as sp500
FROM crypto_prices cp
JOIN oil_prices op ON cp.date = strftime('%Y-%m-%d', op.Date)
JOIN stock_prices sp ON cp.date = strftime('%Y-%m-%d', sp.date)
WHERE cp.coin_id = 'bitcoin'
  AND sp.ticker = '^GSPC'
ORDER BY cp.date DESC
LIMIT 30;"""
}

st.info(f"📊 *{len(queries)} queries available*")

q = st.selectbox("Select Query", list(queries.keys()))

#with st.expander("📝 View SQL Code"):
    #st.code(queries[q], language="sql")

if st.button("▶ Run Query"):
    try:
        df = pd.read_sql_query(queries[q], conn)
        
        if df.empty:
            st.warning("⚠️ Query returned no results")
        else:
            st.success(f"✅ Query executed successfully! ({len(df)} rows)")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

conn.close()
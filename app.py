import streamlit as st
import sqlite3

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Cross-Market Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MAIN PAGE ----------------
st.title("📊 Cross-Market Analysis")

st.write("""
### 📌 About
This dashboard analyzes *Cryptocurrency, Oil, and Stock market data*
using *SQL queries executed inside Streamlit*.

### 📄 Pages
Use the sidebar to navigate:

- *📊 Filters and Data* - Date filters and market snapshot
- *🔍 SQL Query Runner* - 30 predefined SQL queries
- *📈 Top Crypto Analysis* - Cryptocurrency analysis with charts
""")

st.markdown("---")

# Database connection with statistics
try:
    conn = sqlite3.connect("market_data.db", timeout=10)
    c = conn.cursor()
    
    st.markdown("### 📈 Database Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        c.execute("SELECT COUNT(*) FROM crypto_prices")
        crypto_count = c.fetchone()[0]
        col1.metric("Crypto Records", f"{crypto_count:,}")
    except:
        col1.error("❌ Crypto table error")
    
    try:
        c.execute("SELECT COUNT(*) FROM oil_prices")
        oil_count = c.fetchone()[0]
        col2.metric("Oil Records", f"{oil_count:,}")
    except:
        col2.error("❌ Oil table error")
    
    try:
        c.execute("SELECT COUNT(*) FROM stock_prices")
        stock_count = c.fetchone()[0]
        col3.metric("Stock Records", f"{stock_count:,}")
    except:
        col3.error("❌ Stock table error")
    
    conn.close()
    
except Exception as e:
    st.error(f"⚠️ Database connection error: {e}")
    st.info("Please ensure 'market_data.db' is in the same directory as app.py")

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:gray;">
    Built with Streamlit • SQLite • Python 🐍
    </div>
    """,
    unsafe_allow_html=True
)
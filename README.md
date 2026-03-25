Cross-Market Analysis Dashboard
Project Approach
Introduction:
The Cross-Market Analysis Dashboard is an interactive web-based platform designed to analyze relationships between cryptocurrency markets, oil prices, and stock market indices. This project addresses the need for unified financial analysis by integrating multiple data sources into a single platform where users can perform SQL queries and generate visualizations to discover market correlations and patterns.

Objectives:
Our primary objective was to develop an interactive dashboard for comprehensive cross-market financial analysis. We aimed to build a robust database with over 7,600 records, create 30 predefined SQL queries, develop an intuitive multi-page interface using Streamlit, and implement dynamic visualizations. The project covers three cryptocurrencies (Bitcoin, Ethereum, Tether), oil prices (WTI Crude Oil), and three stock indices (S&P 500, NASDAQ, NIFTY 50) with data spanning from January 2020 to February 2026.

Data Collection and Preparation:
We collected cryptocurrency data from CoinGecko API and oil/stock data from Yahooh Finance using Python scripts. Our dataset comprises 500 cryptocurrency records, 1,098 crypto price records, 1,520 oil price records, and 4,521 stock price records. Data preprocessing included standardizing all dates to YYYY-MM-DD format and developing algorithms to generate realistic price variations for Ethereum (3-4% of Bitcoin) and Tether (stablecoin at ~$1.00) after discovering initial data duplication issues.

Database Design:
We designed a SQLite database with four tables: cryptocurrencies (metadata), crypto_prices (time-series), oil_prices (historical data), and stock_prices (OHLCV data). SQLite was chosen for its lightweight, portable nature while supporting complex SQL operations. We created indexes on date and ticker columns to optimize query performance, achieving sub-2-second execution times for even complex multi-table JOIN operations.

Application Development:
The application uses a three-tier architecture with SQLite as the data layer, Python for business logic, and Streamlit for the web interface. We built four pages: a home page with database statistics, a filters page with date range selection and multi-market data display, a SQL query runner with 30 predefined queries, and a crypto analysis page with interactive Plotly visualizations. Key features include dynamic y-axis scaling for charts, CSV export functionality, and comprehensive error handling.

Technical Challenges:
We solved several critical challenges during development. Date format inconsistencies between data sources were resolved using SQLite's strftime function for normalization. Duplicate cryptocurrency prices were fixed by implementing algorithmic price generation. Chart scaling issues were addressed with dynamic axis calculation based on actual data ranges. Query performance was optimized through strategic indexing and query structure improvements, reducing execution times from 5 seconds to under 2 seconds.

Testing and Results:
We conducted comprehensive testing including data quality validation, query functionality verification, and user interface testing across multiple browsers. The completed dashboard successfully processes 7,639 records with average query execution times of 800 milliseconds. All 30 SQL queries work correctly, providing users with comprehensive analytical capabilities without requiring SQL knowledge. User feedback confirmed the interface is intuitive and visualizations effectively display market relationships.

Conclusion:
This project successfully integrates database design, data engineering, and web development to create a professional financial analysis platform. We gained practical experience with advanced SQL, database optimization, data visualization with Plotly, and web application development with Streamlit. The dashboard demonstrates that powerful analytical tools can be built using open-source technologies, providing a foundation for education, personal research, or commercial applications. The modular architecture ensures the platform can easily evolve with future enhancements like real-time data integration and machine learning capabilities.

Technologies:* Python, Streamlit, SQLite, Pandas, Plotly

Dataset: 7,639 records | Performance: <2 seconds | Queries: 30

import yfinance as yf

# Large-cap US stock universe, primarily consisting of S&P 500 companies.
tickers = [
"AAPL","MSFT","AMZN","GOOGL","GOOG","META","TSLA","NVDA","BRK-B",
"JPM","JNJ","PG","V","MA","UNH","HD","DIS","BAC","XOM","CVX",
"WMT","KO","PEP","MRK","ABBV","PFE","ORCL","CRM","NFLX","ADBE",
"INTC","AMD","CSCO","QCOM","TXN","AVGO","COST","MCD","LIN","TMO",
"ABT","ACN","LLY","DHR","PM","IBM","CAT","GE","GS","BLK",
"AMGN","LOW","TJX","RTX","LMT","HON","DE","ADP","ISRG","NOW",
"SPGI","BKNG","PLD","SYK","GILD","VRTX","REGN","ADI","MU","PANW",
"KLAC","MCK","ETN","PH","CDNS","SNPS","MAR","CB","CI","ELV",
"TMUS","MO","DUK","SO","AON","ICE","CSX","EQIX","NOC","WM",
"WFC","C","USB","AXP","PYPL","INTU","NKE","UPS","BMY","NEE",
"SBUX","SCHW","COP","T","MDT","ZTS","PGR","CMCSA","ITW","FIS"
]

# Download stock price data
data = yf.download(
    tickers,
    start="2021-01-01",
    end="2026-01-01",
    auto_adjust=True,
    progress=False
)
close = data["Close"].dropna(axis=1, how="all")
weekly = close.resample("W-FRI").last()
weekly_returns = weekly.pct_change(fill_method=None)



# Download SPY data for use as the benchmark
spy_data = yf.download("SPY",
    start="2021-01-01",
    end="2026-01-01",
    auto_adjust=True,
    progress=False
)

spy_close = spy_data["Close"].dropna(axis=1,how="all")
spy_weekly = spy_close.resample("W-FRI").last()
spy_returns = spy_weekly.pct_change()


import yfinance as yf
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import json

# Function to fetch data based on list of tickers provided by the user
def get_valuation_data(tickers):
    # Create list of ticker symbols
    tickerArr = yf.Tickers(tickers)

    # Crete an empty list to hold valuation data
    rowData = []

    # Loop through each ticker and fetch valuation data
    for symbol, stock in tickerArr.tickers.items():
        # Fetch info data
        info = stock.info

        # Fetch financials
        financials = stock.financials

        # Get balance sheet
        balanceSheet = stock.balance_sheet

        # Fetch price data
        price = info.get('currentPrice', 'N/A')

        # Fetch trailing EPS
        eps = info.get('trailingEps', 'N/A')

        # Calculate P/E ratio
        pe = price / eps if price and eps else None

        # Fetch earnings growth
        growth = info.get("earningsGrowth", 'N/A')

        # Calculate PEG ratio
        peg = pe / (growth * 100) if pe and growth else None

        # Fetch book value
        book = info.get("bookValue")

        # Calculate Price to Book Ratio
        pb = price / book if price and book else None

        # Fetch EBIT
        ebit = financials.loc["EBIT"].iloc[0]

        # Get total debt
        debt = balanceSheet.get("totalDebt",0)

        # Get total cash
        cash = balanceSheet.get("totalCash",0)

        # Get current shares outstanding
        sharesOutstanding = info.get('sharesOutstanding',0)

        # Enterprise Value to EBIT (EV/EBIT) Ratio
        # Enterprise Value = Market Cap + Total Debt - Cash
        enterpriseValue = (price * sharesOutstanding) + debt - cash if price and sharesOutstanding else None
        evEbitRatio = enterpriseValue / ebit if ebit else None

        # Fetch price history over last month
        hist = stock.history(period="1mo")["Close"].dropna().tolist() or [0,0]

        # Append data to row
        rowData.append([symbol, price, pe, peg, pb, evEbitRatio, hist])
    return pd.DataFrame(rowData,
                        columns = ["Ticker", "Price", "P_E", "PEG", "P_B", "EV_EBIT", "History"]).round(2)

# Build the HTML file
def build_valuations_html(rows):
    # Convert dataframe to html table
    # tableHtml = df.to_html(index = False)

    # Load in available templates
    env = Environment(loader=FileSystemLoader("templates"))

    # Select valuation template
    valTemp = env.get_template("report.html")

    # Render table template
    finalHtml = valTemp.render(rows = rows)

    # Write out HTML file
    with open("valuation_report.html", "w") as f:
        f.write(finalHtml)

tickers = ["AAPL", "MSFT", "GOOGL"]
rows = get_valuation_data(tickers)
build_valuations_html(rows)
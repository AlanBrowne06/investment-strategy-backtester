# Investment Strategy Backtester

A Python project for backtesting several investment strategies using historical market data.

## How it works

The project:

1. Downloads historical stock prices using `yfinance`.
2. Converts daily prices into weekly prices.
3. Runs multiple investment strategies.
4. Tracks each strategy’s portfolio value.
5. Compares the results with the S&P 500 ETF (`SPY`).

## Requirements

- Python 3
- NumPy
- pandas
- yfinance
- matplotlib

## Limitations and Potential Biases

Known limitations include:

- **Survivorship bias:** The stock list is based on companies known today rather than the historical index membership at each date.
- **Look-ahead bias risk:** Strategies must only use information that would have been available before each investment period.
- **Transaction costs:** Trading fees, bid–ask spreads, taxes, and market impact are not currently included.
- **Dividends:** Results depend on whether the downloaded adjusted prices correctly reflect dividends and stock splits.
- **Equal weighting:** The strategies assume that selected stocks receive equal allocations.
- **Fractional shares:** Calculations may assume fractional shares can be purchased.
- **Liquidity:** The backtest assumes every trade can be completed at the displayed market price.
- **Limited time period:** Results from the selected historical period may not represent other market conditions.
- **Parameter selection:** Strategy settings may have been chosen after observing the historical data, creating overfitting risk.
- **Data quality:** Missing prices or changes in Yahoo Finance data may affect results.
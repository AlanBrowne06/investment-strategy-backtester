# Investment Strategy Backtester

A Python project for backtesting and evaluating investment strategies using historical US stock market data.

## Overview

This project provides a framework for testing investment strategies on historical market data. Strategies are assigned to portfolios which track their value, returns and holdings over time.

The project also provides tools for analysing strategy performance and comparing results against the SPY ETF benchmark.

## How It Works

The project:

1. Downloads historical stock prices using `yfinance`.
2. Converts daily price data into weekly prices and returns.
3. Runs different investment strategies on the historical data.
4. Tracks portfolio value, returns, dates and holdings.
5. Accounts for estimated transaction costs based on portfolio turnover.
6. Calculates performance and risk metrics.
7. Compares strategies against SPY.
8. Uses in-sample parameter selection and out-of-sample testing to compare the strategies against SPY.

## Strategies

### Random Selection

Randomly selects `n` stocks each week and equally weights them.

This acts as a simple baseline strategy for comparison. A fixed portfolio size of 20 stocks is used in the final out-of-sample comparison.

### Biggest Growers

Selects the `n` stocks with the highest return during the previous week and holds them for the following week.

Only information available before the investment period is used when selecting stocks.

### Momentum

Ranks stocks based on their performance over a configurable lookback period of `t` weeks.

The strategy:

1. Calculates each stock's return over the previous `t` weeks.
2. Ranks the stocks by momentum.
3. Selects the top `n` stocks.
4. Equally weights the selected stocks.
5. Holds the portfolio for one week before recalculating momentum.

Both the lookback period `t` and number of stocks `n` can be changed.

### Mean Reversion

Ranks stocks based on their performance over a configurable lookback period of `t` weeks.

The strategy selects the `n` stocks with the weakest performance over the previous `t` weeks, based on the idea that recent underperformers may subsequently revert toward their longer-term average.

The selected stocks are equally weighted and held for one week before the portfolio is updated.

## Portfolio

The `Portfolio` class tracks:

- Portfolio value
- Historical portfolio values
- Weekly returns
- Dates
- Stocks held
- Transaction costs

Portfolio value is updated each week based on the return of the strategy after estimated transaction costs.

## Transaction Costs

A simplified transaction cost model is included.

The default transaction cost is:

`0.001`, or 0.1% of the value traded.

Portfolio turnover is calculated based on changes in holdings between periods. Both purchases and sales are included when calculating turnover.

This provides a more realistic estimate of strategy performance than assuming trading is completely free.

## Performance Analysis

The `Analysis` class calculates:

- Total return
- Annualised return
- Annualised volatility
- Sharpe ratio
- Maximum drawdown

It can also plot portfolio value over time and compare a strategy against SPY.

## Methodology

Historical data is divided into an in-sample training period and an out-of-sample testing period.

- **Training period:** 2021-2024
- **Out-of-sample period:** 2025

Strategy parameters are selected using only the training period.

The selected parameters are then fixed before evaluating each strategy on the out-of-sample period. This helps reduce the risk of selecting parameters simply because they performed well across the entire historical dataset.

### Parameter Selection

Strategy parameters are selected using the Sharpe ratio as the primary selection criterion.

For Momentum and Mean Reversion, combinations of lookback periods and portfolio sizes are tested jointly. This allows interactions between the two parameters to be considered rather than selecting them independently.

For Biggest Growers, different portfolio sizes are tested.

The selected parameters are:

- **Momentum:** 20-week lookback, 1 stock
- **Biggest Growers:** 2 stocks
- **Mean Reversion:** 8-week lookback, 15 stocks

The Random Selection strategy uses a fixed portfolio size of 20 stocks and acts as a diversified baseline rather than having its parameters optimised.

These parameters are fixed before evaluation on the previously unseen 2025 data.

## Out-of-Sample Results

The strategies were evaluated on the 2025 out-of-sample period using parameters selected only from the 2021-2024 training period.

| Metric | Random Selection | Biggest Growers | Mean Reversion | Momentum | SPY |
| --- | ---: | ---: | ---: | ---: | ---: |
| Total Return | 4.21% | 43.58% | 17.69% | 2.07% | 15.95% |
| Annualised Return | 4.14% | 42.78% | 17.39% | 2.04% | 15.69% |
| Annualised Volatility | 15.52% | 28.62% | 20.57% | 40.06% | 17.16% |
| Sharpe Ratio | 0.338 | 1.381 | 0.879 | 0.249 | 0.932 |
| Maximum Drawdown | -16.61% | -18.91% | -16.37% | -33.21% | -16.88% |

The Biggest Growers strategy produced the strongest out-of-sample performance, returning approximately 43.6% with a Sharpe ratio of 1.38.

Mean Reversion returned approximately 17.7%, slightly exceeding SPY's return of approximately 16.0%. However, SPY achieved a higher Sharpe ratio, indicating stronger risk-adjusted performance.

Momentum performed poorly out of sample despite producing strong results during the training period. It returned approximately 2.1%, with annualised volatility of approximately 40.1% and a maximum drawdown of approximately 33.2%.

Random Selection returned approximately 4.2% and underperformed SPY and the two better-performing systematic strategies.

The difference between the in-sample and out-of-sample Momentum results demonstrates the importance of evaluating strategies on unseen data.

The out-of-sample period covers only one year, so these results should not be interpreted as evidence that the strategies will continue to perform similarly in the future.

## Project Structure

- `market_data.py` - downloads and prepares historical market data.
- `portfolio.py` - contains the `Portfolio` and `Analysis` classes.
- `strategies.py` - contains the investment strategies.
- `main.ipynb` - runs the backtests, performs parameter selection and analyses the results.

## Requirements

- Python 3
- NumPy
- pandas
- yfinance
- matplotlib

## Limitations and Potential Biases

The backtester is a simplified model of real-world investing and has several limitations:

- **Survivorship bias:** The stock universe is based on companies known today rather than the historical constituents of an index at each point in time.
- **Transaction costs:** A simplified proportional transaction cost is included, but bid-ask spreads, taxes and market impact are not explicitly modelled.
- **Equal weighting:** Selected stocks are assumed to receive equal portfolio allocations.
- **Fractional shares:** The backtester effectively assumes that fractional shares can be purchased.
- **Liquidity:** Trades are assumed to be executable at the available market price.
- **Historical period:** The backtest covers a limited historical period and may not represent performance under different market conditions.
- **Out-of-sample period:** The out-of-sample test covers only 2025, so the results are based on a relatively short unseen period.
- **Parameter selection:** Although out-of-sample testing is used, selecting the best parameters from many historical combinations can still introduce overfitting.
- **Stock universe:** The selected universe consists primarily of large US companies and does not represent the entire investable market.
- **Portfolio concentration:** Some parameter combinations, particularly the selected Momentum portfolio, may result in highly concentrated portfolios.
- **Turnover model:** Portfolio turnover is estimated from changes in equal-weighted holdings and does not fully model portfolio weight drift or rebalancing.
- **Data quality:** Missing or inaccurate historical data may affect results.

## Future Improvements

Possible improvements include:

- Using historical index constituents to reduce survivorship bias.
- Testing over a longer historical period.
- Using rolling or walk-forward out-of-sample testing.
- Modelling bid-ask spreads and other trading costs.
- Adding additional investment strategies.
- Adding alternative benchmarks.
- Testing different portfolio weighting methods.
- Improving portfolio turnover calculations.
- Testing strategies across different market regimes.
- Adding portfolio optimisation methods such as Modern Portfolio Theory.
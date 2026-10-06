import pandas as pd
import statistics as st
import matplotlib.pyplot as plt

from market_data import spy_returns


# Tracks the value, returns and holdings of an investment strategy.
class Portfolio:
    def __init__(self, starting_value=1, name="Input Name", transaction_cost=0.001):
        self.value = starting_value
        self.values = []              # History of portfolio values.
        self.dates = []               # Dates corresponding to each portfolio value.
        self.returns = []             # Net returns earned by the portfolio.
        self.name = name
        self.stocks_held = []         # History of stocks held during each period.
        self.transaction_cost = transaction_cost

    # Records the initial value and starting date of the portfolio.
    def start(self, date):
        self.values.append(self.value)
        self.dates.append(date)

    # Calculates portfolio turnover when moving from the previous holdings
    # to a new set of equally weighted holdings.
    def turnover(self, new_holdings):
        turnover = 0

        # The initial investment requires buying the entire portfolio.
        if len(self.stocks_held) == 0:
            return 1

        # Counts stocks entering the portfolio.
        for holding in new_holdings:
            if holding not in self.stocks_held[-1]:
                turnover += 1

        # Multiplied by two to account for both purchases and sales.
        turnover = turnover / len(new_holdings) * 2
        return turnover

    # Updates the portfolio after one investment period.
    def update(self, current_return, date, holdings=None):
        self.dates.append(date)

        # Applies transaction costs when the strategy has specified holdings.
        if holdings != None:
            turnover = self.turnover(holdings)
            cost = turnover * self.transaction_cost
            net_return = current_return - cost
        else:
            net_return = current_return

        self.stocks_held.append(holdings)
        self.returns.append(net_return)
        self.value = self.value * (1 + net_return)
        self.values.append(self.value)


# Calculates performance and risk statistics for one or more portfolios.
class Analysis:
    def __init__(self, portfolios):
        self.portfolios = portfolios

    # Calculates the total return from the start to the end of each portfolio.
    def total_return(self):
        names = []
        returns = []

        for portfolio in self.portfolios:
            names.append(portfolio.name)
            returns.append(portfolio.values[-1] / portfolio.values[0] - 1)

        return pd.Series(returns, index=names)

    # Calculates the annualised return of each portfolio.
    def annualised_return(self):
        names = []
        returns = []

        for portfolio in self.portfolios:
            names.append(portfolio.name)

            # Converts the length of the backtest from days to years.
            delta = portfolio.dates[-1] - portfolio.dates[0]
            years = delta.days / 365.25

            ret = (portfolio.values[-1] / portfolio.values[0]) ** (1 / years) - 1
            returns.append(ret)

        return pd.Series(returns, index=names)

    # Calculates the standard deviation of portfolio returns.
    def volatility(self, annualised=True):
        names = []
        stdevs = []

        for portfolio in self.portfolios:
            names.append(portfolio.name)
            var = st.variance(portfolio.returns)

            # Weekly volatility is annualised using 52 periods per year.
            if annualised:
                stdevs.append((var * 52) ** (1 / 2))
            else:
                stdevs.append(var ** (1 / 2))

        return pd.Series(stdevs, index=names)

    # Calculates the annualised Sharpe ratio of each portfolio.
    def sharpe(self, risk_free_rate=0):
        names = []
        sharpes = []
        for portfolio in self.portfolios:
            names.append(portfolio.name)

            # Converts the annual risk-free rate to a weekly rate.
            weekly_rf = (1 + risk_free_rate) ** (1 / 52) - 1
            excess_returns = [r - weekly_rf for r in portfolio.returns]
            sharpe = (st.mean(excess_returns) / st.stdev(excess_returns) * (52 ** 0.5))
            sharpes.append(sharpe)

        return pd.Series(sharpes, index=names)

    # Calculates the largest percentage decline from a previous portfolio peak.
    def max_drawdown(self):
        names = []
        drawdowns = []

        for portfolio in self.portfolios:
            names.append(portfolio.name)

            values = pd.Series(portfolio.values)
            cummax = values.cummax()
            drawdown = values / cummax - 1

            drawdowns.append(min(drawdown))

        return pd.Series(drawdowns, index=names)

    # Combines the main performance measures into a single table.
    def summary(self):
        data = pd.DataFrame({
            "Total Return": self.total_return(),
            "Annualised Return": self.annualised_return(),
            "Volatility": self.volatility(),
            "Sharpe Ratio": self.sharpe(),
            "Max Drawdown": self.max_drawdown()
        })

        return data

    # Plots portfolio values over time, optionally including SPY as a benchmark.
    def plot(self, benchmark=True):
        for portfolio in self.portfolios:
            plt.plot(
                portfolio.dates,
                portfolio.values,
                label=portfolio.name
            )

        if benchmark:
            bench = self.benchmark(self.portfolios[0])
            plt.plot(
                bench.dates,
                bench.values,
                label=bench.name
            )

        plt.legend()
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title("Strategy Comparison")
        plt.show()

    # Creates a buy-and-hold SPY portfolio over the same period as a given portfolio.
    def benchmark(self, portfolio):
        benchmark = Portfolio(portfolio.values[0], "SPY")

        start = portfolio.dates[0]
        benchmark.start(start)

        for day in portfolio.dates[1:]:
            benchmark.update(spy_returns.loc[day, "SPY"], day)

        return benchmark
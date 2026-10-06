import numpy as np

from market_data import weekly, weekly_returns
from portfolio import Portfolio


# Strategy 1: randomly selects n stocks each week.
def random_stock_selection(
    n=1,
    w=1,
    name="Random Choice",
    transaction_cost=0.001,
    start=None,
    end=None
):
    # The first available weekly return is at index 1.
    if start == None:
        start = 1

    if end == None:
        end = len(weekly)

    portfolio = Portfolio(w, name, transaction_cost)
    portfolio.start(weekly.index[start - 1])

    for i in range(start, end):
        current_week = weekly_returns.iloc[i].dropna()

        # Randomly selects n stocks from those with available return data.
        stocks = np.random.choice(
            current_week.index,
            size=n,
            replace=False
        )

        current_return = current_week[stocks].mean()

        portfolio.update(
            current_return,
            weekly.index[i],
            holdings=list(stocks)
        )

    return portfolio


# Strategy 2: invests in the n stocks with the highest return during the previous week.
def biggest_growers(
    n=3,
    w=1,
    name="Simple Momentum",
    transaction_cost=0.001,
    start=None,
    end=None
):
    # Two weeks of data are required before the first investment return.
    if start == None:
        start = 2

    if end == None:
        end = len(weekly)

    portfolio = Portfolio(w, name, transaction_cost)
    portfolio.start(weekly.index[start - 1])

    for i in range(start, end):
        # Uses the previous week's returns to select stocks.
        previous_week = weekly_returns.iloc[i - 1].dropna()

        top_stocks = previous_week.sort_values(
            ascending=False
        ).head(n).index

        # Earns the selected stocks' returns during the current week.
        current_return = weekly_returns.iloc[i][top_stocks].mean()

        portfolio.update(
            current_return,
            weekly.index[i],
            holdings=list(top_stocks)
        )

    return portfolio


# Strategy 3: invests in the n stocks with the highest momentum over the previous t weeks.
def momentum_strat(
    t=4,
    n=3,
    w=1,
    name="Momentum",
    transaction_cost=0.001,
    start=None,
    end=None
):
    # Enough historical data must be available to calculate the momentum signal.
    if start == None:
        start = t + 1

    if end == None:
        end = len(weekly)

    portfolio = Portfolio(w, name, transaction_cost)
    portfolio.start(weekly.index[start - 1])

    for i in range(start, end):
        # Uses only prices available before the current investment week.
        last_price = weekly.iloc[i - t - 1]
        recent_price = weekly.iloc[i - 1]

        momentum = (recent_price - last_price) / last_price

        # Selects the n stocks with the highest historical momentum.
        top_stocks = momentum.dropna().sort_values(
            ascending=False
        ).head(n).index

        # Earns the selected stocks' returns during the current week.
        current_return = weekly_returns.iloc[i][top_stocks].mean()

        portfolio.update(
            current_return,
            weekly.index[i],
            holdings=list(top_stocks)
        )

    return portfolio


# Strategy 4: invests in the n worst-performing stocks over the previous t weeks.
def mean_reversion(
    t=4,
    n=3,
    w=1,
    name="Mean Reversion",
    transaction_cost=0.001,
    start=None,
    end=None
):
    # Enough historical data must be available to calculate past performance.
    if start == None:
        start = t + 1

    if end == None:
        end = len(weekly)

    portfolio = Portfolio(w, name, transaction_cost)
    portfolio.start(weekly.index[start - 1])

    for i in range(start, end):
        # Uses only prices available before the current investment week.
        last_price = weekly.iloc[i - t - 1]
        recent_price = weekly.iloc[i - 1]

        past_return = (recent_price - last_price) / last_price

        # Selects the n stocks with the lowest historical returns.
        bottom_stocks = past_return.dropna().sort_values(
            ascending=True
        ).head(n).index

        # Earns the selected stocks' returns during the current week.
        current_return = weekly_returns.iloc[i][bottom_stocks].mean()

        portfolio.update(
            current_return,
            weekly.index[i],
            holdings=list(bottom_stocks)
        )

    return portfolio
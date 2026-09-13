from market_data import close, spy_weekly
import numpy as np
import matplotlib.pyplot as plt

# Strategy 1: pick random stocks each period
def random_stock_selection(n=1):
    weekly = close.resample("W-FRI").last()
    weekly_returns = weekly.pct_change()
    value = 1
    values = [1]
    for i in range(1, len(weekly_returns)):
        current_week = weekly_returns.iloc[i].dropna()
        stocks = np.random.choice(
            current_week.index,
            size=n,
            replace=False
        )

        current_return = current_week[stocks].mean()

        value = value * (1 + current_return)
        values.append(value)

    return values

#Strategy 2: look at the biggest growers each week and invest in them
def biggest_growers(n=3):
    value = 1
    values = [1]
    for i in range(2, len(weekly_returns)):
        previous_week = weekly_returns.iloc[i-1].dropna()
        top_stocks = previous_week.sort_values(ascending=False).head(n).index
        current_return = np.mean(weekly_returns.iloc[i][top_stocks])
        value = value * (1 + current_return)
        values.append(value)
    return(values)

#Strategy 3: Momentum of the top n stoscks over the last t weeks
def momentum_strat(t=4,n=3):
    value = 1
    values = [1]
    for i in range(t+1, len(weekly)):
        past_price = weekly.iloc[i-t-1]
        recent_price = weekly.iloc[i-1]
        momentum = (recent_price - past_price)/past_price
        top_stocks = momentum.dropna().sort_values(ascending=False).head(n).index
        current_return = weekly_returns.iloc[i][top_stocks].mean()
        value = value*(1 + current_return)
        values.append(value)
    return  values


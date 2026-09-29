from tkinter.font import names

import pandas as pd
from matplotlib.pyplot import xlabel
from scipy.linalg.interpolative import interp_decomp

from market_data import close, spy_weekly, weekly, weekly_returns
import numpy as np
import statistics as st
import matplotlib.pyplot as plt

#A class called portfolio
class Portfolio:
    def __init__(self,starting_value=1, name="Input Name"):
        self.value = starting_value
        self.values = []
        self.dates = []
        self.returns = []
        self.name = name

    def start(self, date):
        self.values.append(self.value)
        self.dates.append(date)

    def update(self,current_return,date):
        self.returns.append(current_return)
        self.value=self.value * (1+current_return)
        self.values.append(self.value)
        self.dates.append(date)

class Analysis:
    def __init__(self,portfolios):
        self.portfolios = portfolios

    def total_return(self):
        names = []
        returns = []
        for portfolio in self.portfolios:
            names.append(portfolio.name)
            returns.append(portfolio.values[-1]/portfolio.values[0] - 1)
        return pd.Series(returns,index=names)

    def annualised_return(self):
        names = []
        returns = []
        for portfolio in self.portfolios:
            names.append(portfolio.name)
            delta = portfolio.dates[-1] - portfolio.dates[0]
            years = delta.days/365.25
            ret = (portfolio.values[-1]/portfolio.values[0])**(1/years) - 1
            returns.append(ret)
        return pd.Series(returns,index=names)

    def volatility(self,annualised=True):
        names = []
        stdevs = []
        for portfolio in self.portfolios:
            names.append(portfolio.name)
            var = st.variance(portfolio.returns)
            if annualised:
                stdevs.append((var*52)**(1/2) )
            else:
                stdevs.append((var)**(1/2))
        return pd.Series(stdevs,index = names)

    def sharpe(self,risk_free_rate=0):
        names = []
        sharpes = []
        for portfolio in self.portfolios:
            sharpes.append((Analysis([portfolio]).annualised_return().iloc[0] - risk_free_rate)/Analysis([portfolio]).volatility().iloc[0])
            names.append(portfolio.name)
        return pd.Series(sharpes, index=names)

    def max_drawdown(self):
        names = []
        drawdowns = []
        for portfolio in self.portfolios:
            names.append(portfolio.name)
            values = pd.Series(portfolio.values)
            cummax = values.cummax()
            drawdown = values/cummax - 1
            drawdowns.append(min(drawdown))
        return pd.Series(drawdowns,index=names)

    def summary(self):
        data = pd.DataFrame({
            "Total Return": self.total_return(),
            "Annualised Return" : self.annualised_return(),
            "Volatility": self.volatility(),
            "Sharpe Ratio": self.sharpe(),
            "Max Drawdown": self.max_drawdown()
        })
        return data

    def plot(self):
        for portfolio in self.portfolios:
            plt.plot(portfolio.dates,portfolio.values,label=portfolio.name)
        plt.legend()
        plt.xlabel("Date")
        plt.yabel("Value")
        plt.title("Strategy Comparison")




# Strategy 1: pick random stocks each period
def random_stock_selection(n=1,w=1,name="Random Choice"):
    portfolio = Portfolio(w,name)
    portfolio.start(weekly.index[0])

    for i in range(1, len(weekly_returns)):
        current_week = weekly_returns.iloc[i].dropna()
        stocks = np.random.choice(
            current_week.index,
            size=n,
            replace=False
        )
        current_return = current_week[stocks].mean()
        portfolio.update(current_return, weekly.index[i])
    return portfolio


#Strategy 2: look at the biggest growers each week and invest in them
def biggest_growers(n=3,w=1,name="Simple Momentum"):
    portfolio = Portfolio(w,name)
    portfolio.start(weekly.index[1])

    for i in range(2, len(weekly_returns)):
        previous_week = weekly_returns.iloc[i-1].dropna()
        top_stocks = previous_week.sort_values(ascending=False).head(n).index
        current_return = np.mean(weekly_returns.iloc[i][top_stocks])
        portfolio.update(current_return,weekly.index[i])
    return portfolio

#Strategy 3: Momentum of the top n stoscks over the last t weeks
def momentum_strat(t=4,n=3, w=1, name = "Momentum"):

    portfolio = Portfolio(w,name) #init a portfolio class with value w
    portfolio.start(weekly.index[t]) #Start tracking wealth and dates
    for i in range(t+1, len(weekly)):
        last_price = weekly.iloc[i-t-1]
        recent_price = weekly.iloc[i-1]
        momentum = (recent_price - last_price)/last_price

        top_stocks = momentum.dropna().sort_values(ascending=False).head(n).index
        current_return = weekly_returns.iloc[i][top_stocks].mean()
        portfolio.update(current_return,weekly.index[i])
    return(portfolio)

#A fun
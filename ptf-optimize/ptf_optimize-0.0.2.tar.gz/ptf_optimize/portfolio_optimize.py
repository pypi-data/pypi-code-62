import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader as web
from datetime import date, timedelta

class portfolio:
    def __init__(self, tickers, start = date.today() - timedelta(days=5*365) , end=date.today()):
        
        '''
        input:
            tickers: a list of stock tickers to be included in the portfolio
            start: desired start date, default date is 5 years ago
            end : end date, default date is today

        return:
            means: annualized mean return of each stock
            cov_matrix: annualized covariance matrix between the stocks
        '''
        self.tickers = tickers
        # get stock price from yahoo finance
        multpl_stocks = web.get_data_yahoo(tickers,  start = start, end = end)

        # get the monthly return value of each stock
        #multpl_stock_monthly_returns = multpl_stocks['Adj Close'].resample('M').ffill().pct_change()

        #daily
        multpl_stock_daily_returns = multpl_stocks['Adj Close'].pct_change()
        self.means = multpl_stock_daily_returns.mean() * 252
        self.cov_matrix = multpl_stock_daily_returns.cov() * 252

        # annualized mean return of each stock
        #means = multpl_stock_monthly_returns.mean()

        # annualized covariance matrix between the stocks
        #cov_matrix = multpl_stock_monthly_returns.cov() 

        

    ##  equal allocation portfolio
    def equal_allocation(self):
        n = len(self.means)
        weights=np.ones(n)* 1/ n
        self.get_portfolio_stats( weights )
        return weights

    ##  minimum risk portfolio
    def min_risk(self):
        ones = np.ones(len(self.means))
        x = np.dot(np.linalg.inv(self.cov_matrix), ones)
        weights= x / sum(x)
        self.get_portfolio_stats( weights )
        return weights

    ##  optimal portfolio, tangency point
    def opt_portfolio(self, Rf=0.005):
        z = np.dot(np.linalg.inv(self.cov_matrix), self.means-Rf)
        weights = z/sum(z)
        self.get_portfolio_stats( weights )
        return weights

    def get_portfolio_stats(self, weights , Rf=0.005):
        # annual return of the portfolio
        R_p = np.dot(weights.T , self.means)

        # annualized portfolio variance
        port_variance = np.dot( weights.T , np.dot(self.cov_matrix, weights))

        # annualized portfolio volatility 
        port_volatility = np.sqrt(port_variance)

        optimal_port_weights = dict(zip(self.tickers, weights))

        for key, value in optimal_port_weights.items():
            print(' {:5} : {:.4f}'.format( key, value))

        #Show the expected annual return, volatility or risk, and variance.
        percent_var = round(port_variance, 4) 
        percent_vols = round(port_volatility, 4) 
        percent_ret = round(R_p, 4)
        sharpe_ratio = round((R_p-Rf)/port_volatility, 4)
        print("Expected annual return : {:.2f}%".format(percent_ret*100))
        print('Annual volatility/standard deviation/risk : {:.2f}%'.format(percent_vols*100))
        print('Annual variance : {:.2f}%'.format(percent_var*100))
        print('Sharpe ratio : {:.2f}'.format(sharpe_ratio) )

    
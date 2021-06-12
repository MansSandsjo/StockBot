# Portfolio Management of OMXS30 using Statistics and Deep Learning

## Overview
The goal of this project is to manage a portfolio of OMX Stockholm 30 stocks using Single-Period Optimization. This is done by collecting price data, cleaning it from outliers,predict future prices and covariance between the stocks and then optimize a portfolio based on this information. By using holding and trading constraints to solve a convex optimization problem,as formulated by Boyd et. al (2007) for each stock during each trading period, the portfolio isre-balanced with the predictions as parameters. How well the predicted returns and covarianceare estimated for the model is measured by calculating the realized Sharpe ratio (SR) & averageturnover. 

![Overview](/report/final/final%20report%20group%20b/Pics/Mod_overview_future.png)

## Predictions
Initial portfolio management is made on simulated stock data and later on historical stock data is instead used during the years 2010-2020 of OMXS 30 closing prices. The methods used in the project to create predictions of future returns are simple moving average, exponential moving averageand Long Short Term Memory. The covariance matrix in use, is either sample covariancematrix or the covariance matrix as formulated by Ledoit & Wolf (2004). With hyperparameteroptimization the parameters are tuned to get the highest score regarding the metrics described above. The best performance achieved, is a Sharpe ratio of 0.33 with a corresponding average turnover of 23.25. 

![results](/report/final/final%20report%20group%20b/Pics/result/LSTM_LW.png)

## Dependencies
Python is the main language for developing the code in this project. The data is gathered from the financial market platform *Investing.com*, which provides historical data on stock prices. To fetch the data, the library InvestPy 1.0.6 is used. For data handling, this project runs the data science library Pandas 1.2.4, for the NN models, Keras 2.4.0 and lastly the convex optimization is handled with CVXPY 1.1.12 and the solver MOSEK 9.2.43. The solver MOSEK is used in the project since it is more efficient in computation than the standard solver in the CVXPY package.


# BTC_regression
Regression analysis to predict BTC price for T+1

The obective of this script is to determine with a regression analysis, whether the price of BTC is going to be higher or lower in average at T+1 (tommorrow). The script feeds itself with the investing.com API (investpy) and generates graphics with plotly express.

sklearn, pandas, numpy and plotly modules are needed. 

When run, the script will get the historical pricing of BTC from 2019-01-01 until today and analyse whether tommorrows average between high and low price will be higher than the current price (close price). 

To test the efficacy of this model I tested it by spliting the data in an 80/20 fashion and benchmarking it against a HODL strategy. The results (BTC_predictions.xlsx) show that the model is pretty good in predicting tendencies in the asset's price, but not predicting the price itself (Average error of: $1566,39 - 3,42%). However, by being able to predict a higher or lower price in T+ and thus going long or short. 

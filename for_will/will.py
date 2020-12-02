from get_all_tickers import get_tickers as gt
import pandas as pd

# tickers = gt.get_tickers()

# print(type(tickers))
# print(len(tickers))

# df = gt.__exchange2df('nyse')
# df = df.append(gt.__exchange2df('nasdaq'))
# df = df.append(gt.__exchange2df('amex'))
# # df.to_csv('test.csv')

# for key in [gt.Region.EUROPE , gt.Region.ASIA , 
# gt.Region.AUSTRALIA_SOUTH_PACIFIC , gt.Region.CARIBBEAN , 
# gt.Region.SOUTH_AMERICA, gt.Region.MIDDLE_EAST, 
# gt.Region.NORTH_AMERICA]:

# 	ticklist = gt.get_tickers_by_region(key)
# 	print(len(ticklist))


ticklist = gt.get_tickers_by_region(gt.Region.CARIBBEAN)
print(len(ticklist))

ticklist = gt.get_tickers_by_region(gt.Region.NORTH_AMERICA)
print(len(ticklist))


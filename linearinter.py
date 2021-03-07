import numpy as np
import pandas as pd 
from scipy import interpolate, stats
import matplotlib.pyplot as plt
import math 
eca = pd.read_csv('F26_ECa_Dualem_2013.txt', sep='\t')[:-3]
elevation = pd.read_csv('F26_Elevation_RTK_2013.txt', sep = '\t')[:-3]
Yield = pd.read_csv('F26_Yield_Soybeans_2014.txt', sep = '\t')

Yield = Yield.reindex(columns=['Longitude', 'Latitude', 'Yield', 'Moisture'])

new_elevation = interpolate.griddata(elevation.iloc[:,:2], elevation.iloc[:,3], eca.iloc[:,:2], method='linear')
new_yield = interpolate.griddata(Yield.iloc[:,:2], Yield.iloc[:,2], eca.iloc[:,:2], method='linear')

new_yield = [0 if math.isnan(x) else x for x in new_yield]
new_eca = eca.iloc[:,3]
new_eca = [0 if math.isnan(x) else x for x in new_eca]
new_elevation = [0 if math.isnan(x) else x for x in new_elevation]

slope, intercept, r_value, p_value, std_err = stats.linregress(new_eca, new_yield)
print(slope, intercept, r_value, p_value, std_err)
slope, intercept, r_value, p_value, std_err = stats.linregress(new_elevation, new_yield)
print(slope, intercept, r_value, p_value, std_err)
slope, intercept, r_value, p_value, std_err = stats.linregress(new_elevation, new_eca)
print(slope, intercept, r_value, p_value, std_err)
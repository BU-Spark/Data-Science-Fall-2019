import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
#import statsmodels.api as sm
import plotly.express as px
import seaborn as sns

train = pd.read_csv("pc_spark.csv")
train.info()
train.dropna(subset = ["ls_price_pc"], inplace = True)
train = train[train["ls_price_pc"] >10]
#train.drop(train["ls_price_pc"]<10, inplace = True)
columns_todrop = ["f_year","p_prot_2000_5000", "p_prot_1990_5000","gisjoin", "pid", "p_f", "lid", "e_year", #"csd_id", 
"fips", "ls_date_pc", "owner_pc", "f_orgtype", "lake_frontage", "pop_dens_bg_1990", "pop_dens_bg_2000",
 "pop_dens_bg_2006-2010", "pop_dens_tract_1990", "pop_dens_tract_2000", "pop_dens_tract_2006-2010", "hh_inc_med_bg_1990", 
 "hh_inc_med_bg_2000","hh_inc_med_bg_2006-2010", "hh_inc_med_tract_1990", "hh_inc_med_tract_2000", "hh_inc_med_tract_2006-2010", 
 "hh_inc_avg_bg_1990", "hh_inc_avg_bg_2000", "hh_inc_avg_bg_2006-2010", "hh_inc_avg_tract_1990", "hh_inc_avg_tract_2000", "hh_inc_avg_tract_2006-2010", "e_orgtype"]

#train.drop(columns = columns_todrop, inplace = True)
train.fillna(0, inplace = True)
train.to_csv("train.csv")
y = train["ls_price_pc"].tolist()
X = train.drop(columns = ["ls_price_pc"])
X_train, X_test, y_train, y_test  = train_test_split(X,y,test_size=0.2)
regression_model = []
model_include = ["p_water","river_frontage", "p_forest_m","slope", "p_dev_open","p_dev_medium","lake_importance","p_forest_e","ha","p_dev_high","csd_id",
"travel","p_dev_low","p_wetland_w","p_grassland","p_wetland_e","p_pasture","p_e","p_forest_d",  "p_barren","p_crops","p_wet",
"pop_dens_bg_2012-2016","hh_inc_med_bg_2012-2016","hh_inc_avg_bg_2012-2016"] 
# "hh_inc_med_bg_2012-2016","hh_inc_avg_bg_2012-2016" add interaction
include = train.loc[:,model_include]
y = train.loc[:,["ls_price_pc"]].values.tolist()
y = np.log(y)
#distribution
# sns.set(color_codes=True)
# for x_col in model_include:
#     x = train.loc[:,[x_col]]
#     x = x.drop(x[x[x_col] ==0].index)
#     x_l = x[x_col].tolist()
#     sns.distplot(x_l)
#     plt.xlabel(x_col)
#     plt.ylabel('Frequency')
#     plt.show()

#2d plot between y and x
# for x_idx in range(len(model_include)):
#     x_col = model_include[x_idx]
#     x = train.loc[:,[x_col]]
#     x.insert(1,"ls_price_pc",y)
#     x = x.drop(x[x[x_col] ==0].index)
#     x_l = x[x_col].tolist()
#     #x_l = np.log(x_l)
#     #plt.subplot(4,3,x_idx+1)
#     plt.scatter(x_l, x["ls_price_pc"].tolist())
#     plt.xlabel(x_col)
#     plt.ylabel('log(ls_price_pc)')
#     plt.show()
    # plt.tight_layout()

#large correlation scatter plot
# plt.scatter(train["p_dev_medium"].tolist(), train["p_wetland_w"].tolist())
# plt.xlabel("p_dev_medium")
# plt.ylabel('p_wetland_w')
# plt.show()

#Correlation Matrix
# plt.figure(figsize=(12, 7))
# sns.heatmap(include.corr(), annot = True)
# plt.yticks(rotation=0) 
# plt.xticks(rotation = 45)
# plt.show()
# 'RdBu_r' & 'BrBG' are other good diverging colormaps

#scatterplot matrix
# fig = px.scatter_matrix(include.values.tolist())
# fig.show()

#linear regression
# reg = LinearRegression()
# reg.fit(X_train, y_train)
# print(reg.intercept_)
# print(reg.coef_)
# model = sm.OLS(Y,X)
# results = model.fit()
# model.summary()




data.info()
# print(data.describe)
# print(data.shape)


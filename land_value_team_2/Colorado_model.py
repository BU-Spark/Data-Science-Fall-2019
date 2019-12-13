import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
from sklearn.linear_model import LinearRegression,Lasso
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split, KFold
import matplotlib.pyplot as plt
import statsmodels.api as sm
import plotly.express as px
from statsmodels.tools.eval_measures import rmse
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import AdaBoostRegressor
from sklearn.preprocessing import OneHotEncoder
import pickle

#taking train and test set
# X_train = pd.read_csv("X_train.csv")
# y_train = pd.read_csv("y_train.csv")
# X_test = pd.read_csv("X_test.csv")
# y_test = pd.read_csv("y_test.csv")
# full_train = pd.read_csv("full_train.csv")
# model_include = ["pop_dens_tract","travel", "p_dev_medium","year","slope","hh_inc_avg_tract","p_grassland", "p_dev_low", "p_wet","p_shrub","p_dev_open","p_crops" ,"fips","p_prot_2010_5000","pop_dens_bg"] #,"p_prot_2010_5000","pop_dens_bg"
# y = full_train["log_price_per_ha"]
# X_include = full_train.loc[:,model_include]
# X_train, X_test, y_train, y_test = train_test_split(X_include,y,test_size=0.3)
# print(X_train.shape)
# print(y_train.shape)

#variables in model + Linear Regression
# model_include = ["river_frontage", "slope", "p_dev_medium", "p_dev_high", "flips", "travel", "pop_dens_bg_2012-2016", "hh_inc_avg_bg_2012-2016","hh_inc_med_bg_2012-2016", "year", "lake_frontage", "p_wet"]
# model_include = ["p_dev_medium", "year", "pop_dens_tract_2012-2016", "travel", "slope", "p_wet", "p_dev_open", "p_shrub","p_dev_low", "p_prot_2010_5000", "p_grassland", "p_crops","hh_inc_avg_bg_2012-2016","pop_dens_bg_2012-2016","p_pasture","fips"]

# X_include = X_train.loc[:,model_include]
# X_include.fillna(0, inplace = True)
# X_include["flips"] = X_include["flips"].astype(int)
# # print(X_include.isna().sum())
# y = y_train["log_price_per_ha"]
# LRmodel = sm.OLS(y_train, sm.add_constant(X_train)).fit()
# # print(LRmodel.summary())

# X_test_include = X_test.loc[:,model_include]
# X_test_include.fillna(0, inplace = True)
# X_test_include["flips"] = X_test_include["flips"].astype(int)

# y_pred = LRmodel.predict(sm.add_constant(X_test))
# lr_mae = mean_absolute_error(y_test, y_pred)
# print(lr_mae)

#Gradient Boosting
# GBmodel = GradientBoostingRegressor()
# GBmodel = GBmodel.fit(X_train , y_train)
# y_gb = GBmodel.predict(X_test)
# gb_mae = mean_absolute_error(y_test, y_gb)
# print(gb_mae)

#Random Forest
# n = 50 
# while n <= 500:
#     RFmodel = RandomForestRegressor(n_estimators = n)#tested for n from 100 to 500 with 50 as increment
#     RFmodel = RFmodel.fit(X_train , y_train)
#     # dot_data = export_graphviz(RFmodel, out_file='tree.dot') 
#     y_rf = RFmodel.predict(X_test)
#     rf_mae = mean_absolute_error(y_test, y_rf)
#     print(rf_mae)
#     n += 50

# md = [5,10,15,20,21,22,23,24,25]
# for m in md:
#     RFmodel = RandomForestRegressor(n_estimators = 300, max_depth = m)#tested for n from 100 to 500 with 50 as increment
#     RFmodel = RFmodel.fit(X_train , y_train)
#     # dot_data = export_graphviz(RFmodel, out_file='tree.dot') 
#     y_rf = RFmodel.predict(X_test)
#     rf_mae = mean_absolute_error(y_test, y_rf)
#     print(rf_mae)

#n_estimators result plot
# labels = ['n = 100', 'n = 150', 'n = 200', 'n = 250', 'n = 300', 'n = 350','n = 400']
# maeList = [0.8746061989271654,0.8713413087286276,0.8705100144932456,0.8703133688403654,0.8700508268405899,0.8700653377616293,0.8702729019845137]
# plt.plot(labels, maeList)
# plt.xticks(rotation=45)
# #plt.xlabel(labels)
# plt.show()

#AdaBoost
# ABmodel = AdaBoostRegressor(base_estimator = RandomForestRegressor(),n_estimators=20)
# ABmodel = ABmodel.fit(X_train , y_train)
# y_ab = ABmodel.predict(X_test)
# ab_mae = mean_absolute_error(y_test, y_ab)
# print(ab_mae)

# #Extra Tree
# ETmodel = ExtraTreesRegressor()
# ETmodel = ETmodel.fit(X_train , y_train)
# y_et = ETmodel.predict(X_test)
# et_mae = mean_absolute_error(y_test, y_rf)
# print(et_mae)

# maeList = [1.2129580035183372, 0.983006838721895,0.8667471260449512,0.873602916714172,0.8667471260449512]

# print(RFmodel.feature_importances_)
# pickle.dump(RFmodel, open(wf("model.p")), "wb")

#taking the full dataset 
full_train = pd.read_csv("full_train.csv")
full_train ["fips"] = full_train ["fips"].astype(int)
# full_train.info()
# #variable from linear regression
# model_include = ["river_frontage", "slope", "p_dev_medium", "p_dev_high", "fips", "travel", "pop_dens_bg_2012-2016", "hh_inc_avg_bg_2012-2016","hh_inc_med_bg_2012-2016", "year", "lake_frontage", "p_wet"]
# #variable selected based on feature importance
# model_include = ["p_dev_medium", "year", "pop_dens_tract_2012-2016", "travel", "slope", "p_wet", "p_dev_open", "p_shrub","p_dev_low", "p_prot_2010_5000", "p_grassland", "p_crops","hh_inc_avg_bg_2012-2016","pop_dens_bg_2012-2016","p_pasture","fips"]
# #variable selected based on feature importance after combining year for pop_dens and hh_inc
model_include = ["pop_dens_tract","travel", "p_dev_medium","year","slope","hh_inc_avg_tract","p_grassland", "p_dev_low", "p_wet","p_shrub","p_dev_open","p_crops" ,"fips","p_prot_2010_5000","pop_dens_bg"] #,"p_prot_2010_5000","pop_dens_bg"

# train_include = full_train.loc[:,model_include]
# train_include.fillna(0, inplace = True)
# train_include["fips"] = train_include["fips"].astype(int)
# full_y = full_train["log_price_per_ha"]
# full_X = train_include

# feature selection in random forest
# X = full_train.drop(columns = ["log_price_per_ha", "csd_id", 'pid','gisjoin', 'ha','lid','f_orgtype','owner_pc','ls_date_pc','e_orgtype','ls_price_pc', 'Unnamed: 0'])
# X.fillna(0, inplace = True)
# names = X.columns
# rf = RandomForestRegressor()
# rf.fit(X, full_y)
# df_imp = pd.DataFrame(names,rf.feature_importances_,columns=['att'])
# df_imp.reset_index(level=0, inplace=True)
# df_imp.rename(columns = {'index':'imp_rate'}, inplace = True) 
# df_imp = df_imp.sort_values(by=['imp_rate'],ascending=False)
# att_list = df_imp['att'].tolist()
# print(df_imp)
# print("Features sorted by their score:")
# print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), reverse=True))



#use one hot encoder, apply dummpy, increase MAE, do not include
# ohe = OneHotEncoder()
# ohe.fit(full_X[["year"]])
# year_array = ohe.transform(full_X[["year"]]).toarray()
# year_df = pd.DataFrame(year_array, columns = [v[3:] for v in ohe.get_feature_names()],index = full_X.index)
# full_Xc = full_X.drop("year", 1).join(year_df.drop("2000.0", 1))

##using KFlod Cross Validation with random forest
# mae = []
# for train_idx, test_idx in KFold(n_splits = 5, shuffle = True).split(full_X):
#     # print("start")
#     X_train, X_test = full_X.iloc[train_idx],full_X.iloc[test_idx]
#     y_train, y_test = full_y.iloc[train_idx],full_y.iloc[test_idx]
#     RFmodel = RandomForestRegressor(n_estimators = 300, max_depth = 20) #tested for n from 100 to 500 with 50 as increment, 300 is the best. tested md, 20 is the best
#     RFmodel = RFmodel.fit(X_train , y_train)
#     y_rf = RFmodel.predict(X_test)
#     rf_mae = mean_absolute_error(y_test, y_rf)
#     print(rf_mae)
#     mae.append(rf_mae)
# print("Mean of MAE",np.mean(mae)) #the mean

#     # Lmodel = Lasso() #lasso
#     # Lmodel = Lmodel.fit(X_train, y_train)
#     # y_l = Lmodel.predict(X_test)
#     # l_mae = mean_absolute_error(y_test, y_l)
#     # print(l_mae)
#     # mae.append(l_mae)

    # LRmodel = sm.OLS(y_train, sm.add_constant(X_train)).fit()
    # print(LRmodel.summary())
    # y_pred = LRmodel.predict(sm.add_constant(X_test))
    # lr_mae = mean_absolute_error(y_test, y_pred)
    # print(lr_mae)

# print("Mean of MAE",np.mean(mae)) #the mean 

#feature selection with easement
full_train = pd.read_csv("full_train.csv")
# noE = full_train[full_train["e_sold"] == 0]
# y_noE = noE["log_price_per_ha"]

# noE = noE.drop(columns = ["log_price_per_ha", "csd_id", 'pid','gisjoin', 'ha','lid','f_orgtype','owner_pc','ls_date_pc','e_orgtype','ls_price_pc','fips', 'Unnamed: 0'])
# noE.fillna(0, inplace = True)
# names = noE.columns
# rf = RandomForestRegressor(n_estimators = 300)
# rf.fit(noE, y_noE)
# print("Features sorted by their score:")
# print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), names), reverse=True))


#Compare with easement 
#use the data without easement to train the model
DofA = []
DofM = []
m = []
noE = full_train[full_train["e_sold"] == 0]
y_noE = noE["log_price_per_ha"]
X_noE = noE.loc[:,model_include]
X_noE.fillna(0,inplace = True)
y_noE = noE["log_price_per_ha"]
# md = 21
# while md <=30:
RFmodel = RandomForestRegressor(n_estimators = 300, max_depth = 22) #tested for n from 100 to 500 with 50 as increment, 300 is the best. tested md, 20 is the best
RFmodel = RFmodel.fit(X_noE , y_noE)
#     #then predict the price for land with easement
print("Fitting Finished",22)
withE = full_train[full_train["e_sold"] != 0]
print(withE.shape)
X_withE = withE.loc[:,model_include]
y_withE = withE["log_price_per_ha"]
y_rf = RFmodel.predict(X_withE)
rf_mae = mean_absolute_error(y_withE, y_rf)
# y_rf = RFmodel.predict(extracted808)
print("MAE:",rf_mae)
m.append(rf_mae)
print("average of log prediction value:", y_rf.mean())
print("average of log actual value:", y_withE.mean())
print("average of original prediction value:", np.exp(y_rf.mean()))
print("average of original actual value:", np.exp(y_withE.mean()))
print("Difference of average:", np.exp(y_rf.mean())-np.exp(y_withE.mean()))
DofA.append(np.exp(y_rf.mean())-np.exp(y_withE.mean()))
print("median of log prediction value:", np.median(y_rf))
print("median of log actual value:", y_withE.median())
print("median of original prediction value:", np.exp(np.median(y_rf)))
print("median of original actual value:", np.exp(y_withE.median()))
print("Difference of median:" , np.exp(np.median(y_rf)) - np.exp(y_withE.median()))
DofM.append(np.exp(np.median(y_rf)) - np.exp(y_withE.median()))
#     md +=1
print("Average: ",DofA)
# print("Median",DofM)
print("MAE",m)
#compare it with the actual price
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

#Data cleaning and preprocessing 
train = pd.read_csv("pc_spark.csv")

#drop entries with missing value in ls_price_pc
train.dropna(subset = ["ls_price_pc"], inplace = True)
#only keep price above 1000
train = train[train["ls_price_pc"] > 1000]
train.fillna(0, inplace = True)
train.info()
#compute y = log($/ha)
train["log_price_per_ha"] = np.log(train["ls_price_pc"]/train["ha"])
#extract year from ls_date_pc, drop any entry with ~
# train = train[train["ls_date_pc"] != "~"]
#print(train[.iloc[700,])
#print(train.ls_date_pc.unique())
train["ls_date_pc"] = train["ls_date_pc"].apply(str)
train = train[~train.ls_date_pc.str.contains("~")]
#train.drop([28862,28863,28866, 28868, 28869], inplace = True)

#train.drop(train.ls_date_pc.str.contains("~"), inplace = True)
year = []
#print(train["ls_date_pc"].dtypes)
for idx, row in train.iterrows():
    #print(row["ls_date_pc"], idx)
    if row["ls_date_pc"] == 0:
        year.append("0")
    elif "/" in row["ls_date_pc"]:
        #print(row["ls_date_pc"], "0")
        row["ls_date_pc"] = pd.to_datetime(row["ls_date_pc"],errors = "coerce")
        #pd.DatetimeIndex(row['ls_date_pc']).year  
        year.append(row['ls_date_pc'].year)
    elif "-" in row["ls_date_pc"]:
        #print(row["ls_date_pc"])
        year.append(pd.to_datetime(row["ls_date_pc"],errors = "coerce",yearfirst = True).year)
    else:
        year.append(row["ls_date_pc"])
train["year"] = year
train.fillna(0,inplace = True)
train["year"] = train["year"].astype(float)
print(train["year"].unique())
pop_dens_bg = []
pop_dens_tract = []
hh_inc_med_bg = []
hh_inc_med_tract = []
hh_inc_avg_bg = []
hh_inc_avg_tract = []
for idx,row in train.iterrows():
    if row["year"] >= 2012:
        pop_dens_bg.append(row["pop_dens_bg_2012-2016"])
        pop_dens_tract.append(row["pop_dens_tract_2012-2016"])
        hh_inc_med_bg.append(row["hh_inc_med_bg_2012-2016"])
        hh_inc_med_tract.append(row["hh_inc_med_tract_2012-2016"])
        hh_inc_avg_bg.append(row["hh_inc_avg_bg_2012-2016"])
        hh_inc_avg_tract.append(row["hh_inc_avg_tract_2012-2016"])
    elif row["year"] <=2011 and row["year"] >= 2006:
        pop_dens_bg.append(row["pop_dens_bg_2006-2010"])
        pop_dens_tract.append(row["pop_dens_tract_2006-2010"])
        hh_inc_med_bg.append(row["hh_inc_med_bg_2006-2010"])
        hh_inc_med_tract.append(row["hh_inc_med_tract_2006-2010"])
        hh_inc_avg_bg.append(row["hh_inc_avg_bg_2006-2010"])
        hh_inc_avg_tract.append(row["hh_inc_avg_tract_2006-2010"])
    elif row["year"] <= 2005 and row["year"] >= 2000:
        pop_dens_bg.append(row["pop_dens_bg_2000"])
        pop_dens_tract.append(row["pop_dens_tract_2000"])
        hh_inc_med_bg.append(row["hh_inc_med_bg_2000"])
        hh_inc_med_tract.append(row["hh_inc_med_tract_2000"])
        hh_inc_avg_bg.append(row["hh_inc_avg_bg_2000"])
        hh_inc_avg_tract.append(row["hh_inc_avg_tract_2000"])
    else:
        pop_dens_bg.append(row["pop_dens_bg_1990"])
        pop_dens_tract.append(row["pop_dens_tract_1990"])
        hh_inc_med_bg.append(row["hh_inc_med_bg_1990"])
        hh_inc_med_tract.append(row["hh_inc_med_tract_1990"])
        hh_inc_avg_bg.append(row["hh_inc_avg_bg_1990"])
        hh_inc_avg_tract.append(row["hh_inc_avg_tract_1990"])

train["pop_dens_bg"] = pop_dens_bg 
train["pop_dens_tract"] = pop_dens_tract
train["hh_inc_med_bg"] = hh_inc_med_bg 
train["hh_inc_med_tract"] = hh_inc_med_tract
train["hh_inc_avg_bg"] = hh_inc_med_bg 
train["hh_inc_avg_tract"] = hh_inc_med_tract

to_drop = ["pop_dens_bg_2012-2016", "pop_dens_tract_2012-2016", "hh_inc_med_bg_2012-2016", "hh_inc_med_tract_2012-2016", "hh_inc_avg_bg_2012-2016", "hh_inc_avg_tract_2012-2016"
, "pop_dens_bg_2006-2010", "pop_dens_tract_2006-2010", "hh_inc_med_bg_2006-2010", "hh_inc_med_tract_2006-2010", "hh_inc_avg_bg_2006-2010", "hh_inc_avg_tract_2006-2010"
,"pop_dens_bg_2000", "pop_dens_tract_2000", "hh_inc_med_bg_2000", "hh_inc_med_tract_2000", "hh_inc_avg_bg_2000", "hh_inc_avg_tract_2000"
, "pop_dens_bg_1990", "pop_dens_tract_1990", "hh_inc_med_bg_1990", "hh_inc_med_tract_1990", "hh_inc_avg_bg_1990", "hh_inc_avg_tract_1990"]
train.drop(columns = to_drop, inplace = True)





#train["year"] = pd.to_datetime(train["ls_date_pc"]).dt.year
#e_sold: 0: no easement when the land was sold, binary variable
train["e_sold"] = np.where(train["e_year"].le(train["year"].astype(float)), 1, 0)

#split to train and test set ratio 7:3
train.to_csv("full_train.csv")
# y = train["log_price_per_ha"]
# X = train.drop(columns = ["log_price_per_ha"])
# X_train, X_test, y_train, y_test  = train_test_split(X,y,test_size=0.3)
# X_train.to_csv("X_train.csv")
# X_test.to_csv("X_test.csv")
# y_train.to_csv("y_train.csv", header = True)
# y_test.to_csv("y_test.csv", header = True)
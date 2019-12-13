import pandas as pd

#read black and latinX specific SBA datasets
df_bl_all = pd.read_csv('../sba/data_all_bl.csv', index_col=0)
df_hl_all = pd.read_csv('../sba/data_all_hl.csv', index_col=0)

# get number of rows of each dataframe
rowsBL = df_bl_all.shape[0]
rowsHL = df_hl_all.shape[0]

# put each business name in a list
businessNamesBL = []
businessNamesHL = []

# fill respective lists with business names from datasets
for i in range(0,rowsBL):
    businessNamesBL.append(df_bl_all.iloc[i,0].lower())

for i in range(0,rowsHL):
    businessNamesHL.append(df_hl_all.iloc[i,0].lower())

# # print out resulting lists of business names
# print(businessNamesBL)
# print(businessNamesHL)

# go through Final Company Results DB and check each sheet for SBA business
sheet_names = ['ReferenceUSA','USBC','NAIC','Minority VC Funds','BEI','Unique Names','Analysis']
found_in_db = []
for sheet_name in sheet_names:
    df_master_db = pd.read_excel('../Final Company Results.xlsx', sheet_name=sheet_name, index_col=0)
    rowsMasterDB = df_master_db.shape[0]
    print("Checking " + sheet_name + " for duplicates.")
    # go through sheet of final master database and check to see if SBA black owned businesses already exists
    for i in range(0,len(businessNamesBL)):
        found = 0
        for j in range(0,rowsMasterDB):
            if(businessNamesBL[i] == df_master_db.iloc[j,0].lower()):
                # SBA business name is already in the master DB
                found_str = "{} was found in {} on row {}".format(businessNamesBL[i],sheet_name,j)
                print(found_str)
                found_in_db.append(found_str)
                found = 1
        if(found == 0):
            # name wasn't in sheet within master database
            continue

    # go through sheet of final master database and check if SBA latinX owned businesses already exists
    for i in range(0,len(businessNamesHL)):
        found = 0
        for j in range(0,rowsMasterDB):
            if(businessNamesHL[i] == df_master_db.iloc[j,0].lower()):
                # SBA business name is already in the master DB
                found_str = "{} was found in {} on row {}".format(businessNamesHL[i],sheet_name,j)
                print(found_str)
                found_in_db.append(found_str)
                found = 1    
        if(found == 0):
            # name wasn't in sheet within master database
            continue

# print out findings
print("\nSBA Businesses found in Master DB:\n")
for i in range(0,len(found_in_db)):
    print(found_in_db[i])

# SBA Businesses found in Master DB:
# aphios corporation was found in Unique Names on row 4732
# american translation partners, inc. was found in Unique Names on row 3964
# american translation partners, inc. was found in Unique Names on row 4806






import pandas as pd

# SBA Businesses found in Master DB:
# aphios corporation was found in Unique Names on row 4732
# american translation partners, inc. was found in Unique Names on row 3964
# american translation partners, inc. was found in Unique Names on row 4806

# read all SBA sub-datasets
df_bl_all = pd.read_csv('../sba/data_all_bl.csv', index_col=0)
df_hl_all = pd.read_csv('../sba/data_all_hl.csv', index_col=0)
df_wm_all = pd.read_csv('../sba/women_disadvantaged_bl.csv', index_col=0)
df_bl_dis_all = pd.read_csv('../sba/small_disadvantaged_bl.csv', index_col=0)
df_hl_dis_all = pd.read_csv('../sba/small_disadvantaged_hl.csv', index_col=0)

sba_sublist = [df_bl_all, df_hl_all, df_wm_all, df_bl_dis_all, df_hl_dis_all]

# load SBA sheet of master database
df_master_db_sba = pd.read_excel('../Final Company Results.xlsx', sheet_name='SBA', index_col=0)
sba_df = pd.DataFrame(columns=['companyName','tradeName','contact','position','address','city','state','zipCode','capabilitiesNarrative','race_ethnicity','race_ethnicity_alt'])

rowsMasterDB = df_master_db_sba.shape[0]

masterIndex = 0
for sublist in sba_sublist:
    rowNum = sublist.shape[0]
    for i in range(0,rowNum):
        newRow = {'companyName':sublist[i][1], 'tradeName':sublist[i][2], 'contact':sublist[i][3], 'position':sublist[i][4], 'address':sublist[i][5], 'city':sublist[i][7], 'state':sublist[i][8], 'zipCode':sublist[i][9], 'capabilitiesNarrative':sublist[i][10], 'race_ethnicity':sublist[i][14], 'race_ethnicity_alt':sublist[i][15]}
        sba_df = sba_df.append(newRow, ignore_index=True)
        # df_master_db_sba[masterIndex][0] = sublist[i][1] # company name
        # df_master_db_sba[masterIndex][1] = sublist[i][2] # trade name
        # df_master_db_sba[masterIndex][2] = sublist[i][3] # contact
        # df_master_db_sba[masterIndex][3] = sublist[i][4] # position
        # df_master_db_sba[masterIndex][4] = sublist[i][5] # address
        # df_master_db_sba[masterIndex][5] = sublist[i][7] # city
        # df_master_db_sba[masterIndex][6] = sublist[i][8] # state
        # df_master_db_sba[masterIndex][7] = sublist[i][9] # zip code
        # df_master_db_sba[masterIndex][8] = sublist[i][10] # capabilities narrative
        # df_master_db_sba[masterIndex][9] = sublist[i][14] # race_ethnicity_first
        # df_master_db_sba[masterIndex][10] = sublist[i][15] # race_ethnicity_alt
        # # increment master index
        # masterIndex = masterIndex + 1

print(sba_df)
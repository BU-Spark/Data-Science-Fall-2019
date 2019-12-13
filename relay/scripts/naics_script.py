from lxml import html
import requests
import pandas as pd
import math

page = requests.get('https://mailinglists.com/mailinglistsxpress/duns-number-sic-and-naics-code-lookup/what-is-my-company-naics-code/')
tree = html.fromstring(page.content)

# create empty lists of business names and business addresses to put into web form
businessNames = []
businessAddresses = []

csvDF =  pd.read_csv(r'SBA_Search_Results_2019-10-23-09-57-53.csv')
shapeDF = csvDF.shape
rowNum = shapeDF[0]

for i in range(rowNum):
    if isinstance(csvDF.iloc[i,0], int):
        # valid business name- add to businessNames list and business addresses list
        businessNames.append(csvDF.iloc[i,1])
        # addresses downloaded from SBA DB are split into two rows. Combine both and append to businessAddresses list
        fullAddress = str(csvDF.iloc[i,3]) + ' ' + str(csvDF.iloc[i+1,3])
        businessAddresses.append(fullAddress)

# print(businessNames)
# print(businessAddresses)

pd.set_option('display.expand_frame_repr', False)
print(csvDF.iloc[0:20,0:])



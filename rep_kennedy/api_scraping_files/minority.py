import requests
import json
import pandas as pd


"""
Documentation for Filters:
https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_docs/api_documentation/search_filters.md

"""

mbe_duns = pd.read_csv('mbe_duns', sep=',')
mbe_duns = mbe_duns.str
print(mbe_duns)

# URL Base for the USA Spending API 
url_base = 'https://api.usaspending.gov'

# Header for Post Requests
headers = {"Content-type": "application/json"}

# Takes in an award name and creates a request to the API to POST
# award agencies matching the specific name (used to find out
# information about the format)
def status_check(code):
    # Prints Status
    if code == 200:
        print("Sucessful Request")
    elif code == 500:
        print("Server Error")
    else:
        print("Malformation Error")


def advanced_download():
    filter_object = {
        "filters": {
            "recipient_type_": ["Minority Owned Business"], 
            "fields": ["Recipient Name"]
        }
    }

    data = json.dumps(filter_object)

    endpoint = "/api/v2/recipient/duns/"

    response = requests.post(url_base + endpoint, headers=headers, data=data)

    status_check(response.status_code)

    return response.content

#html = advanced_download()
#print(html)
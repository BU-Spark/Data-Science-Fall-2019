import requests
import json

"""
Documentation for Filters:
https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_docs/api_documentation/search_filters.md

"""

# URL Base for the USA Spending API 
url_base = 'https://api.usaspending.gov'

# Header for Post Requests
headers = {"Content-type": "application/json"}

# Takes in an award name and creates a request to the API to POST
# award agencies matching the specific name (used to find out
# information about the format)
def award_agency_search(agency_name):
    # Endpoint for the request
    endpoint = '/api/v2/autocomplete/awarding_agency/'

    search_text = {"search_text": agency_name}

    # Filters the search 
    data = json.dumps(search_text)

    # Request 
    response = requests.post(url_base + endpoint, headers=headers, data=data)

    status_check(response.status_code)

    return response.content


def agency_spending_by_recipiant(year, agency_id):
    endpoint = '/api/v2/award_spending/recipient/' + '?fiscal_year=' + year + '&awarding_agency_id=' + agency_id + 'limit=100'

    response = requests.get(url_base + endpoint)

    # Prints Status
    status_check(response.status_code)

    print(response.content)

    return endpoint


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
        "recipient_locations": [
        {
            "country": "USA",
            "state": "MA",
        }
        ], 
        "time_period": [
            {
                "start_date": "2009-10-01",
                "end_date": "2019-10-01"
            }
        ],
        "agencies": [
           {
                "type": "funding",
                    "tier": "toptier", 
                    "name": "Federal Emergency Management Agency"  

            }, 
            {
                "type": "funding",
                    "tier": "toptier", 
                    "name":"Environmental Protection Agency"
            }, 
            {
                "type": "funding",
                    "tier": "toptier", 
                    "name":"Department of Housing and Urban Development"
            }, 
            {
                "type": "funding",
                    "tier": "toptier", 
                    "name": "Department of Health and Human Services"  
            }, 
            {
                "type": "funding",
                    "tier": "toptier", 
                    "name": "National Science Foundation" 
            }, 
            {
                "type": "funding", 
                    "tier": "subtier",
                    "name": "Department of Transportation"

            },
            {
                "type": "funding",
                    "tier": "subtier",
                    "name": "Small Business Innovation Research"

            }, 
            {
                "type": "funding",
                    "tier": "subtier",
                    "name": "Small Business Administration"
            },
            {
                "type": "funding",
                    "tier": "toptier",
                    "name": "Department of Homeland Security"
            }, 
            {

            }
        ]
        }
    }

    data = json.dumps(filter_object)

    endpoint = "/api/v2/download/awards/"


    response = requests.post(url_base + endpoint, headers=headers, data=data)

    status_check(response.status_code)

    return response.content


def download_status():
    endpoint = "/api/v2/downlaod/count/"

    response = requests.get(url_base + endpoint)

    status_check(response.status_code)

    return response.content


html = advanced_download()
print(html)
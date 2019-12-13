# 0. import the requests package

import requests # downlaoded with 'pip install requests' or however you get your python packages

# 1. the website we're scraping
url_base = 'https://api.usaspending.gov'

# 2. pick an 'endpoint' (you can think of this as a file located in a 
#        directory structure, or a table in a database)

endpoint = '/api/v2/download/awards'

# this endpoint actually downlaods a file on your machine
# That's useful, but for illustrative purposes let's try one that returns an object
endpoint = '/api/v2/search/spending_by_award_count/'

# you can find information about how to interact with this endpoint in the documentation
# start here --> https://api.usaspending.gov/docs/ and click 'API endpoints'
# click on the endpoint you want. On its page, click on 'documentation for this endpoint here'
# which will lead you to this github: 
#    https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_docs/api_documentation/advanced_award_search/spending_over_time.md

# We see that it requires a POST method. 
# This means we need to send it arguments to get a response
# (more info on POST here --> https://en.wikipedia.org/wiki/POST_(HTTP)

# 3. The Github page has an example of a 'Filter Object'
# This is how we will send our arguments in the POST request
filter_object = {
    "filters": {
        "keywords": ["business"]
    }
}

#### THINGS I WAS MISSING
# need json library
import json

# Need to specify the header type
headers = {"Content-type": "application/json"}

# Need to specify the data that you pass as a JSON string
data = json.dumps(filter_object)


# 4. Now, we just make our request!
request_url = url_base + endpoint
response = requests.post(request_url, headers = headers, data = data)

# 5. Let's see what the site returned:
print(response.json())






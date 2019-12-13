from __future__ import print_function
import time
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Configure API key authorization: api_key
configuration = openapi_client.Configuration()
configuration.api_key['X-API-KEY'] = '04f8df5b91aa6c70be88d2d3db870550'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-API-KEY'] = 'Bearer'

# create an instance of the API class
api_instance = openapi_client.AdminApi(openapi_client.ApiClient(configuration))
api_key = 'api_key_example' # str | 
usage_credits = 56 # int | 
user_message = 'user_message_example' # str | 

try:
    # Add usage credits to an API Key.
    api_response = api_instance.add_credits(api_key, usage_credits, user_message)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AdminApi->add_credits: %s\n" % e)
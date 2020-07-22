import requests
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext

context_auth = AuthenticationContext(url='https://share-intra.philips.com/sites/STS020161021115113')
context_auth.acquire_token_for_app(client_id='a6a115ee-fe4b-401d-b706-fbeb557f8669',
                                   client_secret='GKlYLuxQTDOrrBsDwE2a3TQ9IJihKL9Yr2r5J/ZPSbw=')

# session = requests.Session()
# session.cookies
ctx = ClientContext('https://share-intra.philips.com/sites/STS020161021115113', context_auth)

folder_url = "Shared%20Documents"  #folder url where to find
folder_name = "ADM"  #folder name to find
result = ctx.web.get_folder_by_server_relative_url(folder_url).folders.filter("Name eq '{0}'".format(folder_name))
ctx.load(result)
ctx.execute_query()
if len(result) > 0:
    print("Folder has been found: {0}".format(result[0].properties["Name"]))
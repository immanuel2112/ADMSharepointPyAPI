import glob
import os

from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.file_creation_information import FileCreationInformation

path = '//nlyehvdcs4vwa73/BOAShared/Transform/Report/PH_GLD_S4H-PRO/PRO001 Material Master/ttMARA/Post/*.xlsx'
files = glob.glob(path)
print(files)

context_auth = AuthenticationContext(url='https://share-intra.philips.com/sites/STS020161021115113')
context_auth.acquire_token_for_app(client_id='a6a115ee-fe4b-401d-b706-fbeb557f8669',
                                   client_secret='GKlYLuxQTDOrrBsDwE2a3TQ9IJihKL9Yr2r5J/ZPSbw=')
ctx = ClientContext('https://share-intra.philips.com/sites/STS020161021115113', context_auth)

folder_url = "Shared%20Documents"  #folder url where to find
folder_name = "ADM"  #folder name to find

# Testing code
# context_auth = AuthenticationContext(url='https://share.philips.com/sites/WiproDMCC-Immi')
# context_auth.acquire_token_for_app(client_id='b8f99341-7ebd-4bb3-af9e-5b8daa0d0618',
#                                    client_secret='37U0DOjwtXY5fD9FSoMtaqx+a8rRPwOMmlBvGkyk+KI=')
# ctx = ClientContext('https://share.philips.com/sites/WiproDMCC-Immi', context_auth)
# folder_url = "Shared%20Documents"  #folder url where to find
# folder_name = "General"  #folder name to find
# result = ctx.web.get_folder_by_server_relative_url(folder_url).folders.filter("Name eq '{0}'".format(folder_name))
# ctx.load(result)
# ctx.execute_query()
# if len(result) > 0:
#     print("Folder has been found: {0}".format(result[0].properties["Name"]))

for file in files:
    file_info = FileCreationInformation()
    with open(file, 'rb') as content_file:
        print(content_file.name)
        file_info.content = content_file.read()

    file_info.url = os.path.basename(folder_url+"\\"+folder_name+'\\'+content_file.name)
    file_info.overwrite = True
    target_file = ctx.web.get_folder_by_server_relative_url(folder_url+"\\"+folder_name).files.add(file_info)
    ctx.execute_query()

    target_file.set_property("Name", content_file.name)
    ctx.execute_query()
    # f.readlines()
    content_file.close()
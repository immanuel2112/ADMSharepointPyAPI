import sys
import glob
import os

from adm.sp.adm_sp_models import ADMSharepointValue
from adm.sp.persistence import Persistence
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.file_creation_information import FileCreationInformation


def __upload_target_reports(adm_sp_value: ADMSharepointValue) -> None:
    site_url = adm_sp_value.sharepoint_value.site_url + 'sites/' + adm_sp_value.sharepoint_value.site_id

    context_auth = AuthenticationContext(url=site_url)
    context_auth.acquire_token_for_app(client_id=adm_sp_value.sharepoint_value.client_id,
                                       client_secret=adm_sp_value.sharepoint_value.client_secret)
    ctx = ClientContext(site_url, context_auth)

    folder_url = adm_sp_value.sharepoint_value.folder_url  # folder url where to find
    folder_name = adm_sp_value.sharepoint_value.base_folder_name  # folder name to find

    target_report_values = adm_sp_value.target_report_values

    if target_report_values is not None:
        for target_report_value in target_report_values:
            file_path = target_report_value.target_report_location
            files = glob.glob(file_path)

            for file in files:
                file_info = FileCreationInformation()
                with open(file, 'rb') as content_file:
                    file_info.content = content_file.read()

                file_name = content_file.name
                file_info.url = os.path.basename(folder_url + "\\" + folder_name + '\\' + file_name)
                file_info.overwrite = True
                target_file = ctx.web.get_folder_by_server_relative_url(folder_url + "\\" + folder_name).files.add(
                    file_info)
                ctx.execute_query()

                target_file.set_property("Name", file_name)
                ctx.execute_query()
                # f.readlines()
                content_file.close()


def main():
    # Collect command line arguments
    # Expecting 4 input values:
    # 1. Database server
    # 2. Login
    # 3. Password
    # 4. Load Manager table id
    adm_sp_value = ADMSharepointValue()

    i = 1
    for arg in sys.argv[1:]:
        if i == 1:
            adm_sp_value.database_server = arg
        if i == 2:
            adm_sp_value.login = arg
        if i == 3:
            adm_sp_value.password = arg
        if i == 4:
            adm_sp_value.load_manager_id = arg

        i += 1

    print(adm_sp_value)

    # Step 1: Populate sharepoint details from ADM
    persistence = Persistence(adm_sp_value)
    sharepoint_value = persistence.fetch_sharepoint_attributes()
    print(sharepoint_value)

    if sharepoint_value is not None:
        adm_sp_value.sharepoint_value = sharepoint_value
        # Step 2: Populate load manager attributes
        persistence.fetch_load_manager_attributes()
        print(adm_sp_value)
        # Remove after testing
        # adm_sp_value.wave_processarea_object_target_id = '4a32092f-dec8-4607-8f3e-275d5b1da560'
        # print(adm_sp_value)

        # Step 3: Fetch active target report details
        target_report_values = persistence.fetch_target_report_attributes()
        print("Target Report Values: " +str(target_report_values))
        adm_sp_value.target_report_values = target_report_values

        # Step 4: Upload files to sharepoint.
        __upload_target_reports(adm_sp_value)


if __name__ == "__main__":
    main()

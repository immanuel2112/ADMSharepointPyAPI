class ADMSharepointValue:
    def __init__(self):
        self.database_server = None
        self.login = None
        self.password = None
        self.wave_processarea_object_target_id = None
        self.initial_delta = None
        self.src_file_path = None
        self.sharepoint_value = None
        self.version = 0
        self.load_manager_id = 0

    def __str__(self) -> str:
        return "ADMSharepointValue { " \
               "database_server = " + str(self.database_server) + \
               ", login = " + str(self.login) + \
               ", password = ******" \
               ", load_manager_id = " + str(self.load_manager_id) + \
               ", wave_processarea_object_target_id = " + str(self.wave_processarea_object_target_id) + \
               ", initial_delta = " + str(self.initial_delta) + \
               ", version = " + str(self.version) + \
               ", src_file_path = " + str(self.src_file_path) + \
               ", sharepoint_value = " + str(self.sharepoint_value) + \
               "}"


class SharepointValue:
    def __init__(self, site_url, site_id, client_id, client_secret, folder_url, base_folder_name):
        self.site_url = site_url
        self.site_id = site_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.folder_url = folder_url
        self.base_folder_name = base_folder_name

    def __str__(self) -> str:
        return "SharepointValue { " \
               "site_url = " + str(self.site_url) + \
               ", site_id = " + str(self.site_id) + \
               ", client_id = " + str(self.client_id) + \
               ", client_secret = " + str(self.client_secret) + \
               ", folder_url = " + str(self.folder_url) + \
               ", base_folder_name = " + str(self.base_folder_name) + \
               "}"
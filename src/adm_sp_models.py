class ADMSharepointValue:
    def __init__(self) -> None:
        self.database_server = None
        self.login = None
        self.password = None
        self.load_manager_id = 0
        self.wave = None
        self.processarea = None
        self.object = None
        self.target = None
        self.wave_processarea_object_target_id = None
        self.load_cycle = None
        self.initial_delta = None
        self.version = 0
        self.sharepoint_value: SharepointValue = None
        self.target_report_values: list = None
        self.adm_report_path = None

    def __str__(self) -> str:
        return "ADMSharepointValue { " \
               "database_server = " + str(self.database_server) + \
               ", login = " + str(self.login) + \
               ", password = ******" \
               ", load_manager_id = " + str(self.load_manager_id) + \
               ", wave = " + str(self.wave) + \
               ", processarea = " + str(self.processarea) + \
               ", object = " + str(self.object) + \
               ", target = " + str(self.target) + \
               ", wave_processarea_object_target_id = " + str(self.wave_processarea_object_target_id) + \
               ", load_cycle = " + str(self.load_cycle) + \
               ", initial_delta = " + str(self.initial_delta) + \
               ", version = " + str(self.version) + \
               ", sharepoint_value = " + str(self.sharepoint_value) + \
               ", target_report_values = " + str(self.target_report_values) + \
               ", adm_report_path = " + str(self.adm_report_path) + \
               "}"


class SharepointValue:
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.site_url = None
        self.site_id = None
        self.client_id = None
        self.client_secret = None
        self.folder_url = None
        self.base_folder_name = None

    def __str__(self) -> str:
        return "SharepointValue { " \
               "id = " + str(self.id) + \
               ", name = " + str(self.name) + \
               ", site_url = " + str(self.site_url) + \
               ", site_id = " + str(self.site_id) + \
               ", client_id = " + str(self.client_id) + \
               ", client_secret = " + str(self.client_secret) + \
               ", folder_url = " + str(self.folder_url) + \
               ", base_folder_name = " + str(self.base_folder_name) + \
               "}"


class ADMTargetReportValue:
    def __init__(self) -> None:
        self.target_report_id = None
        self.target_report = None
        self.target_report_type = None
        self.target_report_location = None
        self.target_report_segment_by_field = None
        self.target_report_segment_values: list = None

    def __str__(self) -> str:
        return "ADMTargetReportValue { " \
               "target_report_id = " + str(self.target_report_id) + \
               ", target_report = " + str(self.target_report) + \
               ", target_report_type = " + str(self.target_report_type) + \
               ", target_report_location = " + str(self.target_report_location) + \
               ", target_report_segment_by_field = " + str(self.target_report_segment_by_field) + \
               ", target_report_segment_values = " + str(self.target_report_segment_values) + \
               "}"


class ADMTargetReportSegmentValue:
    def __init__(self) -> None:
        self.target_report_segment_by_field_value = None
        self.target_report_segment_report_location = None

    def __str__(self) -> str:
        return "ADMTargetReportSegmentValue { " \
               "target_report_segment_by_field_value = " + str(self.target_report_segment_by_field_value) + \
               ", target_report_segment_report_location = " + str(self.target_report_segment_report_location) + \
               "}"

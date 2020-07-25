import pypyodbc as pyodbc

from adm_sp_models import ADMSharepointValue, SharepointValue, ADMTargetReportValue, ADMTargetReportSegmentValue
import sql_constants


class Persistence:
    def __init__(self, adm_sp_value: ADMSharepointValue):
        self.adm_sp_value = adm_sp_value
        self.__build_connection_string()
        self.connection = None

    def __build_connection_string(self) -> None:
        if len(self.adm_sp_value.login) == 0:
            self.connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + self.adm_sp_value.database_server + ';Database=master;Trusted_Connection=yes;'
        else:
            self.connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=' + self.adm_sp_value.database_server \
                                     + ';Database=master;UID=' + self.adm_sp_value.login + ';PWD=' + self.adm_sp_value.password + ';'

    def fetch_load_manager_attributes(self) -> None:
        self.connection = pyodbc.connect(self.connection_string)
        cursor = self.connection.cursor()
        query = sql_constants.FETCH_LOAD_MANAGER_DETAILS_SQL.format(
            ID=self.adm_sp_value.load_manager_id)
        row = cursor.execute(query).fetchone()
        i = 0
        for field in row:
            if i == 0:
                pass
            elif i == 1:
                self.adm_sp_value.wave = field
            elif i == 2:
                self.adm_sp_value.processarea = field
            elif i == 3:
                self.adm_sp_value.object = field
            elif i == 4:
                self.adm_sp_value.target = field
            elif i == 5:
                if (field is not None) and (str(field).startswith("b'")):
                    self.adm_sp_value.wave_processarea_object_target_id = field.replace("b'","").replace("'","")
            elif i == 6:
                self.adm_sp_value.load_cycle = field
            elif i == 7:
                self.adm_sp_value.initial_delta = field
            elif i == 8:
                self.adm_sp_value.version = field
            else:
                self.adm_sp_value.adm_report_path = field

            i += 1
        cursor.close()
        self.connection.close()

    def fetch_sharepoint_attributes(self) -> SharepointValue:
        sharepoint_value = None
        self.connection = pyodbc.connect(self.connection_string)
        cursor = self.connection.cursor()
        row = cursor.execute(
            sql_constants.FETCH_SHAREPOINT_DETAILS_SQL).fetchone()
        if row is not None:
            sharepoint_value = SharepointValue()
            i = 0
            for field in row:
                if i == 0:
                    if (field is not None) and (str(field).startswith("b'")):
                        sharepoint_value.id = field.replace("b'","").replace("'","")
                elif i == 1:
                    sharepoint_value.name = field
                elif i == 2:
                    sharepoint_value.site_url = field
                elif i == 3:
                    sharepoint_value.site_id = field
                elif i == 4:
                    sharepoint_value.client_id = field
                elif i == 5:
                    sharepoint_value.client_secret = field
                elif i == 6:
                    sharepoint_value.folder_url = field
                else:
                    sharepoint_value.base_folder_name = field

                i += 1
        cursor.close()
        self.connection.close()

        return sharepoint_value

    def fetch_target_report_attributes(self) -> list:
        target_report_values = None
        self.connection = pyodbc.connect(self.connection_string)
        cursor = self.connection.cursor()
        query = sql_constants.FETCH_TARGET_REPORT_DETAILS_SQL.format(
            WaveProcessAreaObjectTargetID=self.adm_sp_value.wave_processarea_object_target_id)
        rows = cursor.execute(query).fetchall()

        if rows is not None and len(rows) > 0:
            target_report_values = []
            for row in rows:
                target_report_value = ADMTargetReportValue()
                i = 0
                for field in row:
                    if i == 0:
                        if (field is not None) and (str(field).startswith("b'")):
                            target_report_value.target_report_id = field.replace("b'","").replace("'","")
                    elif i == 1:
                        target_report_value.target_report = field
                    elif i == 2:
                        target_report_value.target_report_type = field
                    elif i == 3:
                        target_report_value.target_report_location = field
                    else:
                        target_report_value.target_report_segment_by_field = field

                    i += 1
                target_report_values.append(target_report_value)

        if target_report_values is not None:
            self.__fetch_target_report_segment_attributes(cursor, target_report_values)

        cursor.close()
        self.connection.close()

        return target_report_values

    def __fetch_target_report_segment_attributes(self, cursor, target_report_values: list) -> None:
        for target_report_value in target_report_values:
            if target_report_value.target_report_segment_by_field is not None:
                query = sql_constants.FETCH_TARGET_REPORT_SEGMENT_DETAILS_SQL.format(
                    WaveProcessAreaObjectTargetReportID=target_report_value.target_report_id)
                rows = cursor.execute(query).fetchall()

                if rows is not None and len(rows) > 0:
                    target_report_segment_values = []
                    for row in rows:
                        target_report_segment_value = ADMTargetReportSegmentValue()
                        i = 0
                        for field in row:
                            if i == 0:
                                target_report_segment_value.target_report_segment_by_field_value = field
                            else:
                                target_report_segment_value.target_report_segment_report_location = field

                            i += 1
                        target_report_segment_values.append(target_report_segment_value)

                    target_report_value.target_report_segment_values = target_report_segment_values


    # def test_connection(self) -> str:
    #     error_message = ""
    #     try:
    #         self.connection = pyodbc.connect(self.connection_string)
    #         self.connection.close()
    #     except Exception as error:
    #         error_message = str(error)
    #     return error_message
    #
    # def check_application_installation_status(self) -> int:
    #     return_value = 0
    #     self.connection = pyodbc.connect(self.connection_string)
    #     cursor = self.connection.cursor()
    #     row = cursor.execute(
    #         query_constants.APPLICATION_DB_EXISTS_SQL.format(
    #             APPLICATION_SYSTEM_DATABASE=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE)).fetchone()
    #     if row:
    #         print("db_name: " + str(row[0]))
    #         return_value = 1
    #     cursor.close()
    #     self.connection.close()
    #     return return_value
    #
    # def install(self) -> None:
    #     try:
    #         # Step 1: Create sdvSystemMaster database
    #         self.session_details.writeToLog(
    #             msg="Start: Create application database: " + query_constants.APPLICATION_SYSTEM_DATABASE_VALUE)
    #         self.create_database()
    #         self.session_details.writeToLog(msg="Stop: Application database created successfully.")
    #         # Step 2: Create sdv System Master tables
    #         # self.sessiondetails.writeToLog("Create application tables.")
    #         # self.sessiondetails.writeToLog("Application tables created successfully.")
    #         # Step 2: Insert sdv System Master tables data
    #         # self.sessiondetails.writeToLogm,writeToLogm("Populate application default data.")
    #         # self.sessiondetails.writeToLog("Application default data populated successfully.")
    #     except Exception as error:
    #         error_message = str(error)
    #         self.session_details.writeToLog(msg=error_message, error=True)
    #
    # def create_database(self) -> None:
    #     try:
    #         connection = pyodbc.connect(self.connection_string, autocommit=True)
    #         cursor = connection.cursor()
    #         # 1. Creating database
    #         self.session_details.writeToLog(msg="1. Creating database")
    #         query = query_constants.CREATE_DATABASE.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE)
    #         sql = query_constants.EXECUTE_QUERY_IN_DB.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
    #         print("sql: " + sql)
    #         cursor.execute(sql)
    #         # 2. Set Collation property for the database
    #         self.session_details.writeToLog(msg="2. Setting database collation property")
    #         query = query_constants.DATABASE_COLLATE_PROPERTY.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE)
    #         sql = query_constants.EXECUTE_QUERY_IN_DB.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
    #         print("sql: " + sql)
    #         cursor.execute(sql)
    #         # 3. Enable broker property for the database
    #         self.session_details.writeToLog(msg="3. Setting database Enable broker property")
    #         query = query_constants.DATABASE_ENABLE_BROKER_PROPERTY.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE)
    #         sql = query_constants.EXECUTE_QUERY_IN_DB.format(
    #             DatabaseName=query_constants.APPLICATION_SYSTEM_MASTER_DATABASE, query=query)
    #         print("sql: " + sql)
    #         cursor.execute(sql)
    #         connection.close()
    #     except Exception as error:
    #         error_message = str(error)
    #         self.session_details.writeToLog(msg=error_message, error=True)
    #
    # def get_table(self, page) -> Table:
    #     name = page.table
    #     table = Table(name)
    #     self.connection = pyodbc.connect(self.connection_string)
    #     cursor = self.connection.cursor()
    #
    #     query = query_constants.GET_OBJECT_COLUMNS.format(
    #         DatabaseName=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE, Object=name)
    #     header_row = cursor.execute(query).fetchall()
    #     formatted_header_row = application_utility.convert_resultset_to_list(header_row)
    #     table.set_fields(formatted_header_row)
    #
    #     where_clause = ""
    #     if page.filter_field is not None:
    #         where_clause = "WHERE " + page.filter_field + " = '" + page.filter_field_value + "'"
    #
    #     query = query_constants.GET_OBJECT_DATA.format(
    #         DatabaseName=query_constants.APPLICATION_SYSTEM_DATABASE_VALUE, Object=name,
    #         WhereClause=where_clause)
    #
    #     print(query)
    #     data_row = cursor.execute(query).fetchall()
    #     table.set_data(data_row)
    #
    #     if data_row is not None:
    #         table.set_record_count(len(data_row))
    #
    #     cursor.close()
    #     self.connection.close()
    #     return table

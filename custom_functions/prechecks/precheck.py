from custom_functions.prechecks.folder_checks import folder_checks
from custom_functions.prechecks.config_file_checks import check_for_config_file
from custom_functions.prechecks.database_checks import check_for_sql_database
from custom_functions.prechecks.cdm_checks import check_for_cdms

def run_precheck():
    folder_checks()
    check_for_config_file()
    check_for_cdms()
    check_for_sql_database()
    return
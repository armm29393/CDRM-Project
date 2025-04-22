import os

def check_for_config_folder():
    if os.path.isdir(f'{os.getcwd()}/configs'):
        return
    else:
        os.mkdir(f'{os.getcwd()}/configs')
        return

def check_for_database_folder():
    if os.path.isdir(f'{os.getcwd()}/databases'):
        return
    else:
        os.mkdir(f'{os.getcwd()}/databases')
        os.mkdir(f'{os.getcwd()}/databases/sql')
        return

def check_for_cdm_folder():
    if os.path.isdir(f'{os.getcwd()}/configs/CDMs'):
        return
    else:
        os.mkdir(f'{os.getcwd()}/configs/CDMs')
        return

def check_for_wv_cdm_folder():
    if os.path.isdir(f'{os.getcwd()}/configs/CDMs/WV'):
        return
    else:
        os.mkdir(f'{os.getcwd()}/configs/CDMs/WV')
        return

def check_for_cdm_pr_folder():
    if os.path.isdir(f'{os.getcwd()}/configs/CDMs/PR'):
        return
    else:
        os.mkdir(f'{os.getcwd()}/configs/CDMs/PR')
        return

def folder_checks():
    check_for_config_folder()
    check_for_database_folder()
    check_for_cdm_folder()
    check_for_wv_cdm_folder()
    check_for_cdm_pr_folder()
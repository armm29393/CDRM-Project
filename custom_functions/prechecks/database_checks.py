import os
import yaml

def check_for_sqlite_database():
    with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if os.path.exists(f'{os.getcwd()}/databases/key_cache.db'):
        return
    else:
        if config['database_type'].lower() != 'mariadb':
            from custom_functions.database.cache_to_db_sqlite import create_database
            create_database()
            return
        else:
            return

def check_for_mariadb_database():
    with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if config['database_type'].lower() == 'mariadb':
        from custom_functions.database.cache_to_db_mariadb import create_database
        create_database()
        return
    else:
        return

def check_for_sql_database():
    check_for_sqlite_database()
    check_for_mariadb_database()
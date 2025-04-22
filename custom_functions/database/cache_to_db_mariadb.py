import os
import yaml
import mysql.connector
from mysql.connector import Error



def get_db_config():
    # Configure your MariaDB connection
    with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    db_config = {
        'host': f'{config["mariadb"]["host"]}',
        'user': f'{config["mariadb"]["user"]}',
        'password': f'{config["mariadb"]["password"]}',
        'database': f'{config["mariadb"]["database"]}'
    }
    return db_config


def create_database():
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                SERVICE VARCHAR(255),
                PSSH TEXT,
                KID VARCHAR(255) PRIMARY KEY,
                `Key` TEXT,
                License_URL TEXT,
                Headers TEXT,
                Cookies TEXT,
                Data BLOB
            )
            ''')
            conn.commit()
    except Error as e:
        print(f"Error: {e}")

def cache_to_db(service=None, pssh=None, kid=None, key=None, license_url=None, headers=None, cookies=None, data=None):
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT 1 FROM licenses WHERE KID = %s', (kid,))
            existing_record = cursor.fetchone()

            cursor.execute('''
            INSERT INTO licenses (SERVICE, PSSH, KID, `Key`, License_URL, Headers, Cookies, Data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                SERVICE = VALUES(SERVICE),
                PSSH = VALUES(PSSH),
                `Key` = VALUES(`Key`),
                License_URL = VALUES(License_URL),
                Headers = VALUES(Headers),
                Cookies = VALUES(Cookies),
                Data = VALUES(Data)
            ''', (service, pssh, kid, key, license_url, headers, cookies, data))
            conn.commit()

            return True if existing_record else False
    except Error as e:
        print(f"Error: {e}")
        return False

def search_by_pssh_or_kid(search_filter):
    results = set()
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            like_filter = f"%{search_filter}%"

            cursor.execute('SELECT PSSH, KID, `Key` FROM licenses WHERE PSSH LIKE %s', (like_filter,))
            results.update(cursor.fetchall())

            cursor.execute('SELECT PSSH, KID, `Key` FROM licenses WHERE KID LIKE %s', (like_filter,))
            results.update(cursor.fetchall())

        final_results = [{'PSSH': row[0], 'KID': row[1], 'Key': row[2]} for row in results]
        return final_results[:20]
    except Error as e:
        print(f"Error: {e}")
        return []

def get_key_by_kid_and_service(kid, service):
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT `Key` FROM licenses WHERE KID = %s AND SERVICE = %s', (kid, service))
            result = cursor.fetchone()
            return result[0] if result else None
    except Error as e:
        print(f"Error: {e}")
        return None

def get_kid_key_dict(service_name):
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT KID, `Key` FROM licenses WHERE SERVICE = %s', (service_name,))
            return {row[0]: row[1] for row in cursor.fetchall()}
    except Error as e:
        print(f"Error: {e}")
        return {}

def get_unique_services():
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT SERVICE FROM licenses')
            return [row[0] for row in cursor.fetchall()]
    except Error as e:
        print(f"Error: {e}")
        return []

def key_count():
    try:
        with mysql.connector.connect(**get_db_config()) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(KID) FROM licenses')
            return cursor.fetchone()[0]
    except Error as e:
        print(f"Error: {e}")
        return 0

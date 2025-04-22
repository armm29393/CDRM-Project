import os
import sqlite3
from flask import Blueprint, jsonify, request, send_file
import json
from custom_functions.decrypt.api_decrypt import api_decrypt
import shutil
import math
import yaml
import mysql.connector
from io import StringIO
import tempfile
import time

api_bp = Blueprint('api', __name__)
with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
    config = yaml.safe_load(file)
if config['database_type'].lower() != 'mariadb':
    from custom_functions.database.cache_to_db_sqlite import search_by_pssh_or_kid, cache_to_db, \
        get_key_by_kid_and_service, get_unique_services, get_kid_key_dict, key_count
elif config['database_type'].lower() == 'mariadb':
    from custom_functions.database.cache_to_db_mariadb import search_by_pssh_or_kid, cache_to_db, \
        get_key_by_kid_and_service, get_unique_services, get_kid_key_dict, key_count

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

@api_bp.route('/api/cache/search', methods=['POST'])
def get_data():
    search_argument = json.loads(request.data)['input']
    results = search_by_pssh_or_kid(search_filter=search_argument)
    return jsonify(results)

@api_bp.route('/api/cache/<service>/<kid>', methods=['GET'])
def get_single_key_service(service, kid):
    result = get_key_by_kid_and_service(kid=kid, service=service)
    return jsonify({
        'code': 0,
        'content_key': result,
    })

@api_bp.route('/api/cache/<service>', methods=['GET'])
def get_multiple_key_service(service):
    result = get_kid_key_dict(service_name=service)
    pages = math.ceil(len(result) / 10)
    return jsonify({
        'code': 0,
        'content_keys': result,
        'pages': pages
    })

@api_bp.route('/api/cache/<service>/<kid>', methods=['POST'])
def add_single_key_service(service, kid):
    body = request.get_json()
    content_key = body['content_key']
    result = cache_to_db(service=service, kid=kid, key=content_key)
    if result:
        return jsonify({
            'code': 0,
            'updated': True,
        })
    elif result is False:
        return jsonify({
            'code': 0,
            'updated': True,
        })

@api_bp.route('/api/cache/<service>', methods=['POST'])
def add_multiple_key_service(service):
    body = request.get_json()
    keys_added = 0
    keys_updated = 0
    for kid, key in body['content_keys'].items():
        result = cache_to_db(service=service, kid=kid, key=key)
        if result is True:
            keys_updated += 1
        elif result is False:
            keys_added += 1
    return jsonify({
        'code': 0,
        'added': str(keys_added),
        'updated': str(keys_updated),
    })

@api_bp.route('/api/cache', methods=['POST'])
def unique_service():
    services = get_unique_services()
    return jsonify({
        'code': 0,
        'service_list': services,
    })


@api_bp.route('/api/cache/download', methods=['GET'])
def download_database():
    if config['database_type'].lower() != 'mariadb':
        original_database_path = f'{os.getcwd()}/databases/sql/key_cache.db'

        # Make a copy of the original database (without locking the original)
        modified_database_path = f'{os.getcwd()}/databases/sql/key_cache_modified.db'

        # Using shutil.copy2 to preserve metadata (timestamps, etc.)
        shutil.copy2(original_database_path, modified_database_path)

        # Open the copied database for modification using 'with' statement to avoid locks
        with sqlite3.connect(modified_database_path) as conn:
            cursor = conn.cursor()

            # Update all rows to remove Headers and Cookies (set them to NULL or empty strings)
            cursor.execute('''
            UPDATE licenses
            SET Headers = NULL,
                Cookies = NULL
            ''')

            # No need for explicit commit, it's done automatically with the 'with' block
            # The connection will automatically be committed and closed when the block ends

        # Send the modified database as an attachment
        return send_file(modified_database_path, as_attachment=True, download_name='key_cache.db')
    if config['database_type'].lower() == 'mariadb':
        try:
            # Connect to MariaDB
            conn = mysql.connector.connect(**get_db_config())
            cursor = conn.cursor()

            # Update sensitive data (this updates the live DB, you may want to duplicate rows instead)
            cursor.execute('''
            UPDATE licenses
            SET Headers = NULL,
                Cookies = NULL
            ''')

            conn.commit()

            # Now export the table
            cursor.execute('SELECT * FROM licenses')
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            # Dump to SQL-like format
            output = StringIO()
            output.write(f"-- Dump of `licenses` table\n")
            for row in rows:
                values = ', '.join(f"'{str(v).replace('\'', '\\\'')}'" if v is not None else 'NULL' for v in row)
                output.write(f"INSERT INTO licenses ({', '.join(column_names)}) VALUES ({values});\n")

            # Write to a temp file for download
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, 'key_cache.sql')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(output.getvalue())

            return send_file(temp_path, as_attachment=True, download_name='licenses_dump.sql')
        except mysql.connector.Error as err:
            return {"error": str(err)}, 500

_keycount_cache = {
    'count': None,
    'timestamp': 0
}

@api_bp.route('/api/cache/keycount', methods=['GET'])
def get_count():
    now = time.time()
    if now - _keycount_cache['timestamp'] > 10 or _keycount_cache['count'] is None:
        _keycount_cache['count'] = key_count()
        _keycount_cache['timestamp'] = now
    return jsonify({
        'count': _keycount_cache['count']
    })

@api_bp.route('/api/decrypt', methods=['POST'])
def decrypt_data():
    api_request_data = json.loads(request.data)
    if 'pssh' in api_request_data:
        if api_request_data['pssh'] == '':
            api_request_pssh = None
        else:
            api_request_pssh = api_request_data['pssh']
    else:
        api_request_pssh = None
    if 'licurl' in api_request_data:
        if api_request_data['licurl'] == '':
            api_request_licurl = None
        else:
            api_request_licurl = api_request_data['licurl']
    else:
        api_request_licurl = None
    if 'headers' in api_request_data:
        if api_request_data['headers'] == '':
            api_request_headers = None
        else:
            api_request_headers = api_request_data['headers']
    else:
        api_request_headers = None
    if 'cookies' in api_request_data:
        if api_request_data['cookies'] == '':
            api_request_cookies = None
        else:
            api_request_cookies = api_request_data['cookies']
    else:
        api_request_cookies = None
    if 'data' in api_request_data:
        if api_request_data['data'] == '':
            api_request_data = None
        else:
            api_request_data = api_request_data['data']
    else:
        api_request_data = None
    result = api_decrypt(pssh=api_request_pssh, license_url=api_request_licurl, headers=api_request_headers, cookies=api_request_cookies, json_data=api_request_data)
    if result['status'] == 'success':
        return jsonify({
            'status': 'success',
            'message': result['message']
        })
    else:
        return jsonify({
            'status': 'fail',
            'message': result['message']
        })
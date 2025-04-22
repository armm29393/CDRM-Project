import os

def check_for_config_file():
    if os.path.exists(f'{os.getcwd()}/configs/config.yaml'):
        return
    else:
        default_config = """\
default_wv_cdm: ''
default_pr_cdm: ''
# change the type to mariadb to use mariadb below
database_type: 'sqlite'
fqdn: ''
remote_cdm_secret: ''

# uncomment all the lines below to use mariadb and fill out the information
#mariadb:
#  user: ''
#  password: ''
#  host: ''
#  port: ''
#  database: ''
"""
    with open(f'{os.getcwd()}/configs/config.yaml', 'w') as f:
        f.write(default_config)
        return
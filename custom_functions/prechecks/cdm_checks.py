import os
import yaml
import requests



def check_for_wvd_cdm():
    with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if config['default_wv_cdm'] == '':
        answer = ' '
        while answer[0].upper() != 'Y' and answer[0].upper() != 'N':
            answer = input('No default Widevine CDM specified, would you like to download one from The CDM Project? (Y)es/(N)o: ')
        if answer[0].upper() == 'Y':
            response = requests.get(url='https://cdm-project.com/CDRM-Team/CDMs/raw/branch/main/Widevine/L3/public.wvd')
            if response.status_code == 200:
                with open(f'{os.getcwd()}/configs/CDMs/WV/public.wvd', 'wb') as file:
                    file.write(response.content)
                config['default_wv_cdm'] = 'public'
                with open(f'{os.getcwd()}/configs/config.yaml', 'w') as file:
                    yaml.dump(config, file)
                print("Successfully downloaded Widevine CDM")
            else:
                exit(f"Download failed, please try again or place a .wvd file in {os.getcwd()}/configs/CDMs/WV and specify the name in {os.getcwd()}/configs/config.yaml")
        if answer[0].upper() == 'N':
            exit(f"Place a .wvd file in {os.getcwd()}/configs/CDMs/WV and specify the name in {os.getcwd()}/configs/config.yaml")
    else:
        base_name = config["default_wv_cdm"]
        if not base_name.endswith(".wvd"):
            base_name += ".wvd"
        if os.path.exists(f'{os.getcwd()}/configs/CDMs/WV/{base_name}'):
            return
        else:
            exit(f"Widevine CDM {base_name} does not exist in {os.getcwd()}/configs/CDMs/WV")

def check_for_prd_cdm():
    with open(f'{os.getcwd()}/configs/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    if config['default_pr_cdm'] == '':
        answer = ' '
        while answer[0].upper() != 'Y' and answer[0].upper() != 'N':
            answer = input('No default PlayReady CDM specified, would you like to download one from The CDM Project? (Y)es/(N)o: ')
        if answer[0].upper() == 'Y':
            response = requests.get(url='https://cdm-project.com/CDRM-Team/CDMs/raw/branch/main/Playready/SL2000/public.prd')
            if response.status_code == 200:
                with open(f'{os.getcwd()}/configs/CDMs/PR/public.prd', 'wb') as file:
                    file.write(response.content)
                config['default_pr_cdm'] = 'public'
                with open(f'{os.getcwd()}/configs/config.yaml', 'w') as file:
                    yaml.dump(config, file)
                print("Successfully downloaded PlayReady CDM")
            else:
                exit(f"Download failed, please try again or place a .prd file in {os.getcwd()}/configs/CDMs/PR and specify the name in {os.getcwd()}/configs/config.yaml")
        if answer[0].upper() == 'N':
            exit(f"Place a .prd file in {os.getcwd()}/configs/CDMs/PR and specify the name in {os.getcwd()}/configs/config.yaml")
    else:
        base_name = config["default_pr_cdm"]
        if not base_name.endswith(".prd"):
            base_name += ".prd"
        if os.path.exists(f'{os.getcwd()}/configs/CDMs/PR/{base_name}'):
            return
        else:
            exit(f"PlayReady CDM {base_name} does not exist in {os.getcwd()}/configs/CDMs/WV")


def check_for_cdms():
    check_for_wvd_cdm()
    check_for_prd_cdm()
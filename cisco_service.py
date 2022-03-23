import requests
from requests.auth import HTTPBasicAuth
import config
import urllib

# Disable SSL warnings. Not needed in production environments with valid certificates
import urllib3
urllib3.disable_warnings()

class CiscoService:
    BASE_URL = 'https://sesaux7.is.sandvik.com'
    AUTH_URL = '/dna/system/api/v1/auth/token'
    DEVICES_URL = '/dna/intent/api/v1/network-device'
    DEVICE_ENRICHMENT_URL = '/dna/intent/api/v1/device-enrichment-details'

    def __init__(self):
        self.username = config.username
        self.password = config.password

    def get_dnac_jwt_token(self):
        try:
            response = requests.post(self.BASE_URL + self.AUTH_URL,
                                    auth=HTTPBasicAuth(self.username, self.password),
                                    verify=False)
            response.raise_for_status()
            token = response.json()['Token']
            return token
        except requests.exceptions.HTTPError as e:
            raise SystemExit("HTTP ERROR: ", e)
        except requests.exceptions.RequestException as e:
            raise SystemExit("REQUEST ERROR: ", e)

        
    def get_network_devices(self, headers):
        try:
            response = requests.get(self.BASE_URL +  self.DEVICES_URL + "/?family={}".format(urllib.parse.quote("Switches and Hubs")),
                                    headers = headers,
                                    verify=False
                                    )
            response.raise_for_status()
            device_info = response.json()
            return device_info['response']
        except requests.exceptions.HTTPError as e:
            raise SystemExit("HTTP ERROR: ", e)
        except requests.exceptions.RequestException as e:
            raise SystemExit("REQUEST ERROR: ")


    def get_device_enrichment_details(self, headers, mac, retries = 0):
        try:
            headers["entity_type"] = "mac_address"
            headers["entity_value"] = mac
            response = requests.get(self.BASE_URL +  self.DEVICE_ENRICHMENT_URL,
                                    headers = headers,
                                    verify=False
                                )
            response.raise_for_status()
            device_details = response.json()
            return device_details[0]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                if(retries < 4):
                    retries += 1
                    print("Renewing token. Attempt {}".format(retries))
                    token = self.get_dnac_jwt_token()
                    headers["X-Auth-Token"] = token
                    return self.get_device_enrichment_details(headers, mac, retries)
                else: 
                    raise SystemExit("HTTP ERROR: ", e)
            else:
                raise SystemExit("HTTP ERROR: ", e)
        except requests.exceptions.RequestException as e:
            raise SystemExit("REQUEST ERROR: ", e)
        
        

from time import sleep
import csv
from datetime import datetime
import mac_vendor_lookup
import cisco_service

class CiscoDnacMacLookupRunner():

    headers = {'Content-Type': 'application/json'}

    def __init__(self):
        self.cisco = cisco_service.CiscoService()
        self.mac_lookup = mac_vendor_lookup.MacLookup()
        self.today = datetime.now()
        self.filename = "mac_address_lookup_{}T{}Z.csv".format(str(self.today.date()), str(self.today.time()))

    def main(self): 
        print("Obtaining token..")
        token = self.cisco.get_dnac_jwt_token()
        self.headers["X-Auth-Token"] = token
        print("Fetching network devices..")
        devices = self.cisco.get_network_devices(self.headers)
        
        with open(self.filename, 'w') as csvfile:
            print("MAC lookup as begun. This may take a while..")
            print("Estimated run time: {} min".format(int(363/5)))
            csvwriter = csv.writer(csvfile)
            counter_rate_limit = 0
            for item in devices:
                if(counter_rate_limit == 5):
                    sleep(60)
                    counter_rate_limit = 0
                details = self.cisco.get_device_enrichment_details(self.headers, item['macAddress'])
                counter_rate_limit += 1
                if 'links' in details['deviceDetails']['neighborTopology'][0]:
                    for detail in details['deviceDetails']['neighborTopology'][0]['links']:
                        if 'interfaceDetails' in detail and detail['id'] == "CLIENTS":
                            for client in detail['interfaceDetails']:
                                mac_address = client['clientMacAddress']
                                manufacturer = self.mac_lookup.lookup_mac_vendor(mac_address)
                                csvwriter.writerow([mac_address,manufacturer])
            print("Ending script..")
            print("See the result in {}".format(self.filename))


if __name__ == "__main__":
    # Cool banner ofc
    print("""
                        ╔═╗╦╔═╗╔═╗╔═╗  ╔╦╗╔╗╔╔═╗╔═╗  ╔╦╗╔═╗╔═╗  ╦  ╔═╗╔═╗╦╔═╦ ╦╔═╗
                        ║  ║╚═╗║  ║ ║   ║║║║║╠═╣║    ║║║╠═╣║    ║  ║ ║║ ║╠╩╗║ ║╠═╝
                        ╚═╝╩╚═╝╚═╝╚═╝  ═╩╝╝╚╝╩ ╩╚═╝  ╩ ╩╩ ╩╚═╝  ╩═╝╚═╝╚═╝╩ ╩╚═╝╩  

            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWKKNMMMMMMMMMMMMMMMMMMMMWWWMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMXl,co0NWMMMMMMMMMMMMMMXxc:xWMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNd''',;cdkKNNNNNNWNKko,...oWMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMO;''.....';ccllc:,.  ...'kMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMMMMWXOxdllllldxOXWMMMMMMMWNd'........ ....      ..lNMMMMMMMMMMMMMMMMMMM
            MMMMMMMMMN0o:,;;:clllc:;,';oONMMMMMWd'',,,'.        ..... .dWMMMMMMMMMMMMMMMMMMM
            MMMMMWWWO:,cdOO0K0O0K0K0klc:';dXMMMXl,'',;;.        .'''''.lXMMMMMMMMMMMMMMMMMMM
            MMMMMMXo;oKWM0dkkdddoo0xddkW0o',kWM0c...,lol;.  . .ccoc..;cdXMMMMMMMMMMMMMMMMMMM
            MMMMMXo:0MMMMWK0KXXKKKKX00NMMWK:'dWO,....';;'  .. .;::,'',,lKMMMMMMMMMMMMMMMMMMM
            MMMMWxc0MMMMWW0kOxxkKkk0OXWWWMMNl'kO:'........,:'........,,cKMMMMMMMMMMMMMMMMMMM
            MMMMNdxWMMMMMWOxkdddxxdxkKNWWWWMK;cXd'........,,'''.....',,:kXMMMMMMMMMMMMMMMMMM
            MMMMXokMMMMMMMNXXXNNXNX0KXWWWWWWNlcXXd,.'......'..'.','.'',;:oKWMMMMMMMMMMMMMMMM
            MMMMXoxWMMMMMMM0olxkoxxkXWMMMMMMNloNWNd...  ..................:0WMMMMMMMMMMMMMMM
            MMMMNxcOWMMMMMMKkkkOOkOOXWMMMMMMO:kMMNl..                ..   .l0WMMMMMMMMMMMMMM
            MMMMM0:;kNWXXNKO0K0000KKXK0OONWKlcOWNd'                       .,oKWMMMMMMMMMMMMM
            MMMMMWO;'lOxxOddooddlcdxxxlox0Oolo0W0,.                       .,;oKMMMMMMMMMMMMM
            MMMMMMWKc..';dkOKX0KXXXK00Oxdl:;,,oOo.                        .'',oKWMMMMMMMMMMM
            MMMMMMMMWOl,..';coddxxdol:,..,;:;..':;..  ..                  ..''';dKWWMMMMMMMM
            MMMMMMMMMMMN0dl:;''.'',:cokO0KNWW0l..''. ...                   ..,,'':xXWMMMMMMM
            MMMMMMMMMMMMMMMWWNXKKXXWMMMMMMMMMMNl...     .                   ..,'',,:xNWMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM0;..        ..                  .,;::,'cKMMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWx'          .,;'. .......         ..','.lXMMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMK:.         .  .',. ..    ..          ....dWMMM
            MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMk.               ..                    ...cXMMM
            """)
    print("Starting script..")
    CiscoDnacMacLookupRunner().main()
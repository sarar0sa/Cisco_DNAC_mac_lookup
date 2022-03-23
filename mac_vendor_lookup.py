import requests
import io

class MacLookup:
    mac_lookup_database_uri = "https://gitlab.com/wireshark/wireshark/-/raw/master/manuf"

    def __init__(self):
        self.init_mac_db()

    ## Download/Update Mac DB
    def init_mac_db(self):
        try:
            response = requests.get(self.mac_lookup_database_uri, allow_redirects=True)
            open('manuf.txt', 'wb').write(response.content)
        except Exception as e:
            raise SystemExit('Error while fetching manuf-file: {}'.format(e))

    def build_mac_dict_lookup(self):
        try:
            mac_dict = {}
            with io.open('manuf.txt', "r", encoding="utf-8") as read_file:
                manuf_file = io.StringIO(read_file.read())
                # Remove commments from file
                filtered_manuf = filter(None, (line.partition('#')[0].rstrip() for line in manuf_file))
                for line in filtered_manuf:
                    part = line.split('\t')
                    if(part[1] != 'IEEERegi'):
                        if(len(part[0]) == 8):
                            mac_dict[part[0]] = part[1]
                        else:
                            if part[0][0:8] not in mac_dict.keys():
                                mac_dict[part[0][0:8]] = {}
                            mac_dict[part[0][0:8]][part[0]] = part[1]

            return mac_dict
        except Exception as e:
            raise SystemExit('Error while parsing manuf-file: {}'.format(e))

    def calculate_netmask(self, mac, mac_to_calculate):
        for key,value in mac_to_calculate.items():
            mac_bits = int(mac.replace(':', ''), 16)
            lowest_mac = int(key.split("/")[0].replace(':', ''), 16)
            mask = key.split("/")[1]
            highest_mac = lowest_mac + int('1'*(48-int(mask)), 2)
            if mac_bits >= lowest_mac and mac_bits <= highest_mac:
                return value
        return None
    
    def lookup_mac_vendor(self, mac):
        mac_dict = self.build_mac_dict_lookup()
        if(mac[0:8] in mac_dict.keys()):
            if type(mac_dict[mac[0:8]]) == str:
                return mac_dict[mac[0:8]]
            elif type(mac_dict[mac[0:8]]) == dict:
                vendor = self.calculate_netmask(mac, mac_dict[mac[0:8]])
                if(vendor == None):
                    return 'Unknown'
                return vendor
        else:
            return 'Unknown'
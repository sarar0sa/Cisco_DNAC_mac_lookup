# CISCO DNAC MAC LOOKUP

A simple script to look up mac-addresses retrieved from switches via the Cisco DNAC API.\
Uses the manuf-file as database to look for manufacturers.\
Returns a csv-file with mac-address and its corresponding manufacturer.

### How to run
___
```
$ python3 cisco_dnac_mac_lookup_runner.py

```
### Classes
___
**cisco_dnac_mac_lookup_runner.py**

Contains the main-method ands ties all the parts togheter

**cisco_service.py**

Handles the API calls to the Cisco DNAC API.

**mac_vendor_lookup.py**

Does the mac lookup and returns the vendor to the main-method.

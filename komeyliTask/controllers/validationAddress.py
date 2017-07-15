import requests # pip install requests
import xml.etree.ElementTree as ET

class validatoinAddress():
    def __init__(self):
        pass
    def checkValidAddress(self,address):
        newAddress =str(address).replace(" ","+")
        url = "https://maps.googleapis.com/maps/api/geocode/xml?address="+newAddress+"&key=AIzaSyB5TR_rPM1sA3NIuaLAn3IHgRq5FmagSM4"
        print(url)
        r = requests.post(url)
        tree = ET.ElementTree(ET.fromstring(r.text))
        root = tree.getroot()
        if root[0].text == "OK":
            return True
        else:
            return False


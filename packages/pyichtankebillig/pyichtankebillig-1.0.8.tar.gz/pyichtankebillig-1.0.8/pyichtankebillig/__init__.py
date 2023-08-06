import urllib.parse
import hashlib

from bs4 import BeautifulSoup
import json

baseURL = "https://nn3.freenet.de/clevertanken/main.php?cm=1"
autogas = "Autogas"
diesel = "Diesel"
erdgas = "Erdgas"
superplus = "SuperPlus"
super = "Super"
normal = "Normal"

class ITBObject:
    def __init__(self):
        self.version = "1.0.8"
        self.author = "Ludy87"
        self.project = "Ich tanke billig"
        self.page = "https://www.astra-g.org/"
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

def connenctionLib(url):
    try:
        import urllib3 as request
        http = request.PoolManager()
        response = http.request("GET", url)
        return response.data
    except:
        from urllib import request
        response = request.urlopen(url)
        return response.read()

def getStations(kraftstoff = diesel, place = '123', limit = '-1', asJson = False):
    url = baseURL + '&sprit=' + kraftstoff + '&ort=' + urllib.parse.quote(str(place))
    data = connenctionLib(url)
    text = data.decode('utf-8')
    bs = BeautifulSoup(text, 'html.parser')
    rows = bs.find_all('tr')
    me = ITBObject()
    me.fuel_type = kraftstoff
    if len(rows) == 0:
        info_msg = bs.find('div', {"class": "frn_contHead"})
        if info_msg != None:
            me.status = {"error": info_msg.getText()}
        else:
            me.status = {"error": bs.getText().strip()}
    else:
        me.status = 200
        me.stations = []
        i = 0
        for row in rows:
            if not row.text.strip():
                continue
            if not row.find('td'):
                continue
            colErg1 = row.find('td', {"class": "colErg1"})
            colErg2 = row.find('td', {"class": "colErg2"})
            colErg3 = row.find('td', {"class": "colErg3"})

            colErg1_a = colErg1.getText().strip().split('<br>')[0].split('\n')
            stationName = colErg1_a[0].strip()
            street = colErg1_a[1].strip()
            place = colErg1_a[2].strip()

            price = colErg2.getText().strip()

            reloaded = colErg3.getText().strip().split('<br>')[0].split('\n')
            reloaded = reloaded[1].strip() + " " + reloaded[0].strip()
            sum = stationName + street + place
            sum = hashlib.md5(sum.encode()).hexdigest()
            json_data = {
                "id": sum,
                "station_name": stationName,
                "street": street,
                "place": place,
                "price": price,
                "reloaded": reloaded,
                "fuel": kraftstoff,
                "pos": i +1,
            }
            if (limit == str(i)) and (limit != '-1'):
                break
            i += 1
            me.stations.append(json_data)
    if asJson:
        return me.toJSON()
    else:
        return me

import requests
import time
from datetime import date
from datetime import datetime

# Set the day of your simulation (must be day in future)
d = date(2023, 5, 4) #yyyy,mm,dd

# Creates the needed UNIX timestamp
unixtime = int(time.mktime(d.timetuple())) #+ 2*60*60 # UTC+2 = local time
API_KEY = "AIzaSyCOT0qnKLtFddZ_KEBAbPQKtaQ32Tju92Q" 
payload={}
headers = {}

class Destination:
    def __init__(self, addr, max_time_allowed):
        self.addr = addr
        self.max_time = max_time_allowed

    def compute_commute_time(self, origin):
        commute_time = get_time_between(origin, self.addr)
        if commute_time is None:
            return (None, False)
        else:
            commutable = commute_time <= self.max_time
            if not commutable:
                return (None, False)
            return (commute_time, commutable)

def compute_commute_times(origin, destinations):
    # origin is an address
    # destinations is a list of destination objects
    res = []
    for destination in destinations:
        res.append(destination.compute_commute_time(origin))
    return res

def get_time_between(origin_addr, dest_addr):
    url_12 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + origin_addr + "&destinations=" + dest_addr + "&mode=walking|transit&traffic_model=best_guess&departure_time=" + str(unixtime) + "&language=en-EN&sensor=false&key=" + API_KEY
    url_21 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + dest_addr + "&destinations=" + origin_addr + "&mode=walking|transit&traffic_model=best_guess&departure_time=" + str(unixtime) + "&language=en-EN&sensor=false&key=" + API_KEY 
    response12 = requests.request("GET", url_12, headers=headers, data=payload)
    response21 = requests.request("GET", url_21, headers=headers, data=payload)
    # print(response12.text)
    try:
        response12_value_secs = response12.json()['rows'][0]['elements'][0]['duration']['value']
        response21_value_secs = response21.json()['rows'][0]['elements'][0]['duration']['value']
    except KeyError:
        return None
    return (response12_value_secs + response21_value_secs) / 2

def get_coord(addr):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + addr + "&key=" + API_KEY
    response = requests.request("GET", url, headers=headers, data=payload)
    loc = response.json()['results'][0]['geometry']['location']
    coord = str(loc['lat']) + ", " + str(loc['lng'])
    return coord
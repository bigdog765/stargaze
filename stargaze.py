import os
import requests
import base64
from datetime import datetime
import json
import math, time
import liquidcrystal_i2c
from dotenv import load_dotenv

load_dotenv()  # take environment variables

apiUrl = "https://api.astronomyapi.com/api/v2"

time.sleep(8)
lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)

ELEV = "310"
AZIMUTH_RANGE = (130,340) # Most of the western sky.
the_sun = None

authString = base64.b64encode(os.getenv("KEY").encode()).decode()
headers = {'Authorization': 'Basic ' + authString}

class CelestialBody():
    def __init__(self, name, azimuth, altitude):
        self.name = str(name)
        self.azimuth = float(azimuth)
        self.altitude = float(altitude)
    def is_visible(self):
        return self.altitude > 5
    def is_visible_in_range(self, range):
        """Return true if the body is above horizon, as well as if between the range of azimuths."""
        return self.is_visible() and self.azimuth > range[0] and self.azimuth < range[1]

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")
def get_current_time():
    return datetime.now().strftime("%H:%M:%S")
def fetch():
    payload = {
        'latitude': os.getenv("LAT"),
        'longitude': os.getenv("LNG"),
        'elevation': ELEV,
        'from_date': get_current_date(),
        'to_date': get_current_date(),
        'time': get_current_time()
    }
    bodies_res = requests.get(apiUrl + '/bodies/positions', headers=headers, params=payload)
    return json.loads(bodies_res.text)["data"]["table"]["rows"]

def create_bodies(bodies):
    global the_sun
    body_result = []
    for body in bodies:
        cell = body["cells"][0]
        
        name = cell["name"]
        altitude = cell["position"]["horizontal"]["altitude"]["degrees"]
        azimuth = cell["position"]["horizontal"]["azimuth"]["degrees"]
        if cell["id"] == 'sun':
            the_sun = CelestialBody(name, azimuth, altitude)
        else : body_result.append(CelestialBody(name, azimuth, altitude))
    return body_result

def night_sky_visibility(cloudiness, humidity, visibility):
    """Calculate night sky visibility score (0-100)"""
    w_c = 0.5  # Cloud weight
    w_h = 0.3  # Humidity weight
    w_v = 0.2  # Visibility weight
    V_max = 10000  # Max visibility (in m)
 
    score = 100 - ((w_c * cloudiness + w_h * humidity) + w_v * (visibility / V_max * 100))
    # Ensure score stays within 0-100
    return max(0, min(100, math.floor(score)))

def get_weather_data():
    apiKey = os.getenv("WEATHER_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather?lat=" + LAT + "&lon=" + LNG + "&appid=" + apiKey
    res = json.loads(requests.get(url).text)
    return res["clouds"]["all"], res["main"]["humidity"], res["visibility"]

def get_semantic_score(score, step=25):
    c_step = 25
    score_dic = {
        "25": "Bad",
        "50": "Fair",
        "75": "Good",
        "100": "Great"
    }
    if score <= step:
        return score_dic[str(step)]
    else: return get_semantic_score(score,step+c_step)
    
def display():
    
    bodies_res = fetch()
    bodies = create_bodies(bodies_res)
    if the_sun.is_visible():
        lcd.printline(0,"It's still light out")
        lcd.printline(1,"try again when it's night time!")
    else: 
        clouds, humidity, visibility = get_weather_data()
        visibility_score = night_sky_visibility(clouds, humidity, visibility)
        semantic_score = get_semantic_score(visibility_score)
    
        visible_bodies = list(filter(lambda b: b.is_visible_in_range(AZIMUTH_RANGE), bodies))
        names = [vb.name for vb in visible_bodies]

        lcd.printline(0,"Visibility: " + semantic_score)
        lcd.printline(1,"Bodies visible:")
        lcd.printline(2,",".join(names)) # could overflow line
display()

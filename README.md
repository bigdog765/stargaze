# Night Sky Visibility Display for Telescopes

This script is designed to run on a Raspberry Pi and display night sky visibility information on an I²C-connected LCD. It retrieves current celestial body positions from AstronomyAPI and weather data from OpenWeatherMap, calculates a “night sky visibility” score, and then displays the score along with a list of visible celestial bodies in a specified azimuth range.

## Features

- **Celestial Data Retrieval:** Fetches the positions of celestial bodies (including the sun) for the current date and time.
- **Weather Integration:** Obtains weather parameters (cloudiness, humidity, and visibility) from OpenWeatherMap.
- **Visibility Scoring:** Calculates a night sky visibility score based on weather conditions.
- **LCD Display:** Uses an I²C LCD (default address 0x27 on bus 1) to output status messages.
- **Custom Filtering:** Displays only celestial bodies that are above the horizon and within a specified azimuth range.

## Prerequisites

### Hardware:
- Raspberry Pi with network connectivity.
- An I²C LCD display compatible with the `liquidcrystal_i2c` library. https://www.amazon.com/gp/product/B07QLRD3TM/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1

### APIs:
- AstronomyAPI account and API key. https://astronomyapi.com/
- OpenWeatherMap API key. https://openweathermap.org/api

### Software:
- Python 3.x

### Required Python packages:
- `requests`
- `python-dotenv`
- `liquidcrystal_i2c`

## Installation

1. **Clone or Copy the Script:**  
   Place the script in your working directory on the Raspberry Pi.

2. **Install Required Packages:**  
   Use pip to install the dependencies:

   ```bash
   pip install requests python-dotenv liquidcrystal_i2c

   Or download i2c package with git clone https://github.com/pl31/python-liquidcrystal_i2c.git

## Configure Environment Variables:
Create a .env file in the same directory as the script with the following content:

KEY=your_astronomy_api_key

WEATHER_KEY=your_openweathermap_key

LAT=your_latitude

LNG=your_longitude


## Configuration

Elevation and Azimuth Range:

ELEV is set to "310" (meters). Update this value if your elevation differs.

AZIMUTH_RANGE is defined as (130, 340) to focus on most of the western sky. Adjust this tuple to change based on where you want to look in the sky.


You can now execute your script. I chose to run the script automatically when I turn on the power for the RasPi. 


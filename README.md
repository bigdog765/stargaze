# Night Sky Visibility Display

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
- An I²C LCD display compatible with the `liquidcrystal_i2c` library.

### APIs:
- AstronomyAPI account and API key.
- OpenWeatherMap API key (the script currently includes a sample key which you might need to replace).

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

Configure Environment Variables:
Create a .env file in the same directory as the script with the following content:

KEY=your_astronomy_api_key
LAT=your_latitude
LNG=your_longitude

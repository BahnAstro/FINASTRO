import ephem
from datetime import datetime

def calculate_zodiac_boundaries(date, lat, lon, altitude):
    observer = ephem.Observer()
    observer.date = date
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = altitude

    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    zodiac_boundaries = {}

    for sign in zodiac_signs:
        zodiac_object = ephem.constellation(ephem.Sun(observer.date))
        zodiac_boundaries[sign] = {
            "right_ascension": zodiac_object[1].a_ra,
            "declination": zodiac_object[1].a_dec
        }
        observer.date += ephem.hour * 24 * 30  # Increment by approximately one month

    return zodiac_boundaries

if __name__ == "__main__":
    # Example usage
    date = datetime.utcnow()  #
    latitude = 25.0330        # Replace with your latitude
    longitude = 121.5654      # Replace with your longitude
    altitude = 0              # Replace with your altitude in meters

zodiac_boundaries = calculate_zodiac_boundaries(date, latitude, longitude, altitude)

for sign, coords in zodiac_boundaries.items():
    print(f"{sign}: Right Ascension = {coords['right_ascension']}, Declination = {coords['declination']}")


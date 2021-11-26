from astral import LocationInfo
from astral.sun import sun
import certifi
import ssl
import geopy.geocoders
from geopy.geocoders import Nominatim
import datetime
from geopy.location import Location
import pytz
from tzwhere import tzwhere
from datetime import datetime

# Required on windows
geopy.geocoders.options.default_ssl_context = ssl.create_default_context(
    cafile=certifi.where()
)


def _loc_info(location="Mumbai"):
    geolocator = Nominatim(user_agent="scc")
    location = geolocator.geocode(location)
    lat, long = location.latitude, location.longitude
    metadata = geolocator.reverse((lat, long)).raw

    tz_obj = tzwhere.tzwhere()
    tz = tz_obj.tzNameAt(lat, long)
    return (
        metadata["address"]["city"],
        metadata["address"]["country"],
        tz,
        lat,
        long,
    )


def suntime(location="Mumbai", date=datetime.today()):
    city = LocationInfo(*_loc_info(location))
    t = sun(city.observer, date)
    return t["sunrise"], t["sunset"]

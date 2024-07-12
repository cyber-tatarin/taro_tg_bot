import random
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from fake_useragent import UserAgent

from geopy.geocoders import Nominatim
from geopy.adapters import AioHTTPAdapter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

ua = UserAgent()


class GeoService:
    @staticmethod
    async def city_exists(city_name: str) -> bool:
        user_agent = [
            "city_checker", "location_bot", 
            "CustomBot", "CityService", 
            "location_service", "LocationCheck",
        ]
        async with Nominatim(
            user_agent=random.choice(user_agent), adapter_factory=AioHTTPAdapter
        ) as geolocator:
            try:
                location = await geolocator.geocode(city_name)
                if location:
                    return True
                else:
                    return False
            except GeocoderTimedOut as e:
                print(e)
                return True
            except Exception as e:
                print(e)
                return False

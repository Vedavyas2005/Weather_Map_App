import requests
from typing import Dict, List

GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenWeatherMap API key required")
        self.api_key = api_key

    def geocode(self, city: str) -> List[Dict]:
        """Return list of possible locations for given city name."""
        params = {"q": city.strip(), "limit": 5, "appid": self.api_key}
        print("DEBUG>>SENDING REQ:",GEOCODE_URL,params)
        r = requests.get(GEOCODE_URL, params=params, timeout=10)
        print("DEBUG >> Response:", r.status_code, r.text[:200])
        if r.status_code != 200:
            return []
        data = r.json()
        results = []
        for d in data:
            results.append({
                "name": d.get("name"),
                "lat": d.get("lat"),
                "lon": d.get("lon"),
                "country": d.get("country"),
                "state": d.get("state", "")
            })
        return results

    def get_weather(self, lat: float, lon: float, units: str = "metric") -> Dict:
        params = {"lat": lat, "lon": lon, "appid": self.api_key, "units": units}
        r = requests.get(WEATHER_URL, params=params, timeout=10)
        if r.status_code != 200:
            return {}
        j = r.json()
        main = j.get("main", {})
        wind = j.get("wind", {})
        weather = j.get("weather", [{}])[0]
        return {
            "city": j.get("name"),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "humidity": main.get("humidity"),
            "pressure": main.get("pressure"),
            "wind_speed": wind.get("speed"),
            "description": weather.get("description", "").title(),
            "icon": weather.get("icon")
        }

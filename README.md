##🌍Weather Map App – CustomTkinter + TkinterMapView

Ever wanted to just type “Hyderabad” and instantly see it pinned on a world map, with real-time weather, and then smoothly zoom in/out like Google Maps — but all built in Python with no heavy backend? That’s exactly what this project does.

I built this for my placements to showcase how you can create a clean, modular, interactive desktop app using Python, CustomTkinter for UI, and tkintermapview for maps.

## ✨Features

🔎 Search any city → auto-geocoded & pinned on the map.

🌍 Multiple city matches → if you type Hyderabad, you can choose between India, Pakistan, South Africa, etc.

🗺️ Interactive map → zoom in, zoom out, pan smoothly.

☀️ Live weather info → temperature, feels like, humidity, pressure, wind speed, and condition.

🌗 Light/Dark mode toggle → because who doesn’t love dark mode?

📏 Metric ↔ Imperial switch → °C ↔ °F, m/s ↔ mph, instantly updates UI.

🧩 Modular folder structure → code is clean, each part separated (GUI, services, config).

💾 Map caching → tiles are cached locally, so map loads faster after first run.

##🛠️ How to Run

**1. Clone this repo**
```bash
git clone https://github.com/your-username/weather-map-app.git
cd weather-map-app
```
**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```
**3. Install requirements**
```bash
pip install -r requirements.txt
```
Get a free API key from OpenWeatherMap
.
Put your API key in config.py
OPENWEATHER_API_KEY = "your_api_key_here"
**4. Run the app 🎉**
```bash
python app.py
```

##🎥 How to Use
Type a city name in the search bar → press Search & Pin.
If there are multiple matches, pick the right one from the dropdown.
Zoom in / zoom out with buttons (or mouse scroll).
Switch between light/dark mode.
Toggle between metric and imperial units to see weather change.
It’s that simple 🚀

##💡 Why I built this
I wanted something that looks cool in a demo but also shows:
API integration (OpenWeatherMap for geocoding + weather)
Interactive maps inside a Tkinter app
Clean architecture with modular code
UI polish (theme toggle, dropdown for cities, unit conversions)
Perfect mix of software engineering + practical utility.

##📸 Demo (Screenshots / GIFs here)
Demo video at test_video folder

##🚀 Future Improvements
Add 5-day weather forecast panel.
Show weather icons (cloud, rain, sun).
Save favorite/pinned cities.
Offline geocoding fallback if API fails.

##💙 Built with Python, CustomTkinter, tkintermapview, and a lot of protien bars.

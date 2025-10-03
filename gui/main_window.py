import customtkinter as ctk
from .widgets.map_widget import MapWidget
from .widgets.controls import ControlsFrame
from services.weather_service import WeatherService
from services import units as units_module
from config import OPENWEATHER_API_KEY
import threading

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Weather Map Application")
        self.geometry("1000x700")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.weather_service = WeatherService(OPENWEATHER_API_KEY)
        self.current_units = "metric"
        self.current_weather_raw = None
        self.current_location = None
        self._city_menu = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.map_frame = MapWidget(self, width=700, height=600)
        self.map_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_rowconfigure(2, weight=1)

        self.controls = ControlsFrame(
            right_frame,
            search_callback=self.search_city,
            zoom_in_callback=self.map_frame.zoom_in,
            zoom_out_callback=self.map_frame.zoom_out,
            theme_callback=self.toggle_theme,
            unit_callback=self.change_units
        )
        self.controls.grid(row=0, column=0, sticky="ew")

        self.weather_display = ctk.CTkTextbox(right_frame, width=260, height=380)
        self.weather_display.grid(row=1, column=0, pady=12, sticky="n")

    def toggle_theme(self, mode: str):
        ctk.set_appearance_mode(mode)

    def change_units(self, units: str):
        old = self.current_units
        if units == old:
            return
        self.current_units = units
        if self.current_weather_raw and self.current_location:
            self._display_weather(self.current_weather_raw, stored_units=old, convert_to=units)

    def search_city(self, city_name: str):
        self.controls.set_status(f"Searching '{city_name}'...")
        thr = threading.Thread(target=self._search_and_update, args=(city_name,), daemon=True)
        thr.start()

    def _search_and_update(self, city_name: str):
        try:
            geoc_list = self.weather_service.geocode(city_name)
            if not geoc_list:
                self.controls.set_status("City not found")
                return
            if len(geoc_list) > 1:
                self.after(0, lambda: self._show_city_selection(geoc_list))
                return
            self._finalize_location(geoc_list[0])
        except Exception as e:
            self.controls.set_status(f"Error: {e}")

    def _show_city_selection(self, geoc_list):
        if self._city_menu:
            self._city_menu.destroy()

        options = []
        for g in geoc_list:
            label = f"{g['name']}, {g.get('state','')}, {g['country']}"
            options.append(label)

        self._city_var = ctk.StringVar(value=options[0])
        self._city_menu = ctk.CTkOptionMenu(
            self, values=options, variable=self._city_var,
            command=lambda choice: self._on_city_selected(choice, geoc_list)
        )
        self._city_menu.place(relx=0.5, rely=0.05, anchor="n")

    def _on_city_selected(self, choice, geoc_list):
        for g in geoc_list:
            label = f"{g['name']}, {g.get('state','')}, {g['country']}"
            if label == choice:
                self._finalize_location(g)
                break
        if self._city_menu:
            self._city_menu.destroy()
            self._city_menu = None

    def _finalize_location(self, geoc):
        self.current_location = geoc
        lat, lon = geoc["lat"], geoc["lon"]
        weather = self.weather_service.get_weather(lat, lon, units=self.current_units)
        if not weather:
            self.controls.set_status("Could not fetch weather")
            return
        self.current_weather_raw = weather
        self.after(0, lambda: self.map_frame.set_marker(lat, lon, text=f"{geoc['name']}, {geoc.get('country','')}"))
        self.after(0, lambda: self._display_weather(weather, stored_units=self.current_units))
        self.controls.set_status(f"Pinned: {geoc['name']}, {geoc.get('country','')}")

    def _display_weather(self, weather: dict, stored_units: str = "metric", convert_to: str = None):
        if convert_to is None:
            convert_to = stored_units
        temp = weather.get("temperature")
        feels_like = weather.get("feels_like")
        wind = weather.get("wind_speed")

        if stored_units != convert_to:
            temp = units_module.convert_temp(temp, stored_units, convert_to)
            feels_like = units_module.convert_temp(feels_like, stored_units, convert_to)
            wind = units_module.convert_wind_speed(wind, stored_units, convert_to)

        t_label = units_module.temp_label(convert_to)
        s_label = units_module.speed_label(convert_to)

        txt = []
        txt.append(f"City: {weather.get('city')}")
        txt.append(f"Temperature: {temp:.1f}{t_label}" if temp is not None else "Temperature: N/A")
        txt.append(f"Feels like: {feels_like:.1f}{t_label}" if feels_like is not None else "Feels like: N/A")
        txt.append(f"Humidity: {weather.get('humidity')}%")
        txt.append(f"Pressure: {weather.get('pressure')} hPa")
        txt.append(f"Wind speed: {wind:.2f} {s_label}" if wind is not None else "Wind speed: N/A")
        txt.append(f"Conditions: {weather.get('description')}")
        display_text = "\n".join(txt)

        self.weather_display.configure(state="normal")
        self.weather_display.delete("1.0", "end")
        self.weather_display.insert("1.0", display_text)
        self.weather_display.configure(state="disabled")

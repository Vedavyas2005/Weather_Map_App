from gui.main_window import MainWindow
from config import OPENWEATHER_API_KEY
import sys

if not OPENWEATHER_API_KEY:
    print("ERROR: OpenWeatherMap API key not set. Set OPENWEATHER_API_KEY in config.py or as env var.")
    sys.exit(1)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

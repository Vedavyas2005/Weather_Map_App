import customtkinter as ctk
from tkintermapview import TkinterMapView

class MapWidget(ctk.CTkFrame):
    def __init__(self, master, width=800, height=500, **kwargs):
        super().__init__(master, **kwargs)
        self.map_view = TkinterMapView(self, width=width, height=height, corner_radius=0)
        self.map_view.pack(fill="both", expand=True)
        # default location
        self.map_view.set_position(20.5937, 78.9629)  # India center
        self.map_view.set_zoom(2)
        self._current_marker = None

    def set_marker(self, lat, lon, text=""):
        # remove old marker
        if self._current_marker:
            try:
                self._current_marker.delete()
            except Exception:
                pass
            self._current_marker = None
        self._current_marker = self.map_view.set_marker(lat, lon, text=text)
        self.map_view.set_position(lat, lon)
        # set zoom to city-appropriate value
        self.map_view.set_zoom(10)

    def zoom_in(self):
        self.map_view.set_zoom(self.map_view.zoom + 1)

    def zoom_out(self):
        self.map_view.set_zoom(max(self.map_view.zoom - 1, 1))

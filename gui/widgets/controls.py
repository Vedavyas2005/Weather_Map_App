import customtkinter as ctk

class ControlsFrame(ctk.CTkFrame):
    def __init__(self, master, search_callback, zoom_in_callback, zoom_out_callback,
                 theme_callback, unit_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.search_callback = search_callback
        self.theme_callback = theme_callback
        self.unit_callback = unit_callback

        self.search_entry = ctk.CTkEntry(self, placeholder_text="Enter city name")
        self.search_entry.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

        self.search_btn = ctk.CTkButton(self, text="Search & Pin", command=self._on_search)
        self.search_btn.grid(row=0, column=1, padx=8, pady=8)

        self.zoom_in = ctk.CTkButton(self, text="+ Zoom In", command=zoom_in_callback)
        self.zoom_in.grid(row=1, column=0, padx=8, pady=4, sticky="ew")
        self.zoom_out = ctk.CTkButton(self, text="- Zoom Out", command=zoom_out_callback)
        self.zoom_out.grid(row=1, column=1, padx=8, pady=4, sticky="ew")

        self.theme_var = ctk.BooleanVar(value=(ctk.get_appearance_mode() == "dark"))
        self.theme_toggle = ctk.CTkSwitch(
            self, text="Dark Mode", command=self._on_theme_toggle, variable=self.theme_var
        )
        self.theme_toggle.grid(row=2, column=0, padx=8, pady=8, sticky="w")

        self.unit_var = ctk.StringVar(value="metric")
        self.unit_btn = ctk.CTkComboBox(self, values=["metric", "imperial"], command=self._on_unit_change)
        self.unit_btn.set("metric")
        self.unit_btn.grid(row=2, column=1, padx=8, pady=8, sticky="ew")

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, columnspan=2, padx=8, pady=4, sticky="w")

        self.columnconfigure(0, weight=1)

    def _on_search(self):
        text = self.search_entry.get().strip()
        if not text:
            self.set_status("Enter a city name")
            return
        self.search_callback(text)

    def _on_theme_toggle(self, _=None):
        v = self.theme_var.get()
        mode = "dark" if v else "light"
        self.theme_callback(mode)

    def _on_unit_change(self, value):
        self.unit_callback(value)

    def set_status(self, txt: str):
        self.status_label.configure(text=txt)

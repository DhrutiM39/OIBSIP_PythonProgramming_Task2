import tkinter as tk
from datetime import datetime, timezone, timedelta
from config import UNITS
import api_handler
from design_system import COLORS, FONTS, make_button, make_entry, center_window, show_status

# Universal BG Theme Mapping
BG_THEMES = {
    "clear"   : {"bg": "#f59e0b", "card": "#d97706", "text_primary": "#ffffff", "text_secondary": "#fef3c7", "emoji": "☀️"},
    "cloud"   : {"bg": "#334155", "card": "#1e293b", "text_primary": "#ffffff", "text_secondary": "#cbd5e1", "emoji": "☁️"},
    "rain"    : {"bg": "#1e40af", "card": "#1e3a8a", "text_primary": "#ffffff", "text_secondary": "#93c5fd", "emoji": "🌧️"},
    "thunder" : {"bg": "#1e1b4b", "card": "#312e81", "text_primary": "#ffffff", "text_secondary": "#c7d2fe", "emoji": "🌩️"},
    "snow"    : {"bg": "#bae6fd", "card": "#93c5fd", "text_primary": "#0f172a", "text_secondary": "#334155", "emoji": "❄️"},
    "default" : {"bg": "#0f0f1a", "card": "#1a1a2e", "text_primary": "#ffffff", "text_secondary": "#94a3b8", "emoji": "🌈"}
}


class WeatherApp:
    """Main weather application class encapsulating all UI and state logic"""
    
    def __init__(self):
        """Initialize the weather app with all instance variables"""
        # Main window
        self.window = tk.Tk()
        self.window.title("🌦️ Weather App")
        center_window(self.window, 480, 720)
        self.window.resizable(False, False)
        self.window.configure(bg=COLORS["bg_dark"])
        
        # Search UI elements
        self.entry = None
        self.search_btn = None
        self.status_label = None
        self.last_updated_label = None
        self.last_searched_city = ""
        
        # Main weather card elements
        self.title_label = None
        self.search_frame = None
        self.info_card = None
        self.header_label = None
        self.temp_label = None
        self.feels_label = None
        
        # Stat cards (now as tuples for consistency)
        self.stat_humidity_card = None
        self.stat_wind_card = None
        self.stat_pressure_card = None
        
        # Sunrise/Sunset elements
        self.sun_card = None
        self.sunrise_lbl = None
        self.sunset_lbl = None
        self.sunrise_time_lbl = None
        self.sunset_time_lbl = None
        
        # Forecast elements
        self.forecast_frame = None
        self.forecast_cards = []  # items of (card_frame, day_lbl, emoji_lbl, temp_lbl)
    
    def format_local_time(self, timestamp, offset_seconds):
        """Helper to format UTC timestamps correctly into target city's timezone"""
        try:
            if timestamp is None:
                return "--:--"
            tz = timezone(timedelta(seconds=offset_seconds))
            dt = datetime.fromtimestamp(timestamp, tz=tz)
            return dt.strftime("%H:%M")
        except Exception:
            return "--:--"
    
    def recolor_ui(self, theme):
        """Dynamically updates the theme background & foreground across all widgets"""
        # Main Window
        self.window.configure(bg=theme["bg"])
        self.title_label.config(bg=theme["bg"], fg=theme["text_primary"])
        
        # Search frame
        self.search_frame.config(bg=theme["card"])
        
        # Status & Time labels
        self.status_label.config(bg=theme["bg"])
        self.last_updated_label.config(bg=theme["bg"], fg=theme["text_secondary"])
        
        # Core Info Card
        self.info_card.config(bg=theme["card"])
        self.header_label.config(bg=theme["card"], fg=theme["text_primary"])
        self.temp_label.config(bg=theme["card"], fg=theme["text_primary"])
        self.feels_label.config(bg=theme["card"], fg=theme["text_secondary"])
        
        # Recolor Mini Stat Cards (standardized tuple unpacking)
        for card, title, val in [self.stat_humidity_card, self.stat_wind_card, self.stat_pressure_card]:
            card.config(bg=theme["bg"])
            title.config(bg=theme["bg"], fg=theme["text_secondary"])
            val.config(bg=theme["bg"], fg=theme["text_primary"])
            
        # Recolor Sun Times Card
        self.sun_card.config(bg=theme["card"])
        self.sunrise_lbl.config(bg=theme["card"], fg=theme["text_secondary"])
        self.sunset_lbl.config(bg=theme["card"], fg=theme["text_secondary"])
        self.sunrise_time_lbl.config(bg=theme["card"], fg=theme["text_primary"])
        self.sunset_time_lbl.config(bg=theme["card"], fg=theme["text_primary"])
        
        # Recolor 5-Day Forecast Panel
        self.forecast_frame.config(bg=theme["bg"])
        for f_card, day_l, emoji_l, temp_l in self.forecast_cards:
            f_card.config(bg=theme["card"])
            day_l.config(bg=theme["card"], fg=theme["text_secondary"])
            emoji_l.config(bg=theme["card"], fg=theme["text_primary"])
            temp_l.config(bg=theme["card"], fg=theme["text_primary"])
    
    def get_theme_by_condition(self, condition):
        """Maps condition text to BG_THEMES keys"""
        condition = condition.lower()
        if "clear" in condition:      return BG_THEMES["clear"]
        if "cloud" in condition:      return BG_THEMES["cloud"]
        if "rain" in condition or "drizzle" in condition:       return BG_THEMES["rain"]
        if "thunder" in condition:    return BG_THEMES["thunder"]
        if "snow" in condition:       return BG_THEMES["snow"]
        return BG_THEMES["default"]
    
    def search_weather(self):
        """Handles search button trigger and queries api"""
        city = self.entry.get().strip()
        if city == "Enter city name" or not city:
            city = ""
        result = api_handler.validate_input(city)
        
        if result != "ok":
            show_status(self.status_label, result, COLORS["danger"])
            return
            
        self.fetch_data(city)
    
    def auto_refresh(self):
        """Performs background weather auto-refresh every 60s"""
        if self.last_searched_city:
            self.fetch_data(self.last_searched_city, is_auto=True)
        self.window.after(60000, self.auto_refresh)
    
    def fetch_data(self, city, is_auto=False):
        """Triggers data fetching with loader states for both weather and forecast"""
        if not is_auto:
            self.search_btn.config(text="Loading...")
            # Set forecast cards to loading state
            self.set_forecast_loading()
            self.window.update()
            
        weather, error_msg = api_handler.get_weather(city, UNITS)
        
        if weather:
            self.last_searched_city = city
            self.display_weather_gui(weather)
            
            forecast, _ = api_handler.get_forecast(city, UNITS)
            if forecast:
                self.display_forecast_gui(forecast)
                
            show_status(self.status_label, "✅ Data loaded successfully!", COLORS["success"])
            now = datetime.now().strftime("%H:%M:%S")
            self.last_updated_label.config(text=f"🕐 Last updated: {now}")
        else:
            show_status(self.status_label, error_msg, COLORS["danger"])
            
        if not is_auto:
            self.search_btn.config(text="🔍 Search")
    
    def set_forecast_loading(self):
        """Set all forecast cards to loading state with ... placeholder"""
        for card, day_lbl, emoji_lbl, temp_lbl in self.forecast_cards:
            day_lbl.config(text="...")
            emoji_lbl.config(text="⏳")
            temp_lbl.config(text="...")
    
    def display_weather_gui(self, weather):
        """Binds the raw data to the current weather card widgets"""
        emoji = api_handler.get_weather_emoji(weather["condition"])
        unit_symbol = "°C" if UNITS == "metric" else "°F"
        speed_unit = "m/s" if UNITS == "metric" else "mph"
        
        # 1. Update Core Card values
        self.header_label.config(text=f"{weather['city']}, {weather['country']}")
        self.temp_label.config(text=f"{weather['temperature']}{unit_symbol}")
        self.feels_label.config(text=f"Feels like: {weather['feels_like']}{unit_symbol} • {weather['condition'].title()}")
        
        # 2. Update Mini Stat Cards (standardized tuple unpacking)
        card_h, title_h, val_h = self.stat_humidity_card
        val_h.config(text=f"{weather['humidity']}%")
        
        card_w, title_w, val_w = self.stat_wind_card
        val_w.config(text=f"{weather['wind_speed']}{speed_unit}")
        
        card_p, title_p, val_p = self.stat_pressure_card
        val_p.config(text=f"{weather['pressure']}hPa")
        
        # 3. Update Sun Times Corrected for Searched timezone
        sunrise_str = self.format_local_time(weather["sunrise"], weather["timezone"])
        sunset_str = self.format_local_time(weather["sunset"], weather["timezone"])
        self.sunrise_time_lbl.config(text=sunrise_str)
        self.sunset_time_lbl.config(text=sunset_str)
        
        # 4. Trigger Recoloring based on new condition
        theme = self.get_theme_by_condition(weather["condition"])
        self.recolor_ui(theme)
    
    def display_forecast_gui(self, forecast):
        """Binds the raw forecast data to the 5 forecast cards"""
        for i, data in enumerate(forecast):
            if i < len(self.forecast_cards):
                _, day_lbl, emoji_lbl, temp_lbl = self.forecast_cards[i]
                day_lbl.config(text=data['day'])
                emoji_lbl.config(text=data['emoji'])
                temp_lbl.config(text=f"{data['temp']}°")
    
    def build_mini_stat_card(self, parent, icon, label):
        """Builds a premium mini card for single metric, returns standardized tuple"""
        card_frame = tk.Frame(parent, bg=COLORS["bg_surface"], padx=5, pady=8)
        
        title_lbl = tk.Label(card_frame, text=f"{icon} {label}", font=FONTS["small"], bg=COLORS["bg_surface"], fg=COLORS["text_secondary"])
        title_lbl.pack()
        
        val_lbl = tk.Label(card_frame, text="-", font=("Segoe UI", 12, "bold"), bg=COLORS["bg_surface"], fg=COLORS["text_primary"])
        val_lbl.pack(pady=(2, 0))
        
        return card_frame, title_lbl, val_lbl
    
    def build_window(self):
        """Builds the Tkinter window widgets and styles them with unified layout"""
        # Title Label
        self.title_label = tk.Label(self.window, text="🌦️ Weather App", font=FONTS["title"], bg=COLORS["bg_dark"], fg=COLORS["text_primary"])
        self.title_label.pack(pady=(20, 10))

        # Search Bar Card
        self.search_frame = tk.Frame(self.window, bg=COLORS["bg_card"], padx=10, pady=10)
        self.search_frame.pack(pady=10, fill=tk.X, padx=25)

        self.entry = make_entry(self.search_frame, placeholder="Enter city name")
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, ipady=4)
        self.entry.bind("<Return>", lambda e: self.search_weather())

        self.search_btn = make_button(self.search_frame, "🔍 Search", self.search_weather, style="secondary")
        self.search_btn.pack(side=tk.LEFT, padx=5)

        # Main Weather Info Card
        self.info_card = tk.Frame(self.window, bg=COLORS["bg_card"], padx=20, pady=15)
        self.info_card.pack(fill=tk.BOTH, expand=True, padx=25, pady=5)

        self.header_label = tk.Label(self.info_card, text="Search for a city", font=FONTS["heading"], bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        self.header_label.pack(pady=(5, 0))

        self.temp_label = tk.Label(self.info_card, text="--°C", font=("Segoe UI", 42, "bold"), bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        self.temp_label.pack(pady=5)

        self.feels_label = tk.Label(self.info_card, text="Search to reveal conditions", font=FONTS["body"], bg=COLORS["bg_card"], fg=COLORS["text_secondary"])
        self.feels_label.pack(pady=(0, 10))

        # Stats Row (3 Side-by-Side Cards)
        stats_row_frame = tk.Frame(self.info_card, bg=COLORS["bg_card"])
        stats_row_frame.pack(fill=tk.X, pady=10)
        stats_row_frame.columnconfigure(0, weight=1)
        stats_row_frame.columnconfigure(1, weight=1)
        stats_row_frame.columnconfigure(2, weight=1)

        card_h, title_h, val_h = self.build_mini_stat_card(stats_row_frame, "💧", "Humidity")
        card_h.grid(row=0, column=0, sticky="ew", padx=(0, 4))
        self.stat_humidity_card = (card_h, title_h, val_h)

        card_w, title_w, val_w = self.build_mini_stat_card(stats_row_frame, "💨", "Wind")
        card_w.grid(row=0, column=1, sticky="ew", padx=2)
        self.stat_wind_card = (card_w, title_w, val_w)

        card_p, title_p, val_p = self.build_mini_stat_card(stats_row_frame, "🔵", "Pressure")
        card_p.grid(row=0, column=2, sticky="ew", padx=(4, 0))
        self.stat_pressure_card = (card_p, title_p, val_p)

        # Sun-Times Row Panel
        self.sun_card = tk.Frame(self.info_card, bg=COLORS["bg_card"], pady=5)
        self.sun_card.pack(fill=tk.X, pady=(10, 5))

        sunrise_side = tk.Frame(self.sun_card, bg=COLORS["bg_card"])
        sunrise_side.pack(side=tk.LEFT, expand=True)
        self.sunrise_lbl = tk.Label(sunrise_side, text="🌅 Sunrise", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_secondary"])
        self.sunrise_lbl.pack()
        self.sunrise_time_lbl = tk.Label(sunrise_side, text="--:--", font=FONTS["heading"], bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        self.sunrise_time_lbl.pack(pady=2)

        sunset_side = tk.Frame(self.sun_card, bg=COLORS["bg_card"])
        sunset_side.pack(side=tk.RIGHT, expand=True)
        self.sunset_lbl = tk.Label(sunset_side, text="🌇 Sunset", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_secondary"])
        self.sunset_lbl.pack()
        self.sunset_time_lbl = tk.Label(sunset_side, text="--:--", font=FONTS["heading"], bg=COLORS["bg_card"], fg=COLORS["text_primary"])
        self.sunset_time_lbl.pack(pady=2)

        # 5-Day Forecast Row (Below Main Card)
        self.forecast_frame = tk.Frame(self.window, bg=COLORS["bg_dark"])
        self.forecast_frame.pack(pady=(15, 10), fill=tk.X, padx=25)
        
        for i in range(5):
            f_card = tk.Frame(self.forecast_frame, bg=COLORS["bg_card"], padx=5, pady=8)
            f_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if i == 0 else 5, 0))
            
            day_lbl = tk.Label(f_card, text="-", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_secondary"])
            day_lbl.pack()
            
            emoji_lbl = tk.Label(f_card, text="-", font=("Segoe UI", 16), bg=COLORS["bg_card"], fg=COLORS["text_primary"])
            emoji_lbl.pack(pady=2)
            
            temp_lbl = tk.Label(f_card, text="-", font=FONTS["small"], bg=COLORS["bg_card"], fg=COLORS["text_primary"])
            temp_lbl.pack()
            
            self.forecast_cards.append((f_card, day_lbl, emoji_lbl, temp_lbl))

        # Bottom status displays
        self.status_label = tk.Label(self.window, text="", font=FONTS["heading"], bg=COLORS["bg_dark"])
        self.status_label.pack(side=tk.BOTTOM, pady=(2, 5))
        
        self.last_updated_label = tk.Label(self.window, text="", font=FONTS["small"], bg=COLORS["bg_dark"], fg=COLORS["text_muted"])
        self.last_updated_label.pack(side=tk.BOTTOM, pady=2)

        # Start auto-refresh timer
        self.window.after(60000, self.auto_refresh)
        
        # Initialize with default theme styling
        self.recolor_ui(BG_THEMES["default"])
    
    def run(self):
        """Start the application main loop"""
        self.build_window()
        self.window.mainloop()


def build_window():
    """Entry point: instantiate and run the WeatherApp"""
    app = WeatherApp()
    app.run()

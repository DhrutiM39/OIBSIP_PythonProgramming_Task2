# Weather App 🌦️

A beautiful Python desktop weather application with live updates, dynamic theming, and a 5-day forecast. Built with tkinter and the OpenWeatherMap API.

---

## 📌 Objective
To create a real-time weather monitoring application using the OpenWeatherMap API that displays current weather conditions and a 5-day forecast, with a dynamic color theme that adapts automatically to the local weather condition.

---

## 🛠️ Tools Used
- **Language**: Python 3.7+
- **GUI Framework**: Tkinter
- **APIs**: OpenWeatherMap API (Current Weather and 5-Day Forecast endpoints)
- **Libraries**: `requests` (for HTTP requests), `python-dotenv` (for API key security)

---

## 📝 Steps Performed
1. **Configured API Communication** — Created `api_handler.py` to send asynchronous HTTP requests to OpenWeatherMap's Geocoding, Current Weather, and 5-Day Forecast endpoints.
2. **Built the GUI Dashboard** — Designed a cards-based Tkinter GUI in `gui.py` with custom styles defined in `design_system.py`.
3. **Programmed Dynamic Theming** — Added logic to update background and card color gradients depending on the weather status returned (clear sky, rain, snow, thunder, clouds).
4. **Added Units & Calculations** — Implemented unit swapping (Celsius/Fahrenheit) and calculated local time transformations from UTC offsets to compute localized sunrise/sunset times.
5. **Configured Security** — Kept API secrets separate by integrating `python-dotenv` to fetch keys from a git-ignored `.env` file.

---

## ⚡ Features


- **🌡️ Live Weather Updates** — Real-time temperature, humidity, wind speed, and pressure  
- **🎨 Dynamic Theming** — UI colors automatically change based on weather conditions (sunny, cloudy, rainy, snowy, thunderstorm)  
- **📅 5-Day Forecast** — Mini-cards showing daily weather at a glance  
- **🌅 Sunrise & Sunset Times** — Adjusted for the city's local timezone  
- **🔄 Auto-Refresh** — Updates weather data every 60 seconds automatically  
- **⚡ Error Handling** — Friendly messages for network issues, invalid cities, and API errors  
- **🎯 Metric & Imperial Units** — Switch between Celsius/Fahrenheit and m/s/mph  

## 📋 Prerequisites

- Python 3.7+  
- pip (Python package manager)

## 🚀 Setup

### 1. Get a Free OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)  
2. Click **Sign Up** (or **Sign In** if you have an account)  
3. Create a free account and verify your email  
4. Go to **API keys** section in your account dashboard  
5. Copy your **Default API Key** (it's already generated for you)  

### 2. Install Dependencies

```bash
pip install requests python-dotenv
```

### 3. Create the `.env` File

In the project root directory, create a file named `.env` and add your API key:

```
OPENWEATHER_API_KEY=your_api_key_here
```

**Example:**
```
OPENWEATHER_API_KEY=your_api_key_here
```

⚠️ **Important:** Never commit the `.env` file to GitHub. It's already in `.gitignore`.

### 4. Run the Application

```bash
python main.py
```

## 🎮 How to Use

1. **Search for a City** — Type a city name (e.g., "London", "New York") and press Enter or click the search button  
2. **View Weather Details** — The main card shows temperature, feels-like temp, and conditions  
3. **Check Stats** — Humidity, wind speed, and pressure are displayed in mini-cards  
4. **See Sunrise/Sunset** — Times are automatically adjusted for the city's timezone  
5. **View 5-Day Forecast** — Scroll down to see upcoming weather at a glance  
6. **Auto-Refresh** — The app updates every 60 seconds (when a city is selected)  

## 📁 Project Structure

```
.
├── main.py                 # Entry point — starts the application
├── gui.py                  # Tkinter UI logic & WeatherApp class
├── api_handler.py          # OpenWeatherMap API integration
├── config.py               # Configuration & environment variables
├── design_system.py        # Reusable UI components & styling
├── .env                    # API key (DO NOT COMMIT)
├── .gitignore              # Prevents .env from being committed
└── README.md               # This file
```

## 🛠️ Architecture

- **gui.py** — `WeatherApp` class encapsulates all UI state and methods  
- **api_handler.py** — Clean separation of API calls from UI logic  
- **config.py** — Loads sensitive data (API key) from `.env` using `python-dotenv`  
- **design_system.py** — Centralized colors, fonts, and reusable widget builders  

## 🎨 Theme Colors

The app dynamically adjusts its background and card colors based on weather:

| Weather | Theme |
|---------|-------|
| ☀️ Clear | Warm Orange |
| ☁️ Cloudy | Cool Gray |
| 🌧️ Rainy | Deep Blue |
| ❄️ Snow | Light Blue |
| 🌩️ Thunderstorm | Dark Purple |

## ⚠️ Common Issues

**"API key not found" error**  
→ Make sure `.env` file exists in the same folder as `main.py` with your API key

**"City not found" error**  
→ Try full city names with country codes, e.g., "London, UK" or "Paris, FR"

**"No internet connection" error**  
→ Check your internet and ensure the API endpoint is accessible

## 📦 Dependencies

- **tkinter** — Built-in GUI framework (no install needed)  
- **requests** — HTTP library for API calls  
- **python-dotenv** — Load environment variables from `.env`  

## 📝 License

This project is open source and available for personal and educational use.

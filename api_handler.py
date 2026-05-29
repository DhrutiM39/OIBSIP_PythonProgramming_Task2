import requests
from datetime import datetime
from config import API_KEY, BASE_URL, FORECAST_URL

def validate_input(city):
    if not city:
        return "Error: City name cannot be empty!"
    if any(char.isdigit() for char in city):
        return "Error: City name cannot contain numbers!"
    return "ok"

def get_weather_emoji(condition):
    condition = condition.lower()
    if "clear" in condition:      return "☀️"
    if "cloud" in condition:      return "☁️"
    if "rain" in condition:       return "🌧️"
    if "drizzle" in condition:    return "🌦️"
    if "thunder" in condition:    return "🌩️"
    if "snow" in condition:       return "❄️"
    if "mist" in condition:       return "🌫️"
    if "haze" in condition:       return "🌫️"
    if "fog" in condition:        return "🌫️"
    return "🌈"

def get_bg_color(condition):
    condition = condition.lower()
    if "clear" in condition:    return "#f59e0b"  # warm yellow
    if "cloud" in condition:    return "#64748b"  # cool gray
    if "rain" in condition:     return "#1e40af"  # deep blue
    if "thunder" in condition:  return "#1e1b4b"  # dark purple
    if "snow" in condition:     return "#e0f2fe"  # light blue
    return "#1e1e2e"                              # default dark

def get_weather(city, units):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "city"        : data["name"],
            "country"     : data["sys"]["country"],
            "temperature" : data["main"]["temp"],
            "feels_like"  : data["main"]["feels_like"],
            "humidity"    : data["main"]["humidity"],
            "condition"   : data["weather"][0]["description"],
            "wind_speed"  : data["wind"]["speed"],
            "pressure"    : data["main"]["pressure"],
            "visibility"  : data.get("visibility", "N/A"),
            "sunrise"     : data["sys"].get("sunrise"),
            "sunset"      : data["sys"].get("sunset"),
            "timezone"    : data.get("timezone", 0)
        }, "ok"
    except requests.exceptions.ConnectionError:
        return None, "⚠️  No internet connection!"
    except requests.exceptions.Timeout:
        return None, "⚠️  Request timed out! Try again."
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return None, "❌ City not found!"
        return None, f"⚠️  API Error: {response.status_code}"
    except Exception as e:
        return None, "⚠️  Unknown Error occurred."

def get_forecast(city, units):
    url = f"{FORECAST_URL}?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        forecast_list = []
        for i in range(0, len(data['list']), 8):
            item = data['list'][i]
            dt = datetime.fromtimestamp(item['dt'])
            day_name = dt.strftime("%a")
            
            condition = item['weather'][0]['description']
            emoji = get_weather_emoji(condition)
            temp = round(item['main']['temp'])
            
            forecast_list.append({
                "day": day_name,
                "emoji": emoji,
                "temp": temp
            })
            
            if len(forecast_list) == 5:
                break
                
        return forecast_list, "ok"
    except Exception:
        return None, "⚠️  Failed to fetch forecast."

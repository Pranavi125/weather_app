import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import datetime
import io

# -------------------------------
# CONFIGURATION
# -------------------------------
API_KEY = "b979b0f8c15ce97545468d83357cfaf4"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# -------------------------------
# MAIN WINDOW
# -------------------------------
root = tk.Tk()
root.title("Weather App")
root.geometry("520x400")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

# -------------------------------
# SEARCH BAR
# -------------------------------
search_frame = tk.Frame(root, bg="#f2f2f2")
search_frame.pack(pady=15)

city_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 14),
    width=25,
    bd=0,
    relief="flat",
    justify="center"
)
city_entry.insert(0, "delhi")
city_entry.pack(side="left", padx=5)

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Enter city name")
        return

    try:
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=30)

        if response.status_code != 200:
            messagebox.showerror("Error", "Unable to fetch weather data")
            return

        data = response.json()
        update_ui(data)

    except requests.exceptions.ConnectTimeout:
        messagebox.showerror(
            "Network Error",
            "Connection timed out.\nPlease check your internet connection."
        )

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", str(e))

search_btn = tk.Button(
    search_frame,
    text="🔍",
    font=("Segoe UI", 12),
    bd=0,
    command=get_weather
)
search_btn.pack(side="left")

# -------------------------------
# WEATHER INFO
# -------------------------------
weather_frame = tk.Frame(root, bg="#f2f2f2")
weather_frame.pack()

time_label = tk.Label(
    weather_frame,
    text="CURRENT WEATHER",
    font=("Segoe UI", 10, "bold"),
    bg="#f2f2f2"
)
time_label.pack()

clock_label = tk.Label(
    weather_frame,
    text="",
    font=("Segoe UI", 10),
    bg="#f2f2f2"
)
clock_label.pack()

# -------------------------------
# CENTER DISPLAY
# -------------------------------
center_frame = tk.Frame(root, bg="#f2f2f2")
center_frame.pack(pady=15)

icon_label = tk.Label(center_frame, bg="#f2f2f2")
icon_label.pack(side="left", padx=10)

temp_frame = tk.Frame(center_frame, bg="#f2f2f2")
temp_frame.pack(side="left")

temp_label = tk.Label(
    temp_frame,
    text="--°",
    font=("Segoe UI", 40, "bold"),
    fg="#ff4d4d",
    bg="#f2f2f2"
)
temp_label.pack(anchor="w")

desc_label = tk.Label(
    temp_frame,
    text="",
    font=("Segoe UI", 12),
    bg="#f2f2f2"
)
desc_label.pack(anchor="w")

feels_label = tk.Label(
    temp_frame,
    text="",
    font=("Segoe UI", 10),
    bg="#f2f2f2"
)
feels_label.pack(anchor="w")

# -------------------------------
# BOTTOM INFO PANEL
# -------------------------------
bottom_frame = tk.Frame(root, bg="#2aa9e0")
bottom_frame.pack(fill="x", pady=10)

def info_block(parent, title):
    frame = tk.Frame(parent, bg="#2aa9e0")
    frame.pack(side="left", expand=True, fill="both", padx=10, pady=10)

    tk.Label(
        frame,
        text=title,
        font=("Segoe UI", 10, "bold"),
        bg="#2aa9e0",
        fg="white"
    ).pack()

    value_label = tk.Label(
        frame,
        text="--",
        font=("Segoe UI", 11),
        bg="#2aa9e0",
        fg="white"
    )
    value_label.pack()

    return value_label

wind_value = info_block(bottom_frame, "WIND")
humidity_value = info_block(bottom_frame, "HUMIDITY")
desc2_value = info_block(bottom_frame, "DESCRIPTION")
pressure_value = info_block(bottom_frame, "PRESSURE")

# -------------------------------
# UPDATE UI FUNCTION
# -------------------------------
def update_ui(data):
    temp = int(data["main"]["temp"])
    feels = int(data["main"]["feels_like"])
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]
    icon_code = data["weather"][0]["icon"]

    now = datetime.datetime.now().strftime("%I:%M %p")
    clock_label.config(text=now)

    temp_label.config(text=f"{temp}°")
    desc_label.config(text=description.capitalize())
    feels_label.config(text=f"Feels like {feels}°")

    wind_value.config(text=f"{wind} m/s")
    humidity_value.config(text=f"{humidity} %")
    desc2_value.config(text=description.capitalize())
    pressure_value.config(text=f"{pressure} hPa")

    try:
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        img_data = requests.get(icon_url, timeout=30).content
        img = Image.open(io.BytesIO(img_data)).resize((90, 90))
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
    except:
        icon_label.config(image="")

# -------------------------------
# RUN APP
# -------------------------------
root.mainloop()

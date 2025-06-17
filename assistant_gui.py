import tkinter as tk
import pyttsx3
import datetime
import requests

# Text-to-speech setup
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Weather API Function
def get_weather(city):
    api_key = "3072f421eb11f13eb0d71b0f9f1ed2a4"  # Your working OpenWeatherMap key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Error: {data.get('message', 'City not found')}"

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"{city.title()} has {weather} with {temp}°C"

# News API Function
def get_news():
    api_key = "your_newsapi_key"  # Replace with a real NewsAPI key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return "Could not fetch news."

    articles = data.get("articles", [])[:5]
    headlines = [f"{i+1}. {article.get('title', 'No Title')}" for i, article in enumerate(articles)]
    return "\n".join(headlines) if headlines else "No news found."

# Main Logic
def respond():
    command = input_box.get().strip().lower()
    output = ""

    if not command:
        output = "Please type a command like: time, date, news, weather, city [name]"
    elif 'time' in command:
        output = f"Current time is {datetime.datetime.now().strftime('%I:%M %p')}"
    elif 'date' in command:
        output = f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}"
    elif 'weather' in command:
        output = "Type 'city [city name]' to get weather."
    elif command.startswith("city"):
        city = command.replace("city", "").strip()
        if city:
            output = get_weather(city)
        else:
            output = "Please specify a city name, e.g. city Karachi"
    elif 'news' in command:
        output = get_news()
    elif 'exit' in command or 'bye' in command:
        root.quit()
        return
    else:
        output = "Try: time, date, news, weather, or city [name]"

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output)
    speak(output)

# GUI
root = tk.Tk()
root.title("Personal Assistant Bot")
root.geometry("500x400")

title = tk.Label(root, text="Your Python Assistant", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

input_box = tk.Entry(root, font=("Helvetica", 14), width=40)
input_box.pack(pady=10)

submit_btn = tk.Button(root, text="Submit", font=("Helvetica", 12), command=respond)
submit_btn.pack(pady=5)

output_box = tk.Text(root, height=10, width=50, font=("Helvetica", 12))
output_box.pack(pady=10)

root.mainloop()

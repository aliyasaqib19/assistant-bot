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
    api_key = "3072f421eb11f13eb0d71b0f9f1ed2a4"  # Your OpenWeatherMap key
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
    api_key = "your_newsapi_key"  # Replace with actual key
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

    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output)
    output_box.config(state='disabled')
    speak(output)

# GUI Setup
root = tk.Tk()
root.title("Personal Assistant Bot")
root.geometry("650x500")
root.configure(bg="#1e1e2f")  # Dark background

# Fonts and Colors
FONT_MAIN = ("Segoe UI", 12)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_OUTPUT = ("Consolas", 11)
COLOR_PRIMARY = "#00e676"
COLOR_BG = "#1e1e2f"
COLOR_ENTRY = "#2e2e3f"
COLOR_TEXT = "#ffffff"

# Title
title = tk.Label(root, text="💡 Python Assistant Bot", font=FONT_TITLE, fg=COLOR_PRIMARY, bg=COLOR_BG)
title.pack(pady=20)

# Input Frame
input_frame = tk.Frame(root, bg=COLOR_BG)
input_frame.pack(pady=10)

input_box = tk.Entry(input_frame, font=FONT_MAIN, width=40, bd=0,
                     bg=COLOR_ENTRY, fg=COLOR_TEXT, insertbackground=COLOR_TEXT)
input_box.grid(row=0, column=0, padx=10, ipady=6)

submit_btn = tk.Button(input_frame, text="➤ Ask", font=("Segoe UI", 11, "bold"),
                       bg=COLOR_PRIMARY, fg="black", activebackground="#00c853", padx=15,
                       command=respond, relief="flat", cursor="hand2")
submit_btn.grid(row=0, column=1, padx=5)

# Output Label
output_label = tk.Label(root, text="💬 Response:", font=("Segoe UI", 11), bg=COLOR_BG, fg="#aaa")
output_label.pack(pady=(20, 5))

# Output Box
output_box = tk.Text(root, height=12, width=70, font=FONT_OUTPUT, wrap=tk.WORD,
                     bd=0, relief="flat", bg="#282c34", fg=COLOR_TEXT)
output_box.pack()
output_box.config(state='disabled')

# Footer
footer = tk.Label(root, text="Try: time, date, news, weather, or city [name]",
                  font=("Segoe UI", 9), bg=COLOR_BG, fg="#666")
footer.pack(pady=15)

root.mainloop()

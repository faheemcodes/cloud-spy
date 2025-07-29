"""
Weather App named Cloud-Spy - Python Assignment
Name: Faheem Ahmed
Roll No: 2k23/SWE/48
Course: Python Programming
"""

from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    weather = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        if city and city.strip():
            try:
                response = requests.get(
                    f"{"http://api.openweathermap.org/data/2.5/weather"}?q={city}&appid={"ee85f106df44a1d1dd3b1306090491d4"}&units=metric" )
                
                if response.status_code == 200:
                    data = response.json()
                    weather = {
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'temp': round(data['main']['temp']),
                        'feels_like': round(data['main']['feels_like']),
                        'humidity': data['main']['humidity'],
                        'wind': round(data['wind']['speed'] * 3.6, 1),
                        'description': data['weather'][0]['description'].capitalize(),
                        'icon': data['weather'][0]['icon'],
                        'time': datetime.now().strftime("%H:%M")
                    }
                else:
                    error = f"Weather data not found for {city}"
                    
            except Exception as e:
                error = "Service temporarily unavailable"
                print(f"API Error: {e}")
        else:
            error = "Please enter a city name"
    
    return render_template('weather.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)
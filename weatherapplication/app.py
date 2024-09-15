from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '1785c126f4d3a40fa6323ad6296b2a0a'  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    complete_url = f"{BASE_URL}appid={API_KEY}&q={city}&units=metric"
    
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        # Debug: Print the full response
        print("API Response:", data)

        # Check if the response contains the "main" key
        if data.get("cod") == 200:  # Check if the status code is 200 (OK)
            if 'main' in data:  # Make sure the 'main' key exists
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'pressure': data['main']['pressure'],
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
                return render_template('index.html', weather=weather_data)
            else:
                # If 'main' is missing, it means something went wrong with the response
                error_message = "Unexpected response structure from the API."
                return render_template('index.html', error=error_message)
        else:
            # API returned an error
            error_message = f"Error from API: {data.get('message', 'Unknown error')}"
            return render_template('index.html', error=error_message)
    
    except requests.exceptions.RequestException as e:
        # Handle other requests exceptions
        error_message = f"An error occurred while making the API request: {e}"
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)

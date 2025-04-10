import requests
import time

# Your API Keys
OPENWEATHERMAP_API_KEY = 'eac7476519afa11eb143b12859c197af'
THINGSPEAK_API_KEY = 'TNO0NTFBLJ5ZKO33'

# Location for weather data
CITY = 'New York'  

def get_weather_data():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    print(" API response:", data)  

    # Check if API call was successful
    if response.status_code != 200:
        print(f" Error fetching weather data: {data.get('message', 'Unknown error')}")
        return None, None, None, None

    try:
        # Extract required data
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        return temperature, humidity, pressure, wind_speed
    except KeyError as e:
        print(f" Key error in API response: {e}")
        return None, None, None, None

def send_to_thingspeak(temp, hum, pres, wind):
    if None in [temp, hum, pres, wind]:
        print(" Incomplete data. Skipping ThingSpeak update.")
        return

    url = f'https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={temp}&field2={hum}&field3={pres}&field4={wind}'
    response = requests.get(url)
    if response.status_code == 200:
        print(" Data sent successfully to ThingSpeak!")
    else:
        print(f" Failed to send data to ThingSpeak: {response.status_code}")

def main():
    while True:
        temp, hum, pres, wind = get_weather_data()
        print(f' Data: Temp: {temp}°C, Humidity: {hum}%, Pressure: {pres} hPa, Wind Speed: {wind} m/s')
        send_to_thingspeak(temp, hum, pres, wind)

        # Fast mode for class testing: 30 seconds interval
        time.sleep(30)

if __name__ == "__main__":
    main()

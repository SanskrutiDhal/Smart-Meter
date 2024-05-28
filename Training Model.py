import threading
import logging
import sys
import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import random
from datetime import datetime
import schedule
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# authenticate to firebase
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://ipsa-a67be-default-rtdb.firebaseio.com/"})

# creating reference to root node
ref = db.reference("/")

quotes = [
    "Save electricity today, for a brighter tomorrow. 💡🌍",
    "Every watt saved is a step towards a sustainable future. ⚡🌱",
    "Conserve electricity, empower the planet. 🌍💪",
    "Be wise, energize! Save electricity, save money. 💰💡",
    "Switch off, power up! Save electricity and make a difference. ⚡🌍",
    "Small changes, big impact. Save electricity, save the planet. 🌍💡",
    "Choose to save electricity and embrace a greener lifestyle. 🌱💡",
    "Save electricity, save resources, save the world. 🌍💡💪",
    "Energy conservation starts with you. Save electricity, save the future. 💡🌍🌱",
    "Make electricity conservation a habit and contribute to a sustainable world. 🌍💡🌱",
    "💡 विद्युत् संवर्धन करो, ऊर्जा को बचाओ। ⚡️",
    "🕯️ दीपक बचाओ, बिजली की व्यर्था को रोको। ⚡️",
    "🔋 ऊर्जा की आपूर्ति छोटी है, खपत घटाओ और संवर्धन करो। ⚡️",
    "💡 बिजली की बचत करें, भविष्य की सुरक्षा करें। ⚡️",
    "💡 आओ विद्युत् की संरक्षा करें, हर एक बिजली की कण को महत्व दें। ⚡️",
    "💡 विद्युत् की बचत धर्म है, इसे पालन करो और आपदा से बचाओ। ⚡️",
    "💪💡 विद्युत् संवर्धन से होगा देश का विकास, हम सबको मिलकर करना है प्रयास। ⚡️",
    "💡 बिजली की छोड़ो व्यर्थ खपत, सुरक्षित रखो आने वाली पीढ़ी के लिए ऊर्जा बचात। ⚡️",
    "💡 विद्युत् की जरूरत के अनुसार ही खपत करो, धरती की संतानों का हो ध्यान विशेष रखो। ⚡️",
    "💡 बिजली संरक्षण ही हमारा सर्वोपरि कर्तव्य है, अब समय आया है इसे पूरा करने का। ⚡️",
    ]

data = ref.get()  # Retrieve data from Firebase
db.reference("/Hub").set(data["Energy1"]+data["Energy2"])
Limit1=15
Limit2=17
LimitHub=Limit1+Limit2

def measuring():
    c=1
    data = ref.get()  # Retrieve data from Firebase
    while True:
        voltage = random.randint(200, 240)
        voltage = round(voltage * 100) / 100.0

        current = random.uniform(0.5, 5.0)

        power = voltage * current / 1000.0
        power = round(power * 100) / 100.0

        energy = power * c
        energy = round(energy * 100) / 100.0
        c += 1
        # update operation (update existing value)
        db.reference("/").update({"E": energy})
        db.reference("/").update({"P": power})
        db.reference("/").update({"C": current})
        db.reference("/").update({"V": voltage})
        time.sleep(1)

import requests
from datetime import datetime

def get_weather(api_key, city_name):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q=Chandigarh&appid={api_key}"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # You can change to "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data["cod"] == 200:
        return data["main"], data.get("weather"), data.get("sys")
    else:
        print(f"Error: {data['message']}")
        return None, None, None

def is_daytime(sunrise, sunset):
    now = datetime.utcnow().timestamp()
    return sunrise < now < sunset

def main():
    api_key = "bbe3c6f2f9d15e66a401e405d863aa9c"  # Replace with your OpenWeatherMap API key

    city_name = "Chandigarh"  # Replace with the desired city name
    weather_data, weather_condition, sys_data = get_weather(api_key, city_name)

    if weather_data and sys_data:
        # update operation (update existing value)
        db.reference("/").update({"maxtemp": weather_data['temp_max']})
        db.reference("/").update({"mintemp": weather_data['temp_min']})
        db.reference("/").update({"temp": weather_data['temp']})
        print(f"Weather in {city_name} for the whole day:")
        print(f"Temperature: {weather_data['temp']}°C")
        print(f"Feels like: {weather_data['feels_like']}°C")
        print(f"Minimum Temperature: {weather_data['temp_min']}°C")
        print(f"Maximum Temperature: {weather_data['temp_max']}°C")
        print(f"Humidity: {weather_data['humidity']}%")

        if weather_condition:
            weather_condition_main = weather_condition[0]['main']
            db.reference("/").update({"wc": weather_condition_main})
            print(f"Weather Condition: {weather_condition_main}")

        sunrise = sys_data.get('sunrise')
        sunset = sys_data.get('sunset')

        if sunrise and sunset:
            if is_daytime(sunrise, sunset):
                print("It's nighttime.")                
                db.reference("/").update({"time": "It's nighttime."})
            else:
                print("It's daytime.")
                db.reference("/").update({"time": "It's daytime."})
        else:
            print("Sunrise and sunset data not available.")
    else:
        print("Failed to fetch weather data.")

if __name__ == "__main__":
    main()

def MesageLimit(update, context):
    while True:
        data = ref.get()  # Retrieve data from Firebase
        # update operation (update existing value)
        db.reference("/").update({"Energy1": data["Energy1"] + 5})
        db.reference("/").update({"Energy2": data["Energy2"] + 5})
        db.reference("/").update({"Hub": data["Hub"] + 10})
        
        if data["Energy1"] == Limit1 - 10:
            category = data["Energy1"]
            response = f"{category} You are reaching your consumption limit for Room1."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

        if data["Energy1"] == Limit1:
            category = data["Energy1"]
            response = f"{category} You have reached your consumption limit for Room1."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

        if data["Energy2"] == Limit2 - 10:
            category = data["Energy2"]
            response = f"{category} You are reaching your consumption limit for Room2."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

        if data["Energy2"] == Limit2:
            category = data["Energy2"]
            response = f"{category} You have reached your consumption limit for Room2."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

        if data["Hub"] == LimitHub - 10:
            category = data["Hub"]
            response = f"{category} You are reaching your consumption limit for Hub."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        if data["Hub"] == LimitHub:
            category = data["Hub"]
            response = f"{category} You have reached your consumption limit for Hub."
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        time.sleep(5)

def Mesage(update, context):
    while True:
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if(current_time == "10:00:00"):
                data = ref.get()  # Retrieve data from Firebase
                message = '{} at {} in {}'.format(data, current_time, random.choice(quotes))
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        time.sleep(1)

def Alert(update, context):
    data = ref.get()  # Retrieve data from Firebase
    # update operation (update existing value)
    db.reference("/").update({"Energy1":data["Energy1"]+5 })
    db.reference("/").update({"Energy2":data["Energy2"]+5 })
    db.reference("/").update({"Hub":data["Hub"]+10 })

    if data["PIR_State1"] == data["SecurityMode1"] == 1:
        message = "Suspicious activity at Room1"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    if data["PIR_State2"] == data["SecurityMode2"] == 1:
        message = "Suspicious activity at Room2"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

    if data["PIR_StateHub"] == data["SecurityModeHub"] == 1:
        message = "Suspicious activity at Hub"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

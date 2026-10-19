from datetime import datetime
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response  = requests.get(url,timeout=10)
    return response.text
def get_user_city():
    return "Banglore"

    #TOOLS  = [{},{},{}]
TOOLS = [
    {
        "type" : "function",
        "function": {
            "name" :"get_current_time",
            "description":"Returns the current date and time as a formated string.",
            "parameters" : {"type":"object","properties":{},}
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"Return the current weather for a given city.",
            "parameters": {
                "type":"object",
                "properties":{
                    "city": {
                    "type":"string",
                    "description":"City to get the weather for."
                    }
                },
            },
        },
    },
    {
        "type":"function",
        "function": {
            "name":"get_user_city",
            "description":"Return the city wher ethe users live. Use this when the user says 'my city','where I lived ' or 'my location','my home'without naming the city",
            "parameters":{"type":"object","properties":{}},
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_weather":get_city_weather, 
    "get_user_city":get_user_city,
}
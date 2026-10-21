from datetime import datetime
from ddgs import DDGS
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response  = requests.get(url,timeout=10)
    return response.text
def get_user_city():
    return "Banglore"

def calculate_calculator(a,b,operation):
    if operation == "add" or operation=="+" :
       return a+b
    elif operation == "subtract" or operation=="sub" or operation== "-":
        return a-b
    elif operation == "multiply" or operation=="mul" or operation=="*":
        return a*b
    elif operation == "division" or operation=="divide" or operation== "/":
        if b==0:
            return "Cannot divide by zero"
        return a/b

    else:
        return "Invalid operation"

def web_search_tool(query):
    results = DDGS().text(
        query,
        max_results = 5,
        region = "in-en"
    )
    if not results:
        return "result not found in web search"

    formatted_results = []

    for item in results:
        formatted_results.append(
            f"Title:{item.get('title','N/A')}\n"
            f"URL:{item.get('href','N/A')}\n"
            f"Snippet:{item.get('body','N/A')}"
        )
    return "\n\n".join(formatted_results)

    


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
    },
    {
        "type":"function",
        "function":     {
            "name":"calculate_calculator",
            "description":"Perform addition,subtraction,multiplication, or division .Understand natural languange request like add,sum,plus,sub,subtract,minus,multiply,mul,divide,division,div and mathematical symbol.",
            "parameters":{
                "type":"object",
                "properties":{
                    "a":{
                        "type":"number",
                        "description":"The first Number"
                    },
                    "b":{
                        "type":"number",
                        "description":"The second number"
                    },
                    "operation":{
                        "type":"string",
                        "enum":[
                            "add","+",
                            "subtract","sub","-",
                            "multiply","mul","*",
                            "division","divide","/"
                        ],
                        "description":"The matematical operation to perform"
                    }
                },
                "required":["a","b","operation"]
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name":"web_search_tool",
            "description":("Search the internet for information,"
            "recent news, technical documentation,"
            "and other topics requiring web results."
            ),
            "parameters":{
                "type":"object",
                "properties":{
                    "query":{
                        "type":"string",
                        "description":"The topic or question to search for."
                    }
                },
                "required":["query"]
            }
        }
    }
]


FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time" : get_current_time,
    "get_city_weather":get_city_weather, 
    "get_user_city":get_user_city,
    "calculate_calculator":calculate_calculator,
    "web_search_tool":web_search_tool,
}
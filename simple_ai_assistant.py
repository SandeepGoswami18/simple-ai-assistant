from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS,FUNCTION_NAME_TO_FUNCTION_MAP
import json
import os

load_dotenv()#by default look for .env file and load all these value in the environment variable 

client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve kar ke run kiya tha 
    api_key=os.getenv("API_KEY")
)
messages = []

messages.append(
    {
        "role":"system",#behaviour of the agent 
        "content":"Act Like a very humble agent and respond always under 20 words."#behaviour of the agent 
    }
)
while True:
    user_input = input("\nCodeSan:")

    if user_input.lower() in ["exit","quit","bye","goodbye"]:
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages,
        tools = TOOLS,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            func_arg = json.loads(tool_call.function.arguments or "{}")

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_arg)

            messages.append({
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content":str(result),
            })

        #2nd call to LLM API
        response = client.chat.completions.create(
            model = os.getenv("MODEL"),
            messages = messages
        )

        msg = response.choices[0].message 




    messages.append({
       "role": "assistant",
        "content":msg.content
    })

    print("Assistant: " + msg.content)
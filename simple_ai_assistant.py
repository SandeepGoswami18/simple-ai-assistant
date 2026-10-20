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

# safet limit : the max number of model rounds for ONE user operation
MAX_STEPS = 5;

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
   
    #chained tool calling  
    for step in range(MAX_STEPS):
            response = client.chat.completions.create(
                    model=os.getenv("MODEL"),
                    messages=messages,
                    tools = TOOLS,
                )
            
            msg = response.choices[0].message

            if not msg.tool_calls:
                break

            messages.append(msg)

            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                func_arg = {}

                try:
                    func_arg = json.loads(tool_call.function.arguments or "{}")
                    fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                    result = fn(**func_arg)
                except Exception as e:
                     result = f"Error while running {func_name}"
                     
                messages.append({
                    "role":"tool",
                    "tool_call_id": tool_call.id,
                    "content":str(result),
                })
    else:
        # Ran out of steps; the model never gave a final answer.
        fallback = "Sorry, I could not finish this within the step limit."
        messages.append({
            "role": "assistant",
            "content": fallback
        })
        print("Assistant: " + fallback)
        continue

    messages.append({
        "role": "assistant",
        "content": msg.content
    })
    print("Assistant: " + msg.content)
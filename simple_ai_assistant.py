#Standard library imports
import os
from types import SimpleNamespace

#Third-party imports
from openai import OpenAI
from dotenv import load_dotenv

#Local modules
from tools import TOOLS,run_tool
from Utilities.utilities import log


load_dotenv()#by default look for .env file and load all these value in the environment variable 

client = OpenAI(
    base_url=os.getenv("BASE_URL"), # ollama serve kar ke run kiya tha 
    api_key=os.getenv("API_KEY")
)
messages = []

# safet limit : the max number of model rounds for ONE user operation
MAX_STEPS = 5 

messages.append(
    {
            "role":"system",#behaviour of the agent 
            "content": (
                "You are a helpful AI agent. "
                "Use web_search when the user asks for current information "
                "or explicitly requests a web search. "
                "Summarize search results accurately and concisely."
            )
    }
)

def stream_chat(history):
    stream = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=history,
        tools=TOOLS,
        stream=True,
    )

    full_response = ""
    calls = {}
    label_printed = False

    #Streaming started
    try:
        for chunk in stream:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            #1. COntent Streaming : Do we have a content from the LLM
            if delta.content:
                if not label_printed:
                    print("🤖 Assistant: ", end="", flush=True)
                    label_printed = True
                print(delta.content , end="", flush=True)
                full_response += delta.content

            #2 tool Call
            for tc in (delta.tool_calls or []):
                obj = calls.setdefault(
                    tc.index,
                    SimpleNamespace(id=None, function=SimpleNamespace(name="", arguments="")),
                )
                if tc.id:
                    obj.id = tc.id
                if tc.function and tc.function.name:
                    obj.function.name += tc.function.name
                if tc.function and tc.function.arguments:
                    obj.function.arguments += tc.function.arguments

    except KeyboardInterrupt:
        print("\n {Stopped By You}")
        calls = {}

    if label_printed:
        print()

    calls_list = []
    for key in sorted(calls):
        calls_list.append(calls[key])

    return full_response, calls_list

def build_tool_call_payload(tool_call):
    """
    Converts our collected tool call into the dictionary formet
    that the API except inside an assistant message 
    """

    payload = []
    for tool_calls in tool_call:
        tool_call_dict = {
            "id":tool_calls.id,
            "type":"function",
            "function":{
                "name":tool_calls.function.name,
                "arguments":tool_calls.function.arguments,
            },
        }
        payload.append(tool_call_dict)

    return payload


while True:

    user_input = input("💬 You: ")

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
        full_response , tool_call = stream_chat(messages)
            
        #msg = response.choices[0].message

        if not tool_call:
            break

        log(f"Step {step+1}: model requested {len(tool_call)} tool calls")

        messages.append({
            "role":"assistant",
            "content": full_response,
            "tool_calls":build_tool_call_payload(tool_call)
        })
    
        for tool_call in tool_call:
            result = run_tool(tool_call)
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
        print("🤖 Assistant: " + fallback)
        continue

    messages.append({
        "role":"assistant",
        "content":full_response
    })
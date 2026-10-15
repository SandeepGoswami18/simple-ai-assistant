from openai import OpenAI
from dotenv import load_dotenv
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

    if user_input.lower() in ["exit","quit","Bye","goodbye"]:
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append(
            {
                "role":"Assistant",
                "content":response.choices[0].message.content
            }
        )


    print("Assistant "+response.choices[0].message.content) # Response from LLM model : qwen3:4b

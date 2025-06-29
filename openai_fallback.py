import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_openai_response(user_input: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight & free model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        print("❌ OpenAI Error:", e)
        return "Sorry, I'm having trouble right now."

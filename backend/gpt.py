from openai import OpenAI
from dotenv import load_dotenv
import os

# ✅ Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set in environment")

# ✅ Create OpenAI client
client = OpenAI(api_key=api_key)

def ask_gpt(user_health_input, history=None):
    if history is None:
        history = []

    system_prompt = {
        "role": "system",
        "content": (
            "You are a supportive and knowledgeable health assistant. "
            "You help users reflect on their physical and mental well-being, "
            "but do not diagnose or treat. Encourage the user gently and remind them to see a doctor when appropriate."
        )
    }

    history = [system_prompt] + history
    history.append({"role": "user", "content": user_health_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=history,
            temperature=0.7,
            max_tokens=2048,
            top_p=1.0
        )

        reply = response.choices[0].message.content.strip()
        print("✅ GPT response:", reply)

        history.append({"role": "assistant", "content": reply})
        return reply, history

    except Exception as e:
        print("❌ GPT call failed:", e)
        return "An error occurred while communicating with the GPT model.", history

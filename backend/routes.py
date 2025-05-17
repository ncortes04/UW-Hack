from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set in environment")

client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app) 

def ask_gpt(user_health_input, history=None):
    if history is None:
        history = []

    system_prompt = {
        "role": "system",
        "content": (
            "You are a supportive and knowledgeable health assistant. "
            "You provide general wellness feedback and encouragement based on what users say. "
            "You never diagnose or treat — always recommend seeing a doctor if needed."
        )
    }

    history = [system_prompt] + history
    history.append({"role": "user", "content": user_health_input})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=history,
            temperature=0.7,
            max_tokens=2048,
            top_p=1.0
        )

        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        print("❌ GPT call failed:", e)
        return "Sorry, I had trouble understanding that. Please try again."

# Main route
@app.route('/api/process', methods=['POST'])
def process_input():
    try:
        data = request.get_json()
        user_input = data.get('text', '')

        # Send to GPT
        ai_response = ask_gpt(user_input)

        return jsonify({'reply': ai_response}), 200

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

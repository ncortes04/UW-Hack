from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

from classify import load_model, classify_skin_image
import os
os.environ.pop("SSL_CERT_FILE", None)

load_dotenv()
user_context = {}

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


@app.route('/api/process', methods=['POST'])
def process_input():
    try:
        data = request.get_json()
        user_input = data.get('text', '')

        diagnosis_note = ""
        if 'diagnosis' in user_context:
            diagnosis_note = f"The user has been diagnosed by the image model with '{user_context['diagnosis']}'. "

        full_prompt = diagnosis_note + user_input

        ai_response = ask_gpt(full_prompt)
        return jsonify({'reply': ai_response}), 200

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500



@app.route('/api/classify-image', methods=['POST'])
def classify_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        temp_path = f"temp_uploads/{uuid.uuid4().hex}_{file.filename}"
        os.makedirs("temp_uploads", exist_ok=True)
        file.save(temp_path)

        model = load_model()
        label, confidence = classify_skin_image(model, temp_path)

        os.remove(temp_path)

        if label is None:
            return jsonify({'error': 'Classification failed'}), 500

        # Store context for use in GPT prompt
        user_context['diagnosis'] = label

        return jsonify({
            'label': label,
            'confidence': round(confidence * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

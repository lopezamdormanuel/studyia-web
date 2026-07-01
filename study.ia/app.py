from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Tu API Key configurada
client = OpenAI(api_key="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")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_message = data.get('message')
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres StudyIA, una inteligencia artificial diseñada para ayudar a estudiantes. Eres un tutor experto, amigable y divertido."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = response.choices[0].message.content
    except Exception as e:
        bot_response = f"Error en los créditos de OpenAI: {e}"

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
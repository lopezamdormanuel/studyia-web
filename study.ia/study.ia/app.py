from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Pega aquí tu clave gratuita entre las comillas
client = Groq(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get('message')
    
    try:
        # Usamos Llama 3, que es un modelo buenísimo y gratuito en Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama3-8b-8192",
        )
        
        respuesta = chat_completion.choices[0].message.content
        return jsonify({'response': respuesta})
        
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
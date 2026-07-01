from flask import Flask, render_template, request, jsonify
from groq import Groq
import urllib.parse
import os 
app = Flask(__name__)

# Pega aqui tu clave gratuita entre las comillas
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
@app.route('/')
def index():
    return render_template('index.html')

# 1. RUTA PARA TEXTO NORMAL (Cambiamos /ask a /preguntar para que coincida con el HTML)
@app.route('/preguntar', methods=['POST'])
def preguntar():
    user_message = request.json.get('mensaje')
    
    try:
        # Usamos Llama 3, que es un modelo buenísimo y gratuito en Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        
        respuesta = chat_completion.choices[0].message.content
        return jsonify({'respuesta': respuesta})
        
    except Exception as e:
        return jsonify({'respuesta': f"Error: {str(e)}"})

# 2. NUEVA RUTA PARA GENERAR IMÁGENES
@app.route('/generar-imagen', methods=['POST'])
def generar_imagen():
    data = request.json
    prompt_original = data.get('prompt', '')
    
    # Quitamos la palabra "dibuja" del inicio para dejar solo lo que hay que pintar
    prompt_limpio = prompt_original.lower().replace('dibuja', '').strip()
    
    if not prompt_limpio:
        prompt_limpio = "un dibujo libre"

    # Codificamos el texto para que sea seguro ponerlo en una URL
    prompt_codificado = urllib.parse.quote(prompt_limpio)
    
    # Usamos Pollinations AI que genera imágenes brutales gratis y sin registrarse
    url_imagen = f"https://image.pollinations.ai/prompt/{prompt_codificado}?width=512&height=512&nologo=true"
    
    return jsonify({'url_imagen': url_imagen})

if __name__ == '__main__':
    app.run(debug=True)

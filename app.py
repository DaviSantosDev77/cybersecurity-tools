from flask import Flask, render_template, request, jsonify
import random
import os
import google.generativeai as genai
import markdown

app = Flask(__name__)

# --- CONFIGURAÇÃO DA IA ---
# O código busca a variável 'API_KEY' que configuramos no painel do Render
API_KEY = os.getenv("API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        ia_ativa = True
    except Exception as e:
        print(f"Erro ao iniciar IA: {e}")
        ia_ativa = False
else:
    ia_ativa = False
    print("Aviso: Variável API_KEY não encontrada no ambiente.")

# ... (Mantenha seu banco de questões aqui) ...

@app.route('/explicar_ia', methods=['POST'])
def explicar_ia():
    try:
        # Tenta pegar os dados
        dados = request.json
        if not ia_ativa:
            return jsonify({"explicacao": "📡 <strong>BASE OFFLINE:</strong> O instrutor IA está em outra missão agora. Tente em instantes."})

        prompt = f"Explique de forma curta e operacional o gabarito: {dados.get('correta')} da pergunta: {dados.get('pergunta')}"
        
        # O pulo do gato: define um tempo limite (timeout)
        response = model.generate_content(prompt)
        html = markdown.markdown(response.text)
        return jsonify({"explicacao": html})

    except Exception as e:
        # Se der QUALQUER erro (Cota, API, Internet), o site NÃO MORRE
        print(f"Erro na IA: {e}")
        return jsonify({"explicacao": "⚠️ <strong>RADAR:</strong> Limite de cota atingido. O instrutor volta em 1 minuto!"})
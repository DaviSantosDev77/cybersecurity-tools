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
    if not ia_ativa:
        return jsonify({"explicacao": "⚠️ <strong>IA OFFLINE:</strong> Chave de API não configurada corretamente no servidor."})

    dados = request.json
    prompt = f"Explique de forma curta e operacional por que a resposta '{dados.get('correta')}' está correta para a questão: {dados.get('pergunta')}"
    
    try:
        response = model.generate_content(prompt)
        html = markdown.markdown(response.text)
        return jsonify({"explicacao": html})
    except Exception as e:
        return jsonify({"explicacao": "⚠️ Limite de requisições atingido. Tente em 1 minuto."})
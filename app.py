from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# --- BANCO DE QUESTÕES (MANTENHA O SEU COMPLETO AQUI) ---
questoes = [
    {
        "id": 1,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Condutor flagrado dirigindo sob influência de álcool (bafômetro acusou 0,40 mg/L). Qual a penalidade prevista no CTB?",
        "opcoes": ["Multa (x5) e Retenção", "Multa (x10) e Suspensão da CNH", "Apenas Multa Grave", "Cassação da CNH direta"],
        "correta": "Multa (x10) e Suspensão da CNH",
        "explicacao": "Art. 165 CTB. Embriaguez é infração Gravíssima x10 + Suspensão do direito de dirigir por 12 meses."
    },
    {
        "id": 2,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Ultrapassar pela contramão em linha contínua amarela. Classificação da infração:",
        "opcoes": ["Grave", "Gravíssima (x5)", "Gravíssima (x10)", "Média"],
        "correta": "Gravíssima (x5)",
        "explicacao": "Art. 203, V. Ultrapassar em faixa contínua é Gravíssima com fator multiplicador X5."
    },
    {
        "id": 3,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Deixar o condutor ou passageiro de usar o cinto de segurança. Infração e medida administrativa:",
        "opcoes": ["Grave + Retenção do veículo", "Gravíssima + Multa", "Média + Remoção", "Leve + Orientação"],
        "correta": "Grave + Retenção do veículo",
        "explicacao": "Art. 167. Falta de cinto é infração GRAVE. O veículo fica retido até a colocação do cinto."
    },
    {
        "id": 4,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Qual a validade da CNH para condutores com menos de 50 anos de idade (regra nova)?",
        "opcoes": ["5 anos", "10 anos", "3 anos", "Indeterminada"],
        "correta": "10 anos",
        "explicacao": "Pela Nova Lei de Trânsito, condutores com menos de 50 anos renovam a cada 10 anos."
    },
    {
        "id": 5,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Criança de 6 anos no banco da frente. Pode?",
        "opcoes": ["Sim, se usar cinto", "Não, apenas maiores de 10 anos", "Sim, no colo da mãe", "Não, exceto em picape sem banco traseiro"],
        "correta": "Não, apenas maiores de 10 anos",
        "explicacao": "Art. 64. Crianças menores de 10 anos que não tenham atingido 1,45m devem ir no banco traseiro."
    }
]

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    # Garante que funciona mesmo com poucas questões
    if len(questoes) >= 5:
        amostra = random.sample(questoes, 5)
    else:
        amostra = questoes
    
    if request.method == 'POST':
        try:
            id_respondido = int(request.form.get('id_questao'))
            resposta_usuario = request.form.get('resposta')
            
            questao_atual = next((q for q in questoes if q['id'] == id_respondido), None)
            
            if questao_atual:
                acertou = (resposta_usuario == questao_atual['correta'])
                return render_template('quiz.html', 
                                     questoes=amostra, 
                                     resposta_atual=resposta_usuario, 
                                     id_atual=id_respondido, 
                                     acertou=acertou,
                                     questao_focada=questao_atual)
        except:
            pass

    return render_template('quiz.html', questoes=amostra)

# Rota "Fantasma" (Só pra não dar erro se alguém clicar no botão antigo)
@app.route('/explicar_ia', methods=['POST'])
def explicar_ia():
    return jsonify({"explicacao": "Funcionalidade de IA desativada para otimização de performance."})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# --- SEU BANCO DE QUESTÕES COMPLETO ---
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
    },
    {
        "id": 6,
        "materia": "LEGISLAÇÃO DE TRÂNSITO",
        "enunciado": "Recusar-se a realizar o teste do bafômetro (Recusa). Consequência:",
        "opcoes": ["Nenhuma, ninguém é obrigado a produzir prova contra si", "Apenas multa leve", "As mesmas penalidades da embriaguez (Multa x10 + Suspensão)", "Prisão em flagrante imediata"],
        "correta": "As mesmas penalidades da embriaguez (Multa x10 + Suspensão)",
        "explicacao": "Art. 165-A. A recusa sujeita o condutor às mesmas penalidades administrativas de quem soprou e deu positivo."
    },
    {
        "id": 7,
        "materia": "FÍSICA (CINEMÁTICA)",
        "enunciado": "Um carro viaja a 72 km/h. Quanto isso vale em m/s? (Fator de conversão 3,6)",
        "opcoes": ["10 m/s", "15 m/s", "20 m/s", "25 m/s"],
        "correta": "20 m/s",
        "explicacao": "Para transformar km/h em m/s, divide-se por 3,6. Logo: 72 / 3,6 = 20 m/s."
    },
    {
        "id": 8,
        "materia": "FÍSICA (DINÂMICA)",
        "enunciado": "Em uma frenagem de emergência, qual força é responsável por parar o veículo?",
        "opcoes": ["Força Centrífuga", "Força de Atrito", "Força Peso", "Inércia"],
        "correta": "Força de Atrito",
        "explicacao": "É o atrito entre os pneus e o asfalto que gera a desaceleração necessária para parar."
    },
    {
        "id": 9,
        "materia": "DIREITO PENAL",
        "enunciado": "Policial que se apropria de dinheiro apreendido em operação comete:",
        "opcoes": ["Furto", "Roubo", "Peculato-Apropriação", "Prevaricação"],
        "correta": "Peculato-Apropriação",
        "explicacao": "Art. 312 CP. Apropriar-se de bem móvel de que tem a posse em razão do cargo."
    },
    {
        "id": 10,
        "materia": "INFORMÁTICA",
        "enunciado": "Técnica onde o atacante engana a vítima (ex: e-mail falso de banco) para roubar senhas:",
        "opcoes": ["Phishing", "DDoS", "Ransomware", "Firewall"],
        "correta": "Phishing",
        "explicacao": "Phishing (pescaria) é a engenharia social usada para 'pescar' dados do usuário."
    }
]

@app.route('/', methods=['GET', 'POST'])
def index():
    # Lógica simples pra garantir que funciona
    if len(questoes) >= 5:
        questoes_para_exibir = random.sample(questoes, 5)
    else:
        questoes_para_exibir = questoes
    
    if request.method == 'POST':
        id_respondido = int(request.form.get('id_questao'))
        resposta_usuario = request.form.get('resposta')
        
        questao_atual = next((q for q in questoes if q['id'] == id_respondido), None)
        
        if questao_atual:
            acertou = (resposta_usuario == questao_atual['correta'])
            return render_template('quiz.html', 
                                 questoes=questoes_para_exibir, 
                                 resposta_atual=resposta_usuario, 
                                 id_atual=id_respondido, 
                                 acertou=acertou,
                                 questao_focada=questao_atual)

    return render_template('quiz.html', questoes=questoes_para_exibir)

# --- ROTA DE SEGURANÇA ---
# Se clicar no botão IA, ele avisa que está em manutenção em vez de quebrar
@app.route('/explicar_ia', methods=['POST'])
def explicar_ia():
    return jsonify({
        "explicacao": "⚠️ <strong>SISTEMA EM MANUTENÇÃO:</strong> A conexão com o QG (Google AI) está instável no momento. Tente novamente mais tarde ou consulte o gabarito oficial abaixo."
    })

if __name__ == '__main__':
    # Debug=True é o que faz aparecer o erro no navegador se der ruim
    app.run(debug=True)
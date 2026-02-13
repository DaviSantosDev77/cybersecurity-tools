from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)

app.secret_key = 'senha-super-secreta-prf-tactical'

questoes = [
    {"id": 1, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Condutor flagrado dirigindo sob influência de álcool (0,40 mg/L). Penalidade:", "opcoes": ["Multa (x5) e Retenção", "Multa (x10) e Suspensão da CNH", "Apenas Multa Grave", "Cassação direta"], "correta": "Multa (x10) e Suspensão da CNH", "explicacao": "Art. 165 CTB. Infração gravíssima, multa 10x e suspensão por 12 meses."},
    {"id": 2, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Ultrapassar pela contramão em linha contínua amarela:", "opcoes": ["Grave", "Gravíssima (x5)", "Gravíssima (x10)", "Média"], "correta": "Gravíssima (x5)", "explicacao": "Art. 203, V. Ultrapassagem proibida é Gravíssima x5."},
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'acertos' not in session:
        session['acertos'] = 0
    if 'erros' not in session:
        session['erros'] = 0

    if 'questoes_ids' not in session:
        amostra = random.sample(questoes, 5) if len(questoes) >= 5 else questoes
        session['questoes_ids'] = [q['id'] for q in amostra]
    
    questoes_atuais = [q for q in questoes if q['id'] in session['questoes_ids']]

    acertou = None
    resposta_usuario = None
    id_respondido = None
    questao_focada = None

    if request.method == 'POST':
        if 'resetar' in request.form:
            session['acertos'] = 0
            session['erros'] = 0
            session.pop('questoes_ids', None) 
            return redirect(url_for('index'))

        # Lógica de Resposta
        id_respondido = int(request.form.get('id_questao'))
        resposta_usuario = request.form.get('resposta')
        
        questao_focada = next((q for q in questoes_atuais if q['id'] == id_respondido), None)
        
        if questao_focada:
            if resposta_usuario == questao_focada['correta']:
                acertou = True
                session['acertos'] += 1
            else:
                acertou = False
                session['erros'] += 1
            session.modified = True


    return render_template('quiz.html', 
                         questoes=questoes_atuais, 
                         acertos=session['acertos'], 
                         erros=session['erros'],
                         resposta_atual=resposta_usuario,
                         id_atual=id_respondido,
                         acertou=acertou,
                         questao_focada=questao_focada)

@app.route('/nova_bateria')
def nova_bateria():
    session.pop('questoes_ids', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
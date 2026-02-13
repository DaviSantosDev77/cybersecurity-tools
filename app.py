from flask import Flask, render_template, request, session, redirect, url_for
import random
import os

app = Flask(__name__)

app.secret_key = 'chave_secreta_placar_prf'

questoes = [
    {"id": 1, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Condutor flagrado dirigindo sob influência de álcool (bafômetro acusou 0,40 mg/L). Qual a penalidade?", "opcoes": ["Multa (x5) e Retenção", "Multa (x10) e Suspensão da CNH", "Apenas Multa Grave", "Cassação direta"], "correta": "Multa (x10) e Suspensão da CNH", "explicacao": "Art. 165 CTB. Infração gravíssima, multa 10x e suspensão por 12 meses."},
    {"id": 2, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Ultrapassar pela contramão em linha contínua amarela. Classificação:", "opcoes": ["Grave", "Gravíssima (x5)", "Gravíssima (x10)", "Média"], "correta": "Gravíssima (x5)", "explicacao": "Art. 203, V. Ultrapassagem proibida é Gravíssima x5."},
    {"id": 3, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Falta de cinto de segurança (condutor ou passageiro). Infração:", "opcoes": ["Grave + Retenção", "Gravíssima + Multa", "Média + Remoção", "Leve"], "correta": "Grave + Retenção", "explicacao": "Art. 167. Infração Grave e retenção do veículo até colocação do cinto."},
    {"id": 4, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Validade da CNH para condutores com menos de 50 anos:", "opcoes": ["5 anos", "10 anos", "3 anos", "Indeterminada"], "correta": "10 anos", "explicacao": "Lei 14.071/20 ampliou para 10 anos a validade para condutores < 50 anos."},
    {"id": 5, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Criança de 6 anos no banco da frente. Pode?", "opcoes": ["Sim, com cinto", "Não, apenas maiores de 10 anos", "Sim, no colo", "Depende do carro"], "correta": "Não, apenas maiores de 10 anos", "explicacao": "Crianças menores de 10 anos que não atingiram 1,45m devem ir no banco traseiro."},
    {"id": 6, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Recusa ao teste do bafômetro. Consequência:", "opcoes": ["Nenhuma", "Apenas multa", "Mesmas penalidades da embriaguez", "Prisão"], "correta": "Mesmas penalidades da embriaguez", "explicacao": "Art. 165-A. A recusa gera as mesmas sanções administrativas da embriaguez confirmada."},
    {"id": 7, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Qual a categoria de CNH para conduzir veículo de transporte de passageiros com mais de 8 lugares?", "opcoes": ["Categoria B", "Categoria C", "Categoria D", "Categoria E"], "correta": "Categoria D", "explicacao": "Categoria D é exigida para transporte de passageiros (ônibus, vans) > 8 lugares."},
    {"id": 8, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Avançar o sinal vermelho do semáforo é infração:", "opcoes": ["Média", "Grave", "Gravíssima", "Leve"], "correta": "Gravíssima", "explicacao": "Art. 208. Avançar sinal vermelho ou de parada obrigatória é infração Gravíssima."},
    {"id": 9, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Dirigir manuseando telefone celular. Infração:", "opcoes": ["Média", "Grave", "Gravíssima", "Leve"], "correta": "Gravíssima", "explicacao": "Art. 252, Parágrafo único. Segurar ou manusear celular é Gravíssima."},
    {"id": 10, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Estacionar em vaga de idoso/deficiente sem credencial:", "opcoes": ["Leve", "Média", "Grave", "Gravíssima"], "correta": "Gravíssima", "explicacao": "Alteração recente do CTB tornou essa infração Gravíssima."},
    {"id": 11, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Velocidade superior à máxima em mais de 50%. Penalidade:", "opcoes": ["Multa x3 + Suspensão", "Multa Grave", "Multa Média", "Apenas Advertência"], "correta": "Multa x3 + Suspensão", "explicacao": "Art. 218, III. Acima de 50% é Gravíssima x3 e suspensão imediata."},
    {"id": 12, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Transitar em marcha à ré, salvo na distância necessária para pequenas manobras:", "opcoes": ["Permitido sempre", "Infração Grave", "Infração Média", "Infração Leve"], "correta": "Infração Grave", "explicacao": "Art. 194. É infração Grave se não for para pequena manobra."},
    {"id": 13, "materia": "FÍSICA (CINEMÁTICA)", "enunciado": "Converta 72 km/h para m/s:", "opcoes": ["10 m/s", "15 m/s", "20 m/s", "25 m/s"], "correta": "20 m/s", "explicacao": "Divida por 3,6. 72 / 3,6 = 20 m/s."},
    {"id": 14, "materia": "FÍSICA (DINÂMICA)", "enunciado": "Qual força permite que o carro faça uma curva sem derrapar?", "opcoes": ["Centrífuga", "Atrito", "Peso", "Normal"], "correta": "Atrito", "explicacao": "A força de atrito lateral atua como força centrípeta segurando o carro."},
    {"id": 15, "materia": "FÍSICA (CINEMÁTICA)", "enunciado": "Um carro a 108 km/h percorre quantos metros em 1 segundo?", "opcoes": ["20m", "30m", "40m", "50m"], "correta": "30m", "explicacao": "108 / 3,6 = 30 m/s."},
    {"id": 16, "materia": "FÍSICA (DINÂMICA)", "enunciado": "Em uma colisão, se a velocidade dobra, a energia cinética:", "opcoes": ["Dobra", "Quadruplica", "Triplica", "Mantém-se"], "correta": "Quadruplica", "explicacao": "A energia cinética é proporcional ao quadrado da velocidade (v²)."},
    {"id": 17, "materia": "FÍSICA (DINÂMICA)", "enunciado": "A tendência de um corpo em manter seu estado de movimento chama-se:", "opcoes": ["Força", "Aceleração", "Inércia", "Gravidade"], "correta": "Inércia", "explicacao": "Primeira Lei de Newton."},
    {"id": 18, "materia": "FÍSICA (CINEMÁTICA)", "enunciado": "Movimento Retilíneo Uniforme (MRU) possui aceleração:", "opcoes": ["Constante e positiva", "Constante e negativa", "Nula", "Variável"], "correta": "Nula", "explicacao": "No MRU a velocidade é constante, logo a aceleração é zero."},
    {"id": 19, "materia": "DIREITO PENAL", "enunciado": "Policial que se apropria de bem apreendido comete:", "opcoes": ["Furto", "Roubo", "Peculato", "Prevaricação"], "correta": "Peculato", "explicacao": "Art. 312 CP. Peculato-apropriação."},
    {"id": 20, "materia": "DIREITO PENAL", "enunciado": "Exigir vantagem indevida em razão da função (ex: 'caixinha' na blitz):", "opcoes": ["Corrupção Passiva", "Concussão", "Prevaricação", "Suborno"], "correta": "Concussão", "explicacao": "Art. 316. O verbo núcleo é 'Exigir'."},
    {"id": 21, "materia": "DIREITO PENAL", "enunciado": "Solicitar ou receber vantagem indevida:", "opcoes": ["Concussão", "Corrupção Passiva", "Corrupção Ativa", "Peculato"], "correta": "Corrupção Passiva", "explicacao": "Art. 317. O verbo é 'Solicitar' ou 'Receber'."},
    {"id": 22, "materia": "DIREITO PENAL", "enunciado": "Particular que oferece dinheiro ao policial:", "opcoes": ["Corrupção Passiva", "Concussão", "Corrupção Ativa", "Tráfico de Influência"], "correta": "Corrupção Ativa", "explicacao": "Art. 333. O crime do particular é Corrupção Ativa."},
    {"id": 23, "materia": "DIREITO PENAL", "enunciado": "Deixar de praticar ato de ofício por sentimento pessoal (preguiça/dó):", "opcoes": ["Prevaricação", "Peculato", "Corrupção", "Condescendência"], "correta": "Prevaricação", "explicacao": "Art. 319. Retardar ou deixar de praticar ato para satisfazer interesse pessoal."},
    {"id": 24, "materia": "DIREITO PENAL", "enunciado": "Chefe que não pune subordinado por indulgência (dó):", "opcoes": ["Prevaricação", "Condescendência Criminosa", "Peculato", "Favorecimento"], "correta": "Condescendência Criminosa", "explicacao": "Art. 320. Deixar de responsabilizar subordinado por indulgência."},
    {"id": 25, "materia": "DIREITO PENAL", "enunciado": "Legítima defesa exige agressão:", "opcoes": ["Futura", "Passada", "Injusta, atual ou iminente", "Justa"], "correta": "Injusta, atual ou iminente", "explicacao": "Art. 25 CP. Requisitos da Legítima Defesa."},
    {"id": 26, "materia": "DIREITO PENAL", "enunciado": "Estado de Necessidade envolve:", "opcoes": ["Agressão humana", "Perigo atual", "Vingança", "Defesa da honra"], "correta": "Perigo atual", "explicacao": "Art. 24 CP. Salvar-se de perigo atual não provocado por sua vontade."},
    {"id": 27, "materia": "DIREITO CONSTITUCIONAL", "enunciado": "A casa é asilo inviolável, salvo em caso de:", "opcoes": ["Qualquer hora com ordem judicial", "Flagrante delito", "Suspeita sem provas", "Denúncia anônima"], "correta": "Flagrante delito", "explicacao": "Art. 5º, XI. Flagrante, desastre, socorro ou ordem judicial (dia)."},
    {"id": 28, "materia": "DIREITO CONSTITUCIONAL", "enunciado": "A PRF é órgão permanente organizado e mantido pela:", "opcoes": ["Estados", "Municípios", "União", "Forças Armadas"], "correta": "União", "explicacao": "Art. 144. PRF é órgão da União."},
    {"id": 29, "materia": "DIREITO CONSTITUCIONAL", "enunciado": "Ninguém será privado de liberdade sem:", "opcoes": ["Aviso prévio", "Devido processo legal", "Confissão", "Testemunhas"], "correta": "Devido processo legal", "explicacao": "Princípio do Devido Processo Legal (Art. 5º, LIV)."},
    {"id": 30, "materia": "DIREITO CONSTITUCIONAL", "enunciado": "É livre a manifestação do pensamento, sendo vedado:", "opcoes": ["O anonimato", "A crítica política", "O uso da internet", "O debate religioso"], "correta": "O anonimato", "explicacao": "Art. 5º, IV. Vedado o anonimato."},
    {"id": 31, "materia": "DIREITO CONSTITUCIONAL", "enunciado": "Remédio constitucional para garantir liberdade de locomoção:", "opcoes": ["Habeas Data", "Mandado de Segurança", "Habeas Corpus", "Ação Popular"], "correta": "Habeas Corpus", "explicacao": "HC protege o direito de ir e vir."},
    {"id": 32, "materia": "INFORMÁTICA", "enunciado": "Técnica de enganar usuário para roubar senhas (ex: site falso):", "opcoes": ["Phishing", "DDoS", "Virus", "Backup"], "correta": "Phishing", "explicacao": "Engenharia social para 'pescar' dados."},
    {"id": 33, "materia": "INFORMÁTICA", "enunciado": "Software malicioso que sequestra dados e pede resgate:", "opcoes": ["Spyware", "Ransomware", "Worm", "Trojan"], "correta": "Ransomware", "explicacao": "Ransom = Resgate. Criptografa arquivos e cobra em Bitcoin."},
    {"id": 34, "materia": "INFORMÁTICA", "enunciado": "Protocolo seguro de navegação na internet (cadeado):", "opcoes": ["HTTP", "FTP", "HTTPS", "SMTP"], "correta": "HTTPS", "explicacao": "O 'S' indica SSL/TLS (Criptografia)."},
    {"id": 35, "materia": "INFORMÁTICA", "enunciado": "Atalho padrão para bloquear a tela no Windows:", "opcoes": ["Win + L", "Ctrl + C", "Alt + F4", "Win + E"], "correta": "Win + L", "explicacao": "L de Lock (Bloquear)."},
    {"id": 36, "materia": "INFORMÁTICA", "enunciado": "Dispositivo que conecta redes diferentes e escolhe a melhor rota:", "opcoes": ["Switch", "Hub", "Roteador", "Modem"], "correta": "Roteador", "explicacao": "O Roteador (Router) encaminha pacotes entre redes."},
    {"id": 37, "materia": "INFORMÁTICA", "enunciado": "Extensão padrão de scripts Python:", "opcoes": [".py", ".exe", ".java", ".html"], "correta": ".py", "explicacao": "Arquivos Python terminam em .py."},
    {"id": 38, "materia": "ÉTICA", "enunciado": "Princípio que exige que a Administração Pública seja transparente:", "opcoes": ["Legalidade", "Impessoalidade", "Publicidade", "Eficiência"], "correta": "Publicidade", "explicacao": "Atos administrativos devem ser públicos."},
    {"id": 39, "materia": "ÉTICA", "enunciado": "O servidor deve tratar o patrimônio público com:", "opcoes": ["Descaso", "Como se fosse seu", "Zelo e economia", "Apenas uso"], "correta": "Zelo e economia", "explicacao": "Dever de probidade e cuidado com o bem público."},
    {"id": 40, "materia": "ÉTICA", "enunciado": "Princípio onde o administrador só pode fazer o que a lei autoriza:", "opcoes": ["Legalidade", "Moralidade", "Autonomia", "Livre arbítrio"], "correta": "Legalidade", "explicacao": "Na Adm. Pública, só se faz o que a lei permite."},
    {"id": 41, "materia": "GEOPOLÍTICA", "enunciado": "Principal modal de transporte de cargas no Brasil:", "opcoes": ["Ferroviário", "Rodoviário", "Hidroviário", "Aéreo"], "correta": "Rodoviário", "explicacao": "Matriz de transporte brasileira é concentrada em rodovias."},
    {"id": 42, "materia": "GEOPOLÍTICA", "enunciado": "Bioma predominante na região Centro-Oeste:", "opcoes": ["Amazônia", "Cerrado", "Caatinga", "Pampa"], "correta": "Cerrado", "explicacao": "O Cerrado é o bioma típico do planalto central."},
    {"id": 43, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "A CNH deve ser renovada a cada quantos anos para maiores de 70 anos?", "opcoes": ["3 anos", "5 anos", "10 anos", "2 anos"], "correta": "3 anos", "explicacao": "Acima de 70 anos, a validade máxima é de 3 anos."},
    {"id": 44, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Veículos de emergência têm livre circulação quando:", "opcoes": ["Sempre", "Apenas com giroflex ligado", "Com giroflex e sirene ligados", "Apenas de dia"], "correta": "Com giroflex e sirene ligados", "explicacao": "Art. 29. A prioridade depende dos dispositivos sonoros e luminosos acionados."},
    {"id": 45, "materia": "DIREITO PENAL", "enunciado": "Crime impossível (Art. 17 CP) ocorre quando:", "opcoes": ["O agente desiste", "O meio é ineficaz ou o objeto impróprio", "O agente se arrepende", "Não há testemunhas"], "correta": "O meio é ineficaz ou o objeto impróprio", "explicacao": "Não se pune a tentativa quando é impossível consumar o crime."},
    {"id": 46, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Estacionar na contramão de direção. Infração:", "opcoes": ["Média", "Leve", "Grave", "Gravíssima"], "correta": "Média", "explicacao": "Art. 181, XV. Estacionar na contramão é infração Média."},
    {"id": 47, "materia": "DIREITO PROCESSUAL PENAL", "enunciado": "O Inquérito Policial tem natureza:", "opcoes": ["Judicial", "Administrativa e Inquisitorial", "Acusatória", "Pública"], "correta": "Administrativa e Inquisitorial", "explicacao": "O IP é procedimento administrativo para colher provas, sem contraditório pleno."},
    {"id": 48, "materia": "LEGISLAÇÃO DE TRÂNSITO", "enunciado": "Transitar pelo acostamento (quando não permitido). Infração:", "opcoes": ["Grave", "Média", "Gravíssima (x3)", "Leve"], "correta": "Gravíssima (x3)", "explicacao": "Art. 193. Transitar em acostamentos é Gravíssima com multiplicador x3."},
    {"id": 49, "materia": "FÍSICA", "enunciado": "A unidade de Força no Sistema Internacional é:", "opcoes": ["Joule", "Watt", "Newton", "Pascal"], "correta": "Newton", "explicacao": "Newton (N) é a unidade de força (F=m.a)."},
    {"id": 50, "materia": "INFORMÁTICA", "enunciado": "Parte física do computador (peças):", "opcoes": ["Software", "Hardware", "Peopleware", "Firmware"], "correta": "Hardware", "explicacao": "Hardware é o que você chuta, Software é o que você xinga."}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'acertos' not in session:
        session['acertos'] = 0
    if 'erros' not in session:
        session['erros'] = 0

    if 'questoes_ids' not in session:
        qtd = 5 if len(questoes) >= 5 else len(questoes)
        amostra = random.sample(questoes, qtd)
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

        try:
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
        except:
            pass

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
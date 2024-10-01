import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html", methods=['POST'])
def validar_notas():
    nome_aluno = request.form["nome_aluno"]
    turma_aluno = request.form["turma_aluno"]
    notas_1 = float(request.form["nota1_aluno"])
    notas_2 = float(request.form["nota2_aluno"])
    notas_3 = float(request.form["nota3_aluno"])

    
    media = (notas_1 + notas_2 + notas_3) / 3

    
    if media >= 7:
        status = "Aprovado"
    elif media >= 3:
        status = "Recuperação"
    else:
        status = "Reprovado"

    caminho_arquivo = 'models/notas.txt'

    with open(caminho_arquivo, 'a') as arquivo:
        arquivo.write(f"{nome_aluno};{turma_aluno};{notas_1};{notas_2};{notas_3};{media};{status}\n")

    return redirect("/")

@app.route("/consulta2")
def consulta_notas():
    notas = []
    caminho_arquivo = 'models/notas.txt'

    if not os.path.isfile(caminho_arquivo):
        return render_template("consultar_notas.html", prod=notas) 

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            item = linha.strip().split(';')
            if len(item) == 7: 
                notas.append({
                    'nome': item[0],
                    'turma': item[1],
                    'nota1': item[2],
                    'nota2': item[3],
                    'nota3': item[4],
                    'media': round(float(item[5]), 2),
                    'status': item[6]  # Adicionando o status
                })

    return render_template("consultar_notas.html", prod=notas)

@app.route("/excluir_notas", methods=['GET'])
def excluir_notas():
    linha_para_excluir = int(request.args.get('linha')) 
    caminho_arquivo = 'models/notas.txt'
    
    if not os.path.isfile(caminho_arquivo):
        return redirect("/")  # Se não existir, redireciona

    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    if linha_para_excluir < len(linhas):
        del linhas[linha_para_excluir]  

    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)

    return redirect("/consulta2")  # Redireciona para a rota correta

app.run(host='127.0.0.1', port=80, debug=True)

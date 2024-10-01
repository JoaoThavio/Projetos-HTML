import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/validar_imc", methods=['POST'])
def validar_imc():
    nome_aluno = request.form["nome_aluno"]
    peso = float(request.form["peso_pessoa"])
    altura = float(request.form["altura_pessoa"])

    
    media = peso / (altura**2)

    if media <= 18.5:
        status = "Abaixo do Peso"
    elif media <= 24.9:
        status = "Peso Normal"
    elif media <= 34.9:
        status = "Sobrepeso"
    elif media <= 35.9:
        status ='Obesidade grau 1'
    elif media <= 39.9:
        status = 'Obesidade grau 2'
    else:
        status = 'Obesidade grau 3'

    caminho_arquivo = 'models/imc.txt'


    with open(caminho_arquivo, 'a') as arquivo:
        arquivo.write(f"{nome_aluno};{peso};{altura};{media};{status}\n")

    return redirect("/")

@app.route("/consulta2")
def consulta_peso():
    imc = []
    caminho_arquivo = 'models/imc.txt'

    if not os.path.isfile(caminho_arquivo):
        return render_template("consultar_peso.html", prod=imc)  # Retorna lista vazia se não existir

    with open(caminho_arquivo, 'r') as arquivo:
        for linha in arquivo:
            item = linha.strip().split(';')
            if len(item) == 5: 
                imc.append({
                    'nome': item[0],
                    'peso': item[1],
                    'altura': item[2],
                    'media': round(float(item[3]), 2),
                    'status': item[4] 
                })

    return render_template("consultar_peso.html", prod=imc)


@app.route("/excluir_notas", methods=['GET'])
def excluir_notas():
    linha_para_excluir = int(request.args.get('linha')) 
    caminho_arquivo = 'models/imc.txt'
    
    if not os.path.isfile(caminho_arquivo):
        return redirect("/")  #

    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    if linha_para_excluir < len(linhas):
        del linhas[linha_para_excluir]  

    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.writelines(linhas)

    return redirect("/consulta2")# Redireciona para a rota correta

@app.route("/tabela")
def tabela():
    return render_template("tabela.html")

    
app.run(host='127.0.0.1', port=80, debug=True)

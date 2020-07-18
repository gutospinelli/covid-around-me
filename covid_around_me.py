#importando dependencias
import os
import unicodedata
import json
import numpy
import pandas
import requests
from flask import Flask, jsonify, request, render_template, url_for, redirect
from ipyleaflet import Map, Marker
from pandas import json_normalize
from dotenv import load_dotenv, find_dotenv
import csv
from datetime import date

#acha o arquivo .ENV com a senha do kaggle na estrutura do projeto
dotenv_path = find_dotenv()
#carrega o arquivo
load_dotenv(dotenv_path)

#usando a api do cep aberto para pesquisar ceps
#token = os.environ.get("CEP_ABERTO_TOKEN") #pegue seu token pessoal após cadastro no CEP Aberto
token = "7e177ec94db54fe0e92d3b6b2c9935c0"
headers = {'Authorization': 'Token token=%s' % str(token)}

#funções auxiliares
def search_by_cep(cep):
    url = "https://www.cepaberto.com/api/v3/cep?cep=" + cep
    response = requests.get(url, headers=headers)
    return response.json()

def draw_map(latitude, longitude):
    pos = (latitude, longitude)
    m = Map(center=pos, zoom=13)
    m.add_layer(Marker(location=pos))
    display(m)

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return str(text)


#Flask App, Code and Routes
app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def covid_around_me():
    if request.method == "POST":
        cep = request.form["cep"]
        return redirect(url_for("form", cep=cep))

    return render_template("main.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    cep = request.args.get('cep', type=int)

    url_csv = "https://opendata.arcgis.com/datasets/b54234c151aa4d01b488dc12aafd5574_0.csv?outSR=4326"
    url = 'https://opendata.arcgis.com/datasets/b54234c151aa4d01b488dc12aafd5574_0/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

    path = os.getcwd()
    filename = "dados_" + str(date.today()) + ".csv"

    if not os.path.isfile(filename):
        #delete all previous csv
        for item in path:
            if item.endswith(".csv"):
                os.remove(os.path.join(path, item))
        #save the new one
        with open(filename, 'wb') as f, \
                requests.get(url_csv, stream=True) as r:
            for line in r.iter_lines():
                f.write(line)
        #replace colon for new line in file
        with open(filename, 'r') as file:
            filedata = file.read()
            filedata = filedata.replace(',', '\n')
        with open(filename, 'w') as file:
            file.write(filedata)

    columns = ["dt_notific", "dt_inicio_sintomas", "bairro_resid", "ap_resid","evolucao", "dt_obito", "CEP", "dt_atualizacao","manter"]

    df = pandas.read_csv(filename, skiprows=[0,1], skipfooter=1, delimiter=';',names = columns)

    digiteCep = cep
    buscaCep = search_by_cep(str(digiteCep))
    print(buscaCep)
    bairroCep = strip_accents(buscaCep['bairro'])

    casos_sua_rua = df.loc[df.CEP == digiteCep, :]
    print('Casos na sua Rua: {0}'.format(len(casos_sua_rua)))
    lbl_rua = 'Casos na sua Rua: {0}'.format(len(casos_sua_rua))

    casos_seu_bairro = df.loc[df.bairro_resid == bairroCep.upper(), :]
    print('Casos no seu Bairro: {0}'.format(len(casos_seu_bairro)))
    lbl_bairro = 'Casos no seu Bairro: {0}'.format(len(casos_seu_bairro))

    dadosData = str(date.today())

    latitude = buscaCep['latitude']
    longitude = buscaCep['longitude']
    nome_rua = buscaCep['logradouro']

    # return jsonify(rua=lbl_rua, bairro=lbl_bairro, latitude=latitude, longitude=longitude)
    return render_template("form.html", cep = cep, rua=lbl_rua, bairro=lbl_bairro, latitude =latitude ,longitude = longitude, atualizacao = dadosData, logradouro = nome_rua)

#Mai
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
#importando dependencias
import os
import unicodedata
import json
import numpy
import pandas
import requests
from flask import Flask, jsonify, request
from ipyleaflet import Map, Marker
from pandas import json_normalize
from dotenv import load_dotenv, find_dotenv

#acha o arquivo .ENV com a senha do kaggle na estrutura do projeto
dotenv_path = find_dotenv()
#carrega o arquivo
load_dotenv(dotenv_path)

#usando a api do cep aberto para pesquisar ceps
token = os.environ.get("CEP_ABERTO_TOKEN") #pegue seu token pessoal após cadastro no CEP Aberto
headers = {'Authorization': 'Token token=%s' % token}

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

@app.route('/')
def covid_around_me():
    url = 'https://opendata.arcgis.com/datasets/b54234c151aa4d01b488dc12aafd5574_0/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
    result = requests.get(url)
    j = result.json()
    j2 = j['features']

    j2Str = json.dumps(j2)
    val = j2Str.replace(r"u\ufffd", "?").replace(r"\ufffd", "?")
    j = json.loads(val)

    i = 0
    listoflists = []
    a_list = []
    for line in j:
        for v in line.values():
            for key, value in v.items():
                # print(key, value)
                if i % 2 == 0:
                    a_list = value.split(';')
                    listoflists.append(a_list[:])
                i += 1

    df = pandas.DataFrame(numpy.array(listoflists),
                          columns=["dt_notific", "dt_inicio_sintomas", "bairro_resid__estadia", "ap_residencia_estadia",
                                   "evolcao", "dt_obito", "CEP", "Data_atualizacao"])

    digiteCep = 20540195
    buscaCep = search_by_cep("20540195")
    bairroCep = strip_accents(buscaCep['bairro'])

    casos_sua_rua = df.loc[df.CEP == digiteCep, :]
    print('Casos na sua Rua: {0}'.format(len(casos_sua_rua)))
    lbl_rua = 'Casos na sua Rua: {0}'.format(len(casos_sua_rua))

    casos_seu_bairro = df.loc[df.bairro_resid__estadia == bairroCep.upper(), :]
    print('Casos no seu Bairro: {0}'.format(len(casos_seu_bairro)))
    lbl_bairro = 'Casos no seu Bairro: {0}'.format(len(casos_seu_bairro))

    return jsonify(rua = lbl_rua, bairro = lbl_bairro)

    #if request.headers.get('Authorization') == '42':
    #    return jsonify({"42": "a resposta para a vida, o universo e tudo mais"})
    #return jsonify({"message": "Não entre em pânico!"})

#Main
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
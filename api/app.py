import numpy as np
import pandas as pd
import traceback
import jaro

from flask import Flask,request,jsonify,make_response
from flask_restful import Resource, Api
from flask_cors import CORS

from models.request import RequestModel
from models.response import ResponseModel

app = Flask(__name__)

CORS(app)

api = Api(app)

print("carregando o modelo...")
# carrega
from joblib import load
clf = load('model.joblib')  # model
cat = load('cat_pipeline.bin')  # cat
num = load('num_pipeline.bin')  # num

print("carregou o modelo...")

@app.route('/score', methods=['POST'])
def get_score():
    request_data = request.get_json()

    req = RequestModel()

    req.nome = request_data['nome']
    req.email = request_data['email']
    req.cpf = request_data['cpf']
    req.telefone = request_data['telefone']
    req.rua = request_data['rua']
    req.bairro = request_data['bairro']
    req.cidade = request_data['cidade']
    req.estado = request_data['estado']
    req.cep = request_data['cep']
    req.data_de_nascimento = request_data['data_de_nascimento']
    req.produto = request_data['produto']
    req.restringido = request_data['restringido']
    req.bloqueado = request_data['bloqueado']
    req.user_agent = request.headers.get('User-Agent')  # request_data['user_agent']
    req.imei = request_data['imei']

    app.logger.info(vars(req))

    prefixo_email = req.email.split('@')[0]
    name_match_email = compara_tecnicas(prefixo_email, req.nome)
    name_match_email = round(name_match_email * 100, 2)

    instance = {
        'nome': [req.nome],
        'email': [req.email],
        'produto': [req.produto],
        'bloqueado': [str(req.bloqueado)],
        'restringido': [str(req.restringido)],
        'nameMatchEmail': [name_match_email]
    }

    # predict
    instance = pd.DataFrame(instance)
    #
    cat_features = cat.transform(instance)
    num_features = num.transform(instance)
    #
    data_instance = np.hstack([cat_features, num_features])

    pred_y = clf.predict(data_instance)
    is_fraude = (pred_y > 0.5)

    response = make_response(jsonify(
        {
            "score": str(pred_y[0]),
            "is_fraud": str(is_fraude[0])
        }
    ), 200)
    response.headers["Content-Type"] = "application/json"
    app.logger.info(vars(req))

    return response


def compara_tecnicas(prefixo, nome_completo):
    return jaro.jaro_winkler_metric(nome_completo, prefixo)


if __name__ == '__main__':
    app.run(debug=True)
    # prefixo_email = 'test'
    # name_match_email = compara_tecnicas(prefixo_email, 'teste teste')
    # name_match_email = round(name_match_email * 100, 2)
    #
    # instance = {
    #     'nome': ['teste teste'],
    #     'email': ['xablau.99@gmail.com'],
    #     'produto': ['Combate'],
    #     'bloqueado': ['True'],
    #     'restringido': ['True'],
    #     'nameMatchEmail': [name_match_email]
    # }
    #
    # # predict
    # instance = pd.DataFrame(instance)
    # #
    # cat_features = cat.transform(instance)
    # num_features = num.transform(instance)
    # #
    # data_instance = np.hstack([cat_features, num_features])
    # pred_y = clf.predict(data_instance)
    # print(pred_y)
    # is_fraude = (pred_y > 0.5)
    # print(is_fraude)
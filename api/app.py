from flask import Flask,request,jsonify,make_response
from flask_restful import Resource, Api
from flask_cors import CORS
from models.request import RequestModel
from models.response import ResponseModel

app = Flask(__name__)

CORS(app)

api = Api(app)

@app.route('/score', methods=['POST'])
def getScore():
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
    req.user_agent = request_data['user_agent']
    req.imei = request_data['imei']


    res = ResponseModel()
    res.nome = req.nome
    res.email = req.email

    response = make_response(
        jsonify(
            {"GloboIDScore": res.score, "nome": res.nome, "email": res.email}
        ),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == '__main__':
    app.run(debug=True)
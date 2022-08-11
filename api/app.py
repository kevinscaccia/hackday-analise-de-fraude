from flask import Flask,request
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

api = Api(app)

class helloWorld(Resource):
    def get(self):
        print("Hello World :3")

api.add_resource(helloWorld, '/helloWorld')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from http import HTTPStatus
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

# USUARIOS = {
#     'breno': '123',
#     'campos': '321'
# }

# @auth.verify_password
# def verificacao(login, senha):
#     print("Validando usuário")
#     print(USUARIOS.get(login) == senha)
#     if not(login, senha):
#         return False
#     return USUARIOS.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not(login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                "status": HTTPStatus.NOT_FOUND,
                "mensagem": "Registro não encontrado."
            }
        return response
        
    def put(self,nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'status': HTTPStatus.OK,
            'mensagem': 'Registro inserido',
            'dados': dados
        }
        return response

    def post(self):
        pessoa = Pessoas()
        dados = request.json
        response = {
            'status': HTTPStatus.OK,
            'mensagem': 'Registro inserido',
            'dados': dados
        }
        return response
    
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        pessoa.delete()
        response = {
            'status': HTTPStatus.OK,
            'mensagem': 'Registro excluído',
            'pessoa': pessoa.nome
        }
        return response

class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        return response
    
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'status': HTTPStatus.OK,
            'mensagem': 'Registro inserido',
            'dados': dados
        }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id': i.id, 'nome': i.nome, 'pessoa': i.pessoa.nome} for i in atividades]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'status': HTTPStatus.OK,
            'pessoa': atividade.pessoa.nome,
            'atividade': atividade.nome,
            'id': atividade.id
        }
        return response

api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')

if __name__ == '__main__':
    app.run(debug=True)

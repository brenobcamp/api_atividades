from models import Pessoas, Usuarios

def inserir_pessoas():
    pessoa = Pessoas(nome='Breno', idade=25)
    print(pessoa)
    pessoa.save()

def consulta():
    pessoa = Pessoas.query.all()
    for i in pessoa:
        print(i.nome, i.idade)
    pessoa = Pessoas.query.filter_by(nome='Breno')
    for p in pessoa:
        print(p.nome)

def altera_dados():
    pessoa = Pessoas.query.filter_by(nome='Breno').first()
    pessoa.idade = 21
    pessoa.save()

def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Breno').first()
    pessoa.delete()

def inserir_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == '__main__':
    # inserir_usuario('breno', '123')
    # inserir_usuario('campos', '321')
    consulta_todos_usuarios()
    # inserir_pessoas()
    # exclui_pessoa()
    # consulta()
    # altera_dados()

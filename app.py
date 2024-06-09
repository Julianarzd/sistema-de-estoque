from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)


class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), unique=True, nullable=False)
    departamento = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'departamento': self.departamento,
                'quantidade': self.quantidade, 'preco': self.preco}


with app.app_context():
    db.create_all()


# Rota de teste, inicio
@app.route('/inicio', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'Página de inicio)'}), 200)


# Criando um Usuario
@app.route('/estoque', methods=['POST'])
def create_produto():
    try:
        data = request.get_json()
        novo_produto = Produto(nome=data['nome'], departamento=data['departamento'],
                               quantidade=data['quantidade'], preco=data['preco'])
        db.session.add(novo_produto)
        db.session.commit()
        return make_response(jsonify({'message': 'Produto cadastrado!'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao cadastrar o produto. :('}), 500)


# Obtendo todos usuarios
@app.route('/estoque', methods=['GET'])
def get_produtos():
    try:
        produtos = Produto.query.all()
        return make_response(
            jsonify({'message': 'Todos produtos obtidos com sucesso!',
                     'produtos': [produto.json() for produto in produtos]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao obter os produtos'}), 500)


# Obtendo um usuario por id
@app.route('/estoque/<int:id>', methods=['GET'])
def get_produto(id):
    try:
        produto = Produto.query.filter_by(id=id).first()
        if produto:
            return make_response(jsonify({'message': 'Produto Encontrado!', 'produto': produto.json()}), 200)
        return make_response(jsonify({'message': 'Produto não encontrado'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao tentar encontrar um produto'}), 500)


# Atualizando dados de um produto
@app.route('/estoque/<int:id>', methods=['PUT'])
def update_produto(id):
    try:
        produto = Produto.query.filter_by(id=id).first()
        if produto:
            data = request.get_json()
            produto.nome = data['nome']
            produto.departamento = data['departamento']
            produto.quantidade = data['quantidade']
            produto.preco = data['preco']
            db.session.commit()
            return make_response(jsonify({'message': 'Dados do produto atualizado com sucesso!'}), 200)
        return make_response(jsonify({'message': 'Produto não encontrado'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao tentar atualizar um produto'}), 500)


# Excluindo um produto
@app.route('/estoque/<int:id>', methods=['DELETE'])
def delete_produto(id):
    try:
        produto = Produto.query.filter_by(id=id).first()
        if produto:
            db.session.delete(produto)
            db.session.commit()
            return make_response(jsonify({'message': 'Produto excluido com sucesso'}), 200)
        return make_response(jsonify({'message': 'Produto nao encontrado'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Erro ao tentar excluir um produto'}), 500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

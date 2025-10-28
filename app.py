# Importação
from datetime import date
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS ``
from flask_login import UserMixin
# Instância do app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
CORS(app)

# Instância do banco de dados
db = SQLAlchemy(app)

# Definir modelo de usuário 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get('username')).first()

    if user and data.get("password") == user.password:
            return jsonify({"message": "Login bem-sucedido"}), 200
    return jsonify({"error": "Credenciais inválidas"}), 401


# Definir modelo de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Criar o banco de dados
@app.route('/api/products/add', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', '')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "produto cadastrado com sucesso"}), 201


# Rota para deletar um produto
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if  product:
       db.session.delete(product)
       db.session.commit()
       return jsonify({"message": "Produto deletetado com sucesso"})
    return jsonify({"ERROR": "Produto não encontrado"}), 404
    
# Rota para obter um produto pelo ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"ERROR": "Produto não encontrado"}), 404


# Rota para atualizar um produto pelo ID    
@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"ERROR": "Produto não encontrado"}), 404

    data = request.json
    
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()  

    return jsonify({"message": "Produto atualizado com sucesso"})


# Rota para obter todos os produtos
@app.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify(products_list)

# Definir rota raiz e a função
@app.route('/')
def hello_world():
    return 'Hello, world!'


# Executar o app
if __name__ == "__main__":
    app.run(debug=True)


# Importação
from datetime import date
from itertools import product
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin,login_user, LoginManager, login_required, logout_user, current_user

# Instância do app
<<<<<<< HEAD:aplication.py
aplication  = Flask(__name__)
aplication.config['SECRET_KEY'] = 'teste'
aplication.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
CORS(aplication)

login_manager = LoginManager()

=======
app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
CORS(app)
login_manager = LoginManager()
>>>>>>> origin/master:app.py
# Instância do banco de dados
db = SQLAlchemy(aplication)
login_manager.init_app(aplication)
login_manager.login_view = 'login'  

# Definir modelo de usuário 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)
#Autenticação de usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@aplication.route('/login', methods=['POST'])
def login():
    data = request.json
    
    user = User.query.filter_by(username=data.get('username')).first()

    if user and data.get("password") == user.password:
            login_user(user)    
            return jsonify({"message": "Login bem-sucedido"}), 200
    return jsonify({"error": "Credenciais inválidas"}), 401

@aplication.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout bem-sucedido"}), 200
# Definir modelo de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
# Definir modelo de item do carrinho
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)    
# adicionar produto
@aplication.route('/api/products/add', methods=['POST'])
@login_required
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
@aplication.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if  product:
       db.session.delete(product)
       db.session.commit()
       return jsonify({"message": "Produto deletetado com sucesso"})
    return jsonify({"ERROR": "Produto não encontrado"}), 404
    
# Rota para obter um produto pelo ID
@aplication.route('/api/products/<int:product_id>', methods=['GET'])
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
@aplication.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
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
@aplication.route('/api/products', methods=['GET'])
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

#checkpoint para criar o banco de dados
@aplication.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(product_id)
    
    if user and product:
        CartItem_item = CartItem(user_id=user.id, product_id=product.id,)
        db.session.add(CartItem_item)
        db.session.commit()

        return jsonify({"message": "Adicionado com sucesso"}), 200
    return jsonify({"error": "Usuário ou produto não encontrado"}), 404

@aplication.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first() 
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({"message": "Removido com sucesso"}), 200
        return jsonify({"message": "Item não encontrado no carrinho"}), 404
<<<<<<< HEAD:aplication.py

@aplication.route('/api/cart', methods=['GET'])    
=======
    
@app.route('/api/cart', methods=['GET'])    
>>>>>>> origin/master:app.py
@login_required
def view_cart():
    user = User.query.get(int(current_user.id))
    cart_items = user.CartIt
    cart_content = []
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)   
        cart_content.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart_item.quantity
        })

    return jsonify(cart_content), 200

@aplication.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart_items = user.CartIt
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Checkout realizado com sucesso"}), 200

if __name__ == "__main__":
<<<<<<< HEAD:aplication.py
    aplication.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> origin/master:app.py

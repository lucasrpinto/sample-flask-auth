# Importação de módulos
import bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask import Flask, jsonify, request
# Importação de pastas
from models.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# View Login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        # Login
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):     
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso!"})
    return jsonify({"message": "Credenciais inválidas!"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
    
    return jsonify({'message': 'Credenciais inválidas!'}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {'username': user.username, "role": user.role}
    
    return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida!"}), 403
    
    if user and data.get('password'):
        hashed_password = bcrypt.hashpw(str.encode(data.get('password')), bcrypt.gensalt())
        user.password = hashed_password
        db.session.commit()

        return jsonify({'message': f'Usuário {id_user} atualizado com sucesso'})
    
    return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida!"}), 403
    if  id_user == current_user.id:
        return jsonify({'message': 'Usuário logado, não pode ser excluido!'}), 403
    if user and id_user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'Usuário {id_user} removido com sucesso!'})
    
    return jsonify({'message': 'Usuário não encontrado!'}), 404

# Session <- Conexão ativa
if __name__ == '__main__':
    app.run(debug=True)


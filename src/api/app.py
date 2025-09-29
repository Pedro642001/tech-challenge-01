from datetime import timedelta
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os 
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ---- Configuração ----
app = Flask(__name__)
# Configuração JWT
# Em produção, usar uma chave secreta forte e mantê-la segura
# Pode ser gerada com: os.urandom(24)
# exemplo de como armazenar em variável de ambiente:
# export JWT_SECRET_KEY="wflYqfTXbYWhJ8bA1FhX3_g2M2QJbey6h7E7hYX91UzPNu7RtFhW8v-0BBByDJZx0tG8IYg1Ob3zM7FHz0t98A"
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')    # busco na variável de ambiente
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' #'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# ---- Modelo User ----
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    def set_password(self, password):
        """Gera hash da senha"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Valida senha"""
        return bcrypt.check_password_hash(self.password_hash, password)

# Criar tabelas no banco (executado na primeira vez)
with app.app_context():
    db.create_all()

# Blacklist em memória para tokens revogados
BLACKLIST = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST

# ---- Rotas públicas ----
@app.route('/register', methods=['POST'])
def register():
    """Cria um novo usuário"""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')

    if not username or not password:
        return jsonify(msg="username e password são obrigatórios"), 400

    if User.query.filter_by(username=username).first():
        return jsonify(msg="usuário já existe"), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg="usuário criado com sucesso"), 201

@app.route('/login', methods=['POST'])
def login():
    """Login com username/password"""
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(msg="username e password são obrigatórios"), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify(msg="credenciais inválidas"), 401

    claims = {'role': user.role}
    access_token = create_access_token(identity=user.username, additional_claims=claims)
    refresh_token = create_refresh_token(identity=user.username)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)   
def refresh():
    """Usa refresh token para gerar novo access token"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    claims = {'role': user.role}
    new_access = create_access_token(identity=current_user, additional_claims=claims)
    return jsonify(access_token=new_access), 200

# ---- Rotas protegidas ----
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(msg=f"Olá, {current_user}. Esta é sua profile."), 200

@app.route('/admin-area', methods=['GET'])
@jwt_required()
def admin_area():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify(msg="acesso negado: necessita role=admin"), 403
    return jsonify(msg="Bem-vindo à área administrativa"), 200

@app.route('/api/v1/scrapping/trigger', methods=['GET'])
@jwt_required()
def execute():
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify(msg="acesso negado: necessita role=admin"), 403
    else: 
        from scripts.scrapping import Scrapping
        scrapper = Scrapping()
        try:
            qtde = scrapper.run()
            return jsonify({f"qtd livros importados": qtde}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500    

@app.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    """Revoga o token atual"""
    jti = get_jwt()['jti']
    BLACKLIST.add(jti)
    return jsonify(msg="token revogado (logout) com sucesso"), 200

# ---- Health check ----
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(msg="pong"), 200

# ---- Run ----
if __name__ == '__main__':
    app.run(debug=True)

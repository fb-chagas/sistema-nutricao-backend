from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os

# Inicializar extensões
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configuração do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///sistema_nutricao.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-temporaria')
    
    # Aplicar configurações adicionais
    if config:
        app.config.update(config)
    
    # Inicializar extensões com o app
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Rota principal para verificar se o sistema está funcionando
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "message": "Sistema de Nutrição - API funcionando!",
            "status": "online",
            "versao": "1.0.0"
        })
    
    # Rota de teste para módulos
    @app.route('/api/teste', methods=['GET'])
    def teste():
        return jsonify({
            "message": "API de teste funcionando!",
            "modulos_disponiveis": [
                "nfe", "fornecedores", "insumos", "contratos", 
                "cotacoes", "controle_mensal", "fechamento"
            ]
        })
    
    return app

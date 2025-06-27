from backend import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200))
    cargo = db.Column(db.String(100))
    departamento = db.Column(db.String(100))
    nivel_acesso = db.Column(db.String(20), default='usuario')
    ativo = db.Column(db.Boolean, default=True)
    ultimo_acesso = db.Column(db.DateTime)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def set_password(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

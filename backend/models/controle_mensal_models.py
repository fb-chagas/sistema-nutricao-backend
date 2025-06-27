from backend import db
from datetime import datetime

class RegistroMensal(db.Model):
    __tablename__ = 'registros_mensais'
    
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='aberto')
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    entregas = db.relationship('EntregaMensal', backref='registro_mensal', lazy=True, cascade="all, delete-orphan")

class EntregaMensal(db.Model):
    __tablename__ = 'entregas_mensais'
    
    id = db.Column(db.Integer, primary_key=True)
    registro_mensal_id = db.Column(db.Integer, db.ForeignKey('registros_mensais.id'), nullable=False)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('notas_fiscais.id'))
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    data_entrega = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

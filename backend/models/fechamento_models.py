from backend import db
from datetime import datetime

class CustoMedio(db.Model):
    __tablename__ = 'custos_medios'
    
    id = db.Column(db.Integer, primary_key=True)
    insumo_id = db.Column(db.Integer, db.ForeignKey('insumos.id'), nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    quantidade_total = db.Column(db.Float, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    custo_medio = db.Column(db.Float, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Fechamento(db.Model):
    __tablename__ = 'fechamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data_fechamento = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='fechado')
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

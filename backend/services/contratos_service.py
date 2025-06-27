from ..models.contratos_models import db, Contrato, ItemContrato, Cotacao, PlanejamentoCompra
from ..models.nfe_models import Fornecedor, Insumo
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from decimal import Decimal

class ItemContratoSchema(Schema):
    insumo_id = fields.Integer(required=True)
    quantidade = fields.Decimal(required=True)
    valor_unitario = fields.Decimal(required=True)
    valor_total = fields.Decimal(required=True)
    data_entrega_prevista = fields.Date(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")
    
    @validates_schema
    def validate_valores(self, data, **kwargs):
        # Verificar se valor_total é igual a quantidade * valor_unitario
        if 'quantidade' in data and 'valor_unitario' in data and 'valor_total' in data:
            calc_total = Decimal(data['quantidade']) * Decimal(data['valor_unitario'])
            if abs(Decimal(data['valor_total']) - calc_total) > Decimal('0.01'):
                raise ValidationError("Valor total não corresponde a quantidade * valor unitário")


class ContratoSchema(Schema):
    numero = fields.String(required=True)
    fornecedor_id = fields.Integer(required=True)
    data_inicio = fields.Date(required=True)
    data_fim = fields.Date(required=True)
    valor_total = fields.Decimal(required=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    itens = fields.List(fields.Nested(ItemContratoSchema), required=False)
    
    @validates('fornecedor_id')
    def validate_fornecedor(self, value):
        fornecedor = Fornecedor.query.get(value)
        if not fornecedor:
            raise ValidationError(f"Fornecedor com ID {value} não encontrado")
    
    @validates('numero')
    def validate_numero(self, value):
        # Verificar se já existe um contrato com este número
        if self.context.get('contrato_id'):
            # Caso de atualização, ignorar o próprio contrato
            existing = Contrato.query.filter(
                Contrato.numero == value,
                Contrato.id != self.context.get('contrato_id')
            ).first()
        else:
            # Caso de criação
            existing = Contrato.query.filter_by(numero=value).first()
            
        if existing:
            raise ValidationError(f"Já existe um contrato com o número {value}")
    
    @validates_schema
    def validate_datas(self, data, **kwargs):
        # Verificar se data_fim é posterior a data_inicio
        if 'data_inicio' in data and 'data_fim' in data:
            if data['data_fim'] < data['data_inicio']:
                raise ValidationError("Data fim deve ser posterior à data início")


class CotacaoSchema(Schema):
    data = fields.Date(required=True)
    fornecedor_id = fields.Integer(required=True)
    insumo_id = fields.Integer(required=True)
    preco_unitario = fields.Decimal(required=True)
    quantidade = fields.Decimal(allow_none=True)
    prazo_entrega = fields.Integer(allow_none=True)
    validade = fields.Date(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('fornecedor_id')
    def validate_fornecedor(self, value):
        fornecedor = Fornecedor.query.get(value)
        if not fornecedor:
            raise ValidationError(f"Fornecedor com ID {value} não encontrado")
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")


class PlanejamentoCompraSchema(Schema):
    mes_referencia = fields.Date(required=True)
    insumo_id = fields.Integer(required=True)
    quantidade_prevista = fields.Decimal(required=True)
    valor_unitario_previsto = fields.Decimal(allow_none=True)
    valor_total_previsto = fields.Decimal(allow_none=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")
    
    @validates_schema
    def validate_valores(self, data, **kwargs):
        # Verificar se valor_total_previsto é igual a quantidade_prevista * valor_unitario_previsto
        if ('quantidade_prevista' in data and 
            'valor_unitario_previsto' in data and 
            'valor_total_previsto' in data and 
            data['valor_unitario_previsto'] is not None and 
            data['valor_total_previsto'] is not None):
            
            calc_total = Decimal(data['quantidade_prevista']) * Decimal(data['valor_unitario_previsto'])
            if abs(Decimal(data['valor_total_previsto']) - calc_total) > Decimal('0.01'):
                raise ValidationError("Valor total previsto não corresponde a quantidade prevista * valor unitário previsto")


def criar_contrato(data):
    """Cria um novo contrato"""
    schema = ContratoSchema()
    validated_data = schema.load(data)
    
    novo_contrato = Contrato(
        numero=validated_data['numero'],
        fornecedor_id=validated_data['fornecedor_id'],
        data_inicio=validated_data['data_inicio'],
        data_fim=validated_data['data_fim'],
        valor_total=validated_data['valor_total'],
        status=validated_data.get('status', 'ativo'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(novo_contrato)
    db.session.flush()  # Para obter o ID do contrato
    
    # Adicionar itens do contrato
    if 'itens' in validated_data and isinstance(validated_data['itens'], list):
        for item_data in validated_data['itens']:
            item = ItemContrato(
                contrato_id=novo_contrato.id,
                insumo_id=item_data['insumo_id'],
                quantidade=item_data['quantidade'],
                valor_unitario=item_data['valor_unitario'],
                valor_total=item_data['valor_total'],
                data_entrega_prevista=item_data.get('data_entrega_prevista'),
                observacoes=item_data.get('observacoes')
            )
            db.session.add(item)
    
    db.session.commit()
    
    return novo_contrato


def atualizar_contrato(contrato_id, data):
    """Atualiza um contrato existente"""
    contrato = Contrato.query.get(contrato_id)
    if not contrato:
        return None
    
    schema = ContratoSchema(context={'contrato_id': contrato_id})
    validated_data = schema.load(data)
    
    # Atualizar campos do contrato
    for key, value in validated_data.items():
        if key != 'itens':
            setattr(contrato, key, value)
    
    contrato.atualizado_em = datetime.utcnow()
    
    # Remover itens antigos
    for item in contrato.itens:
        db.session.delete(item)
    
    # Adicionar novos itens
    if 'itens' in validated_data and isinstance(validated_data['itens'], list):
        for item_data in validated_data['itens']:
            item = ItemContrato(
                contrato_id=contrato.id,
                insumo_id=item_data['insumo_id'],
                quantidade=item_data['quantidade'],
                valor_unitario=item_data['valor_unitario'],
                valor_total=item_data['valor_total'],
                data_entrega_prevista=item_data.get('data_entrega_prevista'),
                observacoes=item_data.get('observacoes')
            )
            db.session.add(item)
    
    db.session.commit()
    
    return contrato


def buscar_contrato(contrato_id):
    """Busca um contrato pelo ID"""
    return Contrato.query.get(contrato_id)


def listar_contratos(filtros=None):
    """Lista contratos com filtros opcionais"""
    query = Contrato.query
    
    if filtros:
        if 'numero' in filtros:
            query = query.filter(Contrato.numero.ilike(f"%{filtros['numero']}%"))
        
        if 'fornecedor_id' in filtros:
            query = query.filter_by(fornecedor_id=filtros['fornecedor_id'])
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
        
        if 'data_inicio' in filtros and 'data_fim' in filtros:
            query = query.filter(
                Contrato.data_inicio >= datetime.strptime(filtros['data_inicio'], '%Y-%m-%d').date(),
                Contrato.data_fim <= datetime.strptime(filtros['data_fim'], '%Y-%m-%d').date()
            )
    
    # Ordenar por data de início decrescente
    query = query.order_by(Contrato.data_inicio.desc())
    
    return query.all()


def excluir_contrato(contrato_id):
    """Exclui um contrato (exclusão lógica)"""
    contrato = Contrato.query.get(contrato_id)
    if not contrato:
        return False
    
    # Exclusão lógica
    contrato.status = 'cancelado'
    contrato.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True


def criar_cotacao(data):
    """Cria uma nova cotação"""
    schema = CotacaoSchema()
    validated_data = schema.load(data)
    
    nova_cotacao = Cotacao(
        data=validated_data['data'],
        fornecedor_id=validated_data['fornecedor_id'],
        insumo_id=validated_data['insumo_id'],
        preco_unitario=validated_data['preco_unitario'],
        quantidade=validated_data.get('quantidade'),
        prazo_entrega=validated_data.get('prazo_entrega'),
        validade=validated_data.get('validade'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(nova_cotacao)
    db.session.commit()
    
    return nova_cotacao


def atualizar_cotacao(cotacao_id, data):
    """Atualiza uma cotação existente"""
    cotacao = Cotacao.query.get(cotacao_id)
    if not cotacao:
        return None
    
    schema = CotacaoSchema()
    validated_data = schema.load(data)
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(cotacao, key, value)
    
    cotacao.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return cotacao


def buscar_cotacao(cotacao_id):
    """Busca uma cotação pelo ID"""
    return Cotacao.query.get(cotacao_id)


def listar_cotacoes(filtros=None):
    """Lista cotações com filtros opcionais"""
    query = Cotacao.query
    
    if filtros:
        if 'insumo_id' in filtros:
            query = query.filter_by(insumo_id=filtros['insumo_id'])
        
        if 'fornecedor_id' in filtros:
            query = query.filter_by(fornecedor_id=filtros['fornecedor_id'])
        
        if 'data_inicio' in filtros and 'data_fim' in filtros:
            query = query.filter(
                Cotacao.data >= datetime.strptime(filtros['data_inicio'], '%Y-%m-%d').date(),
                Cotacao.data <= datetime.strptime(filtros['data_fim'], '%Y-%m-%d').date()
            )
    
    # Ordenar por data decrescente
    query = query.order_by(Cotacao.data.desc())
    
    return query.all()


def excluir_cotacao(cotacao_id):
    """Exclui uma cotação"""
    cotacao = Cotacao.query.get(cotacao_id)
    if not cotacao:
        return False
    
    db.session.delete(cotacao)
    db.session.commit()
    
    return True


def criar_planejamento(data):
    """Cria um novo planejamento de compra"""
    schema = PlanejamentoCompraSchema()
    validated_data = schema.load(data)
    
    # Calcular valor total se não fornecido
    if ('quantidade_prevista' in validated_data and 
        'valor_unitario_previsto' in validated_data and 
        validated_data['valor_unitario_previsto'] is not None and 
        ('valor_total_previsto' not in validated_data or validated_data['valor_total_previsto'] is None)):
        
        valor_total = Decimal(validated_data['quantidade_prevista']) * Decimal(validated_data['valor_unitario_previsto'])
        validated_data['valor_total_previsto'] = valor_total
    
    novo_planejamento = PlanejamentoCompra(
        mes_referencia=validated_data['mes_referencia'],
        insumo_id=validated_data['insumo_id'],
        quantidade_prevista=validated_data['quantidade_prevista'],
        valor_unitario_previsto=validated_data.get('valor_unitario_previsto'),
        valor_total_previsto=validated_data.get('valor_total_previsto'),
        status=validated_data.get('status', 'pendente'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(novo_planejamento)
    db.session.commit()
    
    return novo_planejamento


def atualizar_planejamento(planejamento_id, data):
    """Atualiza um planejamento de compra existente"""
    planejamento = PlanejamentoCompra.query.get(planejamento_id)
    if not planejamento:
        return None
    
    schema = PlanejamentoCompraSchema()
    validated_data = schema.load(data)
    
    # Calcular valor total se não fornecido
    if ('quantidade_prevista' in validated_data and 
        'valor_unitario_previsto' in validated_data and 
        validated_data['valor_unitario_previsto'] is not None and 
        ('valor_total_previsto' not in validated_data or validated_data['valor_total_previsto'] is None)):
        
        valor_total = Decimal(validated_data['quantidade_prevista']) * Decimal(validated_data['valor_unitario_previsto'])
        validated_data['valor_total_previsto'] = valor_total
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(planejamento, key, value)
    
    planejamento.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return planejamento


def buscar_planejamento(planejamento_id):
    """Busca um planejamento de compra pelo ID"""
    return PlanejamentoCompra.query.get(planejamento_id)


def listar_planejamentos(filtros=None):
    """Lista planejamentos de compra com filtros opcionais"""
    query = PlanejamentoCompra.query
    
    if filtros:
        if 'insumo_id' in filtros:
            query = query.filter_by(insumo_id=filtros['insumo_id'])
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
        
        if 'mes_referencia' in filtros:
            # Filtrar pelo mês de referência (formato: YYYY-MM)
            ano, mes = filtros['mes_referencia'].split('-')
            query = query.filter(
                db.extract('year', PlanejamentoCompra.mes_referencia) == int(ano),
                db.extract('month', PlanejamentoCompra.mes_referencia) == int(mes)
            )
    
    # Ordenar por mês de referência decrescente
    query = query.order_by(PlanejamentoCompra.mes_referencia.desc())
    
    return query.all()


def excluir_planejamento(planejamento_id):
    """Exclui um planejamento de compra (exclusão lógica)"""
    planejamento = PlanejamentoCompra.query.get(planejamento_id)
    if not planejamento:
        return False
    
    # Exclusão lógica
    planejamento.status = 'cancelado'
    planejamento.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True

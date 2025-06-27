from ..models.nfe_models import db, Fornecedor, Insumo, NotaFiscal, ItemNotaFiscal
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from decimal import Decimal

class FornecedorSchema(Schema):
    nome = fields.String(required=True)
    cnpj = fields.String(required=True)
    endereco = fields.String(allow_none=True)
    telefone = fields.String(allow_none=True)
    email = fields.String(allow_none=True)
    contato = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('cnpj')
    def validate_cnpj(self, value):
        # Verificar se já existe um fornecedor com este CNPJ
        if self.context.get('fornecedor_id'):
            # Caso de atualização, ignorar o próprio fornecedor
            existing = Fornecedor.query.filter(
                Fornecedor.cnpj == value,
                Fornecedor.id != self.context.get('fornecedor_id')
            ).first()
        else:
            # Caso de criação
            existing = Fornecedor.query.filter_by(cnpj=value).first()
            
        if existing:
            raise ValidationError(f"Já existe um fornecedor com o CNPJ {value}")


class InsumoSchema(Schema):
    nome = fields.String(required=True)
    codigo = fields.String(required=True)
    descricao = fields.String(allow_none=True)
    unidade_medida = fields.String(required=True)
    estoque_minimo = fields.Decimal(allow_none=True)
    estoque_atual = fields.Decimal(allow_none=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('codigo')
    def validate_codigo(self, value):
        # Verificar se já existe um insumo com este código
        if self.context.get('insumo_id'):
            # Caso de atualização, ignorar o próprio insumo
            existing = Insumo.query.filter(
                Insumo.codigo == value,
                Insumo.id != self.context.get('insumo_id')
            ).first()
        else:
            # Caso de criação
            existing = Insumo.query.filter_by(codigo=value).first()
            
        if existing:
            raise ValidationError(f"Já existe um insumo com o código {value}")


class ItemNotaFiscalSchema(Schema):
    insumo_id = fields.Integer(required=True)
    quantidade = fields.Decimal(required=True)
    valor_unitario = fields.Decimal(required=True)
    valor_total = fields.Decimal(required=True)
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


class NotaFiscalSchema(Schema):
    numero = fields.String(required=True)
    serie = fields.String(required=True)
    data_emissao = fields.Date(required=True)
    data_entrada = fields.Date(required=True)
    fornecedor_id = fields.Integer(required=True)
    valor_total = fields.Decimal(required=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    itens = fields.List(fields.Nested(ItemNotaFiscalSchema), required=False)
    
    @validates('fornecedor_id')
    def validate_fornecedor(self, value):
        fornecedor = Fornecedor.query.get(value)
        if not fornecedor:
            raise ValidationError(f"Fornecedor com ID {value} não encontrado")
    
    @validates('numero')
    def validate_numero(self, value):
        # Verificar se já existe uma nota fiscal com este número e série
        if 'serie' in self.data:
            serie = self.data['serie']
            
            if self.context.get('nota_fiscal_id'):
                # Caso de atualização, ignorar a própria nota fiscal
                existing = NotaFiscal.query.filter(
                    NotaFiscal.numero == value,
                    NotaFiscal.serie == serie,
                    NotaFiscal.id != self.context.get('nota_fiscal_id')
                ).first()
            else:
                # Caso de criação
                existing = NotaFiscal.query.filter_by(numero=value, serie=serie).first()
                
            if existing:
                raise ValidationError(f"Já existe uma nota fiscal com o número {value} e série {serie}")


def criar_fornecedor(data):
    """Cria um novo fornecedor"""
    schema = FornecedorSchema()
    validated_data = schema.load(data)
    
    novo_fornecedor = Fornecedor(
        nome=validated_data['nome'],
        cnpj=validated_data['cnpj'],
        endereco=validated_data.get('endereco'),
        telefone=validated_data.get('telefone'),
        email=validated_data.get('email'),
        contato=validated_data.get('contato'),
        status=validated_data.get('status', 'ativo'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(novo_fornecedor)
    db.session.commit()
    
    return novo_fornecedor


def atualizar_fornecedor(fornecedor_id, data):
    """Atualiza um fornecedor existente"""
    fornecedor = Fornecedor.query.get(fornecedor_id)
    if not fornecedor:
        return None
    
    schema = FornecedorSchema(context={'fornecedor_id': fornecedor_id})
    validated_data = schema.load(data)
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(fornecedor, key, value)
    
    fornecedor.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return fornecedor


def buscar_fornecedor(fornecedor_id):
    """Busca um fornecedor pelo ID"""
    return Fornecedor.query.get(fornecedor_id)


def listar_fornecedores(filtros=None):
    """Lista fornecedores com filtros opcionais"""
    query = Fornecedor.query
    
    if filtros:
        if 'nome' in filtros:
            query = query.filter(Fornecedor.nome.ilike(f"%{filtros['nome']}%"))
        
        if 'cnpj' in filtros:
            query = query.filter(Fornecedor.cnpj.ilike(f"%{filtros['cnpj']}%"))
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
    
    # Ordenar por nome
    query = query.order_by(Fornecedor.nome)
    
    return query.all()


def excluir_fornecedor(fornecedor_id):
    """Exclui um fornecedor (exclusão lógica)"""
    fornecedor = Fornecedor.query.get(fornecedor_id)
    if not fornecedor:
        return False
    
    # Exclusão lógica
    fornecedor.status = 'inativo'
    fornecedor.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True


def criar_insumo(data):
    """Cria um novo insumo"""
    schema = InsumoSchema()
    validated_data = schema.load(data)
    
    novo_insumo = Insumo(
        nome=validated_data['nome'],
        codigo=validated_data['codigo'],
        descricao=validated_data.get('descricao'),
        unidade_medida=validated_data['unidade_medida'],
        estoque_minimo=validated_data.get('estoque_minimo'),
        estoque_atual=validated_data.get('estoque_atual', 0),
        status=validated_data.get('status', 'ativo'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(novo_insumo)
    db.session.commit()
    
    return novo_insumo


def atualizar_insumo(insumo_id, data):
    """Atualiza um insumo existente"""
    insumo = Insumo.query.get(insumo_id)
    if not insumo:
        return None
    
    schema = InsumoSchema(context={'insumo_id': insumo_id})
    validated_data = schema.load(data)
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(insumo, key, value)
    
    insumo.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return insumo


def buscar_insumo(insumo_id):
    """Busca um insumo pelo ID"""
    return Insumo.query.get(insumo_id)


def listar_insumos(filtros=None):
    """Lista insumos com filtros opcionais"""
    query = Insumo.query
    
    if filtros:
        if 'nome' in filtros:
            query = query.filter(Insumo.nome.ilike(f"%{filtros['nome']}%"))
        
        if 'codigo' in filtros:
            query = query.filter(Insumo.codigo.ilike(f"%{filtros['codigo']}%"))
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
    
    # Ordenar por nome
    query = query.order_by(Insumo.nome)
    
    return query.all()


def excluir_insumo(insumo_id):
    """Exclui um insumo (exclusão lógica)"""
    insumo = Insumo.query.get(insumo_id)
    if not insumo:
        return False
    
    # Exclusão lógica
    insumo.status = 'inativo'
    insumo.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True


def criar_nota_fiscal(data):
    """Cria uma nova nota fiscal"""
    schema = NotaFiscalSchema()
    validated_data = schema.load(data)
    
    nova_nota_fiscal = NotaFiscal(
        numero=validated_data['numero'],
        serie=validated_data['serie'],
        data_emissao=validated_data['data_emissao'],
        data_entrada=validated_data['data_entrada'],
        fornecedor_id=validated_data['fornecedor_id'],
        valor_total=validated_data['valor_total'],
        status=validated_data.get('status', 'ativo'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(nova_nota_fiscal)
    db.session.flush()  # Para obter o ID da nota fiscal
    
    # Adicionar itens da nota fiscal
    if 'itens' in validated_data and isinstance(validated_data['itens'], list):
        for item_data in validated_data['itens']:
            item = ItemNotaFiscal(
                nota_fiscal_id=nova_nota_fiscal.id,
                insumo_id=item_data['insumo_id'],
                quantidade=item_data['quantidade'],
                valor_unitario=item_data['valor_unitario'],
                valor_total=item_data['valor_total'],
                observacoes=item_data.get('observacoes')
            )
            db.session.add(item)
            
            # Atualizar estoque do insumo
            insumo = Insumo.query.get(item_data['insumo_id'])
            if insumo:
                insumo.estoque_atual = (insumo.estoque_atual or 0) + Decimal(item_data['quantidade'])
    
    db.session.commit()
    
    return nova_nota_fiscal


def atualizar_nota_fiscal(nota_fiscal_id, data):
    """Atualiza uma nota fiscal existente"""
    nota_fiscal = NotaFiscal.query.get(nota_fiscal_id)
    if not nota_fiscal:
        return None
    
    schema = NotaFiscalSchema(context={'nota_fiscal_id': nota_fiscal_id})
    validated_data = schema.load(data)
    
    # Reverter o estoque dos itens atuais
    for item in nota_fiscal.itens:
        insumo = Insumo.query.get(item.insumo_id)
        if insumo:
            insumo.estoque_atual = (insumo.estoque_atual or 0) - Decimal(item.quantidade)
    
    # Atualizar campos da nota fiscal
    for key, value in validated_data.items():
        if key != 'itens':
            setattr(nota_fiscal, key, value)
    
    nota_fiscal.atualizado_em = datetime.utcnow()
    
    # Remover itens antigos
    for item in nota_fiscal.itens:
        db.session.delete(item)
    
    # Adicionar novos itens
    if 'itens' in validated_data and isinstance(validated_data['itens'], list):
        for item_data in validated_data['itens']:
            item = ItemNotaFiscal(
                nota_fiscal_id=nota_fiscal.id,
                insumo_id=item_data['insumo_id'],
                quantidade=item_data['quantidade'],
                valor_unitario=item_data['valor_unitario'],
                valor_total=item_data['valor_total'],
                observacoes=item_data.get('observacoes')
            )
            db.session.add(item)
            
            # Atualizar estoque do insumo
            insumo = Insumo.query.get(item_data['insumo_id'])
            if insumo:
                insumo.estoque_atual = (insumo.estoque_atual or 0) + Decimal(item_data['quantidade'])
    
    db.session.commit()
    
    return nota_fiscal


def buscar_nota_fiscal(nota_fiscal_id):
    """Busca uma nota fiscal pelo ID"""
    return NotaFiscal.query.get(nota_fiscal_id)


def listar_notas_fiscais(filtros=None):
    """Lista notas fiscais com filtros opcionais"""
    query = NotaFiscal.query
    
    if filtros:
        if 'numero' in filtros:
            query = query.filter(NotaFiscal.numero.ilike(f"%{filtros['numero']}%"))
        
        if 'fornecedor_id' in filtros:
            query = query.filter_by(fornecedor_id=filtros['fornecedor_id'])
        
        if 'data_inicio' in filtros and 'data_fim' in filtros:
            query = query.filter(
                NotaFiscal.data_emissao >= datetime.strptime(filtros['data_inicio'], '%Y-%m-%d').date(),
                NotaFiscal.data_emissao <= datetime.strptime(filtros['data_fim'], '%Y-%m-%d').date()
            )
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
    
    # Ordenar por data de emissão decrescente
    query = query.order_by(NotaFiscal.data_emissao.desc())
    
    return query.all()


def excluir_nota_fiscal(nota_fiscal_id):
    """Exclui uma nota fiscal (exclusão lógica)"""
    nota_fiscal = NotaFiscal.query.get(nota_fiscal_id)
    if not nota_fiscal:
        return False
    
    # Reverter o estoque dos itens
    for item in nota_fiscal.itens:
        insumo = Insumo.query.get(item.insumo_id)
        if insumo:
            insumo.estoque_atual = (insumo.estoque_atual or 0) - Decimal(item.quantidade)
    
    # Exclusão lógica
    nota_fiscal.status = 'cancelado'
    nota_fiscal.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True

from ..models.controle_mensal_models import db, RegistroMensal, EntregaMensal, ProgramacaoFutura
from ..models.nfe_models import Insumo, NotaFiscal
from ..models.contratos_models import Contrato
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from decimal import Decimal

class EntregaMensalSchema(Schema):
    registro_mensal_id = fields.Integer(required=True)
    data_entrega = fields.Date(required=True)
    quantidade = fields.Decimal(required=True)
    nota_fiscal_id = fields.Integer(allow_none=True)
    contrato_id = fields.Integer(allow_none=True)
    valor_total = fields.Decimal(required=True)
    status_pagamento = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('registro_mensal_id')
    def validate_registro_mensal(self, value):
        registro = RegistroMensal.query.get(value)
        if not registro:
            raise ValidationError(f"Registro mensal com ID {value} não encontrado")
    
    @validates('nota_fiscal_id')
    def validate_nota_fiscal(self, value):
        if value is not None:
            nota_fiscal = NotaFiscal.query.get(value)
            if not nota_fiscal:
                raise ValidationError(f"Nota fiscal com ID {value} não encontrada")
    
    @validates('contrato_id')
    def validate_contrato(self, value):
        if value is not None:
            contrato = Contrato.query.get(value)
            if not contrato:
                raise ValidationError(f"Contrato com ID {value} não encontrado")


class RegistroMensalSchema(Schema):
    mes_referencia = fields.Date(required=True)
    insumo_id = fields.Integer(required=True)
    estoque_inicial = fields.Decimal(required=True)
    quantidade_entregue = fields.Decimal(allow_none=True)
    quantidade_contratada = fields.Decimal(allow_none=True)
    quantidade_paga = fields.Decimal(allow_none=True)
    estoque_final = fields.Decimal(allow_none=True)
    observacoes = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    entregas = fields.List(fields.Nested(EntregaMensalSchema), required=False)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")
    
    @validates_schema
    def validate_mes_referencia_insumo(self, data, **kwargs):
        # Verificar se já existe um registro para o mesmo mês e insumo
        if 'mes_referencia' in data and 'insumo_id' in data:
            # Extrair apenas o ano e mês da data
            mes_ref = datetime.strptime(data['mes_referencia'].strftime('%Y-%m-01'), '%Y-%m-%d').date()
            
            if self.context.get('registro_id'):
                # Caso de atualização, ignorar o próprio registro
                existing = RegistroMensal.query.filter(
                    db.func.date_trunc('month', RegistroMensal.mes_referencia) == mes_ref,
                    RegistroMensal.insumo_id == data['insumo_id'],
                    RegistroMensal.id != self.context.get('registro_id')
                ).first()
            else:
                # Caso de criação
                existing = RegistroMensal.query.filter(
                    db.func.date_trunc('month', RegistroMensal.mes_referencia) == mes_ref,
                    RegistroMensal.insumo_id == data['insumo_id']
                ).first()
                
            if existing:
                raise ValidationError(f"Já existe um registro para o mês {mes_ref.strftime('%Y-%m')} e insumo {data['insumo_id']}")


class ProgramacaoFuturaSchema(Schema):
    mes_referencia = fields.Date(required=True)
    insumo_id = fields.Integer(required=True)
    quantidade_prevista = fields.Decimal(required=True)
    contrato_id = fields.Integer(allow_none=True)
    valor_unitario_previsto = fields.Decimal(allow_none=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")
    
    @validates('contrato_id')
    def validate_contrato(self, value):
        if value is not None:
            contrato = Contrato.query.get(value)
            if not contrato:
                raise ValidationError(f"Contrato com ID {value} não encontrado")


def criar_registro_mensal(data):
    """Cria um novo registro mensal"""
    schema = RegistroMensalSchema()
    validated_data = schema.load(data)
    
    # Calcular valores padrão se não fornecidos
    if 'quantidade_entregue' not in validated_data:
        validated_data['quantidade_entregue'] = 0
    
    if 'quantidade_contratada' not in validated_data:
        validated_data['quantidade_contratada'] = 0
    
    if 'quantidade_paga' not in validated_data:
        validated_data['quantidade_paga'] = 0
    
    if 'estoque_final' not in validated_data:
        # Estoque final = Estoque inicial + Quantidade entregue
        validated_data['estoque_final'] = Decimal(validated_data['estoque_inicial']) + Decimal(validated_data['quantidade_entregue'])
    
    novo_registro = RegistroMensal(
        mes_referencia=validated_data['mes_referencia'],
        insumo_id=validated_data['insumo_id'],
        estoque_inicial=validated_data['estoque_inicial'],
        quantidade_entregue=validated_data['quantidade_entregue'],
        quantidade_contratada=validated_data['quantidade_contratada'],
        quantidade_paga=validated_data['quantidade_paga'],
        estoque_final=validated_data['estoque_final'],
        observacoes=validated_data.get('observacoes'),
        status=validated_data.get('status', 'aberto')
    )
    
    db.session.add(novo_registro)
    db.session.flush()  # Para obter o ID do registro
    
    # Adicionar entregas do registro mensal
    if 'entregas' in validated_data and isinstance(validated_data['entregas'], list):
        for entrega_data in validated_data['entregas']:
            entrega_data['registro_mensal_id'] = novo_registro.id
            entrega = criar_entrega_mensal(entrega_data, commit=False)
            
    db.session.commit()
    
    # Atualizar o estoque atual do insumo
    insumo = Insumo.query.get(validated_data['insumo_id'])
    if insumo:
        insumo.estoque_atual = validated_data['estoque_final']
        db.session.commit()
    
    return novo_registro


def atualizar_registro_mensal(registro_id, data):
    """Atualiza um registro mensal existente"""
    registro = RegistroMensal.query.get(registro_id)
    if not registro:
        return None
    
    schema = RegistroMensalSchema(context={'registro_id': registro_id})
    validated_data = schema.load(data)
    
    # Salvar estoque final antigo para ajustar o estoque do insumo
    estoque_final_antigo = registro.estoque_final
    
    # Atualizar campos do registro
    for key, value in validated_data.items():
        if key != 'entregas':
            setattr(registro, key, value)
    
    # Recalcular estoque final se necessário
    if 'estoque_final' not in validated_data:
        registro.estoque_final = Decimal(registro.estoque_inicial) + Decimal(registro.quantidade_entregue)
    
    registro.atualizado_em = datetime.utcnow()
    
    # Remover entregas antigas
    for entrega in registro.entregas:
        db.session.delete(entrega)
    
    # Adicionar novas entregas
    if 'entregas' in validated_data and isinstance(validated_data['entregas'], list):
        for entrega_data in validated_data['entregas']:
            entrega_data['registro_mensal_id'] = registro.id
            entrega = criar_entrega_mensal(entrega_data, commit=False)
    
    db.session.commit()
    
    # Atualizar o estoque atual do insumo
    insumo = Insumo.query.get(registro.insumo_id)
    if insumo:
        # Ajustar o estoque atual do insumo com a diferença entre o estoque final novo e antigo
        diferenca = Decimal(registro.estoque_final) - Decimal(estoque_final_antigo)
        insumo.estoque_atual = (Decimal(insumo.estoque_atual) + diferenca) if insumo.estoque_atual else diferenca
        db.session.commit()
    
    return registro


def buscar_registro_mensal(registro_id):
    """Busca um registro mensal pelo ID"""
    return RegistroMensal.query.get(registro_id)


def listar_registros_mensais(filtros=None):
    """Lista registros mensais com filtros opcionais"""
    query = RegistroMensal.query
    
    if filtros:
        if 'insumo_id' in filtros:
            query = query.filter_by(insumo_id=filtros['insumo_id'])
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
        
        if 'mes_referencia' in filtros:
            # Filtrar pelo mês de referência (formato: YYYY-MM)
            ano, mes = filtros['mes_referencia'].split('-')
            query = query.filter(
                db.extract('year', RegistroMensal.mes_referencia) == int(ano),
                db.extract('month', RegistroMensal.mes_referencia) == int(mes)
            )
    
    # Ordenar por mês de referência decrescente
    query = query.order_by(RegistroMensal.mes_referencia.desc())
    
    return query.all()


def excluir_registro_mensal(registro_id):
    """Exclui um registro mensal"""
    registro = RegistroMensal.query.get(registro_id)
    if not registro:
        return False
    
    # Verificar se o registro está fechado
    if registro.status == 'fechado':
        raise ValueError("Não é possível excluir um registro mensal fechado")
    
    # Excluir o registro e suas entregas
    db.session.delete(registro)
    db.session.commit()
    
    return True


def criar_entrega_mensal(data, commit=True):
    """Cria uma nova entrega mensal"""
    schema = EntregaMensalSchema()
    validated_data = schema.load(data)
    
    nova_entrega = EntregaMensal(
        registro_mensal_id=validated_data['registro_mensal_id'],
        data_entrega=validated_data['data_entrega'],
        quantidade=validated_data['quantidade'],
        nota_fiscal_id=validated_data.get('nota_fiscal_id'),
        contrato_id=validated_data.get('contrato_id'),
        valor_total=validated_data['valor_total'],
        status_pagamento=validated_data.get('status_pagamento', 'pendente'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(nova_entrega)
    
    # Atualizar o registro mensal
    registro = RegistroMensal.query.get(validated_data['registro_mensal_id'])
    if registro:
        registro.quantidade_entregue = Decimal(registro.quantidade_entregue) + Decimal(validated_data['quantidade'])
        
        # Atualizar quantidade paga se o status for 'pago'
        if validated_data.get('status_pagamento') == 'pago':
            registro.quantidade_paga = Decimal(registro.quantidade_paga) + Decimal(validated_data['quantidade'])
        
        # Recalcular estoque final
        registro.estoque_final = Decimal(registro.estoque_inicial) + Decimal(registro.quantidade_entregue)
        
        # Atualizar o estoque atual do insumo
        insumo = Insumo.query.get(registro.insumo_id)
        if insumo:
            insumo.estoque_atual = registro.estoque_final
    
    if commit:
        db.session.commit()
    
    return nova_entrega


def atualizar_entrega_mensal(entrega_id, data):
    """Atualiza uma entrega mensal existente"""
    entrega = EntregaMensal.query.get(entrega_id)
    if not entrega:
        return None
    
    schema = EntregaMensalSchema()
    validated_data = schema.load(data)
    
    # Salvar valores antigos para ajustar o registro mensal
    quantidade_antiga = entrega.quantidade
    status_pagamento_antigo = entrega.status_pagamento
    
    # Atualizar campos da entrega
    for key, value in validated_data.items():
        setattr(entrega, key, value)
    
    entrega.atualizado_em = datetime.utcnow()
    
    # Atualizar o registro mensal
    registro = RegistroMensal.query.get(entrega.registro_mensal_id)
    if registro:
        # Ajustar quantidade entregue
        diferenca_quantidade = Decimal(entrega.quantidade) - Decimal(quantidade_antiga)
        registro.quantidade_entregue = Decimal(registro.quantidade_entregue) + diferenca_quantidade
        
        # Ajustar quantidade paga
        if status_pagamento_antigo == 'pago' and entrega.status_pagamento != 'pago':
            # Remover da quantidade paga
            registro.quantidade_paga = Decimal(registro.quantidade_paga) - Decimal(quantidade_antiga)
        elif status_pagamento_antigo != 'pago' and entrega.status_pagamento == 'pago':
            # Adicionar à quantidade paga
            registro.quantidade_paga = Decimal(registro.quantidade_paga) + Decimal(entrega.quantidade)
        elif status_pagamento_antigo == 'pago' and entrega.status_pagamento == 'pago':
            # Ajustar a diferença
            registro.quantidade_paga = Decimal(registro.quantidade_paga) + diferenca_quantidade
        
        # Recalcular estoque final
        registro.estoque_final = Decimal(registro.estoque_inicial) + Decimal(registro.quantidade_entregue)
        
        # Atualizar o estoque atual do insumo
        insumo = Insumo.query.get(registro.insumo_id)
        if insumo:
            insumo.estoque_atual = registro.estoque_final
    
    db.session.commit()
    
    return entrega


def buscar_entrega_mensal(entrega_id):
    """Busca uma entrega mensal pelo ID"""
    return EntregaMensal.query.get(entrega_id)


def listar_entregas_mensais(registro_id=None):
    """Lista entregas mensais de um registro específico ou todas"""
    query = EntregaMensal.query
    
    if registro_id:
        query = query.filter_by(registro_mensal_id=registro_id)
    
    # Ordenar por data de entrega decrescente
    query = query.order_by(EntregaMensal.data_entrega.desc())
    
    return query.all()


def excluir_entrega_mensal(entrega_id):
    """Exclui uma entrega mensal"""
    entrega = EntregaMensal.query.get(entrega_id)
    if not entrega:
        return False
    
    # Verificar se o registro está fechado
    registro = RegistroMensal.query.get(entrega.registro_mensal_id)
    if registro and registro.status == 'fechado':
        raise ValueError("Não é possível excluir uma entrega de um registro mensal fechado")
    
    # Atualizar o registro mensal
    if registro:
        registro.quantidade_entregue = Decimal(registro.quantidade_entregue) - Decimal(entrega.quantidade)
        
        # Atualizar quantidade paga se o status for 'pago'
        if entrega.status_pagamento == 'pago':
            registro.quantidade_paga = Decimal(registro.quantidade_paga) - Decimal(entrega.quantidade)
        
        # Recalcular estoque final
        registro.estoque_final = Decimal(registro.estoque_inicial) + Decimal(registro.quantidade_entregue)
        
        # Atualizar o estoque atual do insumo
        insumo = Insumo.query.get(registro.insumo_id)
        if insumo:
            insumo.estoque_atual = registro.estoque_final
    
    # Excluir a entrega
    db.session.delete(entrega)
    db.session.commit()
    
    return True


def criar_programacao_futura(data):
    """Cria uma nova programação futura"""
    schema = ProgramacaoFuturaSchema()
    validated_data = schema.load(data)
    
    nova_programacao = ProgramacaoFutura(
        mes_referencia=validated_data['mes_referencia'],
        insumo_id=validated_data['insumo_id'],
        quantidade_prevista=validated_data['quantidade_prevista'],
        contrato_id=validated_data.get('contrato_id'),
        valor_unitario_previsto=validated_data.get('valor_unitario_previsto'),
        status=validated_data.get('status', 'pendente'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(nova_programacao)
    db.session.commit()
    
    return nova_programacao


def atualizar_programacao_futura(programacao_id, data):
    """Atualiza uma programação futura existente"""
    programacao = ProgramacaoFutura.query.get(programacao_id)
    if not programacao:
        return None
    
    schema = ProgramacaoFuturaSchema()
    validated_data = schema.load(data)
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(programacao, key, value)
    
    programacao.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return programacao


def buscar_programacao_futura(programacao_id):
    """Busca uma programação futura pelo ID"""
    return ProgramacaoFutura.query.get(programacao_id)


def listar_programacoes_futuras(filtros=None):
    """Lista programações futuras com filtros opcionais"""
    query = ProgramacaoFutura.query
    
    if filtros:
        if 'insumo_id' in filtros:
            query = query.filter_by(insumo_id=filtros['insumo_id'])
        
        if 'contrato_id' in filtros:
            query = query.filter_by(contrato_id=filtros['contrato_id'])
        
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
        
        if 'mes_referencia' in filtros:
            # Filtrar pelo mês de referência (formato: YYYY-MM)
            ano, mes = filtros['mes_referencia'].split('-')
            query = query.filter(
                db.extract('year', ProgramacaoFutura.mes_referencia) == int(ano),
                db.extract('month', ProgramacaoFutura.mes_referencia) == int(mes)
            )
    
    # Ordenar por mês de referência
    query = query.order_by(ProgramacaoFutura.mes_referencia)
    
    return query.all()


def excluir_programacao_futura(programacao_id):
    """Exclui uma programação futura (exclusão lógica)"""
    programacao = ProgramacaoFutura.query.get(programacao_id)
    if not programacao:
        return False
    
    # Exclusão lógica
    programacao.status = 'cancelado'
    programacao.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return True

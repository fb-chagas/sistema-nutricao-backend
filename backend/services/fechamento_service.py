from ..models.fechamento_models import db, CustoMedio, FechamentoMensal, DetalhesFechamento, AnaliseComparativa
from ..models.nfe_models import Insumo
from ..models.controle_mensal_models import RegistroMensal, EntregaMensal
from datetime import datetime, date
from marshmallow import Schema, fields, ValidationError, validates, validates_schema
from decimal import Decimal
import json

class CustoMedioSchema(Schema):
    mes_referencia = fields.Date(required=True)
    insumo_id = fields.Integer(required=True)
    quantidade_total = fields.Decimal(required=True)
    custo_total = fields.Decimal(required=True)
    custo_medio_unitario = fields.Decimal(required=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")
    
    @validates_schema
    def validate_mes_referencia_insumo(self, data, **kwargs):
        # Verificar se já existe um custo médio para o mesmo mês e insumo
        if 'mes_referencia' in data and 'insumo_id' in data:
            # Extrair apenas o ano e mês da data
            mes_ref = datetime.strptime(data['mes_referencia'].strftime('%Y-%m-01'), '%Y-%m-%d').date()
            
            if self.context.get('custo_medio_id'):
                # Caso de atualização, ignorar o próprio custo médio
                existing = CustoMedio.query.filter(
                    db.func.date_trunc('month', CustoMedio.mes_referencia) == mes_ref,
                    CustoMedio.insumo_id == data['insumo_id'],
                    CustoMedio.id != self.context.get('custo_medio_id')
                ).first()
            else:
                # Caso de criação
                existing = CustoMedio.query.filter(
                    db.func.date_trunc('month', CustoMedio.mes_referencia) == mes_ref,
                    CustoMedio.insumo_id == data['insumo_id']
                ).first()
                
            if existing:
                raise ValidationError(f"Já existe um custo médio para o mês {mes_ref.strftime('%Y-%m')} e insumo {data['insumo_id']}")


class DetalhesFechamentoSchema(Schema):
    insumo_id = fields.Integer(required=True)
    quantidade = fields.Decimal(required=True)
    valor_total = fields.Decimal(required=True)
    custo_medio = fields.Decimal(required=True)
    observacoes = fields.String(allow_none=True)
    
    @validates('insumo_id')
    def validate_insumo(self, value):
        insumo = Insumo.query.get(value)
        if not insumo:
            raise ValidationError(f"Insumo com ID {value} não encontrado")


class FechamentoMensalSchema(Schema):
    mes_referencia = fields.Date(required=True)
    data_fechamento = fields.Date(required=True)
    valor_total_compras = fields.Decimal(required=True)
    quantidade_total = fields.Decimal(required=True)
    custo_medio_geral = fields.Decimal(required=True)
    status = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    detalhes = fields.List(fields.Nested(DetalhesFechamentoSchema), required=False)
    
    @validates_schema
    def validate_mes_referencia(self, data, **kwargs):
        # Verificar se já existe um fechamento para o mesmo mês
        if 'mes_referencia' in data:
            # Extrair apenas o ano e mês da data
            mes_ref = datetime.strptime(data['mes_referencia'].strftime('%Y-%m-01'), '%Y-%m-%d').date()
            
            if self.context.get('fechamento_id'):
                # Caso de atualização, ignorar o próprio fechamento
                existing = FechamentoMensal.query.filter(
                    db.func.date_trunc('month', FechamentoMensal.mes_referencia) == mes_ref,
                    FechamentoMensal.id != self.context.get('fechamento_id')
                ).first()
            else:
                # Caso de criação
                existing = FechamentoMensal.query.filter(
                    db.func.date_trunc('month', FechamentoMensal.mes_referencia) == mes_ref
                ).first()
                
            if existing:
                raise ValidationError(f"Já existe um fechamento para o mês {mes_ref.strftime('%Y-%m')}")


class AnaliseComparativaSchema(Schema):
    titulo = fields.String(required=True)
    tipo = fields.String(required=True)
    data_inicio = fields.Date(required=True)
    data_fim = fields.Date(required=True)
    parametros = fields.Dict(allow_none=True)
    resultados = fields.Dict(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    @validates_schema
    def validate_datas(self, data, **kwargs):
        # Verificar se data_fim é posterior a data_inicio
        if 'data_inicio' in data and 'data_fim' in data:
            if data['data_fim'] < data['data_inicio']:
                raise ValidationError("Data fim deve ser posterior à data início")


def calcular_custo_medio(data):
    """Calcula o custo médio para um insumo em um mês específico"""
    schema = CustoMedioSchema()
    validated_data = schema.load(data)
    
    # Verificar se já existe um custo médio para este mês e insumo
    mes_ref = datetime.strptime(validated_data['mes_referencia'].strftime('%Y-%m-01'), '%Y-%m-%d').date()
    custo_medio = CustoMedio.query.filter(
        db.func.date_trunc('month', CustoMedio.mes_referencia) == mes_ref,
        CustoMedio.insumo_id == validated_data['insumo_id']
    ).first()
    
    if custo_medio:
        # Atualizar custo médio existente
        custo_medio.quantidade_total = validated_data['quantidade_total']
        custo_medio.custo_total = validated_data['custo_total']
        custo_medio.custo_medio_unitario = validated_data['custo_medio_unitario']
        custo_medio.observacoes = validated_data.get('observacoes')
        custo_medio.atualizado_em = datetime.utcnow()
    else:
        # Criar novo custo médio
        custo_medio = CustoMedio(
            mes_referencia=mes_ref,
            insumo_id=validated_data['insumo_id'],
            quantidade_total=validated_data['quantidade_total'],
            custo_total=validated_data['custo_total'],
            custo_medio_unitario=validated_data['custo_medio_unitario'],
            observacoes=validated_data.get('observacoes')
        )
        db.session.add(custo_medio)
    
    db.session.commit()
    
    return custo_medio


def buscar_custo_medio(custo_medio_id):
    """Busca um custo médio pelo ID"""
    return CustoMedio.query.get(custo_medio_id)


def listar_custos_medios(filtros=None):
    """Lista custos médios com filtros opcionais"""
    query = CustoMedio.query
    
    if filtros:
        if 'insumo_id' in filtros:
            query = query.filter_by(insumo_id=filtros['insumo_id'])
        
        if 'mes_referencia' in filtros:
            # Filtrar pelo mês de referência (formato: YYYY-MM)
            ano, mes = filtros['mes_referencia'].split('-')
            query = query.filter(
                db.extract('year', CustoMedio.mes_referencia) == int(ano),
                db.extract('month', CustoMedio.mes_referencia) == int(mes)
            )
    
    # Ordenar por mês de referência decrescente
    query = query.order_by(CustoMedio.mes_referencia.desc())
    
    return query.all()


def criar_fechamento(data):
    """Cria um novo fechamento mensal"""
    schema = FechamentoMensalSchema()
    validated_data = schema.load(data)
    
    # Verificar se já existe um fechamento para este mês
    mes_ref = datetime.strptime(validated_data['mes_referencia'].strftime('%Y-%m-01'), '%Y-%m-%d').date()
    fechamento = FechamentoMensal.query.filter(
        db.func.date_trunc('month', FechamentoMensal.mes_referencia) == mes_ref
    ).first()
    
    if fechamento:
        raise ValidationError(f"Já existe um fechamento para o mês {mes_ref.strftime('%Y-%m')}")
    
    # Criar novo fechamento
    novo_fechamento = FechamentoMensal(
        mes_referencia=mes_ref,
        data_fechamento=validated_data['data_fechamento'],
        valor_total_compras=validated_data['valor_total_compras'],
        quantidade_total=validated_data['quantidade_total'],
        custo_medio_geral=validated_data['custo_medio_geral'],
        status=validated_data.get('status', 'fechado'),
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(novo_fechamento)
    db.session.flush()  # Para obter o ID do fechamento
    
    # Adicionar detalhes do fechamento
    if 'detalhes' in validated_data and isinstance(validated_data['detalhes'], list):
        for detalhe_data in validated_data['detalhes']:
            detalhe = DetalhesFechamento(
                fechamento_id=novo_fechamento.id,
                insumo_id=detalhe_data['insumo_id'],
                quantidade=detalhe_data['quantidade'],
                valor_total=detalhe_data['valor_total'],
                custo_medio=detalhe_data['custo_medio'],
                observacoes=detalhe_data.get('observacoes')
            )
            db.session.add(detalhe)
    
    # Fechar todos os registros mensais do mês
    registros = RegistroMensal.query.filter(
        db.func.date_trunc('month', RegistroMensal.mes_referencia) == mes_ref
    ).all()
    
    for registro in registros:
        registro.status = 'fechado'
    
    db.session.commit()
    
    return novo_fechamento


def buscar_fechamento(fechamento_id):
    """Busca um fechamento mensal pelo ID"""
    return FechamentoMensal.query.get(fechamento_id)


def listar_fechamentos(filtros=None):
    """Lista fechamentos mensais com filtros opcionais"""
    query = FechamentoMensal.query
    
    if filtros:
        if 'status' in filtros:
            query = query.filter_by(status=filtros['status'])
        
        if 'mes_referencia' in filtros:
            # Filtrar pelo mês de referência (formato: YYYY-MM)
            ano, mes = filtros['mes_referencia'].split('-')
            query = query.filter(
                db.extract('year', FechamentoMensal.mes_referencia) == int(ano),
                db.extract('month', FechamentoMensal.mes_referencia) == int(mes)
            )
        
        if 'ano' in filtros:
            # Filtrar pelo ano
            query = query.filter(
                db.extract('year', FechamentoMensal.mes_referencia) == int(filtros['ano'])
            )
    
    # Ordenar por mês de referência decrescente
    query = query.order_by(FechamentoMensal.mes_referencia.desc())
    
    return query.all()


def fechar_fechamento(fechamento_id):
    """Fecha um fechamento mensal"""
    fechamento = FechamentoMensal.query.get(fechamento_id)
    if not fechamento:
        return None
    
    # Verificar se o fechamento já está fechado
    if fechamento.status == 'fechado':
        return fechamento
    
    # Fechar o fechamento
    fechamento.status = 'fechado'
    fechamento.atualizado_em = datetime.utcnow()
    
    # Fechar todos os registros mensais do mês
    mes_ref = datetime.strptime(fechamento.mes_referencia.strftime('%Y-%m-01'), '%Y-%m-%d').date()
    registros = RegistroMensal.query.filter(
        db.func.date_trunc('month', RegistroMensal.mes_referencia) == mes_ref
    ).all()
    
    for registro in registros:
        registro.status = 'fechado'
    
    db.session.commit()
    
    return fechamento


def reabrir_fechamento(fechamento_id):
    """Reabre um fechamento mensal"""
    fechamento = FechamentoMensal.query.get(fechamento_id)
    if not fechamento:
        return None
    
    # Verificar se o fechamento já está reaberto
    if fechamento.status == 'reaberto':
        return fechamento
    
    # Reabrir o fechamento
    fechamento.status = 'reaberto'
    fechamento.atualizado_em = datetime.utcnow()
    
    # Reabrir todos os registros mensais do mês
    mes_ref = datetime.strptime(fechamento.mes_referencia.strftime('%Y-%m-01'), '%Y-%m-%d').date()
    registros = RegistroMensal.query.filter(
        db.func.date_trunc('month', RegistroMensal.mes_referencia) == mes_ref
    ).all()
    
    for registro in registros:
        registro.status = 'aberto'
    
    db.session.commit()
    
    return fechamento


def criar_analise(data):
    """Cria uma nova análise comparativa"""
    schema = AnaliseComparativaSchema()
    validated_data = schema.load(data)
    
    # Converter parametros e resultados para JSON se necessário
    parametros = validated_data.get('parametros')
    if parametros and not isinstance(parametros, str):
        parametros = json.dumps(parametros)
    
    resultados = validated_data.get('resultados')
    if resultados and not isinstance(resultados, str):
        resultados = json.dumps(resultados)
    
    nova_analise = AnaliseComparativa(
        titulo=validated_data['titulo'],
        tipo=validated_data['tipo'],
        data_inicio=validated_data['data_inicio'],
        data_fim=validated_data['data_fim'],
        parametros=parametros,
        resultados=resultados,
        observacoes=validated_data.get('observacoes')
    )
    
    db.session.add(nova_analise)
    db.session.commit()
    
    return nova_analise


def atualizar_analise(analise_id, data):
    """Atualiza uma análise comparativa existente"""
    analise = AnaliseComparativa.query.get(analise_id)
    if not analise:
        return None
    
    schema = AnaliseComparativaSchema()
    validated_data = schema.load(data)
    
    # Converter parametros e resultados para JSON se necessário
    if 'parametros' in validated_data:
        parametros = validated_data['parametros']
        if parametros and not isinstance(parametros, str):
            validated_data['parametros'] = json.dumps(parametros)
    
    if 'resultados' in validated_data:
        resultados = validated_data['resultados']
        if resultados and not isinstance(resultados, str):
            validated_data['resultados'] = json.dumps(resultados)
    
    # Atualizar campos
    for key, value in validated_data.items():
        setattr(analise, key, value)
    
    analise.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return analise


def buscar_analise(analise_id):
    """Busca uma análise comparativa pelo ID"""
    return AnaliseComparativa.query.get(analise_id)


def listar_analises(filtros=None):
    """Lista análises comparativas com filtros opcionais"""
    query = AnaliseComparativa.query
    
    if filtros:
        if 'tipo' in filtros:
            query = query.filter_by(tipo=filtros['tipo'])
        
        if 'data_inicio' in filtros and 'data_fim' in filtros:
            query = query.filter(
                AnaliseComparativa.data_inicio >= datetime.strptime(filtros['data_inicio'], '%Y-%m-%d').date(),
                AnaliseComparativa.data_fim <= datetime.strptime(filtros['data_fim'], '%Y-%m-%d').date()
            )
    
    # Ordenar por data de criação decrescente
    query = query.order_by(AnaliseComparativa.criado_em.desc())
    
    return query.all()


def excluir_analise(analise_id):
    """Exclui uma análise comparativa"""
    analise = AnaliseComparativa.query.get(analise_id)
    if not analise:
        return False
    
    db.session.delete(analise)
    db.session.commit()
    
    return True


def gerar_relatorio_custo_medio(filtros):
    """Gera um relatório de custo médio"""
    # Implementar lógica de relatório de custo médio
    # Este é um exemplo simplificado
    
    insumo_id = filtros.get('insumo_id')
    ano = filtros.get('ano', date.today().year)
    
    # Validar parâmetros
    if not insumo_id:
        raise ValueError("ID do insumo é obrigatório")
    
    # Buscar insumo
    insumo = Insumo.query.get(insumo_id)
    if not insumo:
        raise ValueError(f"Insumo com ID {insumo_id} não encontrado")
    
    # Buscar custos médios do ano
    custos_medios = CustoMedio.query.filter(
        CustoMedio.insumo_id == insumo_id,
        db.extract('year', CustoMedio.mes_referencia) == int(ano)
    ).order_by(CustoMedio.mes_referencia).all()
    
    # Preparar dados do relatório
    dados_mensais = []
    for custo_medio in custos_medios:
        mes = custo_medio.mes_referencia.strftime('%m/%Y')
        dados_mensais.append({
            'mes': mes,
            'quantidade': float(custo_medio.quantidade_total),
            'custo_total': float(custo_medio.custo_total),
            'custo_medio': float(custo_medio.custo_medio_unitario)
        })
    
    # Calcular média anual
    if custos_medios:
        media_anual = sum(float(cm.custo_medio_unitario) for cm in custos_medios) / len(custos_medios)
    else:
        media_anual = 0
    
    return {
        'insumo': {
            'id': insumo.id,
            'nome': insumo.nome,
            'codigo': insumo.codigo,
            'unidade_medida': insumo.unidade_medida
        },
        'ano': ano,
        'dados_mensais': dados_mensais,
        'media_anual': media_anual
    }


def gerar_relatorio_tendencia_precos(filtros):
    """Gera um relatório de tendência de preços"""
    # Implementar lógica de relatório de tendência de preços
    # Este é um exemplo simplificado
    
    insumo_id = filtros.get('insumo_id')
    data_inicio = filtros.get('data_inicio')
    data_fim = filtros.get('data_fim')
    
    # Validar parâmetros
    if not insumo_id:
        raise ValueError("ID do insumo é obrigatório")
    
    if not data_inicio or not data_fim:
        raise ValueError("Data início e data fim são obrigatórios")
    
    # Converter datas
    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    
    # Buscar insumo
    insumo = Insumo.query.get(insumo_id)
    if not insumo:
        raise ValueError(f"Insumo com ID {insumo_id} não encontrado")
    
    # Buscar entregas no período
    entregas = EntregaMensal.query.join(RegistroMensal).filter(
        RegistroMensal.insumo_id == insumo_id,
        EntregaMensal.data_entrega >= data_inicio,
        EntregaMensal.data_entrega <= data_fim
    ).order_by(EntregaMensal.data_entrega).all()
    
    # Preparar dados do relatório
    dados_entregas = []
    for entrega in entregas:
        preco_unitario = float(entrega.valor_total) / float(entrega.quantidade) if entrega.quantidade else 0
        dados_entregas.append({
            'data': entrega.data_entrega.strftime('%d/%m/%Y'),
            'quantidade': float(entrega.quantidade),
            'valor_total': float(entrega.valor_total),
            'preco_unitario': preco_unitario
        })
    
    # Calcular tendência (exemplo simplificado)
    if len(dados_entregas) >= 2:
        primeiro_preco = dados_entregas[0]['preco_unitario']
        ultimo_preco = dados_entregas[-1]['preco_unitario']
        variacao = ((ultimo_preco - primeiro_preco) / primeiro_preco) * 100 if primeiro_preco else 0
    else:
        variacao = 0
    
    return {
        'insumo': {
            'id': insumo.id,
            'nome': insumo.nome,
            'codigo': insumo.codigo,
            'unidade_medida': insumo.unidade_medida
        },
        'periodo': {
            'data_inicio': data_inicio.strftime('%d/%m/%Y'),
            'data_fim': data_fim.strftime('%d/%m/%Y')
        },
        'dados_entregas': dados_entregas,
        'variacao_percentual': variacao,
        'tendencia': 'alta' if variacao > 0 else 'baixa' if variacao < 0 else 'estável'
    }

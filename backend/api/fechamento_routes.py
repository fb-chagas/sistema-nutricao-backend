from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.fechamento_models import db, CustoMedio, FechamentoMensal, DetalhesFechamento, AnaliseComparativa
from ..services.fechamento_service import (
    calcular_custo_medio, buscar_custo_medio, listar_custos_medios,
    criar_fechamento, buscar_fechamento, listar_fechamentos, fechar_fechamento, reabrir_fechamento,
    criar_analise, atualizar_analise, buscar_analise, listar_analises, excluir_analise,
    gerar_relatorio_custo_medio, gerar_relatorio_tendencia_precos
)

# Blueprints
fechamento_bp = Blueprint('fechamento', __name__, url_prefix='/api/fechamento')
analise_bp = Blueprint('analise', __name__, url_prefix='/api/analise')

# Rotas para Custos Médios
@fechamento_bp.route('/custo-medio', methods=['GET'])
def get_custos_medios():
    try:
        filtros = request.args.to_dict()
        custos = listar_custos_medios(filtros)
        return jsonify([custo.to_dict() for custo in custos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/custo-medio/calcular', methods=['POST'])
def post_calcular_custo_medio():
    try:
        data = request.json
        custo_medio = calcular_custo_medio(data)
        return jsonify(custo_medio.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/custo-medio/<int:custo_medio_id>', methods=['GET'])
def get_custo_medio(custo_medio_id):
    try:
        custo_medio = buscar_custo_medio(custo_medio_id)
        if not custo_medio:
            return jsonify({"error": "Custo médio não encontrado"}), 404
        return jsonify(custo_medio.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas para Fechamentos
@fechamento_bp.route('', methods=['GET'])
def get_fechamentos():
    try:
        filtros = request.args.to_dict()
        fechamentos = listar_fechamentos(filtros)
        return jsonify([fechamento.to_dict() for fechamento in fechamentos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('', methods=['POST'])
def post_fechamento():
    try:
        data = request.json
        fechamento = criar_fechamento(data)
        return jsonify(fechamento.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/<int:fechamento_id>', methods=['GET'])
def get_fechamento(fechamento_id):
    try:
        fechamento = buscar_fechamento(fechamento_id)
        if not fechamento:
            return jsonify({"error": "Fechamento não encontrado"}), 404
        return jsonify(fechamento.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/<int:fechamento_id>/fechar', methods=['POST'])
def post_fechar_fechamento(fechamento_id):
    try:
        fechamento = fechar_fechamento(fechamento_id)
        if not fechamento:
            return jsonify({"error": "Fechamento não encontrado"}), 404
        return jsonify(fechamento.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/<int:fechamento_id>/reabrir', methods=['POST'])
def post_reabrir_fechamento(fechamento_id):
    try:
        fechamento = reabrir_fechamento(fechamento_id)
        if not fechamento:
            return jsonify({"error": "Fechamento não encontrado"}), 404
        return jsonify(fechamento.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rotas para Relatórios
@fechamento_bp.route('/relatorio/custo-medio', methods=['GET'])
def get_relatorio_custo_medio():
    try:
        filtros = request.args.to_dict()
        relatorio = gerar_relatorio_custo_medio(filtros)
        return jsonify(relatorio), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fechamento_bp.route('/relatorio/tendencia-precos', methods=['GET'])
def get_relatorio_tendencia_precos():
    try:
        filtros = request.args.to_dict()
        relatorio = gerar_relatorio_tendencia_precos(filtros)
        return jsonify(relatorio), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas para Análises Comparativas
@analise_bp.route('', methods=['GET'])
def get_analises():
    try:
        filtros = request.args.to_dict()
        analises = listar_analises(filtros)
        return jsonify([analise.to_dict() for analise in analises]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analise_bp.route('', methods=['POST'])
def post_analise():
    try:
        data = request.json
        analise = criar_analise(data)
        return jsonify(analise.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@analise_bp.route('/<int:analise_id>', methods=['GET'])
def get_analise(analise_id):
    try:
        analise = buscar_analise(analise_id)
        if not analise:
            return jsonify({"error": "Análise não encontrada"}), 404
        return jsonify(analise.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@analise_bp.route('/<int:analise_id>', methods=['PUT'])
def put_analise(analise_id):
    try:
        data = request.json
        analise = atualizar_analise(analise_id, data)
        if not analise:
            return jsonify({"error": "Análise não encontrada"}), 404
        return jsonify(analise.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@analise_bp.route('/<int:analise_id>', methods=['DELETE'])
def delete_analise(analise_id):
    try:
        resultado = excluir_analise(analise_id)
        if not resultado:
            return jsonify({"error": "Análise não encontrada"}), 404
        return jsonify({"message": "Análise excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

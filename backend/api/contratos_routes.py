from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.contratos_models import db, Contrato, ItemContrato, Cotacao, PlanejamentoCompra
from ..services.contratos_service import (
    criar_contrato, atualizar_contrato, buscar_contrato, listar_contratos, excluir_contrato,
    criar_cotacao, atualizar_cotacao, buscar_cotacao, listar_cotacoes, excluir_cotacao,
    criar_planejamento, atualizar_planejamento, buscar_planejamento, listar_planejamentos, excluir_planejamento
)

# Blueprints
contratos_bp = Blueprint('contratos', __name__, url_prefix='/api/contratos')
cotacoes_bp = Blueprint('cotacoes', __name__, url_prefix='/api/cotacoes')
planejamento_bp = Blueprint('planejamento', __name__, url_prefix='/api/planejamento')

# Rotas para Contratos
@contratos_bp.route('', methods=['GET'])
def get_contratos():
    try:
        filtros = request.args.to_dict()
        contratos = listar_contratos(filtros)
        return jsonify([contrato.to_dict() for contrato in contratos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@contratos_bp.route('', methods=['POST'])
def post_contrato():
    try:
        data = request.json
        contrato = criar_contrato(data)
        return jsonify(contrato.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@contratos_bp.route('/<int:contrato_id>', methods=['GET'])
def get_contrato(contrato_id):
    try:
        contrato = buscar_contrato(contrato_id)
        if not contrato:
            return jsonify({"error": "Contrato não encontrado"}), 404
        return jsonify(contrato.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@contratos_bp.route('/<int:contrato_id>', methods=['PUT'])
def put_contrato(contrato_id):
    try:
        data = request.json
        contrato = atualizar_contrato(contrato_id, data)
        if not contrato:
            return jsonify({"error": "Contrato não encontrado"}), 404
        return jsonify(contrato.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@contratos_bp.route('/<int:contrato_id>', methods=['DELETE'])
def delete_contrato(contrato_id):
    try:
        resultado = excluir_contrato(contrato_id)
        if not resultado:
            return jsonify({"error": "Contrato não encontrado"}), 404
        return jsonify({"message": "Contrato excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@contratos_bp.route('/cronograma', methods=['GET'])
def get_cronograma():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        if not data_inicio or not data_fim:
            return jsonify({"error": "Data início e data fim são obrigatórios"}), 400
            
        # Implementar lógica de cronograma
        # ...
        
        return jsonify({"message": "Cronograma em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas para Cotações
@cotacoes_bp.route('', methods=['GET'])
def get_cotacoes():
    try:
        filtros = request.args.to_dict()
        cotacoes = listar_cotacoes(filtros)
        return jsonify([cotacao.to_dict() for cotacao in cotacoes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cotacoes_bp.route('', methods=['POST'])
def post_cotacao():
    try:
        data = request.json
        cotacao = criar_cotacao(data)
        return jsonify(cotacao.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cotacoes_bp.route('/<int:cotacao_id>', methods=['GET'])
def get_cotacao(cotacao_id):
    try:
        cotacao = buscar_cotacao(cotacao_id)
        if not cotacao:
            return jsonify({"error": "Cotação não encontrada"}), 404
        return jsonify(cotacao.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@cotacoes_bp.route('/<int:cotacao_id>', methods=['PUT'])
def put_cotacao(cotacao_id):
    try:
        data = request.json
        cotacao = atualizar_cotacao(cotacao_id, data)
        if not cotacao:
            return jsonify({"error": "Cotação não encontrada"}), 404
        return jsonify(cotacao.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cotacoes_bp.route('/<int:cotacao_id>', methods=['DELETE'])
def delete_cotacao(cotacao_id):
    try:
        resultado = excluir_cotacao(cotacao_id)
        if not resultado:
            return jsonify({"error": "Cotação não encontrada"}), 404
        return jsonify({"message": "Cotação excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@cotacoes_bp.route('/evolucao-precos', methods=['GET'])
def get_evolucao_precos():
    try:
        insumo_id = request.args.get('insumo_id')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        if not insumo_id:
            return jsonify({"error": "ID do insumo é obrigatório"}), 400
            
        # Implementar lógica de evolução de preços
        # ...
        
        return jsonify({"message": "Evolução de preços em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas para Planejamento de Compras
@planejamento_bp.route('', methods=['GET'])
def get_planejamentos():
    try:
        filtros = request.args.to_dict()
        planejamentos = listar_planejamentos(filtros)
        return jsonify([planejamento.to_dict() for planejamento in planejamentos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@planejamento_bp.route('', methods=['POST'])
def post_planejamento():
    try:
        data = request.json
        planejamento = criar_planejamento(data)
        return jsonify(planejamento.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@planejamento_bp.route('/<int:planejamento_id>', methods=['GET'])
def get_planejamento(planejamento_id):
    try:
        planejamento = buscar_planejamento(planejamento_id)
        if not planejamento:
            return jsonify({"error": "Planejamento não encontrado"}), 404
        return jsonify(planejamento.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@planejamento_bp.route('/<int:planejamento_id>', methods=['PUT'])
def put_planejamento(planejamento_id):
    try:
        data = request.json
        planejamento = atualizar_planejamento(planejamento_id, data)
        if not planejamento:
            return jsonify({"error": "Planejamento não encontrado"}), 404
        return jsonify(planejamento.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@planejamento_bp.route('/<int:planejamento_id>', methods=['DELETE'])
def delete_planejamento(planejamento_id):
    try:
        resultado = excluir_planejamento(planejamento_id)
        if not resultado:
            return jsonify({"error": "Planejamento não encontrado"}), 404
        return jsonify({"message": "Planejamento excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@planejamento_bp.route('/projecao', methods=['GET'])
def get_projecao():
    try:
        mes_inicio = request.args.get('mes_inicio')
        mes_fim = request.args.get('mes_fim')
        
        if not mes_inicio or not mes_fim:
            return jsonify({"error": "Mês início e mês fim são obrigatórios"}), 400
            
        # Implementar lógica de projeção de compras
        # ...
        
        return jsonify({"message": "Projeção de compras em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

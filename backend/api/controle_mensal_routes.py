from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.controle_mensal_models import db, RegistroMensal, EntregaMensal, ProgramacaoFutura
from ..services.controle_mensal_service import (
    criar_registro_mensal, atualizar_registro_mensal, buscar_registro_mensal, listar_registros_mensais, excluir_registro_mensal,
    criar_entrega_mensal, atualizar_entrega_mensal, buscar_entrega_mensal, listar_entregas_mensais, excluir_entrega_mensal,
    criar_programacao_futura, atualizar_programacao_futura, buscar_programacao_futura, listar_programacoes_futuras, excluir_programacao_futura
)

# Blueprints
controle_mensal_bp = Blueprint('controle_mensal', __name__, url_prefix='/api/controle-mensal')
programacao_bp = Blueprint('programacao', __name__, url_prefix='/api/programacao')

# Rotas para Registros Mensais
@controle_mensal_bp.route('/registros', methods=['GET'])
def get_registros_mensais():
    try:
        filtros = request.args.to_dict()
        registros = listar_registros_mensais(filtros)
        return jsonify([registro.to_dict() for registro in registros]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/registros', methods=['POST'])
def post_registro_mensal():
    try:
        data = request.json
        registro = criar_registro_mensal(data)
        return jsonify(registro.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/registros/<int:registro_id>', methods=['GET'])
def get_registro_mensal(registro_id):
    try:
        registro = buscar_registro_mensal(registro_id)
        if not registro:
            return jsonify({"error": "Registro mensal não encontrado"}), 404
        return jsonify(registro.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/registros/<int:registro_id>', methods=['PUT'])
def put_registro_mensal(registro_id):
    try:
        data = request.json
        registro = atualizar_registro_mensal(registro_id, data)
        if not registro:
            return jsonify({"error": "Registro mensal não encontrado"}), 404
        return jsonify(registro.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/registros/<int:registro_id>', methods=['DELETE'])
def delete_registro_mensal(registro_id):
    try:
        resultado = excluir_registro_mensal(registro_id)
        if not resultado:
            return jsonify({"error": "Registro mensal não encontrado"}), 404
        return jsonify({"message": "Registro mensal excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rotas para Entregas Mensais
@controle_mensal_bp.route('/registros/<int:registro_id>/entregas', methods=['GET'])
def get_entregas_mensais(registro_id):
    try:
        entregas = listar_entregas_mensais(registro_id)
        return jsonify([entrega.to_dict() for entrega in entregas]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/registros/<int:registro_id>/entregas', methods=['POST'])
def post_entrega_mensal(registro_id):
    try:
        data = request.json
        data['registro_mensal_id'] = registro_id
        entrega = criar_entrega_mensal(data)
        return jsonify(entrega.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/entregas/<int:entrega_id>', methods=['GET'])
def get_entrega_mensal(entrega_id):
    try:
        entrega = buscar_entrega_mensal(entrega_id)
        if not entrega:
            return jsonify({"error": "Entrega mensal não encontrada"}), 404
        return jsonify(entrega.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/entregas/<int:entrega_id>', methods=['PUT'])
def put_entrega_mensal(entrega_id):
    try:
        data = request.json
        entrega = atualizar_entrega_mensal(entrega_id, data)
        if not entrega:
            return jsonify({"error": "Entrega mensal não encontrada"}), 404
        return jsonify(entrega.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/entregas/<int:entrega_id>', methods=['DELETE'])
def delete_entrega_mensal(entrega_id):
    try:
        resultado = excluir_entrega_mensal(entrega_id)
        if not resultado:
            return jsonify({"error": "Entrega mensal não encontrada"}), 404
        return jsonify({"message": "Entrega mensal excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@controle_mensal_bp.route('/evolucao-estoque', methods=['GET'])
def get_evolucao_estoque():
    try:
        insumo_id = request.args.get('insumo_id')
        ano = request.args.get('ano')
        
        if not insumo_id or not ano:
            return jsonify({"error": "ID do insumo e ano são obrigatórios"}), 400
            
        # Implementar lógica de evolução de estoque
        # ...
        
        return jsonify({"message": "Evolução de estoque em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rotas para Programações Futuras
@programacao_bp.route('', methods=['GET'])
def get_programacoes_futuras():
    try:
        filtros = request.args.to_dict()
        programacoes = listar_programacoes_futuras(filtros)
        return jsonify([programacao.to_dict() for programacao in programacoes]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@programacao_bp.route('', methods=['POST'])
def post_programacao_futura():
    try:
        data = request.json
        programacao = criar_programacao_futura(data)
        return jsonify(programacao.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@programacao_bp.route('/<int:programacao_id>', methods=['GET'])
def get_programacao_futura(programacao_id):
    try:
        programacao = buscar_programacao_futura(programacao_id)
        if not programacao:
            return jsonify({"error": "Programação futura não encontrada"}), 404
        return jsonify(programacao.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@programacao_bp.route('/<int:programacao_id>', methods=['PUT'])
def put_programacao_futura(programacao_id):
    try:
        data = request.json
        programacao = atualizar_programacao_futura(programacao_id, data)
        if not programacao:
            return jsonify({"error": "Programação futura não encontrada"}), 404
        return jsonify(programacao.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@programacao_bp.route('/<int:programacao_id>', methods=['DELETE'])
def delete_programacao_futura(programacao_id):
    try:
        resultado = excluir_programacao_futura(programacao_id)
        if not resultado:
            return jsonify({"error": "Programação futura não encontrada"}), 404
        return jsonify({"message": "Programação futura excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@programacao_bp.route('/projecao-entregas', methods=['GET'])
def get_projecao_entregas():
    try:
        mes_inicio = request.args.get('mes_inicio')
        mes_fim = request.args.get('mes_fim')
        
        if not mes_inicio or not mes_fim:
            return jsonify({"error": "Mês início e mês fim são obrigatórios"}), 400
            
        # Implementar lógica de projeção de entregas
        # ...
        
        return jsonify({"message": "Projeção de entregas em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

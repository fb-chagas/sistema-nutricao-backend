from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..models.nfe_models import db, Fornecedor, Insumo, NotaFiscal, ItemNotaFiscal
from ..services.nfe_service import (
    criar_fornecedor, atualizar_fornecedor, buscar_fornecedor, listar_fornecedores, excluir_fornecedor,
    criar_insumo, atualizar_insumo, buscar_insumo, listar_insumos, excluir_insumo,
    criar_nota_fiscal, atualizar_nota_fiscal, buscar_nota_fiscal, listar_notas_fiscais, excluir_nota_fiscal
)

# Blueprints
fornecedor_bp = Blueprint('fornecedor', __name__, url_prefix='/api/fornecedores')
insumo_bp = Blueprint('insumo', __name__, url_prefix='/api/insumos')
nfe_bp = Blueprint('nfe', __name__, url_prefix='/api/nfe')

# Rotas para Fornecedores
@fornecedor_bp.route('', methods=['GET'])
def get_fornecedores():
    try:
        filtros = request.args.to_dict()
        fornecedores = listar_fornecedores(filtros)
        return jsonify([fornecedor.to_dict() for fornecedor in fornecedores]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fornecedor_bp.route('', methods=['POST'])
def post_fornecedor():
    try:
        data = request.json
        fornecedor = criar_fornecedor(data)
        return jsonify(fornecedor.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fornecedor_bp.route('/<int:fornecedor_id>', methods=['GET'])
def get_fornecedor(fornecedor_id):
    try:
        fornecedor = buscar_fornecedor(fornecedor_id)
        if not fornecedor:
            return jsonify({"error": "Fornecedor não encontrado"}), 404
        return jsonify(fornecedor.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@fornecedor_bp.route('/<int:fornecedor_id>', methods=['PUT'])
def put_fornecedor(fornecedor_id):
    try:
        data = request.json
        fornecedor = atualizar_fornecedor(fornecedor_id, data)
        if not fornecedor:
            return jsonify({"error": "Fornecedor não encontrado"}), 404
        return jsonify(fornecedor.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@fornecedor_bp.route('/<int:fornecedor_id>', methods=['DELETE'])
def delete_fornecedor(fornecedor_id):
    try:
        resultado = excluir_fornecedor(fornecedor_id)
        if not resultado:
            return jsonify({"error": "Fornecedor não encontrado"}), 404
        return jsonify({"message": "Fornecedor excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rotas para Insumos
@insumo_bp.route('', methods=['GET'])
def get_insumos():
    try:
        filtros = request.args.to_dict()
        insumos = listar_insumos(filtros)
        return jsonify([insumo.to_dict() for insumo in insumos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@insumo_bp.route('', methods=['POST'])
def post_insumo():
    try:
        data = request.json
        insumo = criar_insumo(data)
        return jsonify(insumo.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@insumo_bp.route('/<int:insumo_id>', methods=['GET'])
def get_insumo(insumo_id):
    try:
        insumo = buscar_insumo(insumo_id)
        if not insumo:
            return jsonify({"error": "Insumo não encontrado"}), 404
        return jsonify(insumo.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@insumo_bp.route('/<int:insumo_id>', methods=['PUT'])
def put_insumo(insumo_id):
    try:
        data = request.json
        insumo = atualizar_insumo(insumo_id, data)
        if not insumo:
            return jsonify({"error": "Insumo não encontrado"}), 404
        return jsonify(insumo.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@insumo_bp.route('/<int:insumo_id>', methods=['DELETE'])
def delete_insumo(insumo_id):
    try:
        resultado = excluir_insumo(insumo_id)
        if not resultado:
            return jsonify({"error": "Insumo não encontrado"}), 404
        return jsonify({"message": "Insumo excluído com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rotas para Notas Fiscais
@nfe_bp.route('', methods=['GET'])
def get_notas_fiscais():
    try:
        filtros = request.args.to_dict()
        notas_fiscais = listar_notas_fiscais(filtros)
        return jsonify([nf.to_dict() for nf in notas_fiscais]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('', methods=['POST'])
def post_nota_fiscal():
    try:
        data = request.json
        nota_fiscal = criar_nota_fiscal(data)
        return jsonify(nota_fiscal.to_dict()), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('/<int:nota_fiscal_id>', methods=['GET'])
def get_nota_fiscal(nota_fiscal_id):
    try:
        nota_fiscal = buscar_nota_fiscal(nota_fiscal_id)
        if not nota_fiscal:
            return jsonify({"error": "Nota fiscal não encontrada"}), 404
        return jsonify(nota_fiscal.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('/<int:nota_fiscal_id>', methods=['PUT'])
def put_nota_fiscal(nota_fiscal_id):
    try:
        data = request.json
        nota_fiscal = atualizar_nota_fiscal(nota_fiscal_id, data)
        if not nota_fiscal:
            return jsonify({"error": "Nota fiscal não encontrada"}), 404
        return jsonify(nota_fiscal.to_dict()), 200
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('/<int:nota_fiscal_id>', methods=['DELETE'])
def delete_nota_fiscal(nota_fiscal_id):
    try:
        resultado = excluir_nota_fiscal(nota_fiscal_id)
        if not resultado:
            return jsonify({"error": "Nota fiscal não encontrada"}), 404
        return jsonify({"message": "Nota fiscal excluída com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('/relatorio/periodo', methods=['GET'])
def relatorio_periodo():
    try:
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        if not data_inicio or not data_fim:
            return jsonify({"error": "Data início e data fim são obrigatórios"}), 400
            
        # Implementar lógica de relatório por período
        # ...
        
        return jsonify({"message": "Relatório em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@nfe_bp.route('/relatorio/fornecedor/<int:fornecedor_id>', methods=['GET'])
def relatorio_fornecedor(fornecedor_id):
    try:
        # Implementar lógica de relatório por fornecedor
        # ...
        
        return jsonify({"message": "Relatório em desenvolvimento"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

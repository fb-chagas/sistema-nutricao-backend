from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from ..models.auth_models import db, Usuario, LogAcesso
from ..services.auth_service import (
    criar_usuario, atualizar_usuario, buscar_usuario, listar_usuarios, 
    ativar_desativar_usuario, autenticar_usuario, registrar_log_acesso
)
import datetime

# Blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Rotas para Autenticação
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        if not data or 'email' not in data or 'senha' not in data:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        email = data['email']
        senha = data['senha']
        
        usuario, mensagem = autenticar_usuario(email, senha, request.remote_addr)
        
        if not usuario:
            return jsonify({"error": mensagem}), 401
        
        # Login do usuário
        login_user(usuario)
        
        # Atualizar último acesso
        usuario.ultimo_acesso = datetime.datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Login realizado com sucesso",
            "usuario": usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        # Registrar log de logout
        registrar_log_acesso(current_user.id, 'logout', request.remote_addr)
        
        # Logout do usuário
        logout_user()
        
        return jsonify({"message": "Logout realizado com sucesso"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/perfil', methods=['GET'])
@login_required
def get_perfil():
    try:
        return jsonify(current_user.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/perfil', methods=['PUT'])
@login_required
def update_perfil():
    try:
        data = request.json
        
        # Não permitir alteração de nível de acesso pelo próprio usuário
        if 'nivel_acesso' in data:
            del data['nivel_acesso']
        
        usuario = atualizar_usuario(current_user.id, data)
        
        return jsonify(usuario.to_dict()), 200
        
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rotas para Gerenciamento de Usuários (apenas admin)
@auth_bp.route('/usuarios', methods=['GET'])
@login_required
def get_usuarios():
    try:
        # Verificar se o usuário é admin
        if current_user.nivel_acesso != 'admin':
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        filtros = request.args.to_dict()
        usuarios = listar_usuarios(filtros)
        
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/usuarios', methods=['POST'])
@login_required
def post_usuario():
    try:
        # Verificar se o usuário é admin
        if current_user.nivel_acesso != 'admin':
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        data = request.json
        usuario = criar_usuario(data)
        
        return jsonify(usuario.to_dict()), 201
        
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
@login_required
def get_usuario(usuario_id):
    try:
        # Verificar se o usuário é admin ou é o próprio usuário
        if current_user.nivel_acesso != 'admin' and current_user.id != usuario_id:
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        usuario = buscar_usuario(usuario_id)
        
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@login_required
def put_usuario(usuario_id):
    try:
        # Verificar se o usuário é admin ou é o próprio usuário
        if current_user.nivel_acesso != 'admin' and current_user.id != usuario_id:
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        data = request.json
        
        # Se não for admin e estiver tentando alterar o nível de acesso
        if current_user.nivel_acesso != 'admin' and 'nivel_acesso' in data:
            del data['nivel_acesso']
        
        usuario = atualizar_usuario(usuario_id, data)
        
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        return jsonify(usuario.to_dict()), 200
        
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/usuarios/<int:usuario_id>/ativar', methods=['POST'])
@login_required
def post_ativar_usuario(usuario_id):
    try:
        # Verificar se o usuário é admin
        if current_user.nivel_acesso != 'admin':
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        usuario = ativar_desativar_usuario(usuario_id, True)
        
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/usuarios/<int:usuario_id>/desativar', methods=['POST'])
@login_required
def post_desativar_usuario(usuario_id):
    try:
        # Verificar se o usuário é admin
        if current_user.nivel_acesso != 'admin':
            return jsonify({"error": "Acesso não autorizado"}), 403
        
        # Não permitir desativar o próprio usuário
        if current_user.id == usuario_id:
            return jsonify({"error": "Não é possível desativar o próprio usuário"}), 400
        
        usuario = ativar_desativar_usuario(usuario_id, False)
        
        if not usuario:
            return jsonify({"error": "Usuário não encontrado"}), 404
            
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Rota para alterar senha
@auth_bp.route('/alterar-senha', methods=['POST'])
@login_required
def post_alterar_senha():
    try:
        data = request.json
        
        if not data or 'senha_atual' not in data or 'nova_senha' not in data:
            return jsonify({"error": "Senha atual e nova senha são obrigatórias"}), 400
        
        senha_atual = data['senha_atual']
        nova_senha = data['nova_senha']
        
        # Verificar senha atual
        if not current_user.verificar_senha(senha_atual):
            return jsonify({"error": "Senha atual incorreta"}), 400
        
        # Alterar senha
        current_user.set_senha(nova_senha)
        db.session.commit()
        
        return jsonify({"message": "Senha alterada com sucesso"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

from ..models.auth_models import db, Usuario, LogAcesso
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, validates
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioSchema(Schema):
    nome = fields.String(required=True)
    email = fields.String(required=True)
    senha = fields.String(required=False)  # Não obrigatório para atualização
    cargo = fields.String(allow_none=True)
    departamento = fields.String(allow_none=True)
    nivel_acesso = fields.String(allow_none=True)
    
    @validates('email')
    def validate_email(self, value):
        # Verificar se já existe um usuário com este email
        if self.context.get('usuario_id'):
            # Caso de atualização, ignorar o próprio usuário
            existing = Usuario.query.filter(
                Usuario.email == value,
                Usuario.id != self.context.get('usuario_id')
            ).first()
        else:
            # Caso de criação
            existing = Usuario.query.filter_by(email=value).first()
            
        if existing:
            raise ValidationError(f"Já existe um usuário com o email {value}")


def criar_usuario(data):
    """Cria um novo usuário"""
    schema = UsuarioSchema()
    validated_data = schema.load(data)
    
    # Verificar se a senha foi fornecida
    if 'senha' not in validated_data or not validated_data['senha']:
        raise ValidationError("Senha é obrigatória para criar um usuário")
    
    novo_usuario = Usuario(
        nome=validated_data['nome'],
        email=validated_data['email'],
        cargo=validated_data.get('cargo'),
        departamento=validated_data.get('departamento'),
        nivel_acesso=validated_data.get('nivel_acesso', 'usuario')
    )
    
    # Definir senha
    novo_usuario.set_senha(validated_data['senha'])
    
    db.session.add(novo_usuario)
    db.session.commit()
    
    return novo_usuario


def atualizar_usuario(usuario_id, data):
    """Atualiza um usuário existente"""
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return None
    
    schema = UsuarioSchema(context={'usuario_id': usuario_id})
    validated_data = schema.load(data)
    
    # Atualizar campos
    for key, value in validated_data.items():
        if key != 'senha':  # Senha é tratada separadamente
            setattr(usuario, key, value)
    
    # Atualizar senha se fornecida
    if 'senha' in validated_data and validated_data['senha']:
        usuario.set_senha(validated_data['senha'])
    
    usuario.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return usuario


def buscar_usuario(usuario_id):
    """Busca um usuário pelo ID"""
    return Usuario.query.get(usuario_id)


def listar_usuarios(filtros=None):
    """Lista usuários com filtros opcionais"""
    query = Usuario.query
    
    if filtros:
        if 'nome' in filtros:
            query = query.filter(Usuario.nome.ilike(f"%{filtros['nome']}%"))
        
        if 'email' in filtros:
            query = query.filter(Usuario.email.ilike(f"%{filtros['email']}%"))
        
        if 'nivel_acesso' in filtros:
            query = query.filter_by(nivel_acesso=filtros['nivel_acesso'])
        
        if 'ativo' in filtros:
            ativo = filtros['ativo'].lower() == 'true'
            query = query.filter_by(ativo=ativo)
    
    # Ordenar por nome
    query = query.order_by(Usuario.nome)
    
    return query.all()


def ativar_desativar_usuario(usuario_id, ativar=True):
    """Ativa ou desativa um usuário"""
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return None
    
    usuario.ativo = ativar
    usuario.atualizado_em = datetime.utcnow()
    db.session.commit()
    
    return usuario


def autenticar_usuario(email, senha, ip=None):
    """Autentica um usuário"""
    usuario = Usuario.query.filter_by(email=email).first()
    
    # Verificar se o usuário existe
    if not usuario:
        registrar_log_acesso(None, 'falha_login', ip, f"Usuário não encontrado: {email}")
        return None, "Usuário não encontrado"
    
    # Verificar se o usuário está ativo
    if not usuario.ativo:
        registrar_log_acesso(usuario.id, 'falha_login', ip, "Usuário inativo")
        return None, "Usuário inativo"
    
    # Verificar senha
    if not usuario.verificar_senha(senha):
        registrar_log_acesso(usuario.id, 'falha_login', ip, "Senha incorreta")
        return None, "Senha incorreta"
    
    # Registrar login bem-sucedido
    registrar_log_acesso(usuario.id, 'login', ip)
    
    return usuario, "Login bem-sucedido"


def registrar_log_acesso(usuario_id, acao, ip=None, detalhes=None):
    """Registra um log de acesso"""
    log = LogAcesso(
        usuario_id=usuario_id,
        data_hora=datetime.utcnow(),
        ip=ip,
        acao=acao,
        detalhes=detalhes
    )
    
    db.session.add(log)
    db.session.commit()
    
    return log

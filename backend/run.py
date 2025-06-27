import sys
import os

# Garante que o diretório 'backend' está no path (caso rode a partir da raiz)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from __init__ import create_app
from models.auth_models import Usuario
from database import db

app = create_app()

def setup_database():
    with app.app_context():
        db.create_all()

        admin = Usuario.query.filter_by(email='admin@sistema.com').first()
        if not admin:
            try:
                admin = Usuario(
                    nome='Administrador',
                    email='admin@sistema.com',
                    nivel_acesso='admin',
                    ativo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Usuário admin criado com sucesso!")
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao criar usuário admin: {e}")
        else:
            print("Usuário admin já existe!")

if __name__ == '__main__':
    setup_database()
    app.run(host='0.0.0.0', port=5000, debug=True)

from backend import create_app, db
from backend.models.auth_models import Usuario

app = create_app()

# Função para criar as tabelas e o usuário admin
def setup_database():
    try:
        # Criar todas as tabelas
        with app.app_context():
            db.create_all()
            
            # Verificar se já existe um usuário admin
            admin = Usuario.query.filter_by(email='admin@sistema.com').first()
            if not admin:
                try:
                    # Criar usuário admin
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
    except Exception as e:
        print(f"Erro ao configurar banco de dados: {e}")

if __name__ == '__main__':
    # Configurar o banco de dados antes de iniciar o servidor
    setup_database()
    
    # Iniciar o servidor
    app.run(host='0.0.0.0', port=5000, debug=True)

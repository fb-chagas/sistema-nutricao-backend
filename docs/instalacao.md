# Guia de Instalação do Sistema de Nutrição

Este guia fornece instruções detalhadas para instalar e configurar o Sistema de Nutrição em seu ambiente.

## Requisitos do Sistema

- Python 3.8 ou superior
- Node.js 14 ou superior
- PostgreSQL (para ambiente de produção) ou SQLite (para desenvolvimento)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Estrutura de Diretórios

O pacote do sistema contém os seguintes diretórios principais:

```
sistema_nutricao/
├── backend/           # API e lógica de negócio
├── docs/              # Documentação do sistema
├── tests/             # Testes automatizados
├── run_backend.sh     # Script para iniciar o backend
├── run_dev.sh         # Script para ambiente de desenvolvimento
├── run_tests.sh       # Script para executar testes
└── README.md          # Instruções gerais
```

## Passos para Instalação

### 1. Preparar o Ambiente

Primeiro, clone ou extraia o pacote do sistema para um diretório de sua escolha:

```bash
# Se estiver usando Git
git clone [URL_DO_REPOSITORIO] sistema_nutricao
# OU extraia o arquivo ZIP fornecido
```

### 2. Configurar o Backend

Navegue até o diretório do sistema e configure o ambiente Python:

```bash
cd sistema_nutricao

# Criar ambiente virtual Python
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r backend/requirements.txt
```

### 3. Configurar o Banco de Dados

Para desenvolvimento, o sistema usa SQLite por padrão, que não requer configuração adicional.

Para produção com PostgreSQL:

```bash
# Criar banco de dados PostgreSQL
createdb sistema_nutricao

# Configurar variáveis de ambiente
export DATABASE_URL="postgresql://usuario:senha@localhost/sistema_nutricao"
```

### 4. Iniciar o Backend

Execute o script para iniciar o backend:

```bash
# Tornar o script executável (Linux/Mac)
chmod +x run_backend.sh

# Executar o backend
./run_backend.sh
# No Windows:
bash run_backend.sh
```

O backend estará disponível em `http://localhost:5000`.

### 5. Executar Testes (Opcional)

Para verificar se tudo está funcionando corretamente:

```bash
# Tornar o script executável (Linux/Mac)
chmod +x run_tests.sh

# Executar testes
./run_tests.sh
# No Windows:
bash run_tests.sh
```

## Acesso ao Sistema

Após a inicialização, você pode acessar o sistema através do navegador:

- **URL**: http://localhost:5000
- **Usuário padrão**: admin@sistema.com
- **Senha padrão**: admin123

Recomendamos alterar a senha padrão após o primeiro acesso.

## Solução de Problemas

### Problemas de Dependências

Se encontrar problemas com dependências Python:

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall
```

### Problemas de Banco de Dados

Para reiniciar o banco de dados SQLite:

```bash
rm -f backend/sistema_nutricao.db
```

### Logs e Depuração

Os logs do sistema são armazenados em:

```
backend/logs/sistema_nutricao.log
```

## Próximos Passos

Após a instalação bem-sucedida:

1. Altere a senha do usuário administrador
2. Configure os parâmetros do sistema
3. Comece a cadastrar fornecedores e insumos
4. Importe dados históricos (se disponíveis)

## Suporte

Para obter suporte ou relatar problemas, entre em contato através de:

- Email: suporte@sistema.com
- Telefone: (XX) XXXX-XXXX

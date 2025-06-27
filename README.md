# Sistema de Nutrição

Este é o pacote completo do Sistema de Nutrição, desenvolvido para substituir a planilha Excel de controle de nutrição com uma solução robusta, segura e com funcionalidades avançadas.

## Conteúdo do Pacote

- **Backend**: API completa com todos os módulos funcionais
- **Documentação**: Guias detalhados de instalação e uso
- **Testes**: Testes de integração para validação do sistema
- **Scripts**: Automação para facilitar execução e testes

## Módulos Principais

1. **Cadastro de NFe**: Gerenciamento de fornecedores, insumos e notas fiscais
2. **Contratos e Cotações**: Gestão de contratos, cotações e planejamento
3. **Controle Mensal**: Registro de entregas e controle de estoque
4. **Fechamento e Análise**: Cálculos de custo médio e relatórios
5. **Autenticação**: Controle de acesso e perfis de usuário

## Instalação Rápida

Consulte o arquivo `docs/instalacao.md` para instruções detalhadas de instalação.

Resumo dos passos:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r backend/requirements.txt

# Iniciar o sistema
./run_backend.sh
```

## Acesso ao Sistema

- **URL**: http://localhost:5000
- **Usuário padrão**: admin@sistema.com
- **Senha padrão**: admin123

## Suporte e Contato

Para suporte ou dúvidas sobre o sistema, entre em contato através dos canais fornecidos na documentação.

---

Desenvolvido por Manus - 2025

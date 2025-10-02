# Makefile para Sistema Agropecuário
# Comandos comuns para desenvolvimento Django

.PHONY: help install run migrate makemigrations superuser shell test clean reset-db backup restore collectstatic

# Configurações
PYTHON = python
MANAGE = $(PYTHON) manage.py
VENV_DIR = venv
DB_FILE = db.sqlite3
BACKUP_DIR = backups

# Comando padrão - mostra ajuda
help:
	@echo "=== Sistema Agropecuário - Comandos Disponíveis ==="
	@echo ""
	@echo "🚀 Comandos Principais:"
	@echo "  make install        - Instala dependências"
	@echo "  make run            - Executa o servidor de desenvolvimento"
	@echo "  make migrate        - Aplica migrações no banco de dados"
	@echo "  make makemigrations - Cria novas migrações"
	@echo "  make superuser      - Cria um superusuário"
	@echo ""
	@echo "🔧 Comandos de Desenvolvimento:"
	@echo "  make shell          - Abre shell do Django"
	@echo "  make test           - Executa testes"
	@echo "  make collectstatic  - Coleta arquivos estáticos"
	@echo "  make fix-config     - Corrige problemas de configuração"
	@echo ""
	@echo "🗃️ Comandos de Banco de Dados:"
	@echo "  make reset-db       - Reseta o banco de dados (CUIDADO!)"
	@echo "  make backup         - Faz backup do banco de dados"
	@echo "  make restore        - Restaura backup do banco"
	@echo ""
	@echo "🧹 Comandos de Limpeza:"
	@echo "  make clean          - Remove arquivos temporários"
	@echo "  make clean-migrations - Remove arquivos de migração"
	@echo ""
	@echo "📋 Comandos de Setup Completo:"
	@echo "  make setup          - Setup completo (install + migrate + superuser)"
	@echo "  make fresh-start    - Novo início (reset-db + setup)"

# Instala dependências
install:
	@echo "📦 Instalando dependências..."
	pip install -r requirements.txt
	@echo "📁 Criando pastas necessárias..."
	mkdir -p logs backups media staticfiles
	@echo "✅ Dependências instaladas!"

# Executa o servidor de desenvolvimento
run:
	@echo "🚀 Iniciando servidor de desenvolvimento..."
	$(MANAGE) runserver

# Aplica migrações
migrate:
	@echo "🔄 Aplicando migrações..."
	$(MANAGE) migrate
	@echo "✅ Migrações aplicadas!"

# Cria migrações
makemigrations:
	@echo "📝 Criando migrações..."
	$(MANAGE) makemigrations
	@echo "✅ Migrações criadas!"

# Cria superusuário
superuser:
	@echo "👤 Criando superusuário..."
	$(MANAGE) createsuperuser

# Abre shell do Django
shell:
	@echo "🐍 Abrindo shell do Django..."
	$(MANAGE) shell

# Executa testes
test:
	@echo "🧪 Executando testes..."
	$(MANAGE) test

# Coleta arquivos estáticos
collectstatic:
	@echo "📁 Coletando arquivos estáticos..."
	$(MANAGE) collectstatic --noinput

# Reseta banco de dados (CUIDADO!)
reset-db:
	@echo "⚠️  ATENÇÃO: Isso vai apagar todos os dados!"
	@read -p "Tem certeza? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "🗑️  Removendo banco de dados..."
	rm -f $(DB_FILE)
	@echo "🔄 Aplicando migrações..."
	$(MANAGE) migrate
	@echo "✅ Banco de dados resetado!"

# Faz backup do banco
backup:
	@echo "💾 Fazendo backup do banco de dados..."
	mkdir -p $(BACKUP_DIR)
	cp $(DB_FILE) $(BACKUP_DIR)/backup_$(shell date +%Y%m%d_%H%M%S).sqlite3
	@echo "✅ Backup criado em $(BACKUP_DIR)/"

# Restaura backup (lista backups disponíveis)
restore:
	@echo "📋 Backups disponíveis:"
	@ls -la $(BACKUP_DIR)/*.sqlite3 2>/dev/null || echo "Nenhum backup encontrado"
	@echo ""
	@echo "Para restaurar, execute:"
	@echo "cp $(BACKUP_DIR)/backup_YYYYMMDD_HHMMSS.sqlite3 $(DB_FILE)"

# Remove arquivos temporários
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	@echo "✅ Limpeza concluída!"

# Remove migrações (CUIDADO!)
clean-migrations:
	@echo "⚠️  ATENÇÃO: Isso vai remover todas as migrações!"
	@read -p "Tem certeza? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "🗑️  Removendo migrações..."
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete
	@echo "✅ Migrações removidas!"

# Setup completo
setup: install makemigrations migrate
	@echo "🎉 Setup básico concluído!"
	@echo "💡 Execute 'make superuser' para criar um administrador"

# Novo início completo
fresh-start: reset-db setup superuser
	@echo "🎉 Sistema pronto para uso!"
	@echo "🚀 Execute 'make run' para iniciar o servidor"

# Comandos de desenvolvimento rápido
dev-reset: clean-migrations makemigrations migrate
	@echo "🔄 Reset de desenvolvimento concluído!"

# Mostra status do sistema
status:
	@echo "📊 Status do Sistema:"
	@echo "Python: $(shell python --version)"
	@echo "Django: $(shell python -c 'import django; print(django.get_version())' 2>/dev/null || echo 'Não instalado')"
	@echo "Banco: $(shell [ -f $(DB_FILE) ] && echo 'Existe ($(shell ls -lh $(DB_FILE) | cut -d' ' -f5))' || echo 'Não existe')"
	@echo "Migrações pendentes: $(shell $(MANAGE) showmigrations --plan 2>/dev/null | grep -c '\[ \]' || echo 'Erro ao verificar')"

# Comandos úteis para produção
prod-setup: install collectstatic migrate
	@echo "🏭 Setup de produção concluído!"


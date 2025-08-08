# Scripts de Automação

> 🤖 **Scripts e utilitários para automação de tarefas de desenvolvimento**

## 📋 Visão Geral

O diretório de scripts contém todos os scripts de automação, utilitários e ferramentas de linha de comando que facilitam o desenvolvimento, deployment, manutenção e operação do projeto. Estes scripts são essenciais para padronizar processos e aumentar a produtividade da equipe.

## 🏗️ Estrutura Recomendada

```
scripts/
├── 📁 development/            # Scripts para desenvolvimento
│   ├── 📄 setup.sh           # Setup inicial do projeto
│   ├── 📄 install-deps.sh    # Instalação de dependências
│   ├── 📄 start-dev.sh       # Iniciar ambiente dev
│   ├── 📄 test.sh            # Executar testes
│   ├── 📄 lint.sh            # Code linting
│   ├── 📄 format.sh          # Code formatting
│   └── 📄 clean.sh           # Limpeza de cache/temp
├── 📁 database/              # Scripts de banco de dados
│   ├── 📄 migrate.sh         # Executar migrações
│   ├── 📄 seed.sh            # Popular dados iniciais
│   ├── 📄 backup.sh          # Backup do banco
│   ├── 📄 restore.sh         # Restaurar backup
│   ├── 📄 reset.sh           # Reset completo do banco
│   └── 📄 connect.sh         # Conectar ao banco
├── 📁 deployment/            # Scripts de deployment
│   ├── 📄 build.sh           # Build da aplicação
│   ├── 📄 deploy.sh          # Deploy para ambiente
│   ├── 📄 rollback.sh        # Rollback de deploy
│   ├── 📄 health-check.sh    # Verificar saúde do app
│   └── 📄 smoke-test.sh      # Testes básicos pós-deploy
├── 📁 docker/                # Scripts relacionados ao Docker
│   ├── 📄 build-image.sh     # Build da imagem Docker
│   ├── 📄 push-image.sh      # Push para registry
│   ├── 📄 run-container.sh   # Executar container local
│   ├── 📄 cleanup-images.sh  # Limpeza de imagens antigas
│   └── 📄 logs.sh            # Visualizar logs
├── 📁 monitoring/            # Scripts de monitoramento
│   ├── 📄 check-services.sh  # Verificar status dos serviços
│   ├── 📄 performance.sh     # Teste de performance
│   ├── 📄 alerts.sh          # Gerenciar alertas
│   └── 📄 report.sh          # Gerar relatórios
├── 📁 security/              # Scripts de segurança
│   ├── 📄 scan-vulnerabilities.sh  # Scan de vulnerabilidades
│   ├── 📄 check-secrets.sh   # Verificar secrets expostos
│   ├── 📄 audit.sh           # Auditoria de segurança
│   └── 📄 compliance.sh      # Verificação de compliance
├── 📁 maintenance/           # Scripts de manutenção
│   ├── 📄 cleanup-logs.sh    # Limpeza de logs antigos
│   ├── 📄 update-deps.sh     # Atualizar dependências
│   ├── 📄 optimize-db.sh     # Otimização do banco
│   └── 📄 archive-data.sh    # Arquivar dados antigos
├── 📁 utilities/             # Utilitários gerais
│   ├── 📄 generate-secrets.sh # Gerar secrets/tokens
│   ├── 📄 create-user.sh     # Criar usuário
│   ├── 📄 send-notification.sh # Enviar notificações
│   └── 📄 sync-env.sh        # Sincronizar ambientes
├── 📁 git/                   # Scripts relacionados ao Git
│   ├── 📄 pre-commit.sh      # Hook pre-commit
│   ├── 📄 post-merge.sh      # Hook post-merge
│   ├── 📄 release.sh         # Criar release
│   └── 📄 changelog.sh       # Gerar changelog
├── 📄 README.md              # Este arquivo
├── 📄 common.sh              # Funções comuns
└── 📄 config.sh              # Configurações globais
```

## 🔧 Scripts de Desenvolvimento

### **1. Setup Inicial** 🚀

```bash
#!/bin/bash
# scripts/development/setup.sh
# Setup inicial do projeto para novos desenvolvedores

set -euo pipefail

# Importar funções comuns
source "$(dirname "$0")/../common.sh"

print_header "🚀 Setup do Projeto MyApp"

# Verificar dependências do sistema
check_system_dependencies() {
    log "Verificando dependências do sistema..."
    
    local deps=("node" "npm" "git" "docker" "docker-compose")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        error "Dependências faltando: ${missing_deps[*]}"
        log "Instale as dependências antes de continuar."
        exit 1
    fi
    
    success "Todas as dependências estão instaladas"
}

# Configurar Node.js
setup_nodejs() {
    log "Configurando Node.js..."
    
    # Verificar versão do Node
    local node_version=$(node --version | cut -d'v' -f2)
    local required_version="18.0.0"
    
    if ! version_gte "$node_version" "$required_version"; then
        warn "Versão do Node.js ($node_version) é menor que a recomendada ($required_version)"
        read -p "Continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    # Instalar dependências
    log "Instalando dependências do Node.js..."
    npm install
    
    success "Node.js configurado com sucesso"
}

# Configurar Git hooks
setup_git_hooks() {
    log "Configurando Git hooks..."
    
    # Pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
./scripts/git/pre-commit.sh
EOF
    
    # Post-merge hook
    cat > .git/hooks/post-merge << 'EOF'
#!/bin/bash
./scripts/git/post-merge.sh
EOF
    
    chmod +x .git/hooks/pre-commit
    chmod +x .git/hooks/post-merge
    
    success "Git hooks configurados"
}

# Configurar ambiente local
setup_environment() {
    log "Configurando ambiente local..."
    
    # Criar arquivo .env se não existir
    if [ ! -f ".env" ]; then
        log "Criando arquivo .env..."
        cp .env.example .env
        warn "Configure as variáveis de ambiente em .env antes de continuar"
    fi
    
    # Configurar banco de dados local
    if [ -f "docker-compose.yml" ]; then
        log "Inicializando banco de dados local..."
        docker-compose up -d db redis
        
        # Aguardar banco ficar pronto
        log "Aguardando banco de dados..."
        sleep 10
        
        # Executar migrações
        npm run migrate
        
        # Popular dados iniciais
        npm run seed
    fi
    
    success "Ambiente configurado"
}

# Verificar instalação
verify_setup() {
    log "Verificando instalação..."
    
    # Testar build
    if npm run build &> /dev/null; then
        success "Build funcionando"
    else
        error "Falha no build"
    fi
    
    # Testar testes
    if npm run test:unit &> /dev/null; then
        success "Testes funcionando"
    else
        warn "Alguns testes falharam"
    fi
    
    # Testar linter
    if npm run lint &> /dev/null; then
        success "Linter funcionando"
    else
        warn "Problemas no linter encontrados"
    fi
}

# Exibir próximos passos
show_next_steps() {
    print_header "✅ Setup Completo!"
    
    echo "Próximos passos:"
    echo "1. Configure as variáveis em .env"
    echo "2. Execute 'npm run dev' para iniciar o desenvolvimento"
    echo "3. Execute 'npm test' para rodar os testes"
    echo "4. Visite http://localhost:3000 para ver a aplicação"
    echo ""
    echo "Comandos úteis:"
    echo "  npm run dev        - Inicia servidor de desenvolvimento"
    echo "  npm run test       - Executa todos os testes"
    echo "  npm run lint       - Verifica qualidade do código"
    echo "  npm run build      - Build para produção"
    echo "  ./scripts/database/reset.sh - Reseta banco de dados"
}

# Execução principal
main() {
    check_system_dependencies
    setup_nodejs
    setup_git_hooks
    setup_environment
    verify_setup
    show_next_steps
}

main "$@"
```

### **2. Script de Desenvolvimento** 💻

```bash
#!/bin/bash
# scripts/development/start-dev.sh
# Inicia ambiente de desenvolvimento completo

set -euo pipefail

source "$(dirname "$0")/../common.sh"

# Configurações
DEV_PORT="${DEV_PORT:-3000}"
API_PORT="${API_PORT:-3001}"
DB_PORT="${DB_PORT:-5432}"

print_header "🔥 Iniciando Ambiente de Desenvolvimento"

# Verificar se portas estão livres
check_ports() {
    log "Verificando portas disponíveis..."
    
    local ports=("$DEV_PORT" "$API_PORT" "$DB_PORT")
    
    for port in "${ports[@]}"; do
        if is_port_in_use "$port"; then
            error "Porta $port já está em uso"
        fi
    done
    
    success "Todas as portas estão disponíveis"
}

# Iniciar serviços de infraestrutura
start_infrastructure() {
    log "Iniciando serviços de infraestrutura..."
    
    # Docker Compose para banco, cache, etc.
    docker-compose up -d db redis
    
    # Aguardar serviços ficarem prontos
    wait_for_service "database" "localhost" "$DB_PORT" 30
    wait_for_service "redis" "localhost" "6379" 10
    
    success "Infraestrutura iniciada"
}

# Preparar banco de dados
prepare_database() {
    log "Preparando banco de dados..."
    
    # Executar migrações pendentes
    if npm run migrate:status | grep -q "pending"; then
        log "Executando migrações pendentes..."
        npm run migrate
    fi
    
    # Verificar se precisa popular dados
    if ! npm run db:check-data &> /dev/null; then
        log "Populando dados iniciais..."
        npm run seed
    fi
    
    success "Banco de dados preparado"
}

# Iniciar aplicação
start_application() {
    log "Iniciando aplicação..."
    
    # Instalar dependências se necessário
    if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ]; then
        log "Instalando/atualizando dependências..."
        npm install
    fi
    
    # Gerar assets se necessário
    if [ ! -d "dist" ] || find src -newer dist -type f | head -1 | grep -q .; then
        log "Gerando assets..."
        npm run build:dev
    fi
    
    # Iniciar em modo desenvolvimento
    log "Iniciando servidor de desenvolvimento na porta $DEV_PORT..."
    
    # Background processes
    npm run dev:api &
    local api_pid=$!
    
    npm run dev:frontend &
    local frontend_pid=$!
    
    # Wait for services to start
    wait_for_service "API" "localhost" "$API_PORT" 30
    wait_for_service "Frontend" "localhost" "$DEV_PORT" 30
    
    success "Aplicação iniciada com sucesso!"
    
    # Trap para cleanup
    trap "cleanup_processes $api_pid $frontend_pid" EXIT
    
    # Show status
    show_development_status
    
    # Wait for user interrupt
    log "Pressione Ctrl+C para parar..."
    wait
}

# Mostrar status do desenvolvimento
show_development_status() {
    print_header "🌟 Ambiente de Desenvolvimento Ativo"
    
    echo "Serviços disponíveis:"
    echo "  📱 Frontend:    http://localhost:$DEV_PORT"
    echo "  🔌 API:         http://localhost:$API_PORT"
    echo "  🗄️  Database:    localhost:$DB_PORT"
    echo "  📊 Redis:       localhost:6379"
    echo ""
    echo "Ferramentas úteis:"
    echo "  🧪 Testes:      npm test"
    echo "  🔍 Linter:      npm run lint"
    echo "  📝 Logs:        ./scripts/docker/logs.sh"
    echo "  🔄 Reset DB:    ./scripts/database/reset.sh"
}

# Cleanup de processos
cleanup_processes() {
    local pids=("$@")
    
    log "Parando processos..."
    
    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
        fi
    done
    
    # Parar Docker Compose
    docker-compose down
    
    success "Ambiente parado"
}

# Execução principal
main() {
    check_ports
    start_infrastructure
    prepare_database
    start_application
}

main "$@"
```

## 🗄️ Scripts de Banco de Dados

### **1. Migration Script** 📊

```bash
#!/bin/bash
# scripts/database/migrate.sh
# Executar migrações do banco de dados

set -euo pipefail

source "$(dirname "$0")/../common.sh"

# Configurações
ENVIRONMENT="${1:-development}"
ACTION="${2:-up}"

print_header "🗄️ Database Migration - $ENVIRONMENT"

# Validar ambiente
validate_environment() {
    local valid_envs=("development" "staging" "production")
    
    if [[ ! " ${valid_envs[@]} " =~ " $ENVIRONMENT " ]]; then
        error "Ambiente inválido: $ENVIRONMENT"
    fi
    
    # Confirmação para produção
    if [[ "$ENVIRONMENT" == "production" ]]; then
        warn "ATENÇÃO: Executando migração em PRODUÇÃO!"
        read -p "Tem certeza? Digite 'yes' para continuar: " -r
        if [[ ! $REPLY == "yes" ]]; then
            error "Migração cancelada"
        fi
    fi
}

# Verificar conexão com banco
check_database_connection() {
    log "Verificando conexão com banco de dados..."
    
    if npm run db:ping &> /dev/null; then
        success "Conexão com banco estabelecida"
    else
        error "Não foi possível conectar ao banco de dados"
    fi
}

# Backup antes da migração (apenas produção)
backup_before_migration() {
    if [[ "$ENVIRONMENT" == "production" ]]; then
        log "Criando backup antes da migração..."
        
        local backup_file="backup_pre_migration_$(date +%Y%m%d_%H%M%S).sql"
        ./scripts/database/backup.sh "$backup_file"
        
        success "Backup criado: $backup_file"
    fi
}

# Executar migrações
run_migrations() {
    log "Executando migrações..."
    
    case "$ACTION" in
        "up")
            log "Aplicando migrações..."
            npm run migrate:up
            ;;
        "down")
            log "Revertendo última migração..."
            npm run migrate:down
            ;;
        "status")
            log "Status das migrações:"
            npm run migrate:status
            return 0
            ;;
        "reset")
            warn "ATENÇÃO: Isso irá resetar TODAS as migrações!"
            read -p "Continuar? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                npm run migrate:reset
            else
                log "Reset cancelado"
                return 0
            fi
            ;;
        *)
            error "Ação inválida: $ACTION. Use: up, down, status, reset"
            ;;
    esac
    
    success "Migrações executadas com sucesso"
}

# Verificar integridade após migração
verify_database_integrity() {
    log "Verificando integridade do banco..."
    
    # Verificar tabelas essenciais
    if npm run db:verify-tables &> /dev/null; then
        success "Estrutura do banco está íntegra"
    else
        error "Problemas na estrutura do banco detectados"
    fi
    
    # Verificar constraints
    if npm run db:verify-constraints &> /dev/null; then
        success "Constraints estão corretas"
    else
        warn "Alguns problemas com constraints encontrados"
    fi
}

# Mostrar estatísticas do banco
show_database_stats() {
    log "Estatísticas do banco de dados:"
    npm run db:stats
}

# Execução principal
main() {
    validate_environment
    check_database_connection
    backup_before_migration
    run_migrations
    verify_database_integrity
    show_database_stats
}

main "$@"
```

### **2. Backup Script** 💾

```bash
#!/bin/bash
# scripts/database/backup.sh
# Backup do banco de dados

set -euo pipefail

source "$(dirname "$0")/../common.sh"

# Configurações
BACKUP_DIR="${BACKUP_DIR:-./backups}"
ENVIRONMENT="${1:-development}"
BACKUP_NAME="${2:-backup_$(date +%Y%m%d_%H%M%S)}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

print_header "💾 Database Backup - $ENVIRONMENT"

# Criar diretório de backup
setup_backup_directory() {
    log "Configurando diretório de backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Verificar espaço em disco
    local available_space=$(df "$BACKUP_DIR" | awk 'NR==2 {print $4}')
    local required_space=1048576  # 1GB em KB
    
    if [ "$available_space" -lt "$required_space" ]; then
        warn "Pouco espaço em disco disponível"
    fi
    
    success "Diretório de backup configurado: $BACKUP_DIR"
}

# Executar backup
perform_backup() {
    log "Iniciando backup do banco de dados..."
    
    local backup_file="$BACKUP_DIR/${BACKUP_NAME}.sql"
    local backup_file_compressed="${backup_file}.gz"
    
    # Configurar variáveis de ambiente baseado no ambiente
    case "$ENVIRONMENT" in
        "development")
            export DATABASE_URL="${DATABASE_URL:-postgres://postgres:password@localhost:5432/app_dev}"
            ;;
        "staging")
            export DATABASE_URL="${STAGING_DATABASE_URL}"
            ;;
        "production")
            export DATABASE_URL="${PRODUCTION_DATABASE_URL}"
            ;;
    esac
    
    # Executar pg_dump
    log "Executando pg_dump..."
    
    if pg_dump "$DATABASE_URL" \
        --verbose \
        --no-acl \
        --no-owner \
        --clean \
        --if-exists \
        > "$backup_file"; then
        
        # Comprimir backup
        log "Comprimindo backup..."
        gzip "$backup_file"
        
        # Calcular checksum
        local checksum=$(sha256sum "$backup_file_compressed" | cut -d' ' -f1)
        echo "$checksum" > "${backup_file_compressed}.sha256"
        
        # Informações do backup
        local file_size=$(du -h "$backup_file_compressed" | cut -f1)
        
        success "Backup criado com sucesso!"
        log "Arquivo: $backup_file_compressed"
        log "Tamanho: $file_size"
        log "Checksum: $checksum"
        
    else
        error "Falha ao criar backup"
    fi
}

# Verificar integridade do backup
verify_backup() {
    local backup_file="$BACKUP_DIR/${BACKUP_NAME}.sql.gz"
    local checksum_file="${backup_file}.sha256"
    
    log "Verificando integridade do backup..."
    
    if [ -f "$checksum_file" ]; then
        if sha256sum -c "$checksum_file" &> /dev/null; then
            success "Integridade do backup verificada"
        else
            error "Falha na verificação de integridade"
        fi
    else
        warn "Arquivo de checksum não encontrado"
    fi
}

# Limpar backups antigos
cleanup_old_backups() {
    log "Removendo backups antigos (> $RETENTION_DAYS dias)..."
    
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -name "*.sha256" -mtime +$RETENTION_DAYS -delete
    
    local remaining_backups=$(find "$BACKUP_DIR" -name "*.sql.gz" | wc -l)
    success "Limpeza concluída. Backups restantes: $remaining_backups"
}

# Upload para cloud (opcional)
upload_to_cloud() {
    if [ -n "${AWS_S3_BACKUP_BUCKET:-}" ]; then
        log "Fazendo upload para S3..."
        
        local backup_file="$BACKUP_DIR/${BACKUP_NAME}.sql.gz"
        local s3_path="s3://$AWS_S3_BACKUP_BUCKET/database-backups/$ENVIRONMENT/"
        
        if aws s3 cp "$backup_file" "$s3_path" &> /dev/null; then
            success "Upload para S3 concluído"
        else
            warn "Falha no upload para S3"
        fi
    fi
}

# Listar backups disponíveis
list_backups() {
    log "Backups disponíveis:"
    
    find "$BACKUP_DIR" -name "*.sql.gz" -printf "%T@ %Tc %p\n" | sort -n | cut -d' ' -f2-
}

# Execução principal
main() {
    setup_backup_directory
    perform_backup
    verify_backup
    cleanup_old_backups
    upload_to_cloud
    list_backups
}

# Permitir listar backups sem fazer novo backup
if [[ "${1:-}" == "list" ]]; then
    list_backups
else
    main "$@"
fi
```

## 🚀 Scripts de Deploy

### **1. Build Script** 🏗️

```bash
#!/bin/bash
# scripts/deployment/build.sh
# Build da aplicação para diferentes ambientes

set -euo pipefail

source "$(dirname "$0")/../common.sh"

# Configurações
ENVIRONMENT="${1:-production}"
BUILD_NUMBER="${BUILD_NUMBER:-$(date +%Y%m%d%H%M%S)}"
VERSION="${VERSION:-$(git describe --tags --always)}"

print_header "🏗️ Building Application - $ENVIRONMENT"

# Validar ambiente
validate_environment() {
    local valid_envs=("development" "staging" "production")
    
    if [[ ! " ${valid_envs[@]} " =~ " $ENVIRONMENT " ]]; then
        error "Ambiente inválido: $ENVIRONMENT"
    fi
}

# Limpar builds anteriores
clean_previous_builds() {
    log "Limpando builds anteriores..."
    
    rm -rf dist/
    rm -rf build/
    rm -rf .next/
    
    success "Builds anteriores removidos"
}

# Instalar dependências
install_dependencies() {
    log "Instalando dependências..."
    
    # Usar npm ci para builds reproduzíveis
    npm ci --production=false
    
    # Audit de segurança
    if ! npm audit --audit-level moderate; then
        warn "Vulnerabilidades encontradas nas dependências"
        
        if [[ "$ENVIRONMENT" == "production" ]]; then
            read -p "Continuar mesmo assim? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                error "Build cancelado devido a vulnerabilidades"
            fi
        fi
    fi
    
    success "Dependências instaladas"
}

# Executar linting
run_linting() {
    log "Executando linting..."
    
    if npm run lint; then
        success "Linting passou"
    else
        if [[ "$ENVIRONMENT" == "production" ]]; then
            error "Linting falhou - build cancelado"
        else
            warn "Linting falhou - continuando..."
        fi
    fi
}

# Executar testes
run_tests() {
    log "Executando testes..."
    
    # Unit tests
    if npm run test:unit; then
        success "Testes unitários passaram"
    else
        error "Testes unitários falharam"
    fi
    
    # Integration tests (apenas para staging e production)
    if [[ "$ENVIRONMENT" != "development" ]]; then
        if npm run test:integration; then
            success "Testes de integração passaram"
        else
            error "Testes de integração falharam"
        fi
    fi
}

# Build da aplicação
build_application() {
    log "Executando build da aplicação..."
    
    # Configurar variáveis de ambiente do build
    export NODE_ENV="production"
    export BUILD_NUMBER="$BUILD_NUMBER"
    export VERSION="$VERSION"
    export ENVIRONMENT="$ENVIRONMENT"
    
    # Build baseado no tipo de projeto
    if [ -f "next.config.js" ]; then
        # Next.js
        npm run build
    elif [ -f "vite.config.js" ]; then
        # Vite
        npm run build
    elif [ -f "webpack.config.js" ]; then
        # Webpack
        npm run build
    else
        # Generic build
        npm run build
    fi
    
    success "Build da aplicação concluído"
}

# Otimizar assets
optimize_assets() {
    log "Otimizando assets..."
    
    # Comprimir imagens (se imageoptim estiver disponível)
    if command -v imageoptim &> /dev/null; then
        find dist -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | xargs imageoptim
    fi
    
    # Gerar mapas de source (apenas para não-produção)
    if [[ "$ENVIRONMENT" != "production" ]]; then
        npm run build:sourcemaps
    fi
    
    success "Assets otimizados"
}

# Gerar manifest de build
generate_build_manifest() {
    log "Gerando manifest de build..."
    
    local manifest_file="dist/build-manifest.json"
    
    cat > "$manifest_file" << EOF
{
  "version": "$VERSION",
  "buildNumber": "$BUILD_NUMBER",
  "environment": "$ENVIRONMENT",
  "buildDate": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "gitCommit": "$(git rev-parse HEAD)",
  "gitBranch": "$(git rev-parse --abbrev-ref HEAD)",
  "nodeVersion": "$(node --version)",
  "npmVersion": "$(npm --version)"
}
EOF
    
    success "Manifest de build gerado: $manifest_file"
}

# Verificar build
verify_build() {
    log "Verificando build..."
    
    # Verificar se arquivos essenciais existem
    local essential_files=("dist/index.html" "dist/main.js")
    
    for file in "${essential_files[@]}"; do
        if [ ! -f "$file" ]; then
            error "Arquivo essencial não encontrado: $file"
        fi
    done
    
    # Verificar tamanho dos assets
    local total_size=$(du -sh dist/ | cut -f1)
    log "Tamanho total do build: $total_size"
    
    # Verificar se não há arquivos muito grandes
    local large_files=$(find dist -size +5M -type f)
    if [ -n "$large_files" ]; then
        warn "Arquivos grandes encontrados:"
        echo "$large_files"
    fi
    
    success "Build verificado"
}

# Criar archive do build
create_build_archive() {
    log "Criando archive do build..."
    
    local archive_name="build-${ENVIRONMENT}-${BUILD_NUMBER}.tar.gz"
    
    tar -czf "$archive_name" -C dist .
    
    local archive_size=$(du -h "$archive_name" | cut -f1)
    success "Archive criado: $archive_name ($archive_size)"
}

# Execução principal
main() {
    validate_environment
    clean_previous_builds
    install_dependencies
    run_linting
    run_tests
    build_application
    optimize_assets
    generate_build_manifest
    verify_build
    create_build_archive
    
    print_header "✅ Build Completo!"
    log "Ambiente: $ENVIRONMENT"
    log "Versão: $VERSION"
    log "Build: $BUILD_NUMBER"
}

main "$@"
```

## 🧰 Funções Comuns

### **1. Common Functions** 🛠️

```bash
#!/bin/bash
# scripts/common.sh
# Funções comuns utilizadas por outros scripts

# Cores para output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export PURPLE='\033[0;35m'
export CYAN='\033[0;36m'
export WHITE='\033[1;37m'
export NC='\033[0m' # No Color

# Função para logging com timestamp
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Função para warnings
warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARN:${NC} $1"
}

# Função para erros
error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" >&2
    exit 1
}

# Função para sucesso
success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1"
}

# Função para debug (apenas se DEBUG=1)
debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo -e "${PURPLE}[$(date +'%Y-%m-%d %H:%M:%S')] DEBUG:${NC} $1"
    fi
}

# Função para cabeçalhos
print_header() {
    echo
    echo -e "${CYAN}================================${NC}"
    echo -e "${CYAN} $1${NC}"
    echo -e "${CYAN}================================${NC}"
    echo
}

# Função para seções
print_section() {
    echo
    echo -e "${WHITE}--- $1 ---${NC}"
    echo
}

# Verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar se porta está em uso
is_port_in_use() {
    local port=$1
    lsof -i ":$port" >/dev/null 2>&1
}

# Aguardar serviço ficar pronto
wait_for_service() {
    local service_name=$1
    local host=$2
    local port=$3
    local timeout=${4:-30}
    local counter=0
    
    log "Aguardando $service_name ficar pronto..."
    
    while ! nc -z "$host" "$port" >/dev/null 2>&1; do
        if [ $counter -ge $timeout ]; then
            error "$service_name não ficou pronto em ${timeout}s"
        fi
        
        counter=$((counter + 1))
        sleep 1
    done
    
    success "$service_name está pronto"
}

# Verificar se URL responde
wait_for_url() {
    local url=$1
    local timeout=${2:-30}
    local counter=0
    
    log "Aguardando $url responder..."
    
    while ! curl -f -s "$url" >/dev/null 2>&1; do
        if [ $counter -ge $timeout ]; then
            error "$url não respondeu em ${timeout}s"
        fi
        
        counter=$((counter + 1))
        sleep 1
    done
    
    success "$url está respondendo"
}

# Comparar versões (semver)
version_gte() {
    local version1=$1
    local version2=$2
    
    printf '%s\n%s\n' "$version2" "$version1" | sort -V -C
}

# Obter IP público
get_public_ip() {
    curl -s https://ipinfo.io/ip 2>/dev/null || echo "unknown"
}

# Gerar string aleatória
generate_random_string() {
    local length=${1:-32}
    openssl rand -hex $((length / 2))
}

# Verificar se está executando como root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "Este script não deve ser executado como root"
    fi
}

# Verificar se está executando em CI
is_ci() {
    [[ "${CI:-false}" == "true" ]] || [[ -n "${GITHUB_ACTIONS:-}" ]] || [[ -n "${GITLAB_CI:-}" ]]
}

# Confirmar ação perigosa
confirm_dangerous_action() {
    local action=$1
    
    if is_ci; then
        log "Executando em CI, pulando confirmação"
        return 0
    fi
    
    warn "AÇÃO PERIGOSA: $action"
    read -p "Tem certeza? Digite 'yes' para continuar: " -r
    
    if [[ ! $REPLY == "yes" ]]; then
        log "Ação cancelada"
        exit 0
    fi
}

# Backup de arquivo
backup_file() {
    local file=$1
    local backup_file="${file}.backup.$(date +%Y%m%d_%H%M%S)"
    
    if [ -f "$file" ]; then
        cp "$file" "$backup_file"
        log "Backup criado: $backup_file"
    fi
}

# Restaurar backup
restore_backup() {
    local original_file=$1
    local backup_file=$(ls "${original_file}.backup."* 2>/dev/null | tail -n 1)
    
    if [ -f "$backup_file" ]; then
        cp "$backup_file" "$original_file"
        success "Backup restaurado: $backup_file -> $original_file"
    else
        error "Nenhum backup encontrado para $original_file"
    fi
}

# Cleanup trap
cleanup_on_exit() {
    local exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        warn "Script terminou com erro (código: $exit_code)"
    fi
    
    # Cleanup personalizado pode ser adicionado aqui
    debug "Executando cleanup..."
}

# Configurar trap para cleanup
trap cleanup_on_exit EXIT

# Verificar dependências do sistema
check_dependencies() {
    local deps=("$@")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command_exists "$dep"; then
            missing+=("$dep")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        error "Dependências faltando: ${missing[*]}"
    fi
}

# Executar comando com retry
retry() {
    local max_attempts=$1
    shift
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if "$@"; then
            return 0
        fi
        
        warn "Tentativa $attempt/$max_attempts falhou"
        attempt=$((attempt + 1))
        
        if [ $attempt -le $max_attempts ]; then
            sleep $((attempt * 2))
        fi
    done
    
    error "Comando falhou após $max_attempts tentativas: $*"
}

# Verificar espaço em disco
check_disk_space() {
    local path=${1:-.}
    local required_mb=${2:-1024}
    
    local available_mb=$(df "$path" | awk 'NR==2 {print int($4/1024)}')
    
    if [ "$available_mb" -lt "$required_mb" ]; then
        error "Espaço insuficiente em $path. Requerido: ${required_mb}MB, Disponível: ${available_mb}MB"
    fi
    
    debug "Espaço disponível em $path: ${available_mb}MB"
}

# Load environment variables
load_env() {
    local env_file=${1:-.env}
    
    if [ -f "$env_file" ]; then
        export $(grep -v '^#' "$env_file" | xargs)
        debug "Variáveis carregadas de $env_file"
    else
        warn "Arquivo de ambiente não encontrado: $env_file"
    fi
}

# Validar formato de email
validate_email() {
    local email=$1
    local regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if [[ $email =~ $regex ]]; then
        return 0
    else
        return 1
    fi
}

# Validar URL
validate_url() {
    local url=$1
    
    if curl -f -s --head "$url" >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Get script directory
get_script_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)"
}

# Get project root directory
get_project_root() {
    local script_dir=$(get_script_dir)
    echo "$(dirname "$script_dir")"
}
```

## 📋 Configurações

### **1. Config Script** ⚙️

```bash
#!/bin/bash
# scripts/config.sh
# Configurações globais do projeto

# Versões das ferramentas
export NODE_VERSION="20.0.0"
export NPM_VERSION="10.0.0"
export DOCKER_VERSION="24.0.0"

# Configurações de desenvolvimento
export DEV_PORT=3000
export API_PORT=3001
export DB_PORT=5432
export REDIS_PORT=6379

# Configurações de build
export BUILD_TIMEOUT=300
export TEST_TIMEOUT=120
export LINT_TIMEOUT=60

# Configurações de deploy
export DEPLOY_TIMEOUT=600
export HEALTH_CHECK_TIMEOUT=120
export ROLLBACK_TIMEOUT=300

# Configurações de banco
export DB_BACKUP_RETENTION_DAYS=30
export DB_MIGRATION_TIMEOUT=300

# Configurações de monitoramento
export METRICS_ENABLED=true
export LOG_LEVEL=info
export PROMETHEUS_PORT=9090

# Configurações de segurança
export SECURITY_SCAN_ENABLED=true
export DEPENDENCY_CHECK_ENABLED=true

# URLs dos ambientes
export DEV_URL="http://localhost:3000"
export STAGING_URL="https://staging.myapp.com"
export PRODUCTION_URL="https://myapp.com"

# Notificações
export SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
export EMAIL_NOTIFICATIONS="${EMAIL_NOTIFICATIONS:-false}"

# Feature flags
export ENABLE_PERFORMANCE_MONITORING=true
export ENABLE_A_B_TESTING=false
export ENABLE_ADVANCED_LOGGING=true
```

## 🎓 Para Estudantes

### **Projetos por Nível** 📚

**🟢 Iniciante**
- Scripts básicos de setup e build
- Automatização de tarefas simples
- Backup e restore de banco
- Scripts de linting e formatting

**🟡 Intermediário**
- Scripts de deploy automatizado
- Monitoramento e health checks
- Scripts de migração de banco
- Integração com CI/CD

**🔴 Avançado**
- Scripts de automação complexa
- Orquestração multi-serviço
- Scripts de disaster recovery
- Automação de compliance e segurança

### **Skills de Scripting** 🎯

1. **Bash Scripting** → Automação básica
2. **Error Handling** → Tratamento robusto de erros
3. **Configuration Management** → Gerenciamento de configs
4. **Process Automation** → Automação de processos
5. **System Integration** → Integração entre sistemas
6. **Monitoring & Alerting** → Monitoramento automatizado
7. **DevOps Practices** → Práticas de DevOps

### **Boas Práticas** ✅

- Use `set -euo pipefail` para scripts robustos
- Valide parâmetros de entrada
- Implemente logging adequado
- Faça backup antes de mudanças perigosas
- Use funções para código reutilizável
- Documente scripts complexos
- Teste scripts em ambientes seguros

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Scripts devem ser idempotentes
- Valide todas as entradas
- Use logging consistente
- Implemente rollback quando possível
- Teste em ambiente seguro primeiro
- Documente parâmetros e funcionalidades
- Use versionamento para scripts críticos

### **❌ Evite**
- Hard-coding de valores
- Scripts sem tratamento de erro
- Falta de validação de entrada
- Scripts monolíticos muito complexos
- Falta de logging
- Scripts sem documentação
- Executar scripts não testados em produção

### **🎯 Métricas de Sucesso**
- Redução de tarefas manuais
- Tempo de deploy menor
- Menos erros humanos
- Padronização de processos
- Maior confiabilidade
- Facilidade de onboarding
- Automação de compliance

---

**Scripts bem escritos são o coração da automação eficiente. Invista tempo na criação de scripts robustos e reutilizáveis!**

# Database - Banco de Dados e Persistência

> 🗄️ **Schemas, migrations, seeds e gestão de dados**

## 📋 Visão Geral

O módulo de database é responsável pela estrutura, versionamento e gestão dos dados da aplicação. Inclui schemas, migrations, seeds, backups e otimizações de performance para garantir integridade e eficiência dos dados.

## 🏗️ Estrutura Recomendada

```
database/
├── 📁 migrations/              # Scripts de migração (versionamento)
│   ├── 📄 001_create_users.sql
│   ├── 📄 002_create_posts.sql
│   ├── 📄 003_add_user_roles.sql
│   └── 📄 004_create_indexes.sql
├── 📁 seeds/                   # Dados iniciais e de teste
│   ├── 📄 01_users.sql
│   ├── 📄 02_categories.sql
│   └── 📄 03_sample_data.sql
├── 📁 schemas/                 # Definições de schema
│   ├── 📄 schema.sql           # Schema completo atual
│   ├── 📄 constraints.sql      # Constraints e relacionamentos
│   └── 📄 indexes.sql          # Índices para performance
├── 📁 procedures/              # Stored procedures e functions
│   ├── 📄 user_procedures.sql
│   ├── 📄 report_functions.sql
│   └── 📄 data_cleanup.sql
├── 📁 views/                   # Views complexas
│   ├── 📄 user_stats.sql
│   ├── 📄 dashboard_data.sql
│   └── 📄 reports.sql
├── 📁 triggers/                # Triggers de auditoria e validação
│   ├── 📄 audit_triggers.sql
│   └── 📄 validation_triggers.sql
├── 📁 backups/                 # Scripts de backup
│   ├── 📄 backup_script.sh
│   └── 📄 restore_script.sh
├── 📁 docs/                    # Documentação do banco
│   ├── 📄 er_diagram.md        # Diagrama ER
│   ├── 📄 data_dictionary.md   # Dicionário de dados
│   └── 📄 optimization.md      # Guia de otimização
├── 📁 scripts/                 # Scripts utilitários
│   ├── 📄 setup.sh             # Setup inicial
│   ├── 📄 migrate.sh           # Execução de migrations
│   └── 📄 reset.sh             # Reset do banco
├── 📄 docker-compose.db.yml    # Container do banco
├── 📄 .env.example             # Variáveis de ambiente
└── 📄 README.md                # Este arquivo
```

## 🛠️ Tecnologias Recomendadas

### **Bancos Relacionais**
- **PostgreSQL** - Robusto, extensível, open source
- **MySQL/MariaDB** - Popular, bem documentado
- **SQLite** - Leve, ideal para desenvolvimento/teste
- **SQL Server** - Microsoft, integração .NET

### **Bancos NoSQL**
- **MongoDB** - Document-based, flexível
- **Redis** - Cache, sessões, filas
- **Cassandra** - Distribuído, alta escala
- **ElasticSearch** - Busca e analytics

### **Ferramentas de Migration**
- **Flyway** (Java/Spring)
- **Liquibase** (Multi-plataforma)
- **Alembic** (Python/SQLAlchemy)
- **Prisma Migrate** (Node.js)
- **Rails Migrations** (Ruby)

### **ORM/Query Builders**
- **Prisma** (Node.js/TypeScript)
- **TypeORM** (Node.js/TypeScript)
- **SQLAlchemy** (Python)
- **Hibernate** (Java)
- **Entity Framework** (C#/.NET)

## 📊 Design de Banco de Dados

### **1. Modelagem de Dados** 🎨

**Diagrama ER Exemplo**
```sql
-- Usuários (entidade central)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'user',
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Posts (relacionamento 1:N com users)
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    status post_status DEFAULT 'draft',
    author_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tags (relacionamento N:N com posts)
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#666666'
);

CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);
```

### **2. Tipos Customizados** 🔧

```sql
-- Enums para garantir integridade
CREATE TYPE user_role AS ENUM ('admin', 'moderator', 'user');
CREATE TYPE post_status AS ENUM ('draft', 'published', 'archived');
CREATE TYPE notification_type AS ENUM ('info', 'warning', 'error', 'success');

-- Domínios para validação
CREATE DOMAIN email AS VARCHAR(255) 
CHECK (VALUE ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

CREATE DOMAIN phone AS VARCHAR(20) 
CHECK (VALUE ~* '^\+?[1-9]\d{1,14}$');
```

### **3. Constraints e Validações** ✅

```sql
-- Constraints de integridade
ALTER TABLE posts 
ADD CONSTRAINT check_published_date 
CHECK (published_at IS NULL OR published_at >= created_at);

ALTER TABLE users 
ADD CONSTRAINT check_email_format 
CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Índices para performance
CREATE INDEX idx_posts_author_status ON posts(author_id, status);
CREATE INDEX idx_posts_published_date ON posts(published_at) WHERE status = 'published';
CREATE INDEX idx_users_email_active ON users(email) WHERE is_active = true;

-- Índices de texto completo
CREATE INDEX idx_posts_search ON posts USING gin(to_tsvector('portuguese', title || ' ' || content));
```

## 🔄 Migrations e Versionamento

### **1. Sistema de Migrations** 📋

```sql
-- migrations/001_create_users.sql
-- Migration: Create users table
-- Author: Developer Name
-- Date: 2024-01-01

BEGIN;

CREATE TYPE user_role AS ENUM ('admin', 'moderator', 'user');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role user_role DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Trigger para updated_at
CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Inserir admin padrão
INSERT INTO users (email, password_hash, name, role) VALUES 
('admin@example.com', '$2b$12$...', 'Administrador', 'admin');

COMMIT;
```

### **2. Script de Migration** 🚀

```bash
#!/bin/bash
# scripts/migrate.sh

set -e

DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
DB_NAME=${DB_NAME:-myapp}
DB_USER=${DB_USER:-postgres}

echo "🚀 Executing database migrations..."

# Criar tabela de controle se não existir
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME << EOF
CREATE TABLE IF NOT EXISTS schema_migrations (
    version VARCHAR(255) PRIMARY KEY,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
EOF

# Executar migrations pendentes
for migration in migrations/*.sql; do
    if [ -f "$migration" ]; then
        version=$(basename "$migration" .sql)
        
        # Verificar se já foi executada
        exists=$(psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c \
            "SELECT 1 FROM schema_migrations WHERE version = '$version';" | xargs)
        
        if [ "$exists" != "1" ]; then
            echo "📦 Executing migration: $version"
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$migration"
            
            # Registrar execução
            psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c \
                "INSERT INTO schema_migrations (version) VALUES ('$version');"
            
            echo "✅ Migration $version executed successfully"
        else
            echo "⏭️  Migration $version already executed, skipping"
        fi
    fi
done

echo "🎉 All migrations completed!"
```

### **3. Rollback de Migrations** ↩️

```sql
-- migrations/001_create_users_rollback.sql
-- Rollback for: Create users table

BEGIN;

-- Remover trigger
DROP TRIGGER IF EXISTS trigger_users_updated_at ON users;

-- Remover índices
DROP INDEX IF EXISTS idx_users_email;
DROP INDEX IF EXISTS idx_users_role;

-- Remover tabela
DROP TABLE IF EXISTS users;

-- Remover tipo
DROP TYPE IF EXISTS user_role;

-- Remover da tabela de controle
DELETE FROM schema_migrations WHERE version = '001_create_users';

COMMIT;
```

## 🌱 Seeds e Dados Iniciais

### **1. Seeds de Produção** 🎯

```sql
-- seeds/01_essential_data.sql
-- Dados essenciais para o funcionamento do sistema

BEGIN;

-- Usuário administrador padrão
INSERT INTO users (email, password_hash, name, role) VALUES 
('admin@company.com', '$2b$12$encrypted_password', 'Administrator', 'admin')
ON CONFLICT (email) DO NOTHING;

-- Categorias padrão
INSERT INTO categories (name, slug, description) VALUES 
('Technology', 'technology', 'Posts about technology'),
('Business', 'business', 'Business-related content'),
('Education', 'education', 'Educational content')
ON CONFLICT (slug) DO NOTHING;

-- Configurações do sistema
INSERT INTO settings (key, value, description) VALUES 
('site_name', 'My Application', 'Nome do site'),
('site_description', 'A great application', 'Descrição do site'),
('posts_per_page', '10', 'Posts por página'),
('maintenance_mode', 'false', 'Modo de manutenção')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

COMMIT;
```

### **2. Seeds de Desenvolvimento** 🧪

```sql
-- seeds/02_development_data.sql
-- Dados para desenvolvimento e testes

BEGIN;

-- Usuários de teste
INSERT INTO users (email, password_hash, name, role) VALUES 
('john@example.com', '$2b$12$test_password', 'John Doe', 'user'),
('jane@example.com', '$2b$12$test_password', 'Jane Smith', 'moderator'),
('test@example.com', '$2b$12$test_password', 'Test User', 'user');

-- Posts de exemplo
INSERT INTO posts (title, content, slug, status, author_id, category_id) VALUES 
('Welcome to Our Platform', 'This is the first post...', 'welcome-to-our-platform', 'published', 1, 1),
('Getting Started Guide', 'Here is how to get started...', 'getting-started-guide', 'published', 2, 3),
('Draft Post', 'This is a draft post...', 'draft-post', 'draft', 1, 1);

-- Tags de exemplo
INSERT INTO tags (name, slug, color) VALUES 
('Tutorial', 'tutorial', '#3B82F6'),
('News', 'news', '#EF4444'),
('Guide', 'guide', '#10B981');

-- Relacionamentos post-tag
INSERT INTO post_tags (post_id, tag_id) VALUES 
(1, 2), (2, 1), (2, 3), (3, 1);

COMMIT;
```

### **3. Script de Seed** 🌱

```bash
#!/bin/bash
# scripts/seed.sh

set -e

ENVIRONMENT=${1:-development}

echo "🌱 Seeding database for environment: $ENVIRONMENT"

case $ENVIRONMENT in
    "production")
        echo "🎯 Loading production seeds..."
        psql -f seeds/01_essential_data.sql
        ;;
    "development")
        echo "🧪 Loading development seeds..."
        psql -f seeds/01_essential_data.sql
        psql -f seeds/02_development_data.sql
        ;;
    "test")
        echo "🧪 Loading test seeds..."
        psql -f seeds/01_essential_data.sql
        psql -f seeds/03_test_data.sql
        ;;
    *)
        echo "❌ Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "✅ Database seeded successfully!"
```

## ⚡ Performance e Otimização

### **1. Índices Estratégicos** 🔍

```sql
-- indexes.sql
-- Índices para otimização de queries

-- Índices simples para busca rápida
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_posts_status ON posts(status);
CREATE INDEX CONCURRENTLY idx_posts_created_at ON posts(created_at DESC);

-- Índices compostos para queries complexas
CREATE INDEX CONCURRENTLY idx_posts_author_status_date 
ON posts(author_id, status, created_at DESC);

-- Índices parciais para otimizar casos específicos
CREATE INDEX CONCURRENTLY idx_active_users 
ON users(created_at) WHERE is_active = true;

CREATE INDEX CONCURRENTLY idx_published_posts 
ON posts(published_at DESC) WHERE status = 'published';

-- Índices de texto completo
CREATE INDEX CONCURRENTLY idx_posts_fulltext 
ON posts USING gin(to_tsvector('portuguese', title || ' ' || content));

-- Índices para foreign keys
CREATE INDEX CONCURRENTLY idx_posts_author_id ON posts(author_id);
CREATE INDEX CONCURRENTLY idx_posts_category_id ON posts(category_id);
```

### **2. Views Otimizadas** 👁️

```sql
-- views/dashboard_stats.sql
-- View para estatísticas do dashboard

CREATE OR REPLACE VIEW dashboard_stats AS
SELECT 
    (SELECT COUNT(*) FROM users WHERE is_active = true) as active_users,
    (SELECT COUNT(*) FROM posts WHERE status = 'published') as published_posts,
    (SELECT COUNT(*) FROM posts WHERE created_at >= CURRENT_DATE) as posts_today,
    (SELECT COUNT(*) FROM users WHERE created_at >= CURRENT_DATE - INTERVAL '7 days') as new_users_week;

-- View materializada para dados pesados
CREATE MATERIALIZED VIEW user_post_stats AS
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(p.id) as total_posts,
    COUNT(CASE WHEN p.status = 'published' THEN 1 END) as published_posts,
    MAX(p.created_at) as last_post_date,
    AVG(CASE WHEN p.status = 'published' THEN p.views ELSE NULL END) as avg_views
FROM users u
LEFT JOIN posts p ON u.id = p.author_id
GROUP BY u.id, u.name, u.email;

-- Índice na view materializada
CREATE INDEX idx_user_post_stats_total_posts ON user_post_stats(total_posts DESC);

-- Refresh automático da view materializada
CREATE OR REPLACE FUNCTION refresh_user_post_stats()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY user_post_stats;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_refresh_user_post_stats
    AFTER INSERT OR UPDATE OR DELETE ON posts
    FOR EACH STATEMENT
    EXECUTE FUNCTION refresh_user_post_stats();
```

### **3. Stored Procedures** ⚙️

```sql
-- procedures/user_procedures.sql
-- Procedimentos para operações complexas de usuário

-- Função para criar usuário completo
CREATE OR REPLACE FUNCTION create_user_with_profile(
    p_email VARCHAR(255),
    p_password VARCHAR(255),
    p_name VARCHAR(255),
    p_role user_role DEFAULT 'user'
)
RETURNS TABLE(user_id INTEGER, success BOOLEAN, message TEXT) AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    -- Verificar se email já existe
    IF EXISTS (SELECT 1 FROM users WHERE email = p_email) THEN
        RETURN QUERY SELECT NULL::INTEGER, FALSE, 'Email already exists';
        RETURN;
    END IF;
    
    -- Inserir usuário
    INSERT INTO users (email, password_hash, name, role)
    VALUES (p_email, p_password, p_name, p_role)
    RETURNING id INTO v_user_id;
    
    -- Criar perfil padrão
    INSERT INTO user_profiles (user_id, bio, avatar_url)
    VALUES (v_user_id, '', NULL);
    
    -- Retornar sucesso
    RETURN QUERY SELECT v_user_id, TRUE, 'User created successfully';
    
EXCEPTION WHEN OTHERS THEN
    -- Em caso de erro, retornar erro
    RETURN QUERY SELECT NULL::INTEGER, FALSE, SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Função para estatísticas do usuário
CREATE OR REPLACE FUNCTION get_user_statistics(p_user_id INTEGER)
RETURNS JSON AS $$
DECLARE
    v_stats JSON;
BEGIN
    SELECT json_build_object(
        'total_posts', COUNT(*),
        'published_posts', COUNT(CASE WHEN status = 'published' THEN 1 END),
        'draft_posts', COUNT(CASE WHEN status = 'draft' THEN 1 END),
        'total_views', COALESCE(SUM(views), 0),
        'last_post_date', MAX(created_at)
    )
    INTO v_stats
    FROM posts
    WHERE author_id = p_user_id;
    
    RETURN v_stats;
END;
$$ LANGUAGE plpgsql;
```

## 🔄 Backup e Recuperação

### **1. Script de Backup** 💾

```bash
#!/bin/bash
# backups/backup_script.sh

set -e

# Configurações
BACKUP_DIR="/var/backups/database"
DB_NAME=${DB_NAME:-myapp}
DB_USER=${DB_USER:-postgres}
DB_HOST=${DB_HOST:-localhost}
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_backup_${DATE}.sql"
RETENTION_DAYS=30

# Criar diretório se não existir
mkdir -p "$BACKUP_DIR"

echo "🗄️ Starting database backup..."

# Backup completo
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
    --verbose \
    --clean \
    --if-exists \
    --create \
    --format=custom \
    --file="$BACKUP_FILE.custom"

# Backup em SQL texto
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
    --verbose \
    --clean \
    --if-exists \
    --create \
    --file="$BACKUP_FILE"

# Comprimir backup texto
gzip "$BACKUP_FILE"

# Backup apenas de dados (sem schema)
pg_dump -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" \
    --data-only \
    --verbose \
    --file="$BACKUP_DIR/${DB_NAME}_data_${DATE}.sql"

gzip "$BACKUP_DIR/${DB_NAME}_data_${DATE}.sql"

echo "✅ Backup completed: $BACKUP_FILE.gz"

# Limpeza de backups antigos
echo "🧹 Cleaning old backups (older than $RETENTION_DAYS days)..."
find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "${DB_NAME}_data_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "${DB_NAME}_backup_*.sql.custom" -mtime +$RETENTION_DAYS -delete

echo "🎉 Backup process completed!"
```

### **2. Script de Restauração** 🔄

```bash
#!/bin/bash
# backups/restore_script.sh

set -e

BACKUP_FILE=$1
DB_NAME=${DB_NAME:-myapp}
DB_USER=${DB_USER:-postgres}
DB_HOST=${DB_HOST:-localhost}

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ Usage: $0 <backup_file>"
    echo "Available backups:"
    ls -la /var/backups/database/${DB_NAME}_backup_*.sql.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will completely replace the database '$DB_NAME'"
echo "📁 Backup file: $BACKUP_FILE"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 1
fi

echo "🔄 Starting database restore..."

# Se for arquivo comprimido, descomprimir temporariamente
if [[ "$BACKUP_FILE" == *.gz ]]; then
    TEMP_FILE="/tmp/restore_temp.sql"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
elif [[ "$BACKUP_FILE" == *.custom ]]; then
    # Restaurar backup em formato custom
    pg_restore -h "$DB_HOST" -U "$DB_USER" \
        --clean \
        --if-exists \
        --create \
        --verbose \
        "$BACKUP_FILE"
    echo "✅ Database restored successfully!"
    exit 0
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Restaurar backup em SQL
psql -h "$DB_HOST" -U "$DB_USER" -f "$RESTORE_FILE"

# Limpar arquivo temporário
if [ "$RESTORE_FILE" = "/tmp/restore_temp.sql" ]; then
    rm "$TEMP_FILE"
fi

echo "✅ Database restored successfully!"
```

## 🐳 Containerização

### **1. Docker Compose** 🐋

```yaml
# docker-compose.db.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: myapp_postgres
    environment:
      POSTGRES_DB: ${DB_NAME:-myapp}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-password}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=C"
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./schemas:/docker-entrypoint-initdb.d/01-schemas
      - ./seeds:/docker-entrypoint-initdb.d/02-seeds
      - ./backups:/backups
    networks:
      - myapp_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres} -d ${DB_NAME:-myapp}"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: myapp_redis
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    networks:
      - myapp_network
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: myapp_pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "${PGADMIN_PORT:-8080}:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    networks:
      - myapp_network
    depends_on:
      - postgres

volumes:
  postgres_data:
  redis_data:
  pgadmin_data:

networks:
  myapp_network:
    driver: bridge
```

### **2. Initialization Scripts** 🚀

```bash
#!/bin/bash
# scripts/init_db.sh

set -e

echo "🚀 Initializing database..."

# Aguardar PostgreSQL estar pronto
until pg_isready -h localhost -p 5432 -U postgres; do
  echo "⏳ Waiting for PostgreSQL..."
  sleep 2
done

echo "📊 PostgreSQL is ready!"

# Executar migrations
./scripts/migrate.sh

# Executar seeds baseado no ambiente
ENVIRONMENT=${NODE_ENV:-development}
./scripts/seed.sh $ENVIRONMENT

echo "✅ Database initialization completed!"
```

## 🔐 Segurança e Auditoria

### **1. Triggers de Auditoria** 🕵️

```sql
-- triggers/audit_triggers.sql
-- Sistema de auditoria para mudanças críticas

-- Tabela de auditoria
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    record_id VARCHAR(255) NOT NULL,
    operation VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    user_id INTEGER,
    user_ip INET,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Função genérica de auditoria
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
DECLARE
    old_data JSONB;
    new_data JSONB;
BEGIN
    -- Preparar dados baseado na operação
    CASE TG_OP
        WHEN 'INSERT' THEN
            new_data = to_jsonb(NEW);
            INSERT INTO audit_log (table_name, record_id, operation, new_values)
            VALUES (TG_TABLE_NAME, NEW.id::TEXT, TG_OP, new_data);
            RETURN NEW;
            
        WHEN 'UPDATE' THEN
            old_data = to_jsonb(OLD);
            new_data = to_jsonb(NEW);
            INSERT INTO audit_log (table_name, record_id, operation, old_values, new_values)
            VALUES (TG_TABLE_NAME, NEW.id::TEXT, TG_OP, old_data, new_data);
            RETURN NEW;
            
        WHEN 'DELETE' THEN
            old_data = to_jsonb(OLD);
            INSERT INTO audit_log (table_name, record_id, operation, old_values)
            VALUES (TG_TABLE_NAME, OLD.id::TEXT, TG_OP, old_data);
            RETURN OLD;
    END CASE;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar auditoria a tabelas críticas
CREATE TRIGGER users_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER posts_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON posts
    FOR EACH ROW EXECUTE FUNCTION audit_trigger_function();
```

### **2. Row Level Security** 🔒

```sql
-- Habilitar RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Política: usuários só veem seus próprios posts em rascunho
CREATE POLICY posts_author_policy ON posts
    FOR ALL TO authenticated_users
    USING (author_id = current_user_id() OR status = 'published');

-- Política: usuários só editam seus próprios perfis
CREATE POLICY user_profiles_owner_policy ON user_profiles
    FOR ALL TO authenticated_users
    USING (user_id = current_user_id());

-- Função para obter usuário atual (implementar conforme autenticação)
CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER AS $$
BEGIN
    -- Implementar lógica para obter ID do usuário atual
    -- Pode vir de JWT, sessão, etc.
    RETURN COALESCE(current_setting('app.current_user_id', true)::INTEGER, 0);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## 🎓 Para Estudantes

### **Projetos por Nível**

**🟢 Iniciante**
- Blog simples (usuários, posts, comentários)
- Sistema de biblioteca (livros, empréstimos)
- To-do list multiusuário
- E-commerce básico

**🟡 Intermediário**
- Sistema de CRM
- Plataforma de cursos online
- Rede social básica
- Sistema de vendas

**🔴 Avançado**
- Banco digital
- Marketplace complexo
- Sistema ERP
- Plataforma de streaming

### **Skills Progressivas**
1. **SQL Básico** → CRUD, JOINs, agregações
2. **Modelagem** → ER, normalização, relacionamentos
3. **Otimização** → Índices, query optimization
4. **Migrations** → Versionamento de schema
5. **Backup/Recovery** → Continuidade de negócio
6. **Segurança** → Auditoria, RLS, encryption
7. **Escalabilidade** → Sharding, replicação
8. **NoSQL** → Diferentes paradigmas de dados

## 🔧 Ferramentas Recomendadas

### **Design e Modelagem**
- **dbdiagram.io** - Diagramas ER online
- **Lucidchart** - Diagramas profissionais
- **MySQL Workbench** - Design e administração
- **pgModeler** - Modelagem PostgreSQL

### **Administração**
- **pgAdmin** - Interface PostgreSQL
- **phpMyAdmin** - Interface MySQL
- **DBeaver** - Cliente universal
- **DataGrip** - IDE JetBrains

### **Monitoramento**
- **pg_stat_statements** - Análise de queries
- **pgBadger** - Análise de logs
- **Grafana** + **Prometheus** - Métricas
- **New Relic** - APM

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Sempre use migrations para mudanças
- Normalize adequadamente (3NF mínimo)
- Implemente auditoria em dados críticos
- Use constraints para integridade
- Monitore performance constantemente
- Faça backup regularmente
- Documente o schema

### **❌ Evite**
- Mudanças diretas em produção
- Dados sensíveis sem encryption
- Queries sem índices em produção
- Foreign keys sem índices
- Backup sem teste de restore
- Senhas em plain text
- Conexões sem SSL

### **🎯 Métricas de Qualidade**
- Tempo de backup < 30 min
- Query time < 100ms (90%ile)
- Zero violações de integridade
- Uptime > 99.9%
- Recovery time < 1 hora
- Schema documentado 100%
- Cobertura de índices > 95%

---

**Este README deve ser adaptado conforme o SGBD e arquitetura específicas do projeto!**

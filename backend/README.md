# Backend - Servidor e APIs

> 🔧 **Lógica de negócio, APIs e serviços do lado servidor**

## 📋 Visão Geral

O backend é o núcleo do sistema, responsável por processar dados, implementar regras de negócio, gerenciar autenticação, comunicar com o banco de dados e fornecer APIs para o frontend e outras aplicações.

## 🏗️ Estrutura Recomendada

```
backend/
├── 📁 src/                     # Código fonte principal
│   ├── 📁 controllers/         # Controladores (handlers de requisições)
│   ├── 📁 services/            # Lógica de negócio
│   ├── 📁 models/              # Modelos de dados (entidades)
│   ├── 📁 repositories/        # Acesso a dados (padrão Repository)
│   ├── 📁 middleware/          # Middlewares (auth, cors, logging)
│   ├── 📁 routes/              # Definição de rotas
│   ├── 📁 utils/               # Utilitários e helpers
│   ├── 📁 validators/          # Validadores de dados
│   ├── 📁 config/              # Configurações da aplicação
│   └── 📄 app.js               # Ponto de entrada da aplicação
├── 📁 tests/                   # Testes do backend
│   ├── 📁 unit/                # Testes unitários
│   ├── 📁 integration/         # Testes de integração
│   └── 📁 fixtures/            # Dados de teste
├── 📁 docs/                    # Documentação da API
│   ├── 📄 api.md               # Documentação da API
│   ├── 📄 swagger.yaml         # Especificação OpenAPI
│   └── 📄 postman.json         # Collection do Postman
├── 📄 package.json             # Dependências e scripts (Node.js)
├── 📄 requirements.txt         # Dependências (Python)
├── 📄 Dockerfile               # Container para produção
├── 📄 .env.example             # Exemplo de variáveis de ambiente
├── 📄 .gitignore               # Arquivos ignorados pelo Git
└── 📄 README.md                # Este arquivo
```

## 🛠️ Tecnologias Recomendadas

### **JavaScript/TypeScript**
- **Node.js** + Express.js/Fastify
- **TypeScript** para tipagem estática
- **Prisma/TypeORM** para ORM
- **Jest** para testes

### **Python**
- **Django** (framework completo)
- **FastAPI** (moderno, rápido)
- **Flask** (minimalista)
- **SQLAlchemy** para ORM
- **Pytest** para testes

### **Java**
- **Spring Boot** (framework robusto)
- **Maven/Gradle** para build
- **JPA/Hibernate** para ORM
- **JUnit** para testes

### **C#**
- **.NET Core** (multiplataforma)
- **Entity Framework** para ORM
- **xUnit** para testes

## 📦 Componentes Principais

### **1. Controllers** 🎮
- Recebem requisições HTTP
- Validam entrada
- Chamam services apropriados
- Retornam respostas formatadas

**Boas Práticas:**
- Controllers finos (apenas orquestração)
- Validação de entrada
- Tratamento de erros consistente
- Documentação com exemplos

### **2. Services** ⚙️
- Implementam regras de negócio
- Orquestram operações complexas
- São independentes de protocolo (HTTP, etc.)
- Reutilizáveis por diferentes controllers

**Boas Práticas:**
- Uma responsabilidade por service
- Injeção de dependência
- Testes unitários extensivos
- Transações quando necessário

### **3. Models/Entities** 📊
- Representam dados do domínio
- Definem relacionamentos
- Incluem validações básicas
- Mapeiam para o banco de dados

**Boas Práticas:**
- Modelos ricos em comportamento
- Validações no modelo
- Relacionamentos bem definidos
- Migrations versionadas

### **4. Repositories** 🗄️
- Abstraem acesso a dados
- Implementam operações CRUD
- Encapsulam queries complexas
- Facilita mudança de banco

**Boas Práticas:**
- Interface + implementação
- Queries otimizadas
- Paginação por padrão
- Tratamento de erros de DB

### **5. Middleware** 🔀
- Interceptam requisições
- Implementam cross-cutting concerns
- Exemplos: auth, logs, CORS, rate limiting

**Boas Práticas:**
- Ordem de execução bem definida
- Configuração flexível
- Performance otimizada
- Logs detalhados

## 🔐 Autenticação e Autorização

### **Estratégias Recomendadas**

**JWT (JSON Web Tokens)**
```javascript
// Middleware de autenticação
const authenticateToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  // Validar e decodificar token
};
```

**Roles e Permissions**
```javascript
// Middleware de autorização
const requireRole = (roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  next();
};
```

### **Boas Práticas de Segurança**
- ✅ Sempre use HTTPS em produção
- ✅ Hash de senhas com bcrypt/scrypt
- ✅ Rate limiting nas APIs
- ✅ Validação e sanitização de entrada
- ✅ Headers de segurança (CORS, CSP)
- ✅ Logs de auditoria
- ✅ Rotação de tokens
- ✅ Princípio do menor privilégio

## 📡 Design de APIs

### **RESTful APIs**

```http
GET    /api/users          # Listar usuários
GET    /api/users/:id      # Buscar usuário específico
POST   /api/users          # Criar usuário
PUT    /api/users/:id      # Atualizar usuário completo
PATCH  /api/users/:id      # Atualizar usuário parcial
DELETE /api/users/:id      # Deletar usuário
```

### **Padrões de Resposta**

**Sucesso (200-299)**
```json
{
  "data": { /* dados */ },
  "message": "Operação realizada com sucesso",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Erro (400-599)**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dados inválidos",
    "details": [
      {
        "field": "email",
        "message": "Email é obrigatório"
      }
    ]
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### **Versionamento de API**
- URL: `/api/v1/users` vs `/api/v2/users`
- Header: `Accept: application/vnd.api+json;version=1`
- Query param: `/api/users?version=1`

## 🧪 Estratégias de Teste

### **Pirâmide de Testes**

**Testes Unitários (70%)**
- Testam funções isoladas
- Mocks para dependências
- Execução rápida
- Alta cobertura

```javascript
// Exemplo de teste unitário
describe('UserService', () => {
  it('should create user with valid data', async () => {
    const userData = { name: 'João', email: 'joao@email.com' };
    const mockRepo = { create: jest.fn().mockResolvedValue(userData) };
    const userService = new UserService(mockRepo);
    
    const result = await userService.createUser(userData);
    
    expect(result).toEqual(userData);
    expect(mockRepo.create).toHaveBeenCalledWith(userData);
  });
});
```

**Testes de Integração (20%)**
- Testam componentes integrados
- Banco de dados de teste
- APIs reais

```javascript
// Exemplo de teste de integração
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const userData = { name: 'Maria', email: 'maria@email.com' };
    
    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);
    
    expect(response.body.data.name).toBe('Maria');
  });
});
```

**Testes E2E (10%)**
- Testam fluxos completos
- Simulam usuário real
- Ambiente similar à produção

## 🚀 Performance e Otimização

### **Estratégias de Cache**

**Redis para Cache**
```javascript
const redis = require('redis');
const client = redis.createClient();

// Cache de consultas frequentes
app.get('/api/users/:id', async (req, res) => {
  const cached = await client.get(`user:${req.params.id}`);
  if (cached) {
    return res.json(JSON.parse(cached));
  }
  
  const user = await userService.findById(req.params.id);
  await client.setex(`user:${req.params.id}`, 300, JSON.stringify(user));
  res.json(user);
});
```

**Database Optimization**
- Índices estratégicos
- Queries otimizadas
- Connection pooling
- Paginação eficiente

### **Monitoramento**
- Logs estruturados (Winston, Logrus)
- Métricas de performance (Prometheus)
- APM (Application Performance Monitoring)
- Health checks

## 🔧 Configuração de Ambiente

### **Variáveis de Ambiente**

```bash
# .env.example
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
JWT_SECRET=seu-jwt-secret-aqui
REDIS_URL=redis://localhost:6379
LOG_LEVEL=info
```

### **Scripts de Desenvolvimento**

```json
{
  "scripts": {
    "dev": "nodemon src/app.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/",
    "build": "tsc",
    "start": "node dist/app.js",
    "migrate": "prisma migrate dev",
    "seed": "node scripts/seed.js"
  }
}
```

## 📚 Padrões e Arquiteturas

### **Clean Architecture**
```
Controllers -> Services -> Repositories -> Database
     ↑              ↑            ↑
  Presentation   Business     Data
    Layer        Layer       Layer
```

### **SOLID Principles**
- **S**ingle Responsibility
- **O**pen/Closed
- **L**iskov Substitution
- **I**nterface Segregation
- **D**ependency Inversion

### **Design Patterns Úteis**
- **Repository Pattern**: Abstração de dados
- **Service Layer**: Lógica de negócio
- **Factory Pattern**: Criação de objetos
- **Observer Pattern**: Eventos e notificações
- **Strategy Pattern**: Algoritmos intercambiáveis

## 🐳 Containerização

### **Dockerfile Exemplo**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 3000

USER node

CMD ["npm", "start"]
```

### **Docker Compose para Desenvolvimento**

```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - ./src:/app/src
    depends_on:
      - database
      - redis

  database:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password

  redis:
    image: redis:7-alpine
```

## 📖 Documentação da API

### **OpenAPI/Swagger**
- Especificação automática da API
- Interface interativa para testes
- Geração de SDKs
- Documentação sempre atualizada

### **Postman Collections**
- Coleções de requisições
- Ambientes configurados
- Testes automatizados
- Compartilhamento com equipe

## 🔍 Debugging e Logs

### **Logs Estruturados**
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});
```

### **Error Handling**
```javascript
// Middleware de tratamento de erros
app.use((err, req, res, next) => {
  logger.error({
    message: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method,
    ip: req.ip
  });
  
  res.status(500).json({
    error: {
      message: 'Internal Server Error',
      code: 'INTERNAL_ERROR'
    }
  });
});
```

## 🎓 Para Estudantes

### **Projetos por Nível**

**🟢 Iniciante**
- API REST simples (CRUD)
- Autenticação básica
- Banco de dados SQLite
- Testes unitários básicos

**🟡 Intermediário**
- Autenticação JWT
- Validações robustas
- PostgreSQL + migrations
- Testes de integração

**🔴 Avançado**
- Microserviços
- Cache distribuído
- Message queues
- Observabilidade completa

### **Exercícios Recomendados**
1. **Blog API**: CRUD de posts e comentários
2. **E-commerce API**: Produtos, carrinho, pedidos
3. **Chat API**: Mensagens em tempo real
4. **Task Manager**: Projetos e tarefas
5. **Social Network**: Posts, follows, feed

## 🔧 Ferramentas Recomendadas

### **Desenvolvimento**
- **IDE**: VS Code, IntelliJ, PyCharm
- **API Testing**: Postman, Insomnia
- **Database**: DBeaver, pgAdmin
- **Debugging**: Chrome DevTools, debuggers específicos

### **Produção**
- **Monitoring**: New Relic, Datadog
- **Logs**: ELK Stack, Fluentd
- **Deployment**: PM2, Docker, Kubernetes
- **CI/CD**: GitHub Actions, Jenkins

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Sempre valide entrada do usuário
- Use transactions para operações críticas
- Implemente rate limiting
- Mantenha logs detalhados
- Teste edge cases
- Documente decisões arquiteturais

### **❌ Evite**
- Senhas em plain text
- SQL injection vulnerabilities
- Logs com dados sensíveis
- Dependências desatualizadas
- Endpoints sem autenticação
- Queries N+1

### **🎯 Métricas de Qualidade**
- Cobertura de testes > 80%
- Tempo de resposta < 200ms
- Zero vulnerabilidades críticas
- Documentação atualizada
- Código limpo e legível

---

**Este README deve ser adaptado conforme as tecnologias específicas escolhidas para o projeto!**

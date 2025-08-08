# DevOps e Infraestrutura

> 🚀 **Automação, deployment e gerenciamento de infraestrutura**

## 📋 Visão Geral

O diretório DevOps contém toda a infraestrutura como código, pipelines de CI/CD, configurações de deployment, monitoramento e automação necessária para operar a aplicação de forma confiável e escalável em produção.

## 🏗️ Estrutura Recomendada

```
devops/
├── 📁 ci-cd/                  # Pipelines de CI/CD
│   ├── 📁 github-actions/     # GitHub Actions workflows
│   ├── 📁 gitlab-ci/          # GitLab CI pipelines
│   ├── 📁 jenkins/            # Jenkins pipelines
│   ├── 📁 azure-devops/       # Azure DevOps pipelines
│   └── 📁 workflows/          # Workflows customizados
├── 📁 infrastructure/         # Infraestrutura como código
│   ├── 📁 terraform/          # Terraform configurations
│   ├── 📁 cloudformation/     # AWS CloudFormation
│   ├── 📁 pulumi/             # Pulumi configurations
│   ├── 📁 ansible/            # Ansible playbooks
│   └── 📁 helm/               # Helm charts
├── 📁 docker/                 # Containerização
│   ├── 📄 Dockerfile          # Dockerfile principal
│   ├── 📄 Dockerfile.dev      # Dockerfile desenvolvimento
│   ├── 📄 Dockerfile.prod     # Dockerfile produção
│   ├── 📄 docker-compose.yml  # Compose local
│   ├── 📄 docker-compose.dev.yml
│   ├── 📄 docker-compose.prod.yml
│   └── 📁 configs/            # Configurações Docker
├── 📁 kubernetes/             # Kubernetes manifests
│   ├── 📁 base/               # Configurações base
│   ├── 📁 overlays/           # Kustomize overlays
│   │   ├── 📁 development/    # Configs dev
│   │   ├── 📁 staging/        # Configs staging
│   │   └── 📁 production/     # Configs prod
│   ├── 📁 charts/             # Helm charts
│   └── 📁 operators/          # Custom operators
├── 📁 monitoring/             # Observabilidade
│   ├── 📁 prometheus/         # Prometheus configs
│   ├── 📁 grafana/            # Grafana dashboards
│   ├── 📁 elasticsearch/      # ELK stack
│   ├── 📁 jaeger/             # Distributed tracing
│   └── 📁 alerting/           # Regras de alerta
├── 📁 logging/                # Sistema de logs
│   ├── 📁 fluentd/            # Fluentd configs
│   ├── 📁 logstash/           # Logstash configs
│   ├── 📁 vector/             # Vector configs
│   └── 📁 configs/            # Log configurations
├── 📁 security/               # Segurança e compliance
│   ├── 📁 policies/           # Políticas de segurança
│   ├── 📁 rbac/               # Role-based access control
│   ├── 📁 network-policies/   # Network policies K8s
│   ├── 📁 secrets/            # Gestão de secrets
│   └── 📁 scanning/           # Security scanning configs
├── 📁 backup/                 # Backup e disaster recovery
│   ├── 📁 scripts/            # Scripts de backup
│   ├── 📁 policies/           # Políticas de retenção
│   └── 📁 recovery/           # Procedures de recovery
├── 📁 scripts/                # Scripts de automação
│   ├── 📄 deploy.sh           # Script de deploy
│   ├── 📄 rollback.sh         # Script de rollback
│   ├── 📄 health-check.sh     # Health check
│   ├── 📄 database-migrate.sh # Migração de banco
│   └── 📄 cleanup.sh          # Limpeza de recursos
├── 📁 environments/           # Configurações por ambiente
│   ├── 📁 development/        # Configs desenvolvimento
│   ├── 📁 staging/            # Configs staging
│   ├── 📁 production/         # Configs produção
│   └── 📁 local/              # Configs local
├── 📄 README.md               # Este arquivo
├── 📄 DEPLOYMENT.md           # Guia de deployment
└── 📄 RUNBOOK.md              # Runbook operacional
```

## 🔄 CI/CD Pipeline

### **1. GitHub Actions** 🔧

**Workflow Principal**:
```yaml
# .github/workflows/main.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: 🧪 Tests
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      
      - name: 📦 Install dependencies
        run: npm ci
      
      - name: 🔍 Lint code
        run: npm run lint
      
      - name: 🧪 Run unit tests
        run: npm run test:unit
      
      - name: 🔗 Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db
      
      - name: 📊 Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  security:
    name: 🔒 Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: 🔍 Run security scan
        uses: github/super-linter@v4
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 🚨 Dependency vulnerability scan
        run: npm audit --audit-level moderate
      
      - name: 🔐 Secret scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: main
          head: HEAD

  build:
    name: 🏗️ Build
    runs-on: ubuntu-latest
    needs: [test, security]
    
    outputs:
      image: ${{ steps.image.outputs.image }}
      digest: ${{ steps.build.outputs.digest }}
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: 🔑 Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 📝 Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}
      
      - name: 🏗️ Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./devops/docker/Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: 📤 Output image
        id: image
        run: |
          echo "image=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}" >> $GITHUB_OUTPUT

  deploy-staging:
    name: 🚀 Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: ⚙️ Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.28.0'
      
      - name: 🔑 Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-west-2
      
      - name: 📝 Update kubeconfig
        run: |
          aws eks update-kubeconfig --name staging-cluster --region us-west-2
      
      - name: 🚀 Deploy to staging
        run: |
          cd devops/kubernetes/overlays/staging
          kustomize edit set image app=${{ needs.build.outputs.image }}
          kubectl apply -k .
      
      - name: ⏳ Wait for rollout
        run: |
          kubectl rollout status deployment/app -n staging --timeout=300s
      
      - name: 🏥 Health check
        run: |
          kubectl get pods -n staging
          ./devops/scripts/health-check.sh staging

  deploy-production:
    name: 🏭 Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: 🚀 Deploy to production
        run: |
          echo "Deploying to production..."
          # Similar steps as staging but for production

  e2e-tests:
    name: 🌐 E2E Tests
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/develop'
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
      
      - name: 🟢 Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: 🎭 Install Playwright
        run: |
          npm ci
          npx playwright install --with-deps
      
      - name: 🧪 Run E2E tests
        run: npm run test:e2e
        env:
          BASE_URL: https://staging.myapp.com
      
      - name: 📸 Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

**Workflow de Release**:
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    name: 🏷️ Create Release
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 📝 Generate changelog
        id: changelog
        uses: conventional-changelog/conventional-changelog-action@v3
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: 🏷️ Create release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref_name }}
          release_name: Release ${{ github.ref_name }}
          body: ${{ steps.changelog.outputs.changelog }}
          draft: false
          prerelease: false
```

### **2. GitLab CI** 🦊

```yaml
# .gitlab-ci.yml
stages:
  - test
  - security
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

services:
  - docker:20.10.16-dind
  - postgres:14

before_script:
  - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY

test:unit:
  stage: test
  image: node:20
  variables:
    POSTGRES_DB: test_db
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    DATABASE_URL: "postgres://postgres:postgres@postgres:5432/test_db"
  
  script:
    - npm ci
    - npm run lint
    - npm run test:unit
    - npm run test:integration
  
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    paths:
      - coverage/

security:sast:
  stage: security
  include:
    - template: Security/SAST.gitlab-ci.yml

security:dependency:
  stage: security
  include:
    - template: Security/Dependency-Scanning.gitlab-ci.yml

security:container:
  stage: security
  include:
    - template: Security/Container-Scanning.gitlab-ci.yml

build:docker:
  stage: build
  image: docker:20.10.16
  
  script:
    - docker build -f devops/docker/Dockerfile -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  
  only:
    - main
    - develop

deploy:staging:
  stage: deploy
  image: alpine/k8s:1.28.0
  
  script:
    - kubectl config use-context $KUBE_CONTEXT
    - cd devops/kubernetes/overlays/staging
    - kustomize edit set image app=$DOCKER_IMAGE
    - kubectl apply -k .
    - kubectl rollout status deployment/app -n staging
  
  environment:
    name: staging
    url: https://staging.myapp.com
  
  only:
    - develop

deploy:production:
  stage: deploy
  image: alpine/k8s:1.28.0
  
  script:
    - kubectl config use-context $KUBE_CONTEXT
    - cd devops/kubernetes/overlays/production
    - kustomize edit set image app=$DOCKER_IMAGE
    - kubectl apply -k .
    - kubectl rollout status deployment/app -n production
  
  environment:
    name: production
    url: https://myapp.com
  
  when: manual
  only:
    - main
```

## 🐳 Containerização

### **1. Dockerfile Multi-stage** 📦

```dockerfile
# devops/docker/Dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

# Create app user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Security: Run as non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
```

**Dockerfile para Desenvolvimento**:
```dockerfile
# devops/docker/Dockerfile.dev
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose port and start in development mode
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

### **2. Docker Compose** 🔧

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: devops/docker/Dockerfile.dev
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://postgres:password@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: app_dev
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./devops/nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    driver: bridge
```

**Compose para Produção**:
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: myapp:latest
    restart: unless-stopped
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`myapp.com`)"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    volumes:
      - ./devops/nginx/nginx.prod.conf:/etc/nginx/nginx.conf
      - static_files:/app/static
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nginx.rule=Host(`static.myapp.com`)"
```

## ☸️ Kubernetes

### **1. Deployment Manifests** 📋

```yaml
# devops/kubernetes/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
    tier: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      tier: backend
  template:
    metadata:
      labels:
        app: myapp
        tier: backend
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        securityContext:
          allowPrivilegeEscalation: false
          runAsNonRoot: true
          runAsUser: 1001
          capabilities:
            drop:
            - ALL
      securityContext:
        fsGroup: 1001
```

**Service**:
```yaml
# devops/kubernetes/base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
  labels:
    app: myapp
spec:
  selector:
    app: myapp
    tier: backend
  ports:
  - name: http
    port: 80
    targetPort: 3000
    protocol: TCP
  type: ClusterIP
```

**Ingress**:
```yaml
# devops/kubernetes/base/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
  - hosts:
    - myapp.com
    secretName: app-tls
  rules:
  - host: myapp.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app-service
            port:
              number: 80
```

### **2. Kustomization** 🎨

```yaml
# devops/kubernetes/base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml
- ingress.yaml
- configmap.yaml
- secret.yaml

commonLabels:
  app: myapp
  version: v1.0.0

images:
- name: myapp
  newTag: latest
```

**Staging Overlay**:
```yaml
# devops/kubernetes/overlays/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: staging

resources:
- ../../base

patchesStrategicMerge:
- replica-count.yaml
- resources.yaml

configMapGenerator:
- name: app-config
  literals:
  - REDIS_URL=redis://redis.staging.svc.cluster.local:6379
  - LOG_LEVEL=debug

secretGenerator:
- name: app-secrets
  literals:
  - DATABASE_URL=postgres://user:pass@db.staging.svc.cluster.local:5432/app_staging

images:
- name: myapp
  newTag: staging-latest
```

**Production Overlay**:
```yaml
# devops/kubernetes/overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base

patchesStrategicMerge:
- replica-count.yaml
- resources.yaml
- hpa.yaml

configMapGenerator:
- name: app-config
  literals:
  - REDIS_URL=redis://redis.production.svc.cluster.local:6379
  - LOG_LEVEL=info

images:
- name: myapp
  newTag: v1.0.0
```

### **3. Helm Charts** ⛵

```yaml
# devops/kubernetes/charts/myapp/Chart.yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 0.1.0
appVersion: "1.0.0"

dependencies:
- name: postgresql
  version: 12.x.x
  repository: https://charts.bitnami.com/bitnami
  condition: postgresql.enabled
- name: redis
  version: 17.x.x
  repository: https://charts.bitnami.com/bitnami
  condition: redis.enabled
```

**Values**:
```yaml
# devops/kubernetes/charts/myapp/values.yaml
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "latest"

service:
  type: ClusterIP
  port: 80
  targetPort: 3000

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - myapp.com

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

postgresql:
  enabled: true
  auth:
    postgresPassword: "postgres"
    database: "myapp"

redis:
  enabled: true
  auth:
    enabled: false
```

## 🏗️ Infraestrutura como Código

### **1. Terraform** 🏭

```hcl
# devops/infrastructure/terraform/main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = "myapp"
      ManagedBy   = "terraform"
    }
  }
}

# VPC
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "${var.environment}-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  
  tags = {
    Terraform = "true"
    Environment = var.environment
  }
}

# EKS Cluster
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "${var.environment}-cluster"
  cluster_version = "1.28"
  
  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true
  
  node_groups = {
    main = {
      desired_capacity = 3
      max_capacity     = 10
      min_capacity     = 3
      
      instance_types = ["t3.medium"]
      
      k8s_labels = {
        Environment = var.environment
        Application = "myapp"
      }
    }
  }
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier = "${var.environment}-database"
  
  engine         = "postgres"
  engine_version = "14.9"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp2"
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Sun:04:00-Sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {
    Name = "${var.environment}-database"
  }
}

# ElastiCache Redis
resource "aws_elasticache_subnet_group" "main" {
  name       = "${var.environment}-cache-subnet"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_cluster" "main" {
  cluster_id           = "${var.environment}-cache"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.main.name
  security_group_ids   = [aws_security_group.redis.id]
}
```

**Variables**:
```hcl
# devops/infrastructure/terraform/variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "development"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "myapp"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### **2. Ansible Playbooks** 📚

```yaml
# devops/infrastructure/ansible/site.yml
---
- name: Configure web servers
  hosts: webservers
  become: yes
  vars:
    app_user: myapp
    app_dir: /opt/myapp
    node_version: "20"
  
  tasks:
    - name: Update system packages
      apt:
        update_cache: yes
        upgrade: dist
    
    - name: Install required packages
      apt:
        name:
          - curl
          - git
          - nginx
          - nodejs
          - npm
        state: present
    
    - name: Create application user
      user:
        name: "{{ app_user }}"
        system: yes
        shell: /bin/bash
        home: "{{ app_dir }}"
        create_home: yes
    
    - name: Clone application repository
      git:
        repo: https://github.com/mycompany/myapp.git
        dest: "{{ app_dir }}/app"
        version: main
      become_user: "{{ app_user }}"
    
    - name: Install application dependencies
      npm:
        path: "{{ app_dir }}/app"
        production: yes
      become_user: "{{ app_user }}"
    
    - name: Build application
      command: npm run build
      args:
        chdir: "{{ app_dir }}/app"
      become_user: "{{ app_user }}"
    
    - name: Configure Nginx
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/myapp
      notify: restart nginx
    
    - name: Enable Nginx site
      file:
        src: /etc/nginx/sites-available/myapp
        dest: /etc/nginx/sites-enabled/myapp
        state: link
      notify: restart nginx
    
    - name: Configure systemd service
      template:
        src: myapp.service.j2
        dest: /etc/systemd/system/myapp.service
      notify:
        - reload systemd
        - restart myapp
    
    - name: Start and enable application service
      systemd:
        name: myapp
        state: started
        enabled: yes

  handlers:
    - name: restart nginx
      systemd:
        name: nginx
        state: restarted
    
    - name: reload systemd
      systemd:
        daemon_reload: yes
    
    - name: restart myapp
      systemd:
        name: myapp
        state: restarted
```

## 📊 Monitoramento e Observabilidade

### **1. Prometheus + Grafana** 📈

**Prometheus Config**:
```yaml
# devops/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'myapp'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: myapp
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

  - job_name: 'node-exporter'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - source_labels: [__address__]
        regex: '(.*):10250'
        replacement: '${1}:9100'
        target_label: __address__

  - job_name: 'kube-state-metrics'
    static_configs:
      - targets: ['kube-state-metrics:8080']
```

**Alert Rules**:
```yaml
# devops/monitoring/prometheus/alert_rules.yml
groups:
  - name: myapp.rules
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod is crash looping"
          description: "Pod {{ $labels.pod }} is restarting frequently"

      - alert: NodeDown
        expr: up{job="node-exporter"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Node is down"
          description: "Node {{ $labels.instance }} is down"
```

**Grafana Dashboard**:
```json
{
  "dashboard": {
    "title": "MyApp Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{ method }} {{ status }}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      }
    ]
  }
}
```

### **2. ELK Stack (Logging)** 📝

**Elasticsearch Config**:
```yaml
# devops/logging/elasticsearch/elasticsearch.yml
cluster.name: "myapp-logs"
node.name: "elasticsearch-1"
path.data: /usr/share/elasticsearch/data
path.logs: /usr/share/elasticsearch/logs
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
xpack.security.enabled: false
```

**Logstash Config**:
```ruby
# devops/logging/logstash/pipeline/logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][app] == "myapp" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \[%{LOGLEVEL:level}\] %{GREEDYDATA:message}" }
    }
    
    date {
      match => [ "timestamp", "ISO8601" ]
    }
    
    if [level] == "ERROR" {
      mutate {
        add_tag => ["error"]
      }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "myapp-logs-%{+YYYY.MM.dd}"
  }
}
```

**Filebeat Config**:
```yaml
# devops/logging/filebeat/filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/myapp/*.log
  fields:
    app: myapp
  fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]

logging.level: info
```

## 🔒 Segurança

### **1. Network Policies** 🌐

```yaml
# devops/security/network-policies/deny-all.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

```yaml
# devops/security/network-policies/app-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: app-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 3000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

### **2. RBAC** 👥

```yaml
# devops/security/rbac/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-service-account
  namespace: production
```

```yaml
# devops/security/rbac/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: myapp-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "update", "patch"]
```

```yaml
# devops/security/rbac/role-binding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: myapp-role-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: myapp-service-account
  namespace: production
roleRef:
  kind: Role
  name: myapp-role
  apiGroup: rbac.authorization.k8s.io
```

## 📋 Scripts de Automação

### **1. Deploy Script** 🚀

```bash
#!/bin/bash
# devops/scripts/deploy.sh

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT="${1:-staging}"
IMAGE_TAG="${2:-latest}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    error "Invalid environment: $ENVIRONMENT. Must be development, staging, or production."
fi

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    command -v kubectl >/dev/null 2>&1 || error "kubectl is required but not installed."
    command -v kustomize >/dev/null 2>&1 || error "kustomize is required but not installed."
    command -v docker >/dev/null 2>&1 || error "docker is required but not installed."
    
    # Check kubectl context
    current_context=$(kubectl config current-context)
    if [[ "$current_context" != *"$ENVIRONMENT"* ]]; then
        warn "Current kubectl context ($current_context) doesn't seem to match environment ($ENVIRONMENT)"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deployment cancelled"
        fi
    fi
}

# Build and push Docker image
build_and_push() {
    log "Building and pushing Docker image..."
    
    local image_name="myapp:$IMAGE_TAG"
    local registry_image="ghcr.io/mycompany/$image_name"
    
    docker build -f "$PROJECT_ROOT/devops/docker/Dockerfile" -t "$image_name" "$PROJECT_ROOT"
    docker tag "$image_name" "$registry_image"
    docker push "$registry_image"
    
    log "Image pushed: $registry_image"
}

# Run database migrations
run_migrations() {
    log "Running database migrations..."
    
    kubectl run migration-job-$(date +%s) \
        --image=ghcr.io/mycompany/myapp:$IMAGE_TAG \
        --restart=Never \
        --command -- npm run migrate \
        --namespace="$ENVIRONMENT"
    
    # Wait for migration to complete
    kubectl wait --for=condition=complete job/migration-job-* --timeout=300s --namespace="$ENVIRONMENT"
    
    log "Database migrations completed"
}

# Deploy application
deploy_app() {
    log "Deploying application to $ENVIRONMENT..."
    
    cd "$PROJECT_ROOT/devops/kubernetes/overlays/$ENVIRONMENT"
    
    # Update image tag
    kustomize edit set image myapp=ghcr.io/mycompany/myapp:$IMAGE_TAG
    
    # Apply manifests
    kubectl apply -k . --namespace="$ENVIRONMENT"
    
    # Wait for rollout to complete
    kubectl rollout status deployment/app --namespace="$ENVIRONMENT" --timeout=300s
    
    log "Deployment completed"
}

# Run health checks
health_check() {
    log "Running health checks..."
    
    local service_url
    if [[ "$ENVIRONMENT" == "production" ]]; then
        service_url="https://myapp.com"
    else
        service_url="https://$ENVIRONMENT.myapp.com"
    fi
    
    # Wait for service to be ready
    for i in {1..30}; do
        if curl -f -s "$service_url/health" >/dev/null; then
            log "Health check passed"
            return 0
        fi
        log "Waiting for service to be ready... ($i/30)"
        sleep 10
    done
    
    error "Health check failed after 5 minutes"
}

# Cleanup old resources
cleanup() {
    log "Cleaning up old resources..."
    
    # Remove old ReplicaSets
    kubectl delete replicaset --namespace="$ENVIRONMENT" \
        $(kubectl get replicaset --namespace="$ENVIRONMENT" -o jsonpath='{.items[?(@.spec.replicas==0)].metadata.name}') \
        2>/dev/null || true
    
    log "Cleanup completed"
}

# Main deployment flow
main() {
    log "Starting deployment to $ENVIRONMENT with image tag $IMAGE_TAG"
    
    check_prerequisites
    
    if [[ "$ENVIRONMENT" == "production" ]]; then
        read -p "Are you sure you want to deploy to PRODUCTION? (yes/NO): " -r
        if [[ ! $REPLY == "yes" ]]; then
            error "Production deployment cancelled"
        fi
    fi
    
    build_and_push
    run_migrations
    deploy_app
    health_check
    cleanup
    
    log "🎉 Deployment to $ENVIRONMENT completed successfully!"
    log "Application is available at: https://${ENVIRONMENT}.myapp.com"
}

# Run main function
main "$@"
```

### **2. Rollback Script** ⏪

```bash
#!/bin/bash
# devops/scripts/rollback.sh

set -euo pipefail

ENVIRONMENT="${1:-staging}"
REVISION="${2:-previous}"

log() {
    echo -e "\033[0;32m[$(date +'%Y-%m-%d %H:%M:%S')] $1\033[0m"
}

error() {
    echo -e "\033[0;31m[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1\033[0m"
    exit 1
}

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(development|staging|production)$ ]]; then
    error "Invalid environment: $ENVIRONMENT"
fi

# Get current deployment
current_revision=$(kubectl rollout history deployment/app --namespace="$ENVIRONMENT" | tail -n 1 | awk '{print $1}')
log "Current revision: $current_revision"

# Determine target revision
if [[ "$REVISION" == "previous" ]]; then
    target_revision=$((current_revision - 1))
else
    target_revision="$REVISION"
fi

# Confirm rollback
if [[ "$ENVIRONMENT" == "production" ]]; then
    read -p "Are you sure you want to rollback PRODUCTION to revision $target_revision? (yes/NO): " -r
    if [[ ! $REPLY == "yes" ]]; then
        error "Rollback cancelled"
    fi
fi

# Perform rollback
log "Rolling back to revision $target_revision..."
kubectl rollout undo deployment/app --to-revision="$target_revision" --namespace="$ENVIRONMENT"

# Wait for rollback to complete
kubectl rollout status deployment/app --namespace="$ENVIRONMENT" --timeout=300s

log "🔄 Rollback completed successfully!"
```

## 🎓 Para Estudantes

### **Projetos por Nível** 📚

**🟢 Iniciante**
- Containerizar aplicação simples
- Configurar Docker Compose
- Deploy básico com GitHub Actions
- Monitoramento com logs simples

**🟡 Intermediário**
- Kubernetes básico (pods, services, deployments)
- CI/CD com múltiplos ambientes
- Monitoramento com Prometheus
- Infraestrutura como código (Terraform)

**🔴 Avançado**
- Cluster Kubernetes completo
- Observabilidade full-stack
- Security scanning e compliance
- Disaster recovery e backup

### **Skills Essenciais** 🎯

1. **Containerização** → Docker, Docker Compose
2. **Orquestração** → Kubernetes, Helm
3. **CI/CD** → GitHub Actions, GitLab CI
4. **Infrastructure as Code** → Terraform, Ansible
5. **Monitoramento** → Prometheus, Grafana, ELK
6. **Cloud Platforms** → AWS, GCP, Azure
7. **Security** → RBAC, Network Policies, Scanning

---

**DevOps é a ponte entre desenvolvimento e operações, automatizando e otimizando todo o ciclo de vida do software!**

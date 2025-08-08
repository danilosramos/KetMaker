# Testes e Qualidade de Software

> 🧪 **Framework completo de testes e garantia de qualidade**

## 📋 Visão Geral

O diretório de testes contém toda a estratégia, ferramentas e implementações para garantir a qualidade do software através de testes automatizados, manuais e de qualidade de código. Este é um componente essencial para entregar software confiável e maintível.

## 🏗️ Estrutura Recomendada

```
tests/
├── 📁 unit/                    # Testes unitários
│   ├── 📁 backend/             # Testes do backend
│   │   ├── 📁 controllers/     # Testes de controllers
│   │   ├── 📁 services/        # Testes de services
│   │   ├── 📁 models/          # Testes de models
│   │   └── 📁 utils/           # Testes de utilitários
│   ├── 📁 frontend/            # Testes do frontend
│   │   ├── 📁 components/      # Testes de componentes
│   │   ├── 📁 hooks/           # Testes de hooks
│   │   ├── 📁 services/        # Testes de services
│   │   └── 📁 utils/           # Testes de utilitários
│   └── 📁 mobile/              # Testes mobile
├── 📁 integration/             # Testes de integração
│   ├── 📁 api/                 # Testes de API
│   ├── 📁 database/            # Testes de banco
│   ├── 📁 services/            # Integração entre serviços
│   └── 📁 external/            # APIs externas
├── 📁 e2e/                     # Testes end-to-end
│   ├── 📁 web/                 # E2E web
│   ├── 📁 mobile/              # E2E mobile
│   ├── 📁 scenarios/           # Cenários de teste
│   └── 📁 fixtures/            # Dados de teste
├── 📁 performance/             # Testes de performance
│   ├── 📁 load/                # Testes de carga
│   ├── 📁 stress/              # Testes de estresse
│   ├── 📁 volume/              # Testes de volume
│   └── 📁 reports/             # Relatórios
├── 📁 security/                # Testes de segurança
│   ├── 📁 authentication/      # Testes de autenticação
│   ├── 📁 authorization/       # Testes de autorização
│   ├── 📁 vulnerability/       # Testes de vulnerabilidade
│   └── 📁 penetration/         # Testes de penetração
├── 📁 accessibility/           # Testes de acessibilidade
│   ├── 📁 automated/           # Testes automatizados
│   ├── 📁 manual/              # Testes manuais
│   └── 📁 reports/             # Relatórios de acessibilidade
├── 📁 visual/                  # Testes visuais
│   ├── 📁 regression/          # Regressão visual
│   ├── 📁 snapshots/           # Snapshots
│   └── 📁 baselines/           # Imagens baseline
├── 📁 fixtures/                # Dados de teste
│   ├── 📁 database/            # Seeds de teste
│   ├── 📁 files/               # Arquivos de teste
│   ├── 📁 mocks/               # Mocks e stubs
│   └── 📁 factories/           # Factories de dados
├── 📁 utils/                   # Utilitários de teste
│   ├── 📄 test-helpers.js      # Helpers gerais
│   ├── 📄 mock-factory.js      # Factory de mocks
│   ├── 📄 database-helper.js   # Helper de banco
│   └── 📄 setup.js             # Setup global
├── 📁 reports/                 # Relatórios de teste
│   ├── 📁 coverage/            # Cobertura de código
│   ├── 📁 junit/               # Relatórios JUnit
│   ├── 📁 html/                # Relatórios HTML
│   └── 📁 badges/              # Badges de qualidade
├── 📁 config/                  # Configurações de teste
│   ├── 📄 jest.config.js       # Config Jest
│   ├── 📄 cypress.config.js    # Config Cypress
│   ├── 📄 playwright.config.js # Config Playwright
│   └── 📄 vitest.config.js     # Config Vitest
├── 📄 README.md                # Este arquivo
├── 📄 test-strategy.md         # Estratégia de testes
└── 📄 quality-gates.md         # Portões de qualidade
```

## 🧪 Tipos de Teste

### **1. Testes Unitários** 🔬

**Objetivo**: Testar unidades isoladas de código (funções, métodos, componentes)

**Características**:
- Execução rápida (< 1ms por teste)
- Isolados e independentes
- Mocam dependências externas
- Alta cobertura de código
- Feedback imediato

**Exemplo - Backend (Node.js + Jest)**:
```javascript
// tests/unit/backend/services/user.service.test.js
const UserService = require('../../../../src/services/user.service');
const UserRepository = require('../../../../src/repositories/user.repository');

// Mock do repository
jest.mock('../../../../src/repositories/user.repository');

describe('UserService', () => {
  let userService;
  let mockUserRepository;

  beforeEach(() => {
    mockUserRepository = new UserRepository();
    userService = new UserService(mockUserRepository);
    jest.clearAllMocks();
  });

  describe('createUser', () => {
    test('deve criar usuário com dados válidos', async () => {
      // Arrange
      const userData = {
        name: 'João Silva',
        email: 'joao@email.com',
        password: 'senha123'
      };
      const expectedUser = { id: 1, ...userData };
      
      mockUserRepository.create.mockResolvedValue(expectedUser);

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockUserRepository.create).toHaveBeenCalledWith(userData);
      expect(mockUserRepository.create).toHaveBeenCalledTimes(1);
    });

    test('deve lançar erro para email duplicado', async () => {
      // Arrange
      const userData = { email: 'joao@email.com' };
      mockUserRepository.create.mockRejectedValue(
        new Error('Email já cadastrado')
      );

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('Email já cadastrado');
    });
  });

  describe('validateUser', () => {
    test.each([
      ['', false, 'email vazio'],
      ['email-invalido', false, 'email inválido'],
      ['joao@email.com', true, 'email válido']
    ])('deve validar email: %s → %s (%s)', (email, expected, description) => {
      // Act
      const result = userService.validateEmail(email);
      
      // Assert
      expect(result).toBe(expected);
    });
  });
});
```

**Exemplo - Frontend (React + Jest + Testing Library)**:
```javascript
// tests/unit/frontend/components/UserCard.test.jsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserCard from '../../../../src/components/UserCard';

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'João Silva',
    email: 'joao@email.com',
    avatar: 'https://example.com/avatar.jpg'
  };

  test('deve renderizar informações do usuário', () => {
    // Arrange & Act
    render(<UserCard user={mockUser} />);

    // Assert
    expect(screen.getByText('João Silva')).toBeInTheDocument();
    expect(screen.getByText('joao@email.com')).toBeInTheDocument();
    expect(screen.getByAltText('Avatar de João Silva')).toBeInTheDocument();
  });

  test('deve chamar onEdit quando botão editar for clicado', () => {
    // Arrange
    const mockOnEdit = jest.fn();
    render(<UserCard user={mockUser} onEdit={mockOnEdit} />);

    // Act
    fireEvent.click(screen.getByRole('button', { name: /editar/i }));

    // Assert
    expect(mockOnEdit).toHaveBeenCalledWith(mockUser.id);
    expect(mockOnEdit).toHaveBeenCalledTimes(1);
  });

  test('deve mostrar placeholder quando avatar não disponível', () => {
    // Arrange
    const userWithoutAvatar = { ...mockUser, avatar: null };

    // Act
    render(<UserCard user={userWithoutAvatar} />);

    // Assert
    expect(screen.getByTestId('avatar-placeholder')).toBeInTheDocument();
  });

  test('deve aplicar classe CSS para usuário ativo', () => {
    // Arrange
    const activeUser = { ...mockUser, isActive: true };

    // Act
    render(<UserCard user={activeUser} />);

    // Assert
    expect(screen.getByTestId('user-card')).toHaveClass('active');
  });
});
```

### **2. Testes de Integração** 🔗

**Objetivo**: Testar integração entre componentes, módulos ou serviços

**Exemplo - API Integration**:
```javascript
// tests/integration/api/user.api.test.js
const request = require('supertest');
const app = require('../../../src/app');
const { setupTestDatabase, cleanupTestDatabase } = require('../../utils/database-helper');

describe('User API Integration', () => {
  let testDatabase;

  beforeAll(async () => {
    testDatabase = await setupTestDatabase();
  });

  afterAll(async () => {
    await cleanupTestDatabase(testDatabase);
  });

  beforeEach(async () => {
    await testDatabase.cleanup();
  });

  describe('POST /api/users', () => {
    test('deve criar usuário e retornar dados corretos', async () => {
      // Arrange
      const userData = {
        name: 'João Silva',
        email: 'joao@email.com',
        password: 'senha123'
      };

      // Act
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      // Assert
      expect(response.body).toMatchObject({
        id: expect.any(Number),
        name: userData.name,
        email: userData.email,
        createdAt: expect.any(String)
      });
      expect(response.body.password).toBeUndefined();

      // Verificar se foi salvo no banco
      const userInDb = await testDatabase.findUserById(response.body.id);
      expect(userInDb).toBeTruthy();
      expect(userInDb.name).toBe(userData.name);
    });

    test('deve retornar erro 400 para dados inválidos', async () => {
      // Arrange
      const invalidData = { name: '', email: 'email-invalido' };

      // Act
      const response = await request(app)
        .post('/api/users')
        .send(invalidData)
        .expect(400);

      // Assert
      expect(response.body.errors).toContain('Nome é obrigatório');
      expect(response.body.errors).toContain('Email inválido');
    });
  });

  describe('GET /api/users/:id', () => {
    test('deve retornar usuário existente', async () => {
      // Arrange
      const user = await testDatabase.createUser({
        name: 'João Silva',
        email: 'joao@email.com'
      });

      // Act
      const response = await request(app)
        .get(`/api/users/${user.id}`)
        .expect(200);

      // Assert
      expect(response.body).toMatchObject({
        id: user.id,
        name: 'João Silva',
        email: 'joao@email.com'
      });
    });

    test('deve retornar 404 para usuário inexistente', async () => {
      // Act & Assert
      await request(app)
        .get('/api/users/999999')
        .expect(404);
    });
  });
});
```

### **3. Testes End-to-End (E2E)** 🌐

**Objetivo**: Testar fluxos completos da aplicação do ponto de vista do usuário

**Exemplo - Cypress**:
```javascript
// tests/e2e/web/user-registration.cy.js
describe('Cadastro de Usuário', () => {
  beforeEach(() => {
    cy.visit('/registro');
    cy.clearDatabase();
  });

  it('deve permitir cadastro completo de usuário', () => {
    // Preencher formulário
    cy.get('[data-testid="name-input"]').type('João Silva');
    cy.get('[data-testid="email-input"]').type('joao@email.com');
    cy.get('[data-testid="password-input"]').type('senha123');
    cy.get('[data-testid="confirm-password-input"]').type('senha123');

    // Aceitar termos
    cy.get('[data-testid="terms-checkbox"]').check();

    // Submeter formulário
    cy.get('[data-testid="submit-button"]').click();

    // Verificar sucesso
    cy.get('[data-testid="success-message"]')
      .should('be.visible')
      .and('contain', 'Cadastro realizado com sucesso');

    // Verificar redirecionamento
    cy.url().should('include', '/dashboard');

    // Verificar dados do usuário no dashboard
    cy.get('[data-testid="user-name"]').should('contain', 'João Silva');
  });

  it('deve mostrar erros de validação', () => {
    // Tentar submeter formulário vazio
    cy.get('[data-testid="submit-button"]').click();

    // Verificar mensagens de erro
    cy.get('[data-testid="name-error"]')
      .should('be.visible')
      .and('contain', 'Nome é obrigatório');
    
    cy.get('[data-testid="email-error"]')
      .should('be.visible')
      .and('contain', 'Email é obrigatório');
  });

  it('deve impedir cadastro com email duplicado', () => {
    // Criar usuário existente
    cy.createUser({ email: 'joao@email.com' });

    // Tentar cadastrar com mesmo email
    cy.get('[data-testid="email-input"]').type('joao@email.com');
    cy.get('[data-testid="name-input"]').type('Outro João');
    cy.get('[data-testid="password-input"]').type('senha123');
    cy.get('[data-testid="submit-button"]').click();

    // Verificar erro
    cy.get('[data-testid="error-message"]')
      .should('be.visible')
      .and('contain', 'Email já cadastrado');
  });
});
```

**Exemplo - Playwright**:
```javascript
// tests/e2e/web/user-journey.spec.js
const { test, expect } = require('@playwright/test');

test.describe('Jornada Completa do Usuário', () => {
  test('deve completar fluxo de cadastro até primeira compra', async ({ page }) => {
    // Página inicial
    await page.goto('/');
    await expect(page).toHaveTitle(/Loja Virtual/);

    // Cadastro
    await page.click('[data-testid="register-link"]');
    await page.fill('[data-testid="name"]', 'João Silva');
    await page.fill('[data-testid="email"]', 'joao@email.com');
    await page.fill('[data-testid="password"]', 'senha123');
    await page.click('[data-testid="register-button"]');

    // Verificar dashboard
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Bem-vindo, João Silva');

    // Navegar para produtos
    await page.click('[data-testid="products-link"]');
    await expect(page.locator('[data-testid="product-list"]')).toBeVisible();

    // Adicionar produto ao carrinho
    await page.click('[data-testid="product-1"] [data-testid="add-to-cart"]');
    await expect(page.locator('[data-testid="cart-badge"]')).toContainText('1');

    // Ir para carrinho
    await page.click('[data-testid="cart-link"]');
    await expect(page.locator('[data-testid="cart-item"]')).toHaveCount(1);

    // Finalizar compra
    await page.click('[data-testid="checkout-button"]');
    await page.fill('[data-testid="address"]', 'Rua das Flores, 123');
    await page.selectOption('[data-testid="payment-method"]', 'credit-card');
    await page.click('[data-testid="confirm-order"]');

    // Verificar sucesso
    await expect(page.locator('[data-testid="success-message"]'))
      .toContainText('Pedido realizado com sucesso');
  });
});
```

### **4. Testes de Performance** ⚡

**Exemplo - K6 Load Testing**:
```javascript
// tests/performance/load/api-load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

export const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 200 }, // Ramp up to 200
    { duration: '5m', target: 200 }, // Stay at 200
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% das requests < 500ms
    http_req_failed: ['rate<0.05'],   // Taxa de erro < 5%
    errors: ['rate<0.1'],             // Taxa de erro customizada < 10%
  },
};

export default function () {
  // Test de login
  const loginResponse = http.post('https://api.example.com/auth/login', {
    email: 'test@example.com',
    password: 'password123'
  });

  const loginSuccess = check(loginResponse, {
    'login status is 200': (r) => r.status === 200,
    'login response time < 500ms': (r) => r.timings.duration < 500,
    'token received': (r) => r.json('token') !== undefined,
  });

  errorRate.add(!loginSuccess);

  if (loginSuccess) {
    const token = loginResponse.json('token');
    
    // Test de listagem de usuários
    const usersResponse = http.get('https://api.example.com/users', {
      headers: { Authorization: `Bearer ${token}` },
    });

    const usersSuccess = check(usersResponse, {
      'users status is 200': (r) => r.status === 200,
      'users response time < 1000ms': (r) => r.timings.duration < 1000,
      'users list not empty': (r) => r.json().length > 0,
    });

    errorRate.add(!usersSuccess);
  }

  sleep(1);
}
```

### **5. Testes de Segurança** 🔒

**Exemplo - OWASP ZAP Integration**:
```javascript
// tests/security/vulnerability-scan.js
const ZAP = require('zaproxy');

describe('Security Vulnerability Scan', () => {
  let zap;

  beforeAll(async () => {
    zap = new ZAP({
      proxy: 'http://localhost:8080'
    });
    await zap.spider.scan('http://localhost:3000');
  });

  test('deve não ter vulnerabilidades críticas', async () => {
    const alerts = await zap.core.alerts('High');
    expect(alerts).toHaveLength(0);
  });

  test('deve não ter vulnerabilidades de SQL Injection', async () => {
    const sqlInjectionAlerts = await zap.core.alerts('Medium', null, 'SQL Injection');
    expect(sqlInjectionAlerts).toHaveLength(0);
  });

  test('deve não ter vulnerabilidades XSS', async () => {
    const xssAlerts = await zap.core.alerts('Medium', null, 'Cross Site Scripting');
    expect(xssAlerts).toHaveLength(0);
  });
});
```

### **6. Testes de Acessibilidade** ♿

**Exemplo - Axe + Jest**:
```javascript
// tests/accessibility/axe.test.js
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import App from '../../src/App';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  test('página principal deve ser acessível', async () => {
    const { container } = render(<App />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('formulário de login deve ser acessível', async () => {
    const { container } = render(<LoginForm />);
    const results = await axe(container, {
      rules: {
        'color-contrast': { enabled: true },
        'keyboard-navigation': { enabled: true },
        'focus-management': { enabled: true }
      }
    });
    expect(results).toHaveNoViolations();
  });
});
```

## 🛠️ Ferramentas e Frameworks

### **1. Testes Unitários** 🔧

**JavaScript/TypeScript**:
- **Jest** - Framework popular para Node.js e React
- **Vitest** - Alternativa moderna e rápida ao Jest
- **Mocha + Chai** - Flexível e personalizável
- **Jasmine** - Framework BDD (Behavior Driven Development)

**Python**:
- **pytest** - Framework mais popular
- **unittest** - Biblioteca padrão do Python
- **nose2** - Extensão do unittest

**Java**:
- **JUnit 5** - Framework padrão
- **TestNG** - Alternativa mais flexível
- **Mockito** - Framework de mocking

**C#**:
- **NUnit** - Framework popular
- **MSTest** - Framework da Microsoft
- **xUnit** - Framework moderno

### **2. Testes E2E** 🌐

**Web Testing**:
- **Playwright** - Cross-browser, rápido e confiável
- **Cypress** - Developer-friendly, debugging excelente
- **Selenium** - Padrão da indústria, multi-linguagem
- **Puppeteer** - Chrome/Chromium específico

**Mobile Testing**:
- **Appium** - Cross-platform mobile testing
- **Detox** - React Native específico
- **Maestro** - Mobile UI testing simples
- **WebdriverIO** - Web e mobile

### **3. Performance Testing** ⚡

- **K6** - Modern load testing tool
- **JMeter** - GUI-based performance testing
- **Artillery** - Simple load testing
- **Gatling** - High-performance load testing

### **4. API Testing** 🔗

- **Postman/Newman** - Popular API testing
- **REST Assured** - Java API testing
- **Insomnia** - API design and testing
- **Supertest** - Node.js HTTP assertion

### **5. Security Testing** 🔒

- **OWASP ZAP** - Web application security scanner
- **Burp Suite** - Web vulnerability scanner
- **SonarQube** - Code quality and security
- **Snyk** - Dependency vulnerability scanning

## 📊 Estratégia de Testes

### **1. Pirâmide de Testes** 🏔️

```
           /\
          /  \
         / E2E \         ← Poucos, caros, lentos
        /______\
       /        \
      /   API    \       ← Alguns, médio custo
     /____________\
    /              \
   /     UNIT       \    ← Muitos, baratos, rápidos
  /__________________\
```

**Distribuição Recomendada**:
- **70%** Testes Unitários
- **20%** Testes de Integração/API
- **10%** Testes E2E

**Justificativa**:
- Testes unitários são rápidos e detectam bugs cedo
- Testes de integração validam interfaces
- Testes E2E validam jornadas críticas

### **2. Test-Driven Development (TDD)** 🔄

**Ciclo Red-Green-Refactor**:

```
1. 🔴 RED: Escreva um teste que falha
2. 🟢 GREEN: Implemente código para passar
3. 🔵 REFACTOR: Melhore o código mantendo os testes
```

**Exemplo TDD**:
```javascript
// 1. RED - Teste que falha
describe('Calculator', () => {
  test('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// 2. GREEN - Implementação mínima
class Calculator {
  add(a, b) {
    return a + b;
  }
}

// 3. REFACTOR - Melhorar implementação
class Calculator {
  add(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number') {
      throw new Error('Arguments must be numbers');
    }
    return a + b;
  }
}
```

### **3. Behavior-Driven Development (BDD)** 📝

**Gherkin Syntax**:
```gherkin
# features/user-login.feature
Feature: User Login
  As a registered user
  I want to log into the system
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login
    Given I have a valid account
    When I enter my email "joao@email.com"
    And I enter my password "senha123"
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome, João"

  Scenario: Invalid credentials
    When I enter my email "wrong@email.com"
    And I enter my password "wrongpassword"
    And I click the login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page
```

**Step Definitions**:
```javascript
// steps/login-steps.js
const { Given, When, Then } = require('@cucumber/cucumber');

Given('I am on the login page', async function () {
  await this.page.goto('/login');
});

Given('I have a valid account', async function () {
  await this.database.createUser({
    email: 'joao@email.com',
    password: 'senha123'
  });
});

When('I enter my email {string}', async function (email) {
  await this.page.fill('[data-testid="email"]', email);
});

When('I enter my password {string}', async function (password) {
  await this.page.fill('[data-testid="password"]', password);
});

When('I click the login button', async function () {
  await this.page.click('[data-testid="login-button"]');
});

Then('I should be redirected to the dashboard', async function () {
  await expect(this.page).toHaveURL('/dashboard');
});
```

## 📈 Métricas e Cobertura

### **1. Cobertura de Código** 📊

**Tipos de Cobertura**:
- **Line Coverage** - % de linhas executadas
- **Branch Coverage** - % de branches executados
- **Function Coverage** - % de funções chamadas
- **Statement Coverage** - % de statements executados

**Configuração Jest**:
```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/reportWebVitals.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/components/': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95
    }
  }
};
```

### **2. Métricas de Qualidade** 📏

**Test Metrics**:
- **Test Coverage** - % de código coberto
- **Test Pass Rate** - % de testes que passam
- **Test Execution Time** - Tempo de execução
- **Flaky Test Rate** - % de testes instáveis
- **Test Maintenance Effort** - Esforço para manter testes

**Code Quality Metrics**:
- **Cyclomatic Complexity** - Complexidade do código
- **Code Duplication** - % de código duplicado
- **Technical Debt** - Dívida técnica estimada
- **Maintainability Index** - Índice de maintibilidade

**Exemplo SonarQube**:
```yaml
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0

# Source code
sonar.sources=src
sonar.tests=tests
sonar.test.inclusions=**/*.test.js,**/*.spec.js

# Coverage
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.coverage.exclusions=**/*.test.js,**/*.spec.js

# Quality Gates
sonar.qualitygate.wait=true
```

## 🚀 CI/CD Integration

### **1. GitHub Actions** 🔄

```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info

  integration-tests:
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
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/test_db

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Start application
        run: |
          npm run build
          npm run start &
          npx wait-on http://localhost:3000
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: playwright-report/

  security-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scan
        uses: securecodewarrior/github-action-add-sarif@v1
        with:
          sarif-file: security-scan-results.sarif
      
      - name: Dependency vulnerability scan
        run: npm audit --audit-level moderate

  quality-gate:
    needs: [unit-tests, integration-tests, e2e-tests, security-tests]
    runs-on: ubuntu-latest
    steps:
      - name: Quality Gate
        run: echo "All tests passed! 🎉"
```

### **2. Quality Gates** 🚪

**Critérios de Qualidade**:
```yaml
# quality-gates.yml
quality_gates:
  code_coverage:
    minimum: 80%
    target: 90%
  
  test_success_rate:
    minimum: 98%
    target: 100%
  
  performance:
    response_time_p95: 500ms
    error_rate: <1%
  
  security:
    critical_vulnerabilities: 0
    high_vulnerabilities: 0
  
  code_quality:
    maintainability_rating: A
    reliability_rating: A
    security_rating: A
    technical_debt_ratio: <5%
```

## 🧰 Utilities e Helpers

### **1. Test Helpers** 🛠️

```javascript
// tests/utils/test-helpers.js

// Database helpers
export const createTestUser = async (userData = {}) => {
  return await User.create({
    name: 'Test User',
    email: 'test@example.com',
    password: 'password123',
    ...userData
  });
};

export const cleanDatabase = async () => {
  await User.deleteMany({});
  await Product.deleteMany({});
  await Order.deleteMany({});
};

// Mock factories
export const mockUser = (overrides = {}) => ({
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  createdAt: new Date(),
  ...overrides
});

export const mockApiResponse = (data, status = 200) => ({
  data,
  status,
  headers: {},
  config: {}
});

// DOM helpers
export const waitForElement = async (selector, timeout = 5000) => {
  return new Promise((resolve, reject) => {
    const interval = setInterval(() => {
      const element = document.querySelector(selector);
      if (element) {
        clearInterval(interval);
        resolve(element);
      }
    }, 100);

    setTimeout(() => {
      clearInterval(interval);
      reject(new Error(`Element ${selector} not found`));
    }, timeout);
  });
};

// Form helpers
export const fillForm = async (formData) => {
  for (const [field, value] of Object.entries(formData)) {
    const input = screen.getByLabelText(new RegExp(field, 'i'));
    fireEvent.change(input, { target: { value } });
  }
};

// Custom matchers
expect.extend({
  toBeValidEmail(received) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const pass = emailRegex.test(received);
    
    return {
      message: () => `expected ${received} ${pass ? 'not ' : ''}to be a valid email`,
      pass,
    };
  },
  
  toHaveBeenCalledWithUser(received, user) {
    const pass = received.mock.calls.some(call => 
      call[0] && call[0].id === user.id
    );
    
    return {
      message: () => `expected function ${pass ? 'not ' : ''}to have been called with user ${user.id}`,
      pass,
    };
  }
});
```

### **2. Mock Factory** 🏭

```javascript
// tests/utils/mock-factory.js
import { faker } from '@faker-js/faker';

export class MockFactory {
  static user(overrides = {}) {
    return {
      id: faker.datatype.number(),
      name: faker.name.fullName(),
      email: faker.internet.email(),
      avatar: faker.internet.avatar(),
      createdAt: faker.date.past(),
      isActive: faker.datatype.boolean(),
      ...overrides
    };
  }

  static product(overrides = {}) {
    return {
      id: faker.datatype.number(),
      name: faker.commerce.productName(),
      description: faker.commerce.productDescription(),
      price: parseFloat(faker.commerce.price()),
      category: faker.commerce.department(),
      inStock: faker.datatype.number({ min: 0, max: 100 }),
      imageUrl: faker.image.business(),
      ...overrides
    };
  }

  static order(overrides = {}) {
    return {
      id: faker.datatype.uuid(),
      userId: faker.datatype.number(),
      products: Array.from({ length: faker.datatype.number({ min: 1, max: 5 }) }, 
        () => this.product()
      ),
      total: parseFloat(faker.commerce.price()),
      status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered']),
      createdAt: faker.date.past(),
      ...overrides
    };
  }

  static generateMultiple(factory, count = 5, overrides = {}) {
    return Array.from({ length: count }, () => factory(overrides));
  }
}

// Usage examples:
const user = MockFactory.user({ name: 'João Silva' });
const users = MockFactory.generateMultiple(MockFactory.user, 10);
const products = MockFactory.generateMultiple(MockFactory.product, 20, { inStock: 0 });
```

## 🎓 Para Estudantes

### **Projetos por Nível** 📚

**🟢 Iniciante**
- Escrever testes unitários básicos
- Usar Jest ou similar
- Cobertura de código > 70%
- Testes de funções puras

**🟡 Intermediário**
- Testes de integração com banco
- Testes E2E básicos
- Mocking e stubbing
- TDD em pequenos projetos

**🔴 Avançado**
- Estratégia completa de testes
- Performance e security testing
- BDD com Cucumber
- CI/CD com quality gates

### **Skills Essenciais** 🎯

1. **Testing Fundamentals** → Tipos e conceitos
2. **Test Frameworks** → Jest, Cypress, etc.
3. **Mocking/Stubbing** → Isolamento de dependências
4. **TDD/BDD** → Metodologias de desenvolvimento
5. **CI/CD Integration** → Automação de testes
6. **Performance Testing** → Load testing e optimization
7. **Security Testing** → Vulnerability assessment

### **Exercícios Práticos** 💪

**Exercício 1: Calculator TDD**
```javascript
// Implemente uma calculadora usando TDD
// Funções: add, subtract, multiply, divide
// Casos especiais: divisão por zero, números inválidos
```

**Exercício 2: User Management API**
```javascript
// Teste uma API de gerenciamento de usuários
// CRUD operations, validation, authentication
// Unit + Integration + E2E tests
```

**Exercício 3: E-commerce Flow**
```javascript
// Teste completo de fluxo de e-commerce
// Cadastro → Login → Produtos → Carrinho → Compra
// Performance e acessibilidade
```

## 📋 Checklists

### **Checklist de Qualidade** ✅

**Antes de fazer merge**:
- [ ] Todos os testes passam
- [ ] Cobertura de código > threshold
- [ ] Nenhuma vulnerabilidade crítica
- [ ] Performance dentro dos limites
- [ ] Code review aprovado
- [ ] Documentação atualizada

**Para cada feature**:
- [ ] Testes unitários escritos
- [ ] Testes de integração quando necessário
- [ ] E2E tests para fluxos críticos
- [ ] Edge cases cobertos
- [ ] Error handling testado
- [ ] Performance validada

**Para releases**:
- [ ] Smoke tests executados
- [ ] Regression tests passando
- [ ] Load testing realizado
- [ ] Security scan limpo
- [ ] User acceptance testing
- [ ] Rollback plan testado

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Mantenha testes simples e focados
- Use nomes descritivos para testes
- Organize testes em suites lógicas
- Mantenha dados de teste isolados
- Execute testes rapidamente
- Automatize tudo que for possível
- Monitore métricas de qualidade

### **❌ Evite**
- Testes que dependem de outros testes
- Hard-coded values em testes
- Testes que fazem muitas coisas
- Ignorar testes falhando
- Baixa cobertura de código
- Testes lentos e instáveis
- Falta de testes de regressão

### **🎯 Métricas de Sucesso**
- Redução de bugs em produção
- Tempo de deploy menor
- Confiança para refatorar
- Onboarding mais rápido
- Documentação viva (testes)
- Feedback rápido de qualidade
- ROI positivo dos testes

---

**Testes são um investimento na qualidade e confiabilidade do software. Uma boa estratégia de testes permite desenvolvimento mais rápido e com menos bugs!**

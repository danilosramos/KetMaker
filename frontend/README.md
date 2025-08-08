# Frontend - Interface do Usuário

> 🎨 **Interface web moderna, responsiva e acessível**

## 📋 Visão Geral

O frontend é responsável pela experiência do usuário, apresentando as funcionalidades do sistema de forma intuitiva, responsiva e acessível. Inclui desde a interface visual até a comunicação com APIs backend.

## 🏗️ Estrutura Recomendada

```
frontend/
├── 📁 public/                  # Arquivos estáticos públicos
│   ├── 📄 index.html           # Template HTML principal
│   ├── 📄 favicon.ico          # Ícone do site
│   ├── 📄 manifest.json        # PWA manifest
│   └── 📁 images/              # Imagens públicas
├── 📁 src/                     # Código fonte principal
│   ├── 📁 components/          # Componentes reutilizáveis
│   │   ├── 📁 common/          # Componentes genéricos (Button, Input)
│   │   ├── 📁 layout/          # Componentes de layout (Header, Footer)
│   │   └── 📁 forms/           # Componentes de formulário
│   ├── 📁 pages/               # Páginas/Views da aplicação
│   │   ├── 📁 auth/            # Páginas de autenticação
│   │   ├── 📁 dashboard/       # Dashboard principal
│   │   └── 📁 profile/         # Perfil do usuário
│   ├── 📁 hooks/               # Custom hooks (React)
│   ├── 📁 services/            # Chamadas para APIs
│   ├── 📁 store/               # Gerenciamento de estado global
│   ├── 📁 utils/               # Utilitários e helpers
│   ├── 📁 styles/              # Estilos globais e temas
│   ├── 📁 assets/              # Imagens, ícones, fontes
│   ├── 📁 types/               # Tipos TypeScript
│   ├── 📁 constants/           # Constantes da aplicação
│   └── 📄 main.tsx             # Ponto de entrada
├── 📁 tests/                   # Testes do frontend
│   ├── 📁 components/          # Testes de componentes
│   ├── 📁 pages/               # Testes de páginas
│   ├── 📁 utils/               # Testes de utilidades
│   └── 📁 __mocks__/           # Mocks para testes
├── 📁 docs/                    # Documentação específica
│   ├── 📄 components.md        # Guia de componentes
│   ├── 📄 styleguide.md        # Guia de estilos
│   └── 📄 storybook.md         # Documentação Storybook
├── 📄 package.json             # Dependências e scripts
├── 📄 vite.config.ts           # Configuração do bundler
├── 📄 tailwind.config.js       # Configuração do CSS framework
├── 📄 .env.example             # Variáveis de ambiente
├── 📄 .eslintrc.json           # Configuração do linter
├── 📄 Dockerfile               # Container para produção
└── 📄 README.md                # Este arquivo
```

## 🛠️ Tecnologias Recomendadas

### **React Ecosystem**
- **React 18** + TypeScript
- **Vite** (build tool rápido)
- **React Router** (roteamento)
- **React Query/SWR** (estado servidor)
- **Zustand/Redux Toolkit** (estado global)

### **Vue.js Ecosystem**
- **Vue 3** + TypeScript
- **Vite** + Vue CLI
- **Vue Router** (roteamento)
- **Pinia** (estado global)
- **VueUse** (composables)

### **Angular Ecosystem**
- **Angular 17+** + TypeScript
- **Angular CLI**
- **RxJS** (programação reativa)
- **NgRx** (estado global)
- **Angular Material** (componentes)

### **Styling Solutions**
- **Tailwind CSS** (utility-first)
- **Styled Components** (CSS-in-JS)
- **Sass/SCSS** (preprocessor)
- **CSS Modules** (modular CSS)

## 📦 Componentes e Arquitetura

### **1. Component Architecture** 🧩

**Atomic Design Principles**
```
Atoms → Molecules → Organisms → Templates → Pages
```

**Exemplo de Estrutura**
```tsx
// Button (Atom)
const Button = ({ variant, children, onClick }) => (
  <button className={`btn btn-${variant}`} onClick={onClick}>
    {children}
  </button>
);

// SearchForm (Molecule)
const SearchForm = ({ onSearch }) => (
  <form onSubmit={onSearch}>
    <Input placeholder="Buscar..." />
    <Button variant="primary" type="submit">Buscar</Button>
  </form>
);

// ProductCard (Organism)
const ProductCard = ({ product }) => (
  <Card>
    <Image src={product.image} />
    <Title>{product.name}</Title>
    <Price>{product.price}</Price>
    <Button variant="secondary">Adicionar ao Carrinho</Button>
  </Card>
);
```

### **2. State Management** 🗃️

**Local State (useState, ref)**
```tsx
const [loading, setLoading] = useState(false);
const [formData, setFormData] = useState({});
```

**Server State (React Query)**
```tsx
const { data: users, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers()
});
```

**Global State (Zustand)**
```tsx
const useAuthStore = create((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null })
}));
```

### **3. Routing & Navigation** 🧭

**React Router Example**
```tsx
<BrowserRouter>
  <Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/login" element={<LoginPage />} />
    <Route path="/dashboard" element={
      <ProtectedRoute>
        <DashboardPage />
      </ProtectedRoute>
    } />
    <Route path="/users/:id" element={<UserProfile />} />
  </Routes>
</BrowserRouter>
```

**Protected Routes**
```tsx
const ProtectedRoute = ({ children }) => {
  const { user } = useAuthStore();
  return user ? children : <Navigate to="/login" />;
};
```

## 🎨 Design System & UI/UX

### **Design Tokens**
```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  
  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  
  /* Typography */
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
}
```

### **Responsive Design**
```css
/* Mobile First Approach */
.container {
  padding: var(--space-md);
}

@media (min-width: 768px) {
  .container {
    padding: var(--space-lg);
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### **Accessibility (a11y)**
```tsx
// Exemplo de componente acessível
const Modal = ({ isOpen, onClose, title, children }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
      // Foca no primeiro elemento focável
      modalRef.current?.focus();
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      ref={modalRef}
      tabIndex={-1}
    >
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose} aria-label="Fechar modal">
        ×
      </button>
    </div>
  );
};
```

## 🔗 Integração com Backend

### **API Client Setup**
```tsx
// api/client.ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

// Interceptor para autenticação
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirecionar para login
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

### **Custom Hooks para APIs**
```tsx
// hooks/useUsers.ts
export const useUsers = () => {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const { data } = await api.get('/users');
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutos
  });
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (userData) => {
      const { data } = await api.post('/users', userData);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['users']);
    },
  });
};
```

### **Error Handling**
```tsx
// components/ErrorBoundary.tsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Enviar erro para serviço de monitoramento
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Algo deu errado!</h2>
          <button onClick={() => window.location.reload()}>
            Recarregar página
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## 🧪 Estratégias de Teste

### **Testing Library Setup**
```tsx
// tests/setup.ts
import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';

configure({
  testIdAttribute: 'data-testid',
});

// Mock de APIs
global.fetch = jest.fn();
```

### **Component Testing**
```tsx
// tests/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../components/Button';

describe('Button Component', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    
    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies correct variant class', () => {
    render(<Button variant="primary">Click me</Button>);
    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });
});
```

### **Integration Testing**
```tsx
// tests/pages/LoginPage.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { LoginPage } from '../pages/LoginPage';
import { AuthProvider } from '../contexts/AuthContext';

const renderWithProviders = (component) => {
  return render(
    <AuthProvider>
      {component}
    </AuthProvider>
  );
};

describe('LoginPage', () => {
  it('submits form with valid credentials', async () => {
    renderWithProviders(<LoginPage />);
    
    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@email.com' }
    });
    fireEvent.change(screen.getByLabelText(/senha/i), {
      target: { value: 'password123' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /entrar/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/bem-vindo/i)).toBeInTheDocument();
    });
  });
});
```

### **E2E Testing (Playwright)**
```typescript
// tests/e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test('user can login successfully', async ({ page }) => {
  await page.goto('/login');
  
  await page.fill('[data-testid="email-input"]', 'test@email.com');
  await page.fill('[data-testid="password-input"]', 'password123');
  await page.click('[data-testid="login-button"]');
  
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
});
```

## 🚀 Performance e Otimização

### **Code Splitting**
```tsx
// Lazy loading de páginas
const DashboardPage = lazy(() => import('../pages/DashboardPage'));
const ProfilePage = lazy(() => import('../pages/ProfilePage'));

// Wrapper com Suspense
const App = () => (
  <Router>
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
    </Suspense>
  </Router>
);
```

### **Memoization**
```tsx
// React.memo para componentes
const UserCard = React.memo(({ user }) => (
  <div>
    <h3>{user.name}</h3>
    <p>{user.email}</p>
  </div>
));

// useMemo para cálculos caros
const expensiveValue = useMemo(() => {
  return heavyCalculation(data);
}, [data]);

// useCallback para funções
const handleSubmit = useCallback((formData) => {
  submitForm(formData);
}, []);
```

### **Bundle Optimization**
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@headlessui/react', '@heroicons/react'],
        },
      },
    },
  },
});
```

### **Image Optimization**
```tsx
// Componente de imagem otimizada
const OptimizedImage = ({ src, alt, width, height }) => {
  const [isLoaded, setIsLoaded] = useState(false);
  
  return (
    <div className="relative">
      {!isLoaded && <ImageSkeleton />}
      <img
        src={src}
        alt={alt}
        width={width}
        height={height}
        loading="lazy"
        onLoad={() => setIsLoaded(true)}
        className={`transition-opacity ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
      />
    </div>
  );
};
```

## 📱 Progressive Web App (PWA)

### **Service Worker**
```javascript
// public/sw.js
const CACHE_NAME = 'app-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
  );
});
```

### **Manifest.json**
```json
{
  "name": "Minha Aplicação",
  "short_name": "MinhaApp",
  "description": "Uma aplicação web progressiva",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#3b82f6",
  "background_color": "#ffffff",
  "icons": [
    {
      "src": "/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## 🔧 Ferramentas de Desenvolvimento

### **Linting & Formatting**
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "react-hooks"
  ],
  "rules": {
    "react/jsx-uses-react": "error",
    "react/jsx-uses-vars": "error",
    "no-unused-vars": "warn"
  }
}
```

### **Storybook para Componentes**
```tsx
// stories/Button.stories.tsx
export default {
  title: 'Components/Button',
  component: Button,
  parameters: {
    docs: {
      description: {
        component: 'Componente de botão reutilizável',
      },
    },
  },
};

export const Primary = {
  args: {
    variant: 'primary',
    children: 'Button Primary',
  },
};

export const Secondary = {
  args: {
    variant: 'secondary',
    children: 'Button Secondary',
  },
};
```

### **Husky + Lint-staged**
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

## 🌐 Internacionalização (i18n)

### **React-i18next Setup**
```tsx
// i18n/index.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      pt: {
        translation: {
          welcome: 'Bem-vindo',
          login: 'Entrar',
        }
      },
      en: {
        translation: {
          welcome: 'Welcome',
          login: 'Login',
        }
      }
    },
    lng: 'pt',
    fallbackLng: 'en',
  });

// Uso nos componentes
const { t } = useTranslation();
return <h1>{t('welcome')}</h1>;
```

## 🔐 Segurança Frontend

### **Input Sanitization**
```tsx
import DOMPurify from 'dompurify';

const SafeHTML = ({ content }) => {
  const sanitizedContent = DOMPurify.sanitize(content);
  return <div dangerouslySetInnerHTML={{ __html: sanitizedContent }} />;
};
```

### **CSP Headers**
```html
<!-- index.html -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline'; 
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;">
```

### **Environment Variables**
```typescript
// .env.example
VITE_API_URL=http://localhost:3000/api
VITE_APP_NAME=Minha Aplicação
VITE_ENVIRONMENT=development

// Uso no código
const apiUrl = import.meta.env.VITE_API_URL;
```

## 🎓 Para Estudantes

### **Projetos por Nível**

**🟢 Iniciante**
- Todo List com localStorage
- Calculadora
- Weather App (API pública)
- Galeria de fotos

**🟡 Intermediário**
- Dashboard com gráficos
- E-commerce frontend
- Chat em tempo real
- Blog com CMS

**🔴 Avançado**
- SaaS dashboard completo
- Aplicação PWA
- Microfrontends
- Editor online (tipo Figma)

### **Skills Progressivas**
1. **HTML/CSS/JS** → Fundamentos sólidos
2. **React/Vue/Angular** → Framework moderno
3. **TypeScript** → Tipagem estática
4. **State Management** → Gerenciamento de estado
5. **Testing** → Testes automatizados
6. **Performance** → Otimização
7. **Accessibility** → Inclusão digital
8. **PWA** → Web apps avançadas

## 🔧 Scripts e Automação

### **Package.json Scripts**
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "lint": "eslint . --ext ts,tsx",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write src/",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  }
}
```

### **CI/CD Pipeline**
```yaml
# .github/workflows/frontend.yml
name: Frontend CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run test
      - run: npm run build
      
      - uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Componentização inteligente
- Estado mínimo e derivado
- Performance first (lazy loading, memoization)
- Acessibilidade desde o início
- Testes como documentação
- Design system consistente
- SEO-friendly (meta tags, SSR se necessário)

### **❌ Evite**
- Mutação direta de estado
- Props drilling excessivo
- Re-renders desnecessários
- Componentes gigantes
- CSS global desorganizado
- JavaScript inline em produção
- Dependências desnecessárias

### **🎯 Métricas de Qualidade**
- Lighthouse Score > 90
- Bundle size otimizado
- Cobertura de testes > 80%
- Zero erros de acessibilidade
- Tempo de carregamento < 3s
- Core Web Vitals verdes

---

**Este README deve ser adaptado conforme o framework e ferramentas específicas escolhidas para o projeto!**

# Mobile - Aplicação Mobile

> 📱 **Aplicação mobile nativa ou híbrida para iOS e Android**

## 📋 Visão Geral

A aplicação mobile estende a funcionalidade do sistema para dispositivos móveis, oferecendo uma experiência otimizada para smartphones e tablets. Pode ser desenvolvida como app nativo, híbrido ou PWA, dependendo dos requisitos do projeto.

## 🏗️ Estrutura Recomendada

```
mobile/
├── 📁 src/                     # Código fonte principal
│   ├── 📁 screens/             # Telas da aplicação
│   │   ├── 📁 auth/            # Telas de autenticação
│   │   ├── 📁 home/            # Tela principal/dashboard
│   │   ├── 📁 profile/         # Perfil do usuário
│   │   └── 📁 settings/        # Configurações
│   ├── 📁 components/          # Componentes reutilizáveis
│   │   ├── 📁 common/          # Componentes genéricos
│   │   ├── 📁 forms/           # Componentes de formulário
│   │   └── 📁 navigation/      # Componentes de navegação
│   ├── 📁 navigation/          # Configuração de navegação
│   ├── 📁 services/            # Serviços e APIs
│   ├── 📁 store/               # Gerenciamento de estado
│   ├── 📁 utils/               # Utilitários e helpers
│   ├── 📁 styles/              # Estilos e temas
│   ├── 📁 assets/              # Imagens, ícones, fontes
│   ├── 📁 types/               # Tipos TypeScript
│   ├── 📁 hooks/               # Custom hooks
│   └── 📄 App.tsx              # Componente principal
├── 📁 android/                 # Código nativo Android
│   ├── 📁 app/src/main/        # Código Java/Kotlin
│   └── 📄 build.gradle         # Configuração de build
├── 📁 ios/                     # Código nativo iOS
│   ├── 📁 ProjectName/         # Código Swift/Objective-C
│   └── 📄 Podfile              # Dependências iOS
├── 📁 tests/                   # Testes da aplicação
│   ├── 📁 components/          # Testes de componentes
│   ├── 📁 screens/             # Testes de telas
│   ├── 📁 services/            # Testes de serviços
│   └── 📁 e2e/                 # Testes end-to-end
├── 📁 docs/                    # Documentação específica
│   ├── 📄 setup.md             # Guia de configuração
│   ├── 📄 building.md          # Guia de build
│   └── 📄 deployment.md        # Guia de deploy
├── 📄 package.json             # Dependências (React Native/Expo)
├── 📄 app.json                 # Configuração Expo
├── 📄 metro.config.js          # Configuração do bundler
├── 📄 .env.example             # Variáveis de ambiente
└── 📄 README.md                # Este arquivo
```

## 🛠️ Tecnologias Recomendadas

### **React Native**
- **React Native** + TypeScript
- **Expo** (managed workflow)
- **React Navigation** (navegação)
- **React Query** (estado servidor)
- **AsyncStorage** (persistência local)

### **Flutter**
- **Flutter** + Dart
- **Provider/Riverpod** (estado)
- **GoRouter** (navegação)
- **Dio** (HTTP client)
- **Hive/SQLite** (banco local)

### **Native Development**
- **Swift** (iOS)
- **Kotlin/Java** (Android)
- **SwiftUI/UIKit** (iOS UI)
- **Jetpack Compose** (Android UI)

### **Hybrid Solutions**
- **Ionic** + Angular/React/Vue
- **Cordova/PhoneGap**
- **Capacitor**

## 📱 Arquitetura Mobile

### **1. Screen-based Architecture** 📺

```typescript
// React Native example
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
        <Stack.Screen name="Settings" component={SettingsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### **2. Component Structure** 🧩

```typescript
// components/Button/Button.tsx
interface ButtonProps {
  title: string;
  variant?: 'primary' | 'secondary';
  onPress: () => void;
  disabled?: boolean;
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  variant = 'primary',
  onPress,
  disabled = false,
  loading = false,
}) => {
  return (
    <TouchableOpacity
      style={[styles.button, styles[variant]]}
      onPress={onPress}
      disabled={disabled || loading}
    >
      {loading ? (
        <ActivityIndicator color="white" />
      ) : (
        <Text style={styles.buttonText}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};
```

### **3. State Management** 🗃️

```typescript
// store/authStore.ts (Zustand)
interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  isLoading: false,
  
  login: async (credentials) => {
    set({ isLoading: true });
    try {
      const { user, token } = await authService.login(credentials);
      await AsyncStorage.setItem('token', token);
      set({ user, token, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },
  
  logout: async () => {
    await AsyncStorage.removeItem('token');
    set({ user: null, token: null });
  },
}));
```

## 🔗 Integração com Backend

### **API Client Setup**
```typescript
// services/api.ts
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const api = axios.create({
  baseURL: 'https://api.myapp.com',
  timeout: 10000,
});

// Interceptor para autenticação
api.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('token');
      // Navegar para tela de login
    }
    return Promise.reject(error);
  }
);
```

### **Offline Support**
```typescript
// hooks/useOfflineSync.ts
import NetInfo from '@react-native-netinfo/netinfo';

export const useOfflineSync = () => {
  const [isOnline, setIsOnline] = useState(true);
  const [pendingActions, setPendingActions] = useState([]);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected);
      
      if (state.isConnected && pendingActions.length > 0) {
        syncPendingActions();
      }
    });

    return unsubscribe;
  }, []);

  const addPendingAction = (action) => {
    if (!isOnline) {
      setPendingActions(prev => [...prev, action]);
    }
  };

  const syncPendingActions = async () => {
    for (const action of pendingActions) {
      try {
        await executeAction(action);
      } catch (error) {
        console.error('Failed to sync action:', error);
      }
    }
    setPendingActions([]);
  };

  return { isOnline, addPendingAction };
};
```

## 🎨 Design e UX Mobile

### **Design Principles**
```typescript
// styles/theme.ts
export const theme = {
  colors: {
    primary: '#007AFF',
    secondary: '#5856D6',
    success: '#34C759',
    warning: '#FF9500',
    danger: '#FF3B30',
    text: '#000000',
    textSecondary: '#6D6D70',
    background: '#FFFFFF',
    surface: '#F2F2F7',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  typography: {
    h1: {
      fontSize: 28,
      fontWeight: 'bold',
    },
    body: {
      fontSize: 16,
      fontWeight: 'normal',
    },
    caption: {
      fontSize: 12,
      fontWeight: 'normal',
    },
  },
};
```

### **Responsive Design**
```typescript
// utils/dimensions.ts
import { Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export const deviceSize = {
  width,
  height,
  isSmall: width < 350,
  isMedium: width >= 350 && width < 414,
  isLarge: width >= 414,
};

// Uso nos componentes
const styles = StyleSheet.create({
  container: {
    padding: deviceSize.isSmall ? 12 : 16,
  },
});
```

### **Platform-specific Code**
```typescript
// components/Header.tsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  header: {
    height: Platform.OS === 'ios' ? 88 : 56,
    paddingTop: Platform.OS === 'ios' ? 44 : 0,
    backgroundColor: Platform.select({
      ios: 'white',
      android: '#2196F3',
    }),
  },
});
```

## 📱 Funcionalidades Nativas

### **Permissions**
```typescript
// utils/permissions.ts
import { request, PERMISSIONS, RESULTS } from 'react-native-permissions';

export const requestCameraPermission = async () => {
  const permission = Platform.OS === 'ios' 
    ? PERMISSIONS.IOS.CAMERA 
    : PERMISSIONS.ANDROID.CAMERA;

  const result = await request(permission);
  
  switch (result) {
    case RESULTS.GRANTED:
      return true;
    case RESULTS.DENIED:
      Alert.alert('Permissão necessária', 'Esta funcionalidade requer acesso à câmera');
      return false;
    case RESULTS.BLOCKED:
      Alert.alert('Permissão bloqueada', 'Habilite a permissão nas configurações do dispositivo');
      return false;
    default:
      return false;
  }
};
```

### **Push Notifications**
```typescript
// services/notificationService.ts
import PushNotification from 'react-native-push-notification';

class NotificationService {
  configure() {
    PushNotification.configure({
      onRegister: (token) => {
        console.log('TOKEN:', token);
        // Enviar token para o backend
      },
      
      onNotification: (notification) => {
        console.log('NOTIFICATION:', notification);
        
        if (notification.userInteraction) {
          // Usuário tocou na notificação
          this.handleNotificationTap(notification);
        }
      },
      
      requestPermissions: Platform.OS === 'ios',
    });
  }

  localNotification(title: string, message: string) {
    PushNotification.localNotification({
      title,
      message,
      playSound: true,
      soundName: 'default',
    });
  }
}

export default new NotificationService();
```

### **Biometric Authentication**
```typescript
// services/biometricService.ts
import TouchID from 'react-native-touch-id';

export const authenticateWithBiometrics = async () => {
  const optionalConfigObject = {
    title: 'Autenticação Requerida',
    subtitle: 'Use sua impressão digital para continuar',
    imageColor: '#e00606',
    imageErrorColor: '#ff0000',
    sensorDescription: 'Toque no sensor',
    sensorErrorDescription: 'Falhou',
    cancelText: 'Cancelar',
    fallbackLabel: 'Usar senha',
    unifiedErrors: false,
    passcodeFallback: false,
  };

  try {
    const biometryType = await TouchID.isSupported(optionalConfigObject);
    console.log('Biometry Type Supported: ', biometryType);
    
    const isAuthenticated = await TouchID.authenticate(
      'Para acessar sua conta',
      optionalConfigObject
    );
    
    return isAuthenticated;
  } catch (error) {
    console.log('Authentication Failed: ', error);
    return false;
  }
};
```

## 🗄️ Persistência Local

### **AsyncStorage**
```typescript
// services/storageService.ts
import AsyncStorage from '@react-native-async-storage/async-storage';

class StorageService {
  async setItem(key: string, value: any): Promise<void> {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error saving data', error);
    }
  }

  async getItem<T>(key: string): Promise<T | null> {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Error reading data', error);
      return null;
    }
  }

  async removeItem(key: string): Promise<void> {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing data', error);
    }
  }

  async clear(): Promise<void> {
    try {
      await AsyncStorage.clear();
    } catch (error) {
      console.error('Error clearing storage', error);
    }
  }
}

export default new StorageService();
```

### **SQLite Database**
```typescript
// services/databaseService.ts
import SQLite from 'react-native-sqlite-storage';

class DatabaseService {
  private db: SQLite.SQLiteDatabase | null = null;

  async initDatabase() {
    try {
      this.db = await SQLite.openDatabase({
        name: 'myapp.db',
        location: 'default',
      });
      
      await this.createTables();
    } catch (error) {
      console.error('Database initialization failed:', error);
    }
  }

  private async createTables() {
    if (!this.db) return;

    const createUsersTable = `
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
    `;

    await this.db.executeSql(createUsersTable);
  }

  async insertUser(user: { name: string; email: string }) {
    if (!this.db) return;

    const query = 'INSERT INTO users (name, email) VALUES (?, ?)';
    const result = await this.db.executeSql(query, [user.name, user.email]);
    return result;
  }

  async getUsers() {
    if (!this.db) return [];

    const query = 'SELECT * FROM users ORDER BY created_at DESC';
    const [results] = await this.db.executeSql(query);
    
    const users = [];
    for (let i = 0; i < results.rows.length; i++) {
      users.push(results.rows.item(i));
    }
    
    return users;
  }
}

export default new DatabaseService();
```

## 🧪 Estratégias de Teste

### **Unit Testing**
```typescript
// tests/components/Button.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { Button } from '../src/components/Button';

describe('Button Component', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <Button title="Test Button" onPress={() => {}} />
    );
    
    expect(getByText('Test Button')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const mockPress = jest.fn();
    const { getByText } = render(
      <Button title="Test Button" onPress={mockPress} />
    );
    
    fireEvent.press(getByText('Test Button'));
    expect(mockPress).toHaveBeenCalledTimes(1);
  });

  it('shows loading indicator when loading', () => {
    const { getByTestId } = render(
      <Button title="Test Button" onPress={() => {}} loading />
    );
    
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });
});
```

### **Integration Testing**
```typescript
// tests/screens/LoginScreen.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { LoginScreen } from '../src/screens/LoginScreen';

jest.mock('../src/services/authService');

describe('LoginScreen', () => {
  it('submits form with valid credentials', async () => {
    const { getByPlaceholderText, getByText } = render(<LoginScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Email'), 'test@email.com');
    fireEvent.changeText(getByPlaceholderText('Senha'), 'password123');
    fireEvent.press(getByText('Entrar'));
    
    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith({
        email: 'test@email.com',
        password: 'password123',
      });
    });
  });
});
```

### **E2E Testing (Detox)**
```typescript
// e2e/login.e2e.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should login successfully', async () => {
    await element(by.id('email-input')).typeText('test@email.com');
    await element(by.id('password-input')).typeText('password123');
    await element(by.id('login-button')).tap();
    
    await waitFor(element(by.text('Dashboard')))
      .toBeVisible()
      .withTimeout(5000);
  });
});
```

## 🚀 Build e Deploy

### **Android Build**
```bash
# Debug build
npx react-native run-android

# Release build
cd android
./gradlew assembleRelease

# Generate signed APK
./gradlew assembleRelease -PMYAPP_UPLOAD_STORE_FILE=myapp.keystore \
                         -PMYAPP_UPLOAD_KEY_ALIAS=myapp \
                         -PMYAPP_UPLOAD_STORE_PASSWORD=password \
                         -PMYAPP_UPLOAD_KEY_PASSWORD=password
```

### **iOS Build**
```bash
# Debug build
npx react-native run-ios

# Release build with Xcode
open ios/MyApp.xcworkspace

# Command line build
xcodebuild -workspace ios/MyApp.xcworkspace \
           -scheme MyApp \
           -configuration Release \
           -destination generic/platform=iOS \
           -archivePath MyApp.xcarchive \
           archive
```

### **Expo Build**
```bash
# Install EAS CLI
npm install -g @expo/cli

# Configure build
eas build:configure

# Build for all platforms
eas build --platform all

# Build for specific platform
eas build --platform ios
eas build --platform android
```

## 📊 Performance e Otimização

### **Image Optimization**
```typescript
// components/OptimizedImage.tsx
import FastImage from 'react-native-fast-image';

interface OptimizedImageProps {
  uri: string;
  style?: any;
  resizeMode?: 'contain' | 'cover' | 'stretch' | 'center';
}

export const OptimizedImage: React.FC<OptimizedImageProps> = ({
  uri,
  style,
  resizeMode = 'cover',
}) => {
  return (
    <FastImage
      style={style}
      source={{
        uri,
        priority: FastImage.priority.high,
        cache: FastImage.cacheControl.immutable,
      }}
      resizeMode={FastImage.resizeMode[resizeMode]}
    />
  );
};
```

### **List Optimization**
```typescript
// components/OptimizedList.tsx
import { FlatList, VirtualizedList } from 'react-native';

const OptimizedList = ({ data, renderItem }) => {
  const getItemLayout = (data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  });

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      getItemLayout={getItemLayout}
      removeClippedSubviews={true}
      maxToRenderPerBatch={10}
      updateCellsBatchingPeriod={50}
      initialNumToRender={10}
      windowSize={10}
    />
  );
};
```

### **Memory Management**
```typescript
// hooks/useMemoryWarning.ts
import { AppState } from 'react-native';

export const useMemoryWarning = () => {
  useEffect(() => {
    const handleAppStateChange = (nextAppState) => {
      if (nextAppState === 'background') {
        // Limpar caches, fechar conexões, etc.
        clearImageCache();
        closeUnnecessaryConnections();
      }
    };

    AppState.addEventListener('change', handleAppStateChange);
    
    return () => {
      AppState.removeEventListener('change', handleAppStateChange);
    };
  }, []);
};
```

## 🔐 Segurança Mobile

### **Certificate Pinning**
```typescript
// services/secureApi.ts
import { NetworkingModule } from 'react-native';

const api = axios.create({
  baseURL: 'https://api.myapp.com',
  // Certificate pinning configuration
  httpsAgent: {
    pinCertificates: ['SHA256:certificateHash'],
  },
});
```

### **Secure Storage**
```typescript
// services/secureStorage.ts
import { setInternetCredentials, getInternetCredentials } from 'react-native-keychain';

export const secureStorage = {
  async setItem(key: string, value: string) {
    await setInternetCredentials(key, key, value);
  },

  async getItem(key: string): Promise<string | null> {
    try {
      const credentials = await getInternetCredentials(key);
      return credentials ? credentials.password : null;
    } catch (error) {
      return null;
    }
  },
};
```

### **Root/Jailbreak Detection**
```typescript
// services/securityService.ts
import JailMonkey from 'jail-monkey';

export const checkDeviceSecurity = () => {
  const isJailBroken = JailMonkey.isJailBroken();
  const canMockLocation = JailMonkey.canMockLocation();
  const isDebugged = JailMonkey.isDebugged();

  if (isJailBroken || canMockLocation || isDebugged) {
    Alert.alert(
      'Dispositivo Comprometido',
      'Este dispositivo pode não ser seguro. Algumas funcionalidades podem estar limitadas.',
      [{ text: 'OK' }]
    );
    return false;
  }

  return true;
};
```

## 🎓 Para Estudantes

### **Projetos por Nível**

**🟢 Iniciante**
- Lista de tarefas (Todo App)
- Calculadora
- Timer/Cronômetro
- Galeria de fotos

**🟡 Intermediário**
- App de receitas
- Chat simples
- App de clima
- Loja simples

**🔴 Avançado**
- App bancário
- Rede social
- E-commerce completo
- App de streaming

### **Skills Progressivas**
1. **Layout & Styling** → Design responsivo
2. **Navigation** → Fluxos complexos
3. **State Management** → Estado global
4. **API Integration** → Comunicação com backend
5. **Local Storage** → Persistência de dados
6. **Push Notifications** → Engajamento
7. **Camera/GPS** → Funcionalidades nativas
8. **Performance** → Otimizações avançadas

## 🔧 Ferramentas Recomendadas

### **Desenvolvimento**
- **React Native Debugger** - Debug avançado
- **Flipper** - Debug e profiling
- **Reactotron** - Estado e API monitoring
- **VS Code** + React Native Tools

### **Design**
- **Figma** - Design de interfaces
- **Zeplin** - Handoff design-dev
- **Lottie** - Animações
- **React Native Elements** - Componentes

### **Testing**
- **Jest** - Unit testing
- **Testing Library** - Component testing
- **Detox** - E2E testing
- **Maestro** - UI testing

### **Deploy**
- **Fastlane** - Automação de deploy
- **CodePush** - Updates over-the-air
- **App Center** - CI/CD Microsoft
- **Bitrise** - CI/CD mobile

---

## 💡 Dicas Importantes

### **✅ Boas Práticas**
- Performance first (60fps)
- Design system consistente
- Offline-first approach
- Testes em dispositivos reais
- Acessibilidade desde o início
- Bundle size otimizado
- Permissões just-in-time

### **❌ Evite**
- Renderização excessiva
- Imagens não otimizadas
- Animações bloqueantes
- Memory leaks
- Rede sem cache
- UI thread blocking
- Dependências desnecessárias

### **🎯 Métricas de Qualidade**
- App size < 50MB
- Startup time < 3s
- Crash rate < 1%
- ANR rate < 0.5%
- Battery usage otimizado
- 60fps constante
- 5 estrelas nas lojas

---

**Este README deve ser adaptado conforme a plataforma e tecnologias específicas escolhidas para o projeto mobile!**

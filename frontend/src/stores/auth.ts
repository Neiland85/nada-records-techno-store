import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'user' | 'admin';
  createdAt: string;
  preferences: {
    theme: 'light' | 'dark' | 'system';
    language: string;
    notifications: boolean;
  };
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  lastLoginAttempt: Date | null;
}

interface AuthActions {
  // Autenticación
  login: (email: string, password: string) => Promise<void>;
  register: (userData: {
    email: string;
    password: string;
    name: string;
  }) => Promise<void>;
  logout: () => void;

  // Gestión de usuario
  updateUser: (userData: Partial<User>) => void;
  updatePreferences: (preferences: Partial<User['preferences']>) => void;

  // Utilidades
  clearError: () => void;
  setLoading: (loading: boolean) => void;
  refreshToken: () => Promise<void>;
}

type AuthStore = AuthState & AuthActions;

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
  lastLoginAttempt: null,
};

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Autenticación
      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null, lastLoginAttempt: new Date() });

        try {
          // Aquí iría la llamada a la API con email y password
          console.log('Login attempt for:', email);
          await new Promise(resolve => setTimeout(resolve, 1000));

          // Simular respuesta de API
          const mockUser: User = {
            id: '1',
            email,
            name: email.split('@')[0],
            role: 'user',
            createdAt: new Date().toISOString(),
            preferences: {
              theme: 'dark',
              language: 'es',
              notifications: true,
            },
          };

          set({
            user: mockUser,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Error de autenticación',
            isLoading: false,
          });
        }
      },

      register: async (userData) => {
        set({ isLoading: true, error: null });

        try {
          // Aquí iría la llamada a la API de registro
          await new Promise(resolve => setTimeout(resolve, 1500));

          // Simular respuesta de API
          const mockUser: User = {
            id: Date.now().toString(),
            email: userData.email,
            name: userData.name,
            role: 'user',
            createdAt: new Date().toISOString(),
            preferences: {
              theme: 'dark',
              language: 'es',
              notifications: true,
            },
          };

          set({
            user: mockUser,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error) {
          set({
            error: error instanceof Error ? error.message : 'Error de registro',
            isLoading: false,
          });
        }
      },

      logout: () => {
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      // Gestión de usuario
      updateUser: (userData) => {
        const { user } = get();
        if (user) {
          set({
            user: { ...user, ...userData },
          });
        }
      },

      updatePreferences: (preferences) => {
        const { user } = get();
        if (user) {
          set({
            user: {
              ...user,
              preferences: { ...user.preferences, ...preferences },
            },
          });
        }
      },

      // Utilidades
      clearError: () => set({ error: null }),
      setLoading: (loading) => set({ isLoading: loading }),

      refreshToken: async () => {
        // Aquí iría la lógica para refrescar el token
        console.log('Refreshing token...');
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
      skipHydration: true,
    }
  )
);

// Selectores útiles
export const useUser = () => useAuthStore((state) => state.user);
export const useIsAuthenticated = () => useAuthStore((state) => state.isAuthenticated);
export const useAuthLoading = () => useAuthStore((state) => state.isLoading);
export const useAuthError = () => useAuthStore((state) => state.error);

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type Theme = 'light' | 'dark' | 'system';
export type NotificationType = 'success' | 'error' | 'warning' | 'info';

export interface Notification {
  id: string;
  type: NotificationType;
  title: string;
  message?: string;
  duration?: number;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export interface ModalState {
  id: string;
  isOpen: boolean;
  title?: string;
  content?: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  onClose?: () => void;
}

interface UIState {
  // Tema
  theme: Theme;
  systemTheme: 'light' | 'dark';

  // Modales
  modals: ModalState[];

  // Notificaciones
  notifications: Notification[];

  // Estados de carga
  loadingStates: Record<string, boolean>;

  // Sidebar/Navigation
  sidebarOpen: boolean;
  mobileMenuOpen: boolean;

  // Búsqueda
  searchOpen: boolean;
  searchQuery: string;

  // Player expandido
  playerExpanded: boolean;
}

interface UIActions {
  // Tema
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;

  // Modales
  openModal: (modal: Omit<ModalState, 'isOpen'>) => void;
  closeModal: (modalId: string) => void;
  closeAllModals: () => void;

  // Notificaciones
  addNotification: (notification: Omit<Notification, 'id'>) => void;
  removeNotification: (notificationId: string) => void;
  clearNotifications: () => void;

  // Estados de carga
  setLoading: (key: string, loading: boolean) => void;
  isLoading: (key: string) => boolean;

  // Sidebar/Navigation
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleMobileMenu: () => void;
  setMobileMenuOpen: (open: boolean) => void;

  // Búsqueda
  toggleSearch: () => void;
  setSearchOpen: (open: boolean) => void;
  setSearchQuery: (query: string) => void;

  // Player
  togglePlayerExpanded: () => void;
  setPlayerExpanded: (expanded: boolean) => void;
}

type UIStore = UIState & UIActions;

const initialState: UIState = {
  theme: 'system',
  systemTheme: 'dark',
  modals: [],
  notifications: [],
  loadingStates: {},
  sidebarOpen: false,
  mobileMenuOpen: false,
  searchOpen: false,
  searchQuery: '',
  playerExpanded: false,
};

export const useUIStore = create<UIStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Tema
      setTheme: (theme) => {
        set({ theme });

        // Aplicar tema al documento
        const root = document.documentElement;
        const systemTheme = get().systemTheme;

        if (theme === 'system') {
          root.classList.toggle('dark', systemTheme === 'dark');
        } else {
          root.classList.toggle('dark', theme === 'dark');
        }
      },

      toggleTheme: () => {
        const currentTheme = get().theme;
        const nextTheme = currentTheme === 'light' ? 'dark' :
                         currentTheme === 'dark' ? 'system' : 'light';
        get().setTheme(nextTheme);
      },

      // Modales
      openModal: (modal) => {
        set((state) => ({
          modals: [...state.modals, { ...modal, isOpen: true }],
        }));
      },

      closeModal: (modalId) => {
        set((state) => ({
          modals: state.modals.map((modal) =>
            modal.id === modalId ? { ...modal, isOpen: false } : modal
          ),
        }));

        // Remover modal después de la animación
        setTimeout(() => {
          set((state) => ({
            modals: state.modals.filter((modal) => modal.id !== modalId),
          }));
        }, 300);
      },

      closeAllModals: () => {
        set((state) => ({
          modals: state.modals.map((modal) => ({ ...modal, isOpen: false })),
        }));

        // Limpiar modales después de la animación
        setTimeout(() => {
          set({ modals: [] });
        }, 300);
      },

      // Notificaciones
      addNotification: (notification) => {
        const id = Date.now().toString();
        const newNotification: Notification = {
          ...notification,
          id,
          duration: notification.duration ?? 5000,
        };

        set((state) => ({
          notifications: [...state.notifications, newNotification],
        }));

        // Auto-remover después de la duración
        if (newNotification.duration && newNotification.duration > 0) {
          setTimeout(() => {
            get().removeNotification(id);
          }, newNotification.duration);
        }
      },

      removeNotification: (notificationId) => {
        set((state) => ({
          notifications: state.notifications.filter(
            (notification) => notification.id !== notificationId
          ),
        }));
      },

      clearNotifications: () => {
        set({ notifications: [] });
      },

      // Estados de carga
      setLoading: (key, loading) => {
        set((state) => ({
          loadingStates: {
            ...state.loadingStates,
            [key]: loading,
          },
        }));
      },

      isLoading: (key) => {
        return get().loadingStates[key] ?? false;
      },

      // Sidebar/Navigation
      toggleSidebar: () => {
        set((state) => ({ sidebarOpen: !state.sidebarOpen }));
      },

      setSidebarOpen: (open) => {
        set({ sidebarOpen: open });
      },

      toggleMobileMenu: () => {
        set((state) => ({ mobileMenuOpen: !state.mobileMenuOpen }));
      },

      setMobileMenuOpen: (open) => {
        set({ mobileMenuOpen: open });
      },

      // Búsqueda
      toggleSearch: () => {
        set((state) => ({ searchOpen: !state.searchOpen }));
      },

      setSearchOpen: (open) => {
        set({ searchOpen: open });
      },

      setSearchQuery: (query) => {
        set({ searchQuery: query });
      },

      // Player
      togglePlayerExpanded: () => {
        set((state) => ({ playerExpanded: !state.playerExpanded }));
      },

      setPlayerExpanded: (expanded) => {
        set({ playerExpanded: expanded });
      },
    }),
    {
      name: 'ui-storage',
      partialize: (state) => ({
        theme: state.theme,
        sidebarOpen: state.sidebarOpen,
        playerExpanded: state.playerExpanded,
      }),
    }
  )
);

// Selectores útiles
export const useTheme = () => useUIStore((state) => state.theme);
export const useNotifications = () => useUIStore((state) => state.notifications);
export const useModals = () => useUIStore((state) => state.modals);
export const useSidebarOpen = () => useUIStore((state) => state.sidebarOpen);
export const useMobileMenuOpen = () => useUIStore((state) => state.mobileMenuOpen);
export const useSearchOpen = () => useUIStore((state) => state.searchOpen);
export const usePlayerExpanded = () => useUIStore((state) => state.playerExpanded);

// Hooks compuestos
export const useCurrentTheme = () => {
  const theme = useUIStore((state) => state.theme);
  const systemTheme = useUIStore((state) => state.systemTheme);

  return theme === 'system' ? systemTheme : theme;
};

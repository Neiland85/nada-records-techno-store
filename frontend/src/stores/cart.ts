import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CartItem {
  id: string;
  productId: string;
  name: string;
  price: number;
  image: string;
  quantity: number;
  variant?: {
    size?: string;
    color?: string;
    format?: 'vinyl' | 'cd' | 'digital';
  };
  addedAt: Date;
}

interface CartState {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
  isOpen: boolean;
  discountCode?: string;
  discountAmount: number;
}

interface CartActions {
  // Gestión del carrito
  addItem: (item: Omit<CartItem, 'id' | 'addedAt'>) => void;
  removeItem: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  clearCart: () => void;

  // Utilidades del carrito
  toggleCart: () => void;
  openCart: () => void;
  closeCart: () => void;

  // Códigos de descuento
  applyDiscount: (code: string) => Promise<boolean>;
  removeDiscount: () => void;

  // Cálculos
  calculateTotals: () => void;
}

type CartStore = CartState & CartActions;

const initialState: CartState = {
  items: [],
  totalItems: 0,
  totalPrice: 0,
  isOpen: false,
  discountAmount: 0,
};

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Gestión del carrito
      addItem: (newItem) => {
        const { items, calculateTotals } = get();

        // Verificar si el item ya existe
        const existingItem = items.find(
          (item) =>
            item.productId === newItem.productId &&
            JSON.stringify(item.variant) === JSON.stringify(newItem.variant)
        );

        if (existingItem) {
          // Incrementar cantidad si ya existe
          get().updateQuantity(existingItem.id, existingItem.quantity + newItem.quantity);
        } else {
          // Agregar nuevo item
          const cartItem: CartItem = {
            ...newItem,
            id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
            addedAt: new Date(),
          };

          set((state) => ({
            items: [...state.items, cartItem],
          }));

          calculateTotals();
        }
      },

      removeItem: (itemId) => {
        set((state) => ({
          items: state.items.filter((item) => item.id !== itemId),
        }));

        get().calculateTotals();
      },

      updateQuantity: (itemId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(itemId);
          return;
        }

        set((state) => ({
          items: state.items.map((item) =>
            item.id === itemId ? { ...item, quantity } : item
          ),
        }));

        get().calculateTotals();
      },

      clearCart: () => {
        set({
          items: [],
          totalItems: 0,
          totalPrice: 0,
          discountCode: undefined,
          discountAmount: 0,
        });
      },

      // Utilidades del carrito
      toggleCart: () => {
        set((state) => ({ isOpen: !state.isOpen }));
      },

      openCart: () => {
        set({ isOpen: true });
      },

      closeCart: () => {
        set({ isOpen: false });
      },

      // Códigos de descuento
      applyDiscount: async (code) => {
        try {
          // Aquí iría la validación del código de descuento con la API
          await new Promise(resolve => setTimeout(resolve, 500));

          // Simular validación
          const validCodes = ['TECHNO10', 'VINYL20', 'SUMMER15'];
          const isValid = validCodes.includes(code.toUpperCase());

          if (isValid) {
            const discountPercentage = code.toUpperCase() === 'TECHNO10' ? 0.1 :
                                     code.toUpperCase() === 'VINYL20' ? 0.2 : 0.15;

            set((state) => ({
              discountCode: code.toUpperCase(),
              discountAmount: state.totalPrice * discountPercentage,
            }));

            get().calculateTotals();
            return true;
          }

          return false;
        } catch (error) {
          console.error('Error applying discount:', error);
          return false;
        }
      },

      removeDiscount: () => {
        set({
          discountCode: undefined,
          discountAmount: 0,
        });

        get().calculateTotals();
      },

      // Cálculos
      calculateTotals: () => {
        const { items, discountAmount } = get();

        const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
        const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        const totalPrice = Math.max(0, subtotal - discountAmount);

        set({
          totalItems,
          totalPrice,
        });
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({
        items: state.items,
        discountCode: state.discountCode,
        discountAmount: state.discountAmount,
      }),
      skipHydration: true,
    }
  )
);

// Selectores útiles
export const useCartItems = () => useCartStore((state) => state.items);
export const useCartTotal = () => useCartStore((state) => state.totalPrice);
export const useCartItemCount = () => useCartStore((state) => state.totalItems);
export const useCartIsOpen = () => useCartStore((state) => state.isOpen);

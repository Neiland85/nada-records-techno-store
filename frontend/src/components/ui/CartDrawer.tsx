'use client';

import { useCartStore } from '@/stores';
import { Minus, Plus, ShoppingCart, Trash2, X } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';

interface CartDrawerProps {
  className?: string;
}

export function CartDrawer({ className = '' }: CartDrawerProps) {
  const {
    items,
    totalItems,
    totalPrice,
    isOpen,
    closeCart,
    updateQuantity,
    removeItem,
    clearCart
  } = useCartStore();

  if (!isOpen) return null;

  return (
    <div className={`fixed inset-0 bg-black/50 backdrop-blur-sm z-50 ${className}`}>
      {/* Overlay */}
      <div
        className="absolute inset-0"
        onClick={closeCart}
      />

      {/* Drawer */}
      <div className="absolute right-0 top-0 h-full w-full max-w-md bg-gray-900 border-l border-techno-primary/20 shadow-xl">
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-techno-primary/20">
            <div className="flex items-center space-x-2">
              <ShoppingCart className="w-6 h-6 text-techno-primary" />
              <h2 className="text-xl font-bold text-white">
                Carrito ({totalItems})
              </h2>
            </div>
            <button
              onClick={closeCart}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Cart Items */}
          <div className="flex-1 overflow-y-auto p-6">
            {items.length === 0 ? (
              <div className="text-center py-12">
                <ShoppingCart className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400 text-lg mb-2">Tu carrito está vacío</p>
                <p className="text-gray-500 text-sm">
                  ¡Agrega algunos tracks o álbumes!
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {items.map((item) => (
                  <div
                    key={item.id}
                    className="flex items-center space-x-4 bg-gray-800/50 rounded-lg p-4"
                  >
                    <Image
                      src={item.image}
                      alt={item.name}
                      width={64}
                      height={64}
                      className="w-16 h-16 object-cover rounded"
                    />
                    <div className="flex-1 min-w-0">
                      <h3 className="text-white font-medium truncate">
                        {item.name}
                      </h3>
                      <p className="text-gray-400 text-sm">
                        ${item.price.toFixed(2)}
                      </p>
                      {item.variant && (
                        <p className="text-gray-500 text-xs">
                          {item.variant.format && `${item.variant.format} • `}
                          {item.variant.size && `Talla: ${item.variant.size} • `}
                          {item.variant.color && `Color: ${item.variant.color}`}
                        </p>
                      )}
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <Minus className="w-4 h-4" />
                      </button>
                      <span className="text-white w-8 text-center">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="text-gray-400 hover:text-white transition-colors"
                      >
                        <Plus className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="text-red-400 hover:text-red-300 transition-colors ml-2"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Footer */}
          {items.length > 0 && (
            <div className="border-t border-techno-primary/20 p-6">
              <div className="flex justify-between items-center mb-4">
                <span className="text-gray-400">Total:</span>
                <span className="text-white text-xl font-bold">
                  ${totalPrice.toFixed(2)}
                </span>
              </div>

              <div className="space-y-3">
                <button
                  onClick={clearCart}
                  className="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded-lg transition-colors"
                >
                  Vaciar Carrito
                </button>
                <Link
                  href="/checkout"
                  onClick={closeCart}
                  className="block w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-3 px-4 rounded-lg text-center transition-colors"
                >
                  Ir al Checkout
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

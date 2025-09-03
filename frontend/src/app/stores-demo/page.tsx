'use client';

import { useAudioPlayerStore, useAuthStore, useCartStore, useUIStore } from '@/stores';
import { useState } from 'react';

export default function StoresDemoPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Auth Store
  const { login, logout, user, isAuthenticated, isLoading: authLoading } = useAuthStore();

  // Cart Store
  const { addItem, items, totalPrice, clearCart } = useCartStore();

  // UI Store
  const { addNotification, toggleTheme, theme } = useUIStore();

  // Audio Player Store
  const { playTrack, currentTrack, isPlaying, volume } = useAudioPlayerStore();

  const handleLogin = async () => {
    if (!email || !password) {
      addNotification({
        type: 'error',
        title: 'Error',
        message: 'Por favor ingresa email y contraseña',
      });
      return;
    }

    try {
      await login(email, password);
      addNotification({
        type: 'success',
        title: '¡Bienvenido!',
        message: 'Has iniciado sesión correctamente',
      });
    } catch (error) {
      console.error('Login error:', error);
      addNotification({
        type: 'error',
        title: 'Error de autenticación',
        message: 'Credenciales incorrectas',
      });
    }
  };

  const handleAddToCart = () => {
    addItem({
      productId: 'demo-track-1',
      name: 'Demo Track',
      price: 9.99,
      image: '/placeholder.jpg',
      quantity: 1,
      variant: { format: 'digital' },
    });

    addNotification({
      type: 'success',
      title: 'Agregado al carrito',
      message: 'Demo Track ha sido agregado',
    });
  };

  const handlePlayDemo = () => {
    playTrack({
      id: 'demo-1',
      title: 'Demo Track',
      artist: 'Demo Artist',
      duration: 180,
      url: '/demo-track.mp3',
      coverUrl: '/placeholder.jpg',
    });

    addNotification({
      type: 'info',
      title: 'Reproduciendo',
      message: 'Demo Track está sonando',
    });
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">
            Demo de Zustand Stores
          </h1>
          <p className="text-gray-400">
            Prueba todas las funcionalidades de nuestros stores de estado
          </p>
        </div>

        {/* Authentication Demo */}
        <div className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
            🔐 Autenticación
            {isAuthenticated && <span className="bg-green-600 text-white text-xs px-2 py-1 rounded">Conectado</span>}
          </h2>
          <p className="text-gray-400 mb-4">
            Prueba el sistema de login/logout
          </p>

          {!isAuthenticated ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
                  className="bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
                <input
                  type="password"
                  placeholder="Contraseña"
                  value={password}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                  className="bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white"
                />
              </div>
              <button
                onClick={handleLogin}
                disabled={authLoading}
                className="w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded disabled:opacity-50"
              >
                {authLoading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="text-center">
                <p className="text-green-400">¡Bienvenido, {user?.name}!</p>
                <p className="text-gray-400 text-sm">{user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="w-full bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded"
              >
                Cerrar Sesión
              </button>
            </div>
          )}
        </div>

        {/* Shopping Cart Demo */}
        <div className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
            🛒 Carrito de Compras
            <span className="bg-blue-600 text-white text-xs px-2 py-1 rounded">{items.length} items</span>
          </h2>
          <p className="text-gray-400 mb-4">
            Agrega productos y gestiona tu carrito
          </p>

          <div className="flex justify-between items-center mb-4">
            <span>Total: ${totalPrice.toFixed(2)}</span>
            <div className="space-x-2">
              <button
                onClick={handleAddToCart}
                className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded"
              >
                Agregar Demo Track
              </button>
              {items.length > 0 && (
                <button
                  onClick={clearCart}
                  className="bg-gray-700 hover:bg-gray-600 text-white py-2 px-4 rounded"
                >
                  Vaciar Carrito
                </button>
              )}
            </div>
          </div>

          {items.length > 0 && (
            <div className="space-y-2">
              <h4 className="font-medium text-white">Items en el carrito:</h4>
              {items.map((item) => (
                <div key={item.id} className="flex justify-between items-center bg-gray-800 p-2 rounded">
                  <span className="text-white">{item.name} (x{item.quantity})</span>
                  <span className="text-gray-300">${(item.price * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* UI Store Demo */}
        <div className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-2">🎨 UI State</h2>
          <p className="text-gray-400 mb-4">
            Gestiona el estado de la interfaz
          </p>

          <div className="flex items-center justify-between mb-4">
            <span className="text-white">Tema actual: {theme}</span>
            <button
              onClick={toggleTheme}
              className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded"
            >
              Cambiar Tema
            </button>
          </div>

          <div className="space-x-2">
            <button
              onClick={() => addNotification({
                type: 'success',
                title: '¡Éxito!',
                message: 'Esta es una notificación de éxito',
              })}
              className="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded"
            >
              Notificación Éxito
            </button>
            <button
              onClick={() => addNotification({
                type: 'error',
                title: 'Error',
                message: 'Esta es una notificación de error',
              })}
              className="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded"
            >
              Notificación Error
            </button>
          </div>
        </div>

        {/* Audio Player Demo */}
        <div className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
            🎵 Audio Player
            {isPlaying && <span className="bg-orange-600 text-white text-xs px-2 py-1 rounded">Reproduciendo</span>}
          </h2>
          <p className="text-gray-400 mb-4">
            Controla la reproducción de audio
          </p>

          <div className="text-center mb-4">
            {currentTrack ? (
              <div>
                <p className="font-medium text-white">{currentTrack.title}</p>
                <p className="text-gray-400">{currentTrack.artist}</p>
                <p className="text-sm text-gray-500">Volumen: {Math.round(volume * 100)}%</p>
              </div>
            ) : (
              <p className="text-gray-400">No hay pista reproduciéndose</p>
            )}
          </div>

          <button
            onClick={handlePlayDemo}
            className="w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded"
          >
            {isPlaying ? 'Pausar' : 'Reproducir Demo Track'}
          </button>
        </div>

        {/* Store Status Summary */}
        <div className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6">
          <h2 className="text-xl font-bold text-white mb-2">📊 Estado de los Stores</h2>
          <p className="text-gray-400 mb-4">
            Resumen del estado actual de todos los stores
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div className="bg-gray-800 p-4 rounded">
              <div className="text-2xl font-bold text-green-400">
                {isAuthenticated ? '✅' : '❌'}
              </div>
              <div className="text-sm text-gray-400">Auth</div>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <div className="text-2xl font-bold text-blue-400">
                {items.length}
              </div>
              <div className="text-sm text-gray-400">Cart Items</div>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <div className="text-2xl font-bold text-purple-400">
                {theme}
              </div>
              <div className="text-sm text-gray-400">Theme</div>
            </div>
            <div className="bg-gray-800 p-4 rounded">
              <div className="text-2xl font-bold text-orange-400">
                {isPlaying ? '▶️' : '⏸️'}
              </div>
              <div className="text-sm text-gray-400">Audio</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

'use client';

import { AudioLines, Menu, Search, ShoppingCart, User, X } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { useAuthStore, useCartStore, useUIStore } from '../../stores';
import { CartDrawer } from '../ui/CartDrawer';
import { SearchBar } from '../ui/SearchBar';

interface HeaderProps {
  className?: string;
}

export function Header({ className = '' }: HeaderProps) {
  // Estado local para menú móvil (temporal, luego migraremos a UI store)
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  // Zustand stores
  const cartItemCount = useCartStore((state) => state.totalItems);
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const user = useAuthStore((state) => state.user);
  const { toggleSearch } = useUIStore();

  return (
    <header className={`bg-black/90 backdrop-blur-lg border-b border-techno-primary/20 ${className}`}>
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <AudioLines className="w-8 h-8 text-techno-primary" />
            <span className="text-xl font-bold text-white">Nada Records</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-300 hover:text-techno-primary transition-colors">
              Inicio
            </Link>
            <Link href="/tracks" className="text-gray-300 hover:text-techno-primary transition-colors">
              Tracks
            </Link>
            <Link href="/albums" className="text-gray-300 hover:text-techno-primary transition-colors">
              Álbumes
            </Link>
            <Link href="/about" className="text-gray-300 hover:text-techno-primary transition-colors">
              Sobre
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleSearch}
              className="text-gray-300 hover:text-techno-primary transition-colors"
            >
              <Search className="w-5 h-5" />
            </button>
            <button
              onClick={() => useCartStore.getState().openCart()}
              className="text-gray-300 hover:text-techno-primary transition-colors relative"
            >
              <ShoppingCart className="w-5 h-5" />
              {cartItemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-techno-primary text-black text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                  {cartItemCount > 99 ? '99+' : cartItemCount}
                </span>
              )}
            </button>
            <Link
              href={isAuthenticated ? "/dashboard" : "/auth"}
              className="text-gray-300 hover:text-techno-primary transition-colors"
            >
              <User className="w-5 h-5" />
            </Link>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden text-gray-300 hover:text-techno-primary transition-colors"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <nav className="md:hidden mt-4 pb-4 border-t border-techno-primary/20 pt-4">
            <div className="flex flex-col space-y-4">
              <Link
                href="/"
                className="text-gray-300 hover:text-techno-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Inicio
              </Link>
              <Link
                href="/tracks"
                className="text-gray-300 hover:text-techno-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Tracks
              </Link>
              <Link
                href="/albums"
                className="text-gray-300 hover:text-techno-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Álbumes
              </Link>
              <Link
                href="/about"
                className="text-gray-300 hover:text-techno-primary transition-colors"
                onClick={() => setIsMenuOpen(false)}
              >
                Sobre
              </Link>

              {/* User section in mobile menu */}
              {isAuthenticated && user && (
                <>
                  <div className="border-t border-techno-primary/20 pt-4 mt-4">
                    <div className="text-sm text-gray-400 mb-2">
                      Hola, {user.name}
                    </div>
                    <Link
                      href="/dashboard"
                      className="text-gray-300 hover:text-techno-primary transition-colors block"
                      onClick={() => setIsMenuOpen(false)}
                    >
                      Dashboard
                    </Link>
                  </div>
                </>
              )}
            </div>
          </nav>
        )}
      </div>

      {/* Search Bar */}
      <SearchBar />

      {/* Cart Drawer */}
      <CartDrawer />
    </header>
  );
}

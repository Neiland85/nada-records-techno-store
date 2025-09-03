'use client';

import { ReactNode } from 'react';
import { Header } from '../';
import { CartDrawer } from '../ui/CartDrawer';
import { SearchBar } from '../ui/SearchBar';

interface RootLayoutProps {
  children: ReactNode;
}

export function RootLayout({ children }: RootLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black">
      <Header />
      <main className="flex-1">
        {children}
      </main>

      {/* Global Components */}
      <SearchBar />
      <CartDrawer />

      {/* Footer */}
      <footer className="bg-black border-t border-techno-primary/20 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center text-gray-400">
            <p>&copy; 2025 Nada Records. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

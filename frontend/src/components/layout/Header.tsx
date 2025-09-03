'use client';

import { AudioLines, Menu, Search, ShoppingCart, User, X } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

interface HeaderProps {
  className?: string;
}

export function Header({ className = '' }: HeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

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
            <button className="text-gray-300 hover:text-techno-primary transition-colors">
              <Search className="w-5 h-5" />
            </button>
            <button className="text-gray-300 hover:text-techno-primary transition-colors">
              <ShoppingCart className="w-5 h-5" />
            </button>
            <button className="text-gray-300 hover:text-techno-primary transition-colors">
              <User className="w-5 h-5" />
            </button>

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
            </div>
          </nav>
        )}
      </div>
    </header>
  );
}

'use client';

import { useUIStore } from '@/stores';
import { Search, X } from 'lucide-react';

interface SearchBarProps {
  className?: string;
}

export function SearchBar({ className = '' }: SearchBarProps) {
  const { searchOpen, setSearchOpen, searchQuery, setSearchQuery } = useUIStore();

  if (!searchOpen) return null;

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Aquí iría la lógica de búsqueda
    console.log('Searching for:', searchQuery);
  };

  return (
    <div className={`fixed inset-0 bg-black/90 backdrop-blur-lg z-50 flex items-center justify-center p-4 ${className}`}>
      <div className="w-full max-w-2xl">
        <form onSubmit={handleSearch} className="relative">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Buscar tracks, álbumes, artistas..."
              className="w-full pl-12 pr-12 py-4 bg-gray-900/50 border border-techno-primary/30 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-techno-primary focus:ring-1 focus:ring-techno-primary text-lg"
              autoFocus
            />
            <button
              type="button"
              onClick={() => setSearchOpen(false)}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </form>

        {/* Resultados de búsqueda (placeholder) */}
        {searchQuery && (
          <div className="mt-6 bg-gray-900/30 rounded-lg border border-techno-primary/20 p-4">
            <div className="text-gray-400 text-sm mb-2">
              Resultados para &quot;{searchQuery}&quot;
            </div>
            <div className="text-gray-500 text-center py-8">
              🔍 Funcionalidad de búsqueda próximamente...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import { Filter, Grid, List, Play, Search, ShoppingCart } from 'lucide-react';
import Image from 'next/image';
import { useState } from 'react';
import { useCartStore, useUIStore } from '../../stores';

export default function TracksPage() {
  const { addItem } = useCartStore();
  const { setSearchOpen } = useUIStore();

  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('newest');

  // Mock data - en producción vendría de la API
  const tracks = [
    {
      id: '1',
      title: 'Neon Pulse',
      artist: 'DJ Vortex',
      price: 2.99,
      image: '/placeholder.jpg',
      duration: '4:23',
      genre: 'Techno',
      bpm: 140,
      releaseDate: '2025-01-15',
      isNew: true,
      description: 'Un beat techno clásico con toques modernos',
    },
    {
      id: '2',
      title: 'Dark Matter',
      artist: 'Synth Master',
      price: 3.49,
      image: '/placeholder.jpg',
      duration: '5:12',
      genre: 'Dark Techno',
      bpm: 135,
      releaseDate: '2025-01-10',
      isNew: false,
      description: 'Atmósferas oscuras y beats profundos',
    },
    {
      id: '3',
      title: 'Electric Dreams',
      artist: 'Pulse Wave',
      price: 2.79,
      image: '/placeholder.jpg',
      duration: '3:58',
      genre: 'Electro',
      bpm: 128,
      releaseDate: '2025-01-08',
      isNew: true,
      description: 'Energía electro con sintetizadores vintage',
    },
    {
      id: '4',
      title: 'Industrial Revolution',
      artist: 'Machine Beat',
      price: 4.99,
      image: '/placeholder.jpg',
      duration: '6:45',
      genre: 'Industrial',
      bpm: 145,
      releaseDate: '2025-01-05',
      isNew: false,
      description: 'Sonidos industriales con beats agresivos',
    },
    {
      id: '5',
      title: 'Minimal Wave',
      artist: 'Clean Sound',
      price: 3.29,
      image: '/placeholder.jpg',
      duration: '4:12',
      genre: 'Minimal',
      bpm: 125,
      releaseDate: '2025-01-03',
      isNew: true,
      description: 'Minimalismo techno con groove perfecto',
    },
    {
      id: '6',
      title: 'Acid Rain',
      artist: 'Chemical Brothers',
      price: 3.99,
      image: '/placeholder.jpg',
      duration: '5:33',
      genre: 'Acid',
      bpm: 130,
      releaseDate: '2025-01-01',
      isNew: false,
      description: 'Acid house con toques modernos',
    },
  ];

  const genres = ['all', 'Techno', 'Dark Techno', 'Electro', 'Industrial', 'Minimal', 'Acid'];

  const filteredTracks = tracks.filter(track =>
    selectedGenre === 'all' || track.genre === selectedGenre
  );

  const sortedTracks = [...filteredTracks].sort((a, b) => {
    switch (sortBy) {
      case 'newest':
        return new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime();
      case 'oldest':
        return new Date(a.releaseDate).getTime() - new Date(b.releaseDate).getTime();
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'title':
        return a.title.localeCompare(b.title);
      default:
        return 0;
    }
  });

  const handleAddToCart = (track: typeof tracks[0]) => {
    addItem({
      productId: track.id,
      name: track.title,
      price: track.price,
      image: track.image,
      quantity: 1,
      variant: { format: 'digital' },
    });
  };

  return (
    <div className="min-h-screen bg-black">
      {/* Header Section */}
      <section className="bg-gradient-to-r from-gray-900 to-black py-16">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-4">
              Tracks
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Explora nuestra colección completa de tracks techno. Desde beats clásicos hasta las últimas producciones.
            </p>
          </div>
        </div>
      </section>

      {/* Filters and Controls */}
      <section className="py-8 bg-gray-900 border-b border-techno-primary/20">
        <div className="container mx-auto px-4">
          <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
            {/* Search */}
            <div className="flex items-center gap-4">
              <button
                onClick={() => setSearchOpen(true)}
                className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors"
              >
                <Search className="w-4 h-4" />
                Buscar
              </button>
            </div>

            {/* Filters */}
            <div className="flex flex-wrap items-center gap-4">
              {/* Genre Filter */}
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <select
                  value={selectedGenre}
                  onChange={(e) => setSelectedGenre(e.target.value)}
                  className="bg-gray-800 text-white px-3 py-2 rounded border border-gray-600 focus:border-techno-primary focus:outline-none"
                >
                  {genres.map(genre => (
                    <option key={genre} value={genre}>
                      {genre === 'all' ? 'Todos los Géneros' : genre}
                    </option>
                  ))}
                </select>
              </div>

              {/* Sort */}
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="bg-gray-800 text-white px-3 py-2 rounded border border-gray-600 focus:border-techno-primary focus:outline-none"
              >
                <option value="newest">Más Recientes</option>
                <option value="oldest">Más Antiguos</option>
                <option value="price-low">Precio: Menor a Mayor</option>
                <option value="price-high">Precio: Mayor a Menor</option>
                <option value="title">Título A-Z</option>
              </select>

              {/* View Mode */}
              <div className="flex bg-gray-800 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 rounded ${viewMode === 'grid' ? 'bg-techno-primary text-black' : 'text-gray-400 hover:text-white'}`}
                >
                  <Grid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 rounded ${viewMode === 'list' ? 'bg-techno-primary text-black' : 'text-gray-400 hover:text-white'}`}
                >
                  <List className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Results Count */}
          <div className="mt-4 text-gray-400">
            {sortedTracks.length} track{sortedTracks.length !== 1 ? 's' : ''} encontrado{sortedTracks.length !== 1 ? 's' : ''}
          </div>
        </div>
      </section>

      {/* Tracks Grid/List */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {sortedTracks.map((track) => (
                <div
                  key={track.id}
                  className="bg-gray-900/50 border border-techno-primary/20 rounded-lg overflow-hidden hover:border-techno-primary/50 transition-all duration-300 group"
                >
                  <div className="relative">
                    <Image
                      src={track.image}
                      alt={track.title}
                      width={300}
                      height={300}
                      className="w-full h-48 object-cover"
                    />
                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <button className="bg-techno-primary text-black p-3 rounded-full hover:scale-110 transition-transform">
                        <Play className="w-6 h-6" />
                      </button>
                    </div>
                    {track.isNew && (
                      <div className="absolute top-3 left-3 bg-techno-primary text-black px-2 py-1 rounded text-xs font-bold">
                        NUEVO
                      </div>
                    )}
                  </div>

                  <div className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1 min-w-0">
                        <h3 className="text-lg font-bold text-white mb-1 truncate">{track.title}</h3>
                        <p className="text-gray-400 text-sm truncate">{track.artist}</p>
                      </div>
                      <div className="text-right ml-2">
                        <p className="text-xl font-bold text-techno-primary">${track.price}</p>
                        <p className="text-xs text-gray-500">{track.duration}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded">
                        {track.genre} • {track.bpm} BPM
                      </span>
                    </div>

                    <button
                      onClick={() => handleAddToCart(track)}
                      className="w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded transition-colors flex items-center justify-center gap-2"
                    >
                      <ShoppingCart className="w-4 h-4" />
                      Agregar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-4">
              {sortedTracks.map((track) => (
                <div
                  key={track.id}
                  className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-4 hover:border-techno-primary/50 transition-all duration-300"
                >
                  <div className="flex items-center gap-4">
                    <div className="relative w-16 h-16 flex-shrink-0">
                      <Image
                        src={track.image}
                        alt={track.title}
                        width={64}
                        height={64}
                        className="w-full h-full object-cover rounded"
                      />
                      <button className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center rounded">
                        <Play className="w-4 h-4 text-techno-primary" />
                      </button>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-lg font-bold text-white">{track.title}</h3>
                          <p className="text-gray-400">{track.artist}</p>
                          <p className="text-sm text-gray-500">{track.description}</p>
                        </div>
                        <div className="text-right ml-4">
                          <p className="text-xl font-bold text-techno-primary">${track.price}</p>
                          <p className="text-xs text-gray-500">{track.duration}</p>
                        </div>
                      </div>

                      <div className="flex items-center justify-between mt-2">
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <span>{track.genre}</span>
                          <span>{track.bpm} BPM</span>
                          <span>{track.releaseDate}</span>
                        </div>
                        <button
                          onClick={() => handleAddToCart(track)}
                          className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-2 px-4 rounded transition-colors flex items-center gap-2"
                        >
                          <ShoppingCart className="w-4 h-4" />
                          Agregar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Load More */}
      <section className="py-12 bg-gray-900">
        <div className="container mx-auto px-4 text-center">
          <button className="bg-transparent border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-black font-bold py-3 px-8 rounded-lg transition-all duration-300">
            Cargar Más Tracks
          </button>
        </div>
      </section>
    </div>
  );
}

'use client';

import { useCartStore, useUIStore } from '@/stores';
import { Filter, Grid, List, Play, Search, ShoppingCart } from 'lucide-react';
import Image from 'next/image';
import { useState } from 'react';

export default function AlbumsPage() {
  const { addItem } = useCartStore();
  const { setSearchOpen } = useUIStore();

  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [selectedGenre, setSelectedGenre] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('newest');

  // Mock data - en producción vendría de la API
  const albums = [
    {
      id: 'album-1',
      title: 'Midnight Sessions',
      artist: 'Various Artists',
      price: 12.99,
      image: '/placeholder.jpg',
      trackCount: 12,
      duration: '68:45',
      genre: 'Techno',
      releaseDate: '2025-01-15',
      isNew: true,
      description: 'Una colección de sesiones nocturnas techno de los mejores productores',
      tracks: [
        'Opening Ceremony',
        'Deep Underground',
        'Techno Pulse',
        'Midnight Drive',
        'Dark Atmosphere',
        'Industrial Beat',
        'Minimal Groove',
        'Acid Dreams',
        'Synth Wave',
        'Closing Ritual',
        'Bonus Track 1',
        'Bonus Track 2'
      ]
    },
    {
      id: 'album-2',
      title: 'Techno Revolution',
      artist: 'DJ Vortex',
      price: 15.99,
      image: '/placeholder.jpg',
      trackCount: 10,
      duration: '62:30',
      genre: 'Dark Techno',
      releaseDate: '2025-01-10',
      isNew: false,
      description: 'La revolución techno llega con beats oscuros y atmosféricos',
      tracks: [
        'Revolution Start',
        'Dark Forces',
        'Technological Advance',
        'Digital Age',
        'Future Sound',
        'Machine Learning',
        'AI Dreams',
        'Cyber Punk',
        'Virtual Reality',
        'Revolution End'
      ]
    },
    {
      id: 'album-3',
      title: 'Electric Dreams',
      artist: 'Pulse Wave',
      price: 11.99,
      image: '/placeholder.jpg',
      trackCount: 8,
      duration: '45:20',
      genre: 'Electro',
      releaseDate: '2025-01-08',
      isNew: true,
      description: 'Sueños eléctricos con sintetizadores vintage y beats modernos',
      tracks: [
        'Electric Awakening',
        'Dream Sequence',
        'Wave Function',
        'Pulse Modulation',
        'Digital Dreams',
        'Analog Heart',
        'Electric Soul',
        'Dream Ending'
      ]
    },
    {
      id: 'album-4',
      title: 'Industrial Strength',
      artist: 'Machine Beat',
      price: 14.99,
      image: '/placeholder.jpg',
      trackCount: 11,
      duration: '71:15',
      genre: 'Industrial',
      releaseDate: '2025-01-05',
      isNew: false,
      description: 'Fuerza industrial con beats agresivos y sonidos mecánicos',
      tracks: [
        'Factory Floor',
        'Machine Age',
        'Industrial Revolution',
        'Steel & Concrete',
        'Gear Up',
        'Power Plant',
        'Assembly Line',
        'Metal Works',
        'Circuit Board',
        'Final Assembly',
        'Quality Control'
      ]
    },
    {
      id: 'album-5',
      title: 'Minimal Movement',
      artist: 'Clean Sound',
      price: 13.49,
      image: '/placeholder.jpg',
      trackCount: 9,
      duration: '54:10',
      genre: 'Minimal',
      releaseDate: '2025-01-03',
      isNew: true,
      description: 'El movimiento minimal llega con grooves perfectos y sonidos puros',
      tracks: [
        'Minimal Beginning',
        'Clean Groove',
        'Pure Sound',
        'Essential Beat',
        'Simple Melody',
        'Clear Vision',
        'Minimal Dance',
        'Pure Energy',
        'Movement End'
      ]
    },
    {
      id: 'album-6',
      title: 'Acid Evolution',
      artist: 'Chemical Brothers',
      price: 16.99,
      image: '/placeholder.jpg',
      trackCount: 13,
      duration: '78:30',
      genre: 'Acid',
      releaseDate: '2025-01-01',
      isNew: false,
      description: 'La evolución del acid house con toques modernos y clásicos',
      tracks: [
        'Acid Rain',
        'Chemical Reaction',
        'Synthesizer Soul',
        'Digital Acid',
        'Analog Dreams',
        'Bass Line Evolution',
        'Filter Sweep',
        'Resonance Peak',
        'Square Wave',
        'Sawtooth Symphony',
        'Acid Trip',
        'Chemical Burn',
        'Evolution Complete'
      ]
    },
  ];

  const genres = ['all', 'Techno', 'Dark Techno', 'Electro', 'Industrial', 'Minimal', 'Acid'];

  const filteredAlbums = albums.filter(album =>
    selectedGenre === 'all' || album.genre === selectedGenre
  );

  const sortedAlbums = [...filteredAlbums].sort((a, b) => {
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

  const handleAddToCart = (album: typeof albums[0]) => {
    addItem({
      productId: album.id,
      name: album.title,
      price: album.price,
      image: album.image,
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
              Álbumes
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Colecciones completas de los mejores productores techno. Sumérgete en experiencias musicales completas.
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
            {sortedAlbums.length} álbum{sortedAlbums.length !== 1 ? 'es' : ''} encontrado{sortedAlbums.length !== 1 ? 's' : ''}
          </div>
        </div>
      </section>

      {/* Albums Grid/List */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          {viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {sortedAlbums.map((album) => (
                <div
                  key={album.id}
                  className="bg-gray-900/50 border border-techno-primary/20 rounded-lg overflow-hidden hover:border-techno-primary/50 transition-all duration-300 group"
                >
                  <div className="relative">
                    <Image
                      src={album.image}
                      alt={album.title}
                      width={400}
                      height={400}
                      className="w-full h-64 object-cover"
                    />
                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <button className="bg-techno-primary text-black p-4 rounded-full hover:scale-110 transition-transform">
                        <Play className="w-8 h-8" />
                      </button>
                    </div>
                    {album.isNew && (
                      <div className="absolute top-4 left-4 bg-techno-primary text-black px-2 py-1 rounded text-sm font-bold">
                        NUEVO
                      </div>
                    )}
                  </div>

                  <div className="p-6">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1 min-w-0">
                        <h3 className="text-xl font-bold text-white mb-1">{album.title}</h3>
                        <p className="text-gray-400">{album.artist}</p>
                        <p className="text-sm text-gray-500 mt-1">{album.description}</p>
                      </div>
                      <div className="text-right ml-4">
                        <p className="text-2xl font-bold text-techno-primary">${album.price}</p>
                      </div>
                    </div>

                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <span className="bg-gray-800 px-2 py-1 rounded">{album.genre}</span>
                        <span>{album.trackCount} tracks</span>
                        <span>{album.duration}</span>
                      </div>
                    </div>

                    <button
                      onClick={() => handleAddToCart(album)}
                      className="w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-3 px-6 rounded transition-colors flex items-center justify-center gap-2"
                    >
                      <ShoppingCart className="w-5 h-5" />
                      Agregar al Carrito
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="space-y-6">
              {sortedAlbums.map((album) => (
                <div
                  key={album.id}
                  className="bg-gray-900/50 border border-techno-primary/20 rounded-lg p-6 hover:border-techno-primary/50 transition-all duration-300"
                >
                  <div className="flex gap-6">
                    <div className="relative w-32 h-32 flex-shrink-0">
                      <Image
                        src={album.image}
                        alt={album.title}
                        width={128}
                        height={128}
                        className="w-full h-full object-cover rounded"
                      />
                      <button className="absolute inset-0 bg-black/50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center rounded">
                        <Play className="w-6 h-6 text-techno-primary" />
                      </button>
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h3 className="text-2xl font-bold text-white mb-1">{album.title}</h3>
                          <p className="text-gray-400 text-lg">{album.artist}</p>
                          <p className="text-gray-500 mt-1">{album.description}</p>
                        </div>
                        <div className="text-right ml-4">
                          <p className="text-3xl font-bold text-techno-primary">${album.price}</p>
                          <p className="text-sm text-gray-500">{album.trackCount} tracks • {album.duration}</p>
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <span className="bg-gray-800 text-gray-300 px-3 py-1 rounded text-sm">{album.genre}</span>
                          <span className="text-gray-500 text-sm">{album.releaseDate}</span>
                        </div>
                        <button
                          onClick={() => handleAddToCart(album)}
                          className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-3 px-6 rounded transition-colors flex items-center gap-2"
                        >
                          <ShoppingCart className="w-5 h-5" />
                          Agregar al Carrito
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
            Cargar Más Álbumes
          </button>
        </div>
      </section>
    </div>
  );
}

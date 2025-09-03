import { useAuthStore, useCartStore } from '@/stores';
import { Disc, Music, Play, ShoppingCart } from 'lucide-react';
import Image from 'next/image';
import Link from 'next/link';

export default function Home() {
  const { addItem } = useCartStore();
  const { isAuthenticated } = useAuthStore();

  const featuredTracks = [
    {
      id: '1',
      title: 'Neon Pulse',
      artist: 'DJ Vortex',
      price: 2.99,
      image: '/placeholder.jpg',
      duration: '4:23',
      genre: 'Techno',
      isNew: true,
    },
    {
      id: '2',
      title: 'Dark Matter',
      artist: 'Synth Master',
      price: 3.49,
      image: '/placeholder.jpg',
      duration: '5:12',
      genre: 'Dark Techno',
      isNew: false,
    },
    {
      id: '3',
      title: 'Electric Dreams',
      artist: 'Pulse Wave',
      price: 2.79,
      image: '/placeholder.jpg',
      duration: '3:58',
      genre: 'Electro',
      isNew: true,
    },
  ];

  const newReleases = [
    {
      id: 'album-1',
      title: 'Midnight Sessions',
      artist: 'Various Artists',
      price: 12.99,
      image: '/placeholder.jpg',
      trackCount: 12,
      releaseDate: '2025',
    },
    {
      id: 'album-2',
      title: 'Techno Revolution',
      artist: 'DJ Vortex',
      price: 15.99,
      image: '/placeholder.jpg',
      trackCount: 10,
      releaseDate: '2025',
    },
  ];

  const handleAddToCart = (track: typeof featuredTracks[0]) => {
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
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* Background Video/Image */}
        <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black">
          <div className="absolute inset-0 bg-[url('/techno-bg.jpg')] bg-cover bg-center opacity-20"></div>
          <div className="absolute inset-0 bg-techno-primary/10"></div>
        </div>

        {/* Animated Background Elements */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-techno-primary rounded-full animate-pulse"></div>
          <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-techno-primary rounded-full animate-ping"></div>
          <div className="absolute bottom-1/4 left-1/3 w-3 h-3 bg-techno-primary/50 rounded-full animate-bounce"></div>
          <div className="absolute bottom-1/3 right-1/4 w-2 h-2 bg-techno-primary rounded-full animate-pulse delay-1000"></div>
        </div>

        {/* Hero Content */}
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto">
          <h1 className="text-6xl md:text-8xl font-bold text-white mb-6 tracking-wider">
            NADA
            <span className="block text-techno-primary">RECORDS</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl mx-auto">
            La vanguardia del techno underground. Descubre beats que definen el futuro de la música electrónica.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/tracks"
              className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300 transform hover:scale-105"
            >
              Explorar Tracks
            </Link>
            <Link
              href="/albums"
              className="border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300"
            >
              Ver Álbumes
            </Link>
          </div>
        </div>

        {/* Scroll Indicator */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-techno-primary rounded-full flex justify-center">
            <div className="w-1 h-3 bg-techno-primary rounded-full mt-2 animate-pulse"></div>
          </div>
        </div>
      </section>

      {/* Featured Tracks Section */}
      <section className="py-20 bg-black">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Tracks Destacados
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Los beats más calientes del momento. Sumérgete en el sonido del futuro.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {featuredTracks.map((track) => (
              <div
                key={track.id}
                className="bg-gray-900/50 border border-techno-primary/20 rounded-lg overflow-hidden hover:border-techno-primary/50 transition-all duration-300 group"
              >
                <div className="relative">
                  <Image
                    src={track.image}
                    alt={track.title}
                    width={400}
                    height={192}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <button className="bg-techno-primary text-black p-4 rounded-full hover:scale-110 transition-transform">
                      <Play className="w-6 h-6" />
                    </button>
                  </div>
                  {track.isNew && (
                    <div className="absolute top-4 left-4 bg-techno-primary text-black px-2 py-1 rounded text-sm font-bold">
                      NUEVO
                    </div>
                  )}
                </div>

                <div className="p-6">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="text-xl font-bold text-white mb-1">{track.title}</h3>
                      <p className="text-gray-400">{track.artist}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-techno-primary">${track.price}</p>
                      <p className="text-sm text-gray-500">{track.duration}</p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500 bg-gray-800 px-2 py-1 rounded">
                      {track.genre}
                    </span>
                    <button
                      onClick={() => handleAddToCart(track)}
                      className="bg-techno-primary hover:bg-techno-primary/80 text-black px-4 py-2 rounded font-bold transition-colors flex items-center gap-2"
                    >
                      <ShoppingCart className="w-4 h-4" />
                      Agregar
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link
              href="/tracks"
              className="inline-flex items-center gap-2 bg-transparent border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-black font-bold py-3 px-8 rounded-lg transition-all duration-300"
            >
              Ver Todos los Tracks
              <Music className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* New Releases Section */}
      <section className="py-20 bg-gray-900">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Nuevos Lanzamientos
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Los últimos álbumes que están revolucionando la escena techno.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {newReleases.map((album) => (
              <div
                key={album.id}
                className="bg-black/50 border border-techno-primary/20 rounded-lg overflow-hidden hover:border-techno-primary/50 transition-all duration-300 group"
              >
                <div className="relative">
                  <Image
                    src={album.image}
                    alt={album.title}
                    width={400}
                    height={256}
                    className="w-full h-64 object-cover"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <button className="bg-techno-primary text-black p-4 rounded-full hover:scale-110 transition-transform">
                      <Play className="w-8 h-8" />
                    </button>
                  </div>
                </div>

                <div className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-2xl font-bold text-white mb-1">{album.title}</h3>
                      <p className="text-gray-400">{album.artist}</p>
                      <p className="text-sm text-gray-500">{album.trackCount} tracks • {album.releaseDate}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-3xl font-bold text-techno-primary">${album.price}</p>
                    </div>
                  </div>

                  <button className="w-full bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-3 px-6 rounded transition-colors flex items-center justify-center gap-2">
                    <ShoppingCart className="w-5 h-5" />
                    Agregar al Carrito
                  </button>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Link
              href="/albums"
              className="inline-flex items-center gap-2 bg-transparent border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-black font-bold py-3 px-8 rounded-lg transition-all duration-300"
            >
              Explorar Todos los Álbumes
              <Disc className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-black">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold text-techno-primary mb-2 group-hover:scale-110 transition-transform">
                500+
              </div>
              <div className="text-gray-400">Tracks Disponibles</div>
            </div>
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold text-techno-primary mb-2 group-hover:scale-110 transition-transform">
                50+
              </div>
              <div className="text-gray-400">Artistas</div>
            </div>
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold text-techno-primary mb-2 group-hover:scale-110 transition-transform">
                1000+
              </div>
              <div className="text-gray-400">Descargas</div>
            </div>
            <div className="group">
              <div className="text-4xl md:text-5xl font-bold text-techno-primary mb-2 group-hover:scale-110 transition-transform">
                24/7
              </div>
              <div className="text-gray-400">Streaming</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-black via-gray-900 to-black">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            ¿Listo para la Experiencia?
          </h2>
          <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
            Únete a la comunidad techno más exclusiva. Descubre, compra y disfruta de la mejor música electrónica.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {!isAuthenticated ? (
              <>
                <Link
                  href="/auth"
                  className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300 transform hover:scale-105"
                >
                  Crear Cuenta
                </Link>
                <Link
                  href="/auth"
                  className="border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300"
                >
                  Iniciar Sesión
                </Link>
              </>
            ) : (
              <Link
                href="/dashboard"
                className="bg-techno-primary hover:bg-techno-primary/80 text-black font-bold py-4 px-8 rounded-lg text-lg transition-all duration-300 transform hover:scale-105"
              >
                Ir al Dashboard
              </Link>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}

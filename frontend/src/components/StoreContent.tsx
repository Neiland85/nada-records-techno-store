'use client';


export default function StoreContent() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8 text-neon-pink">
          Nada Records Techno Store
        </h1>
        <p className="text-center text-lg mb-8">
          Bienvenido a la tienda de música techno. Aquí encontrarás los mejores vinilos y tracks.
        </p>
        {/* Aquí irá el contenido extraído de App.tsx del proyecto Vite */}
        <div className="text-center">
          <p>Contenido de la tienda próximamente...</p>
        </div>
      </div>
    </div>
  );
}

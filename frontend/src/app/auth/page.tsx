'use client';


export default function AuthPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white flex items-center justify-center">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-6 text-neon-pink">
          Iniciar Sesión
        </h1>
        {/* Aquí irá el componente AuthLayout extraído de Vite */}
        <p className="text-center">Componente de autenticación próximamente...</p>
      </div>
    </div>
  );
}

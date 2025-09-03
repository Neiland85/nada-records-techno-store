'use client';

import { AudioUploadForm } from '@/components/upload/AudioUploadForm';

export default function UploadExamplePage() {
  // Para este ejemplo, usaremos un albumId de ejemplo
  const exampleAlbumId = 'example-album-123';

  const handleUploadSuccess = (data: {
    uploadId: string;
    fileUrl: string;
    fileSize: number;
    filename: string;
    message: string;
  }) => {
    console.log('🎵 Upload successful!', data);

    // Aquí puedes:
    // 1. Guardar la información en tu base de datos
    // 2. Actualizar el estado de la aplicación
    // 3. Mostrar una notificación al usuario
    // 4. Redirigir a otra página

    alert(`Archivo subido exitosamente: ${data.filename}`);
  };

  const handleUploadError = (error: string) => {
    console.error('❌ Upload failed:', error);
    alert(`Error al subir archivo: ${error}`);
  };

  const handleUploadStart = () => {
    console.log('🚀 Starting upload...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4">
              🎵 Nada Records Upload
            </h1>
            <p className="text-gray-300 text-lg">
              Sube tus tracks techno y almacénalos en la nube
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-8 border border-white/20">
            <AudioUploadForm
              albumId={exampleAlbumId}
              onSuccess={handleUploadSuccess}
              onError={handleUploadError}
              onStart={handleUploadStart}
              disabled={false}
            />

            <div className="mt-8 p-4 bg-blue-500/20 rounded-lg border border-blue-500/30">
              <h3 className="text-white font-semibold mb-2">💡 Consejos:</h3>
              <ul className="text-gray-300 text-sm space-y-1">
                <li>• Formatos soportados: MP3, WAV, FLAC, AAC, OGG</li>
                <li>• Tamaño máximo: 500MB por archivo</li>
                <li>• Los archivos se almacenan en Vercel Blob Storage</li>
                <li>• Revisa la consola para ver los detalles del upload</li>
                <li>• Album ID de ejemplo: {exampleAlbumId}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

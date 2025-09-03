'use client';

import { AudioUploadForm } from '../../components/upload/AudioUploadForm';

export default function UploadPage() {
  // Ejemplo de uso del componente AudioUploadForm
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

    // Aquí puedes:
    // 1. Mostrar un mensaje de error al usuario
    // 2. Loggear el error para debugging
    // 3. Intentar reintentar la subida

    alert(`Error al subir archivo: ${error}`);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            🎵 Subir Música - Nada Records
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Sube tus tracks de techno y música electrónica a la plataforma.
          </p>
        </div>

        {/* Componente principal de upload */}
        <AudioUploadForm
          albumId="550e8400-e29b-41d4-a716-446655440000" // Ejemplo de UUID
          onSuccess={handleUploadSuccess}
          onError={handleUploadError}
        />

        {/* Información adicional */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            📋 Información importante
          </h2>
          <ul className="space-y-2 text-gray-600 dark:text-gray-400">
            <li>• Formatos soportados: MP3, WAV, FLAC, AAC, OGG</li>
            <li>• Tamaño máximo: 500MB por archivo</li>
            <li>• Los archivos se almacenan en Vercel Blob Storage</li>
            <li>• Se genera automáticamente un preview de 30 segundos</li>
            <li>• Metadata se extrae automáticamente del archivo</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

'use client';

import { AlertCircle, Music, Upload, X } from 'lucide-react';
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-hot-toast';

// Tipos de archivo soportados
const acceptedFileTypes = {
  'audio/mpeg': ['.mp3'],
  'audio/wav': ['.wav'],
  'audio/flac': ['.flac'],
  'audio/aac': ['.aac'],
  'audio/ogg': ['.ogg'],
};

const maxFileSize = 500 * 1024 * 1024; // 500MB

interface AudioUploadFormProps {
  albumId: string;
  onSuccess?: (data: {
    uploadId: string;
    fileUrl: string;
    fileSize: number;
    filename: string;
    message: string;
  }) => void;
  onError?: (error: string) => void;
  onStart?: () => void;
  disabled?: boolean;
}

export function AudioUploadForm({
  albumId,
  onSuccess,
  onError,
  onStart,
  disabled,
}: AudioUploadFormProps) {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  const uploadFile = useCallback(
    async (file: File) => {
      onStart?.();
      setUploading(true);
      setUploadProgress(0);

      try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('albumId', albumId);

        const progressInterval = setInterval(() => {
          setUploadProgress(prev => {
            if (prev >= 90) {
              clearInterval(progressInterval);
              return 90;
            }
            return prev + 10;
          });
        }, 200);

        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        });

        clearInterval(progressInterval);

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Upload failed');
        }

        const data = await response.json();
        setUploadProgress(100);

        toast.success('Archivo subido exitosamente!');
        onSuccess?.(data);
      } catch (error) {
        console.error('Upload error:', error);
        const errorMessage =
          error instanceof Error ? error.message : 'Error al subir el archivo';
        toast.error(errorMessage);
        onError?.(errorMessage);
      } finally {
        setUploading(false);
        setUploadProgress(0);
      }
    },
    [albumId, onSuccess, onError, onStart],
  );

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      const isValidType = Object.keys(acceptedFileTypes).includes(file.type);
      if (!isValidType) {
        const error =
          'Tipo de archivo no soportado. Use MP3, WAV, FLAC, AAC o OGG.';
        toast.error(error);
        onError?.(error);
        return;
      }

      if (file.size > maxFileSize) {
        const error = 'El archivo es demasiado grande. Máximo 500MB.';
        toast.error(error);
        onError?.(error);
        return;
      }

      setUploadedFile(file);
      await uploadFile(file);
    },
    [onError, uploadFile],
  );

  const removeFile = () => {
    setUploadedFile(null);
    setUploadProgress(0);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFileTypes,
    maxSize: maxFileSize,
    multiple: false,
    disabled: uploading || disabled,
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            Subir Archivo de Audio
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">
            Arrastra y suelta tu archivo de audio aquí, o haz click para seleccionar
          </p>
        </div>

        <div
          {...getRootProps()}
          className={`
            relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${
              isDragActive
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            }
            ${uploading || disabled ? 'pointer-events-none opacity-50' : ''}
          `}
        >
          <input {...getInputProps()} />

          {uploadedFile ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-3">
                <Music className="w-8 h-8 text-green-500" />
                <div className="text-left">
                  <p className="font-medium text-gray-900 dark:text-gray-100">
                    {uploadedFile.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {(uploadedFile.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
                {!uploading && (
                  <button
                    onClick={e => {
                      e.stopPropagation();
                      removeFile();
                    }}
                    className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                  >
                    <X className="w-4 h-4 text-gray-500" />
                  </button>
                )}
              </div>

              {uploading && (
                <div className="space-y-2">
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Subiendo... {uploadProgress}%
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <Upload
                className={`w-12 h-12 mx-auto ${
                  isDragActive ? 'text-blue-500' : 'text-gray-400'
                }`}
              />
              <div>
                <p className="text-lg font-medium text-gray-900 dark:text-gray-100">
                  {isDragActive
                    ? 'Suelta el archivo aquí'
                    : 'Selecciona tu archivo'}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  MP3, WAV, FLAC, AAC, OGG hasta 500MB
                </p>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-blue-500 mt-0.5" />
            <div className="text-sm text-gray-600 dark:text-gray-300">
              <p className="font-medium mb-1">Información importante:</p>
              <ul className="space-y-1 text-xs">
                <li>• El archivo se subirá a Vercel Blob Storage</li>
                <li>• Se generará automáticamente un preview de 30 segundos</li>
                <li>• Los metadatos se extraerán del archivo de audio</li>
                <li>
                  • El archivo estará disponible inmediatamente después de la
                  subida
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

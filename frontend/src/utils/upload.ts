import {
  AUDIO_EXTENSIONS,
  DEFAULT_UPLOAD_CONFIG,
  type UploadErrorDetails,
} from '@/types/upload';

/**
 * Valida si un archivo es un tipo de audio soportado
 */
export function isValidAudioFile(file: File): boolean {
  return DEFAULT_UPLOAD_CONFIG.acceptedFormats.includes(file.type);
}

/**
 * Valida el tamaño del archivo
 */
export function isValidFileSize(file: File): boolean {
  return file.size <= DEFAULT_UPLOAD_CONFIG.maxFileSize;
}

/**
 * Obtiene la extensión del archivo basada en el tipo MIME
 */
export function getFileExtension(mimeType: string): readonly string[] {
  return AUDIO_EXTENSIONS[mimeType as keyof typeof AUDIO_EXTENSIONS] || [];
}

/**
 * Convierte bytes a formato legible (MB, GB, etc.)
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Calcula el porcentaje de progreso de upload
 */
export function calculateUploadProgress(loaded: number, total: number): number {
  if (total === 0) return 0;
  return Math.round((loaded / total) * 100);
}

/**
 * Genera un ID único para el upload
 */
export function generateUploadId(): string {
  return `upload_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
}

/**
 * Valida completamente un archivo antes del upload
 */
export function validateFile(file: File): {
  isValid: boolean;
  error?: UploadErrorDetails;
} {
  // Validar tipo de archivo
  if (!isValidAudioFile(file)) {
    return {
      isValid: false,
      error: {
        type: 'INVALID_FORMAT',
        message: 'Tipo de archivo no soportado. Use MP3, WAV, FLAC, AAC o OGG.',
        details: {
          fileType: file.type,
          supportedTypes: DEFAULT_UPLOAD_CONFIG.acceptedFormats,
        },
      },
    };
  }

  // Validar tamaño
  if (!isValidFileSize(file)) {
    return {
      isValid: false,
      error: {
        type: 'FILE_TOO_LARGE',
        message: `El archivo es demasiado grande. Máximo ${formatFileSize(DEFAULT_UPLOAD_CONFIG.maxFileSize)}.`,
        details: {
          fileSize: file.size,
          maxSize: DEFAULT_UPLOAD_CONFIG.maxFileSize,
        },
      },
    };
  }

  return { isValid: true };
}

/**
 * Extrae metadatos básicos del archivo
 */
export function extractFileMetadata(file: File) {
  return {
    name: file.name,
    size: file.size,
    type: file.type,
    lastModified: file.lastModified,
    formattedSize: formatFileSize(file.size),
  };
}

/**
 * Crea un FormData para el upload
 */
export function createUploadFormData(file: File, albumId: string): FormData {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('albumId', albumId);
  return formData;
}

/**
 * Maneja errores de red y servidor
 */
export function handleUploadError(error: unknown): UploadErrorDetails {
  if (error instanceof Error && error.message.includes('NetworkError')) {
    return {
      type: 'NETWORK_ERROR',
      message: 'Error de conexión. Verifique su conexión a internet.',
      details: error as unknown as Record<string, unknown>, // Conversión a unknown primero
    };
  }

  if (error instanceof Response && error.status >= 500) {
    return {
      type: 'SERVER_ERROR',
      message: 'Error del servidor. Intente nuevamente más tarde.',
      details: { status: error.status, statusText: error.statusText },
    };
  }

  return {
    type: 'UNKNOWN_ERROR',
    message: 'Error desconocido durante el upload.',
    details:
      typeof error === 'object' && error !== null
        ? (error as Record<string, unknown>)
        : undefined, // Validación y conversión
  };
}

/**
 * Simula progreso de upload (útil para testing)
 */
export function simulateUploadProgress(
  onProgress: (progress: number) => void,
  duration: number = 2000
): Promise<void> {
  return new Promise(resolve => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        resolve();
      }
      onProgress(Math.round(progress));
    }, duration / 10);
  });
}

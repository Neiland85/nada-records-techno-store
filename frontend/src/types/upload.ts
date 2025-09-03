// Tipos e interfaces para el sistema de upload de archivos de audio

export interface UploadResponse {
  uploadId: string;
  fileUrl: string;
  fileSize: number;
  filename: string;
  message: string;
}

export interface AudioFileMetadata {
  title?: string;
  artist?: string;
  album?: string;
  genre?: string;
  duration?: number;
  bitrate?: number;
  sampleRate?: number;
  channels?: number;
  format: string;
  size: number;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

export interface AudioUploadFormProps {
  albumId: string;
  onSuccess?: (data: UploadResponse) => void;
  onError?: (error: string) => void;
  maxFileSize?: number;
  acceptedFormats?: string[];
}

export interface UploadState {
  isUploading: boolean;
  progress: number;
  error: string | null;
  uploadedFile: File | null;
}

export interface DatabaseTrack {
  id: string;
  title: string;
  artist: string;
  album: string;
  genre: string;
  duration: number;
  fileUrl: string;
  fileSize: number;
  uploadDate: Date;
  albumId: string;
}

export interface DatabaseAlbum {
  id: string;
  title: string;
  artist: string;
  description?: string;
  genre?: string;
  coverUrl?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface UploadConfig {
  maxFileSize: number;
  acceptedFormats: string[];
  chunkSize: number;
  retryAttempts: number;
  timeout: number;
}

// Tipos para errores
export type UploadError =
  | 'FILE_TOO_LARGE'
  | 'INVALID_FORMAT'
  | 'NETWORK_ERROR'
  | 'SERVER_ERROR'
  | 'UNKNOWN_ERROR';

export interface UploadErrorDetails {
  type: UploadError;
  message: string;
  details?: Record<string, unknown>; // Cambiado de 'any' a un tipo más específico
}

// Tipos para el estado del componente
export type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

// Constantes de configuración
export const DEFAULT_UPLOAD_CONFIG: UploadConfig = {
  maxFileSize: 500 * 1024 * 1024, // 500MB
  acceptedFormats: [
    'audio/mpeg',
    'audio/wav',
    'audio/flac',
    'audio/aac',
    'audio/ogg',
  ],
  chunkSize: 1024 * 1024, // 1MB chunks
  retryAttempts: 3,
  timeout: 30000, // 30 seconds
};

export const AUDIO_EXTENSIONS = {
  'audio/mpeg': ['.mp3'],
  'audio/wav': ['.wav'],
  'audio/flac': ['.flac'],
  'audio/aac': ['.aac', '.m4a'],
  'audio/ogg': ['.ogg'],
} as const;

'use client';

import React, { useCallback, useState } from 'react';
import { toast } from 'react-hot-toast';
import { FileUpload } from './FileUpload';

// Simplified schema for now
interface AudioUploadData {
  title: string;
  albumId: string;
  trackNumber: number;
  genre?: string;
  description?: string;
  bpm?: number;
  key?: string;
  price?: number;
  isFree: boolean;
}

interface AudioUploadFormProps {
  albumId: string;
  onSuccess?: (data: { uploadId: string; fileUrl: string; fileSize: number; filename: string; message: string }) => void;
  onError?: (error: string) => void;
}

export const AudioUploadForm: React.FC<AudioUploadFormProps> = ({
  albumId,
  onSuccess,
  onError,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [formData, setFormData] = useState<AudioUploadData>({
    title: '',
    albumId,
    trackNumber: 1,
    genre: '',
    description: '',
    bpm: undefined,
    key: '',
    price: undefined,
    isFree: false,
  });

  const handleFileSelect = useCallback((file: File) => {
    setSelectedFile(file);
    setUploadStatus('idle');
    setErrorMessage('');
  }, []);

  const handleFileRemove = useCallback(() => {
    setSelectedFile(null);
    setUploadStatus('idle');
    setErrorMessage('');
  }, []);

  const handleInputChange = (field: keyof AudioUploadData, value: string | number | boolean | undefined) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      setErrorMessage('Por favor selecciona un archivo de audio');
      setUploadStatus('error');
      return;
    }

    if (!formData.title.trim()) {
      setErrorMessage('El título es requerido');
      setUploadStatus('error');
      return;
    }

    setUploadStatus('uploading');
    setUploadProgress(0);
    setErrorMessage('');

    try {
      const submitData = new FormData();
      submitData.append('file', selectedFile);
      submitData.append('title', formData.title);
      submitData.append('albumId', formData.albumId);
      submitData.append('trackNumber', formData.trackNumber.toString());
      if (formData.genre) submitData.append('genre', formData.genre);
      if (formData.description) submitData.append('description', formData.description);
      if (formData.bpm) submitData.append('bpm', formData.bpm.toString());
      if (formData.key) submitData.append('key', formData.key);
      if (formData.price) submitData.append('price', formData.price.toString());

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await fetch('/api/upload/audio', {
        method: 'POST',
        body: submitData,
      });

      clearInterval(progressInterval);

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Error al subir el archivo');
      }

      const result = await response.json();
      setUploadProgress(100);
      setUploadStatus('success');

      toast.success('Archivo de audio subido exitosamente');

      // Reset form
      setFormData({
        title: '',
        albumId,
        trackNumber: 1,
        genre: '',
        description: '',
        bpm: undefined,
        key: '',
        price: undefined,
        isFree: false,
      });
      setSelectedFile(null);
      setUploadProgress(0);

      onSuccess?.(result);

    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
      setErrorMessage(error instanceof Error ? error.message : 'Error desconocido');
      toast.error('Error al subir el archivo');

      onError?.(error instanceof Error ? error.message : 'Error desconocido');
    }
  };

  const genres = [
    'electronic', 'techno', 'house', 'ambient', 'experimental',
    'hip_hop', 'pop', 'rock', 'jazz', 'classical', 'other'
  ];

  return (
    <div className="w-full max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          Subir Archivo de Audio
        </h2>
        <p className="text-gray-600 dark:text-gray-400">
          Sube un archivo de audio para tu álbum. Soporta formatos MP3, WAV, FLAC, AAC y OGG.
        </p>
      </div>

      <form onSubmit={onSubmit} className="space-y-6">
        {/* File Upload */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Archivo de Audio *
          </label>
          <FileUpload
            onFileSelect={handleFileSelect}
            onFileRemove={handleFileRemove}
            acceptedFileTypes="audio/*"
            maxFileSize={500 * 1024 * 1024} // 500MB
            placeholder="Selecciona un archivo de audio"
            selectedFile={selectedFile}
            uploadProgress={uploadProgress}
            uploadStatus={uploadStatus}
            errorMessage={errorMessage}
          />
        </div>

        {/* Title */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Título *
          </label>
          <input
            type="text"
            value={formData.title}
            onChange={(e) => handleInputChange('title', e.target.value)}
            placeholder="Título de la pista"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
            required
          />
        </div>

        {/* Track Number */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Número de Track *
          </label>
          <input
            type="number"
            value={formData.trackNumber}
            onChange={(e) => handleInputChange('trackNumber', parseInt(e.target.value) || 1)}
            placeholder="1"
            min="1"
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
            required
          />
        </div>

        {/* Genre */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Género
          </label>
          <select
            value={formData.genre}
            onChange={(e) => handleInputChange('genre', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
          >
            <option value="">Selecciona un género</option>
            {genres.map((genre) => (
              <option key={genre} value={genre}>
                {genre.charAt(0).toUpperCase() + genre.slice(1).replace('_', ' ')}
              </option>
            ))}
          </select>
        </div>

        {/* Description */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Descripción
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            placeholder="Descripción opcional de la pista"
            rows={3}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
          />
        </div>

        {/* BPM and Key */}
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              BPM
            </label>
            <input
              type="number"
              value={formData.bpm || ''}
              onChange={(e) => handleInputChange('bpm', parseInt(e.target.value) || undefined)}
              placeholder="120"
              min="60"
              max="200"
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
            />
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Tonalidad
            </label>
            <input
              type="text"
              value={formData.key}
              onChange={(e) => handleInputChange('key', e.target.value)}
              placeholder="C# minor"
              maxLength={10}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100"
            />
          </div>
        </div>

        {/* Price */}
        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Precio (USD)
          </label>
          <input
            type="number"
            step="0.01"
            value={formData.price || ''}
            onChange={(e) => handleInputChange('price', parseFloat(e.target.value) || undefined)}
            placeholder="9.99"
            min="0"
            disabled={formData.isFree}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-gray-100 disabled:opacity-50"
          />
        </div>

        {/* Is Free */}
        <div className="flex items-center space-x-2">
          <input
            id="isFree"
            type="checkbox"
            checked={formData.isFree}
            onChange={(e) => handleInputChange('isFree', e.target.checked)}
            className="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
          />
          <label htmlFor="isFree" className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Disponible gratis
          </label>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={uploadStatus === 'uploading'}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 disabled:cursor-not-allowed"
        >
          {uploadStatus === 'uploading' ? 'Subiendo...' : 'Subir Audio'}
        </button>
      </form>
    </div>
  );
};

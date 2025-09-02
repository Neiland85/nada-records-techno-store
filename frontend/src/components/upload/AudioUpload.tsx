'use client';

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, FileAudio, AlertCircle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface AudioUploadProps {
  albumId: string;
  onUploadComplete?: (result: UploadResult) => void;
  onUploadError?: (error: string) => void;
}

interface UploadResult {
  uploadId: string;
  fileUrl: string;
  fileSize: number;
  filename: string;
  contentType: string;
  uploadedAt: string;
}

interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'error';
  error?: string;
}

const AudioUpload: React.FC<AudioUploadProps> = ({
  albumId,
  onUploadComplete,
  onUploadError,
}) => {
  const [uploads, setUploads] = useState<UploadProgress[]>([]);
  const [trackMetadata, setTrackMetadata] = useState<Record<string, {
    title: string;
    trackNumber: number;
    genre?: string;
  }>>({});

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    // Filter audio files
    const audioFiles = acceptedFiles.filter(file =>
      file.type.startsWith('audio/')
    );

    if (audioFiles.length === 0) {
      onUploadError?.('Please select audio files only');
      return;
    }

    // Initialize upload progress for each file
    const newUploads = audioFiles.map(file => ({
      file,
      progress: 0,
      status: 'uploading' as const,
    }));

    setUploads(prev => [...prev, ...newUploads]);

    // Process each file
    for (let i = 0; i < audioFiles.length; i++) {
      const file = audioFiles[i];
      const fileId = `${file.name}-${Date.now()}`;

      try {
        // Initialize metadata for this file
        setTrackMetadata(prev => ({
          ...prev,
          [fileId]: {
            title: file.name.replace(/\.[^/.]+$/, ''), // Remove extension
            trackNumber: uploads.length + i + 1,
            genre: '',
          }
        }));

        // Create FormData
        const formData = new FormData();
        formData.append('file', file);
        formData.append('title', trackMetadata[fileId]?.title || file.name);
        formData.append('albumId', albumId);
        formData.append('trackNumber', String(trackMetadata[fileId]?.trackNumber || uploads.length + i + 1));
        if (trackMetadata[fileId]?.genre) {
          formData.append('genre', trackMetadata[fileId].genre);
        }

        // Upload file
        const response = await fetch('/api/upload/audio', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.error || 'Upload failed');
        }

        const result: UploadResult = await response.json();

        // Update progress
        setUploads(prev =>
          prev.map(upload =>
            upload.file === file
              ? { ...upload, progress: 100, status: 'completed' }
              : upload
          )
        );

        onUploadComplete?.(result);

      } catch (error) {
        console.error('Upload error:', error);

        // Update progress with error
        setUploads(prev =>
          prev.map(upload =>
            upload.file === file
              ? {
                  ...upload,
                  status: 'error',
                  error: error instanceof Error ? error.message : 'Upload failed'
                }
              : upload
          )
        );

        onUploadError?.(error instanceof Error ? error.message : 'Upload failed');
      }
    }
  }, [albumId, uploads.length, trackMetadata, onUploadComplete, onUploadError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'audio/*': ['.mp3', '.wav', '.flac', '.aac', '.ogg']
    },
    multiple: true,
    maxSize: 500 * 1024 * 1024, // 500MB
  });

  const removeUpload = (file: File) => {
    setUploads(prev => prev.filter(upload => upload.file !== file));
  };

  const updateMetadata = (fileId: string, field: string, value: string | number) => {
    setTrackMetadata(prev => ({
      ...prev,
      [fileId]: {
        ...prev[fileId],
        [field]: value,
      }
    }));
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Dropzone */}
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
          }
        `}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
          {isDragActive ? 'Drop your audio files here' : 'Upload Audio Files'}
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Drag & drop audio files here, or click to select files
        </p>
        <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
          Supported formats: MP3, WAV, FLAC, AAC, OGG (max 500MB each)
        </p>
      </div>

      {/* Upload Progress */}
      <AnimatePresence>
        {uploads.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-6 space-y-4"
          >
            {uploads.map((upload, index) => {
              const fileId = `${upload.file.name}-${Date.now()}`;

              return (
                <motion.div
                  key={`${upload.file.name}-${index}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  className="bg-white dark:bg-gray-800 rounded-lg border p-4"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <FileAudio className="h-5 w-5 text-blue-500" />
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">
                          {upload.file.name}
                        </p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {(upload.file.size / (1024 * 1024)).toFixed(2)} MB
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2">
                      {upload.status === 'completed' && (
                        <CheckCircle className="h-5 w-5 text-green-500" />
                      )}
                      {upload.status === 'error' && (
                        <AlertCircle className="h-5 w-5 text-red-500" />
                      )}
                      <button
                        onClick={() => removeUpload(upload.file)}
                        className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-3">
                    <motion.div
                      className={`h-2 rounded-full ${
                        upload.status === 'completed'
                          ? 'bg-green-500'
                          : upload.status === 'error'
                          ? 'bg-red-500'
                          : 'bg-blue-500'
                      }`}
                      initial={{ width: 0 }}
                      animate={{ width: `${upload.progress}%` }}
                      transition={{ duration: 0.3 }}
                    />
                  </div>

                  {/* Track Metadata Form */}
                  {upload.status === 'uploading' && (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Title
                        </label>
                        <input
                          type="text"
                          value={trackMetadata[fileId]?.title || ''}
                          onChange={(e) => updateMetadata(fileId, 'title', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                          placeholder="Track title"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Track #
                        </label>
                        <input
                          type="number"
                          min="1"
                          value={trackMetadata[fileId]?.trackNumber || ''}
                          onChange={(e) => updateMetadata(fileId, 'trackNumber', parseInt(e.target.value))}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                          Genre
                        </label>
                        <select
                          value={trackMetadata[fileId]?.genre || ''}
                          onChange={(e) => updateMetadata(fileId, 'genre', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
                        >
                          <option value="">Select genre</option>
                          <option value="electronic">Electronic</option>
                          <option value="techno">Techno</option>
                          <option value="house">House</option>
                          <option value="ambient">Ambient</option>
                          <option value="experimental">Experimental</option>
                        </select>
                      </div>
                    </div>
                  )}

                  {/* Status Messages */}
                  {upload.status === 'error' && upload.error && (
                    <p className="text-sm text-red-600 dark:text-red-400 mt-2">
                      {upload.error}
                    </p>
                  )}

                  {upload.status === 'completed' && (
                    <p className="text-sm text-green-600 dark:text-green-400 mt-2">
                      Upload completed successfully
                    </p>
                  )}
                </motion.div>
              );
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AudioUpload;

'use client';

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Image as ImageIcon, AlertCircle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';

interface CoverArtUploadProps {
  albumId: string;
  currentCoverUrl?: string;
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
  preview?: string;
}

const CoverArtUpload: React.FC<CoverArtUploadProps> = ({
  albumId,
  currentCoverUrl,
  onUploadComplete,
  onUploadError,
}) => {
  const [upload, setUpload] = useState<UploadProgress | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]; // Only one cover art per album

    if (!file) return;

    // Create preview URL
    const preview = URL.createObjectURL(file);

    setUpload({
      file,
      progress: 0,
      status: 'uploading',
      preview,
    });

    try {
      // Create FormData
      const formData = new FormData();
      formData.append('file', file);
      formData.append('albumId', albumId);

      // Upload file
      const response = await fetch('/api/upload/cover-art', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Upload failed');
      }

      const result: UploadResult = await response.json();

      // Update progress
      setUpload(prev => prev ? {
        ...prev,
        progress: 100,
        status: 'completed'
      } : null);

      onUploadComplete?.(result);

    } catch (error) {
      console.error('Upload error:', error);

      // Update progress with error
      setUpload(prev => prev ? {
        ...prev,
        status: 'error',
        error: error instanceof Error ? error.message : 'Upload failed'
      } : null);

      onUploadError?.(error instanceof Error ? error.message : 'Upload failed');
    }
  }, [albumId, onUploadComplete, onUploadError]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeUpload = () => {
    if (upload?.preview) {
      URL.revokeObjectURL(upload.preview);
    }
    setUpload(null);
  };

  // Show current cover or upload area
  const displayUrl = upload?.preview || currentCoverUrl;

  return (
    <div className="w-full max-w-md mx-auto">
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-lg cursor-pointer transition-all duration-200
          ${isDragActive
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
            : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
          }
          ${displayUrl ? 'aspect-square' : 'p-8'}
        `}
      >
        <input {...getInputProps()} />

        {displayUrl ? (
          // Show image preview
          <div className="relative w-full h-full">
            <Image
              src={displayUrl}
              alt="Album cover"
              fill
              className="object-cover rounded-lg"
            />

            {/* Overlay with upload status */}
            <div className="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
              <div className="text-center text-white">
                <Upload className="mx-auto h-8 w-8 mb-2" />
                <p className="text-sm font-medium">
                  {isDragActive ? 'Drop to replace' : 'Click to replace cover'}
                </p>
              </div>
            </div>

            {/* Status indicator */}
            {upload && (
              <div className="absolute top-2 right-2">
                {upload.status === 'completed' && (
                  <CheckCircle className="h-6 w-6 text-green-500 bg-white rounded-full" />
                )}
                {upload.status === 'error' && (
                  <AlertCircle className="h-6 w-6 text-red-500 bg-white rounded-full" />
                )}
                {upload.status === 'uploading' && (
                  <div className="h-6 w-6 bg-blue-500 rounded-full flex items-center justify-center">
                    <div className="animate-spin rounded-full h-3 w-3 border border-white"></div>
                  </div>
                )}
              </div>
            )}

            {/* Remove button */}
            {upload && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeUpload();
                }}
                className="absolute top-2 left-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            )}
          </div>
        ) : (
          // Show upload area
          <div className="text-center">
            <ImageIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              {isDragActive ? 'Drop your cover art here' : 'Upload Cover Art'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Drag & drop an image, or click to select
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
              Supported: JPEG, PNG, WebP (max 10MB)
            </p>
          </div>
        )}
      </div>

      {/* Upload Progress */}
      <AnimatePresence>
        {upload && upload.status === 'uploading' && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-4"
          >
            <div className="bg-white dark:bg-gray-800 rounded-lg border p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  Uploading {upload.file.name}
                </span>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {(upload.file.size / (1024 * 1024)).toFixed(2)} MB
                </span>
              </div>

              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <motion.div
                  className="bg-blue-500 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${upload.progress}%` }}
                  transition={{ duration: 0.3 }}
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Error Message */}
      <AnimatePresence>
        {upload && upload.status === 'error' && upload.error && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mt-4 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4"
          >
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
              <p className="text-sm text-red-700 dark:text-red-400">
                {upload.error}
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CoverArtUpload;

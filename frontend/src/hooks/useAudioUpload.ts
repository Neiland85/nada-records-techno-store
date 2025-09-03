import {
  type UploadErrorDetails,
  type UploadResponse,
  type UploadStatus,
} from '@/types/upload';
import {
  createUploadFormData,
  handleUploadError,
  simulateUploadProgress,
  validateFile,
} from '@/utils/upload';
import { useCallback, useState } from 'react';

interface UseAudioUploadOptions {
  albumId: string;
  onSuccess?: (data: UploadResponse) => void;
  onError?: (error: UploadErrorDetails) => void;
  simulateProgress?: boolean;
}

interface UseAudioUploadReturn {
  uploadFile: (file: File) => Promise<void>;
  status: UploadStatus;
  progress: number;
  error: UploadErrorDetails | null;
  reset: () => void;
}

export function useAudioUpload({
  albumId,
  onSuccess,
  onError,
  simulateProgress = false,
}: UseAudioUploadOptions): UseAudioUploadReturn {
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<UploadErrorDetails | null>(null);

  const reset = useCallback(() => {
    setStatus('idle');
    setProgress(0);
    setError(null);
  }, []);

  const uploadFile = useCallback(
    async (file: File) => {
      // Reset previous state
      reset();

      // Validate file
      const validation = validateFile(file);
      if (!validation.isValid) {
        const uploadError = validation.error!;
        setStatus('error');
        setError(uploadError);
        onError?.(uploadError);
        return;
      }

      setStatus('uploading');

      try {
        const formData = createUploadFormData(file, albumId);

        // Simulate progress if requested
        if (simulateProgress) {
          simulateUploadProgress(setProgress, 2000);
        }

        // Upload file
        const response = await fetch('/api/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Upload failed');
        }

        const data: UploadResponse = await response.json();

        setStatus('success');
        setProgress(100);
        onSuccess?.(data);
      } catch (err) {
        const uploadError = handleUploadError(err);
        setStatus('error');
        setError(uploadError);
        onError?.(uploadError);
      }
    },
    [albumId, onSuccess, onError, simulateProgress, reset]
  );

  return {
    uploadFile,
    status,
    progress,
    error,
    reset,
  };
}

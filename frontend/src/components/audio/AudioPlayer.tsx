'use client';

import { AnimatePresence, motion } from 'framer-motion';
import {
  AlertCircle,
  Loader2,
  Pause,
  Play,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
} from 'lucide-react';
import Image from 'next/image';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';

// Types
interface AudioPlayerProps {
  /** Audio source URL */
  src: string;
  /** Track title */
  title?: string;
  /** Artist name */
  artist?: string;
  /** Album cover URL */
  coverUrl?: string;
  /** Auto play when component mounts */
  autoPlay?: boolean;
  /** Show waveform visualization */
  showWaveform?: boolean;
  /** Custom waveform colors */
  waveformColors?: {
    wave: string;
    progress: string;
    cursor: string;
  };
  /** Callback when track ends */
  onEnded?: () => void;
  /** Callback when play state changes */
  onPlayStateChange?: (isPlaying: boolean) => void;
  /** Callback when time updates */
  onTimeUpdate?: (currentTime: number, duration: number) => void;
}

interface PlayerState {
  isPlaying: boolean;
  isLoading: boolean;
  hasError: boolean;
  errorMessage?: string;
  currentTime: number;
  duration: number;
  volume: number;
  isMuted: boolean;
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({
  src,
  title = 'Unknown Track',
  artist = 'Unknown Artist',
  coverUrl,
  autoPlay = false,
  showWaveform = true,
  waveformColors = {
    wave: '#64748b',
    progress: '#3b82f6',
    cursor: '#ef4444',
  },
  onEnded,
  onPlayStateChange,
  onTimeUpdate,
}) => {
  // Refs
  const waveformRef = useRef<HTMLDivElement>(null);
  const wavesurferRef = useRef<WaveSurfer | null>(null);

  // State
  const [state, setState] = useState<PlayerState>({
    isPlaying: false,
    isLoading: true,
    hasError: false,
    currentTime: 0,
    duration: 0,
    volume: 0.8,
    isMuted: false,
  });

  // Format time helper
  const formatTime = useCallback((seconds: number): string => {
    if (isNaN(seconds)) return '0:00';

    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }, []);

  // Initialize WaveSurfer
  const initializeWaveSurfer = useCallback(async () => {
    if (!waveformRef.current || !src) return;

    try {
      setState(prev => ({ ...prev, isLoading: true, hasError: false }));

      // Cleanup existing instance
      if (wavesurferRef.current) {
        wavesurferRef.current.destroy();
      }

      // Create new WaveSurfer instance
      const wavesurfer = WaveSurfer.create({
        container: waveformRef.current,
        waveColor: waveformColors.wave,
        progressColor: waveformColors.progress,
        cursorColor: waveformColors.cursor,
        height: 80,
        normalize: true,
        backend: 'WebAudio',
        mediaControls: false,
        interact: true,
        hideScrollbar: true,
        barWidth: 2,
        barGap: 1,
      });

      wavesurferRef.current = wavesurfer;

      // Event listeners
      wavesurfer.on('ready', () => {
        setState(prev => ({
          ...prev,
          isLoading: false,
          duration: wavesurfer.getDuration(),
        }));

        if (autoPlay) {
          wavesurfer.play();
        }
      });

      wavesurfer.on('play', () => {
        setState(prev => ({ ...prev, isPlaying: true }));
        onPlayStateChange?.(true);

        // Set up MediaSession API
        if ('mediaSession' in navigator) {
          navigator.mediaSession.metadata = new MediaMetadata({
            title,
            artist,
            artwork: coverUrl
              ? [{ src: coverUrl, sizes: '512x512', type: 'image/jpeg' }]
              : undefined,
          });

          navigator.mediaSession.setActionHandler('play', () =>
            wavesurfer.play()
          );
          navigator.mediaSession.setActionHandler('pause', () =>
            wavesurfer.pause()
          );
          navigator.mediaSession.setActionHandler('seekbackward', () => {
            const currentTime = wavesurfer.getCurrentTime();
            wavesurfer.seekTo(
              Math.max(0, currentTime - 10) / wavesurfer.getDuration()
            );
          });
          navigator.mediaSession.setActionHandler('seekforward', () => {
            const currentTime = wavesurfer.getCurrentTime();
            const duration = wavesurfer.getDuration();
            wavesurfer.seekTo(Math.min(duration, currentTime + 10) / duration);
          });
        }
      });

      wavesurfer.on('pause', () => {
        setState(prev => ({ ...prev, isPlaying: false }));
        onPlayStateChange?.(false);
      });

      wavesurfer.on('audioprocess', () => {
        const currentTime = wavesurfer.getCurrentTime();
        const duration = wavesurfer.getDuration();

        setState(prev => ({ ...prev, currentTime }));
        onTimeUpdate?.(currentTime, duration);
      });

      wavesurfer.on('finish', () => {
        setState(prev => ({ ...prev, isPlaying: false, currentTime: 0 }));
        onPlayStateChange?.(false);
        onEnded?.();
      });

      wavesurfer.on('error', error => {
        console.error('WaveSurfer error:', error);
        setState(prev => ({
          ...prev,
          hasError: true,
          isLoading: false,
          errorMessage: 'Failed to load audio',
        }));
      });

      // Load the audio
      await wavesurfer.load(src);
    } catch (error) {
      console.error('Failed to initialize WaveSurfer:', error);
      setState(prev => ({
        ...prev,
        hasError: true,
        isLoading: false,
        errorMessage: error instanceof Error ? error.message : 'Unknown error',
      }));
    }
  }, [
    src,
    waveformColors,
    autoPlay,
    title,
    artist,
    coverUrl,
    onPlayStateChange,
    onTimeUpdate,
    onEnded,
  ]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Only handle if no input is focused
      if (
        document.activeElement?.tagName === 'INPUT' ||
        document.activeElement?.tagName === 'TEXTAREA'
      ) {
        return;
      }

      switch (event.code) {
        case 'Space':
          event.preventDefault();
          togglePlayPause();
          break;
        case 'ArrowLeft':
          event.preventDefault();
          seek(-10);
          break;
        case 'ArrowRight':
          event.preventDefault();
          seek(10);
          break;
        case 'ArrowUp':
          event.preventDefault();
          adjustVolume(0.1);
          break;
        case 'ArrowDown':
          event.preventDefault();
          adjustVolume(-0.1);
          break;
        case 'KeyM':
          event.preventDefault();
          toggleMute();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [togglePlayPause, seek, adjustVolume, toggleMute]);

  // Initialize on mount and src change
  useEffect(() => {
    initializeWaveSurfer();

    return () => {
      if (wavesurferRef.current) {
        wavesurferRef.current.destroy();
        wavesurferRef.current = null;
      }
    };
  }, [initializeWaveSurfer]);

  // Player controls
  const togglePlayPause = useCallback(() => {
    if (!wavesurferRef.current) return;

    if (state.isPlaying) {
      wavesurferRef.current.pause();
    } else {
      wavesurferRef.current.play();
    }
  }, [state.isPlaying]);

  const seek = useCallback((seconds: number) => {
    if (!wavesurferRef.current) return;

    const currentTime = wavesurferRef.current.getCurrentTime();
    const duration = wavesurferRef.current.getDuration();
    const newTime = Math.max(0, Math.min(duration, currentTime + seconds));

    wavesurferRef.current.seekTo(newTime / duration);
  }, []);

  const adjustVolume = useCallback(
    (delta: number) => {
      if (!wavesurferRef.current) return;

      const newVolume = Math.max(0, Math.min(1, state.volume + delta));
      wavesurferRef.current.setVolume(newVolume);
      setState(prev => ({
        ...prev,
        volume: newVolume,
        isMuted: newVolume === 0,
      }));
    },
    [state.volume]
  );

  const toggleMute = useCallback(() => {
    if (!wavesurferRef.current) return;

    if (state.isMuted) {
      wavesurferRef.current.setVolume(state.volume);
      setState(prev => ({ ...prev, isMuted: false }));
    } else {
      wavesurferRef.current.setVolume(0);
      setState(prev => ({ ...prev, isMuted: true }));
    }
  }, [state.isMuted, state.volume]);

  if (state.hasError) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <AlertCircle className="w-8 h-8 text-red-500 mx-auto mb-2" />
        <p className="text-red-700 font-medium">Audio Loading Error</p>
        <p className="text-red-600 text-sm mt-1">{state.errorMessage}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      {/* Track Info */}
      <div className="flex items-center space-x-4 mb-6">
        {coverUrl && (
          <Image
            src={coverUrl}
            alt={`${title} cover`}
            width={64}
            height={64}
            className="w-16 h-16 rounded-lg object-cover shadow-sm"
          />
        )}
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {title}
          </h3>
          <p className="text-gray-600 truncate">{artist}</p>
        </div>
      </div>

      {/* Waveform */}
      {showWaveform && (
        <div className="mb-6">
          <AnimatePresence>
            {state.isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex items-center justify-center h-20 bg-gray-100 rounded"
              >
                <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
                <span className="ml-2 text-gray-600">Loading waveform...</span>
              </motion.div>
            )}
          </AnimatePresence>

          <div
            ref={waveformRef}
            className={`${state.isLoading ? 'hidden' : 'block'} cursor-pointer`}
          />
        </div>
      )}

      {/* Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {/* Previous Track Button */}
          <button
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            title="Previous (not implemented)"
          >
            <SkipBack className="w-5 h-5 text-gray-600" />
          </button>

          {/* Play/Pause Button */}
          <button
            onClick={togglePlayPause}
            disabled={state.isLoading}
            className="p-3 bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 rounded-full transition-colors"
            title={state.isPlaying ? 'Pause (Space)' : 'Play (Space)'}
          >
            {state.isLoading ? (
              <Loader2 className="w-6 h-6 text-white animate-spin" />
            ) : state.isPlaying ? (
              <Pause className="w-6 h-6 text-white" />
            ) : (
              <Play className="w-6 h-6 text-white ml-1" />
            )}
          </button>

          {/* Next Track Button */}
          <button
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            title="Next (not implemented)"
          >
            <SkipForward className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Time Display */}
        <div className="text-sm text-gray-600 font-mono">
          {formatTime(state.currentTime)} / {formatTime(state.duration)}
        </div>

        {/* Volume Control */}
        <div className="flex items-center space-x-2">
          <button
            onClick={toggleMute}
            className="p-2 rounded-full hover:bg-gray-100 transition-colors"
            title={state.isMuted ? 'Unmute (M)' : 'Mute (M)'}
          >
            {state.isMuted ? (
              <VolumeX className="w-5 h-5 text-gray-600" />
            ) : (
              <Volume2 className="w-5 h-5 text-gray-600" />
            )}
          </button>

          <input
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={state.isMuted ? 0 : state.volume}
            onChange={e => {
              const newVolume = parseFloat(e.target.value);
              if (wavesurferRef.current) {
                wavesurferRef.current.setVolume(newVolume);
                setState(prev => ({
                  ...prev,
                  volume: newVolume,
                  isMuted: newVolume === 0,
                }));
              }
            }}
            className="w-20 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            title="Volume (↑↓ arrows)"
          />
        </div>
      </div>

      {/* Keyboard Shortcuts Help */}
      <div className="mt-4 text-xs text-gray-500">
        <p>
          Keyboard shortcuts: Space (play/pause), ←/→ (seek), ↑/↓ (volume), M
          (mute)
        </p>
      </div>
    </div>
  );
};

export default AudioPlayer;

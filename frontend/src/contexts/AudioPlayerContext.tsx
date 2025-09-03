'use client';

import React, { createContext, ReactNode, useContext, useReducer } from 'react';

// Tipos para el estado del audio player
interface AudioTrack {
  id: string;
  title: string;
  artist: string;
  url: string;
  duration: number;
  coverUrl?: string;
}

interface AudioPlayerState {
  currentTrack: AudioTrack | null;
  isPlaying: boolean;
  volume: number;
  currentTime: number;
  duration: number;
  playlist: AudioTrack[];
  currentIndex: number;
  isLoading: boolean;
  error: string | null;
}

// Tipos para las acciones
type AudioPlayerAction =
  | { type: 'SET_TRACK'; payload: AudioTrack }
  | { type: 'SET_PLAYING'; payload: boolean }
  | { type: 'SET_VOLUME'; payload: number }
  | { type: 'SET_CURRENT_TIME'; payload: number }
  | { type: 'SET_DURATION'; payload: number }
  | { type: 'SET_PLAYLIST'; payload: AudioTrack[] }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'NEXT_TRACK' }
  | { type: 'PREVIOUS_TRACK' }
  | { type: 'PLAY_TRACK'; payload: AudioTrack };

// Estado inicial
const initialState: AudioPlayerState = {
  currentTrack: null,
  isPlaying: false,
  volume: 0.8,
  currentTime: 0,
  duration: 0,
  playlist: [],
  currentIndex: -1,
  isLoading: false,
  error: null,
};

// Reducer para manejar el estado
function audioPlayerReducer(
  state: AudioPlayerState,
  action: AudioPlayerAction
): AudioPlayerState {
  switch (action.type) {
    case 'SET_TRACK':
      return {
        ...state,
        currentTrack: action.payload,
        currentIndex: state.playlist.findIndex(track => track.id === action.payload.id),
      };

    case 'SET_PLAYING':
      return { ...state, isPlaying: action.payload };

    case 'SET_VOLUME':
      return { ...state, volume: action.payload };

    case 'SET_CURRENT_TIME':
      return { ...state, currentTime: action.payload };

    case 'SET_DURATION':
      return { ...state, duration: action.payload };

    case 'SET_PLAYLIST':
      return { ...state, playlist: action.payload };

    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };

    case 'SET_ERROR':
      return { ...state, error: action.payload };

    case 'NEXT_TRACK':
      if (state.currentIndex < state.playlist.length - 1) {
        const nextIndex = state.currentIndex + 1;
        return {
          ...state,
          currentTrack: state.playlist[nextIndex],
          currentIndex: nextIndex,
        };
      }
      return state;

    case 'PREVIOUS_TRACK':
      if (state.currentIndex > 0) {
        const prevIndex = state.currentIndex - 1;
        return {
          ...state,
          currentTrack: state.playlist[prevIndex],
          currentIndex: prevIndex,
        };
      }
      return state;

    case 'PLAY_TRACK':
      return {
        ...state,
        currentTrack: action.payload,
        currentIndex: state.playlist.findIndex(track => track.id === action.payload.id),
        isPlaying: true,
      };

    default:
      return state;
  }
}

// Contexto
const AudioPlayerContext = createContext<{
  state: AudioPlayerState;
  dispatch: React.Dispatch<AudioPlayerAction>;
} | null>(null);

// Provider
interface AudioPlayerProviderProps {
  children: ReactNode;
}

export function AudioPlayerProvider({ children }: AudioPlayerProviderProps) {
  const [state, dispatch] = useReducer(audioPlayerReducer, initialState);

  return (
    <AudioPlayerContext.Provider value={{ state, dispatch }}>
      {children}
    </AudioPlayerContext.Provider>
  );
}

// Hook para usar el contexto
export function useAudioPlayer() {
  const context = useContext(AudioPlayerContext);
  if (!context) {
    throw new Error('useAudioPlayer must be used within an AudioPlayerProvider');
  }
  return context;
}

// Tipos exportados
export type { AudioPlayerAction, AudioPlayerState, AudioTrack };

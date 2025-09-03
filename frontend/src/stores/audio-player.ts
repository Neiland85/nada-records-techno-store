import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Tipos para el estado del audio player
export interface AudioTrack {
  id: string;
  title: string;
  artist: string;
  url: string;
  duration: number;
  coverUrl?: string;
  bpm?: number;
  genre?: string;
  label?: string;
  price?: number;
  formats?: {
    mp3: { size: string; bitrate: string; price: number };
    wav: { size: string; bitrate: string; price: number };
    flac: { size: string; bitrate: string; price: number };
  };
}

interface AudioPlayerState {
  // Estado actual
  currentTrack: AudioTrack | null;
  isPlaying: boolean;
  volume: number;
  currentTime: number;
  duration: number;
  playlist: AudioTrack[];
  currentIndex: number;
  isLoading: boolean;
  error: string | null;

  // Historial y favoritos
  recentlyPlayed: AudioTrack[];
  favorites: AudioTrack[];

  // Configuración
  repeatMode: 'none' | 'one' | 'all';
  shuffleMode: boolean;
  autoPlay: boolean;
}

interface AudioPlayerActions {
  // Acciones básicas
  setTrack: (track: AudioTrack) => void;
  setPlaying: (playing: boolean) => void;
  setVolume: (volume: number) => void;
  setCurrentTime: (time: number) => void;
  setDuration: (duration: number) => void;
  setPlaylist: (playlist: AudioTrack[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  // Navegación
  nextTrack: () => void;
  previousTrack: () => void;
  playTrack: (track: AudioTrack) => void;

  // Historial y favoritos
  addToRecentlyPlayed: (track: AudioTrack) => void;
  toggleFavorite: (track: AudioTrack) => void;
  removeFromFavorites: (trackId: string) => void;

  // Configuración
  setRepeatMode: (mode: 'none' | 'one' | 'all') => void;
  toggleShuffle: () => void;
  setAutoPlay: (autoPlay: boolean) => void;

  // Utilidades
  clearPlaylist: () => void;
  removeFromPlaylist: (trackId: string) => void;
  reorderPlaylist: (fromIndex: number, toIndex: number) => void;
}

type AudioPlayerStore = AudioPlayerState & AudioPlayerActions;

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
  recentlyPlayed: [],
  favorites: [],
  repeatMode: 'none',
  shuffleMode: false,
  autoPlay: false,
};

export const useAudioPlayerStore = create<AudioPlayerStore>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Acciones básicas
      setTrack: (track) => set({ currentTrack: track }),
      setPlaying: (playing) => set({ isPlaying: playing }),
      setVolume: (volume) => set({ volume }),
      setCurrentTime: (time) => set({ currentTime: time }),
      setDuration: (duration) => set({ duration }),
      setPlaylist: (playlist) => set({ playlist }),
      setLoading: (loading) => set({ isLoading: loading }),
      setError: (error) => set({ error }),

      // Navegación
      nextTrack: () => {
        const { playlist, currentIndex, repeatMode, shuffleMode } = get();
        if (playlist.length === 0) return;

        let nextIndex = currentIndex;

        if (shuffleMode) {
          // Shuffle mode: seleccionar track aleatorio
          nextIndex = Math.floor(Math.random() * playlist.length);
        } else {
          // Normal mode
          nextIndex = currentIndex + 1;
          if (nextIndex >= playlist.length) {
            if (repeatMode === 'all') {
              nextIndex = 0;
            } else {
              return; // Fin de la playlist
            }
          }
        }

        const nextTrack = playlist[nextIndex];
        set({
          currentTrack: nextTrack,
          currentIndex: nextIndex,
          currentTime: 0,
          isPlaying: true
        });
      },

      previousTrack: () => {
        const { playlist, currentIndex, currentTime } = get();
        if (playlist.length === 0) return;

        // Si estamos en los primeros 3 segundos, ir al track anterior
        if (currentTime > 3) {
          set({ currentTime: 0 });
          return;
        }

        let prevIndex = currentIndex - 1;
        if (prevIndex < 0) {
          prevIndex = playlist.length - 1;
        }

        const prevTrack = playlist[prevIndex];
        set({
          currentTrack: prevTrack,
          currentIndex: prevIndex,
          currentTime: 0,
          isPlaying: true
        });
      },

      playTrack: (track) => {
        const { playlist } = get();
        const trackIndex = playlist.findIndex(t => t.id === track.id);

        if (trackIndex !== -1) {
          set({
            currentTrack: track,
            currentIndex: trackIndex,
            isPlaying: true,
            currentTime: 0
          });
        } else {
          // Track no está en playlist, agregarlo y reproducirlo
          const newPlaylist = [...playlist, track];
          set({
            playlist: newPlaylist,
            currentTrack: track,
            currentIndex: newPlaylist.length - 1,
            isPlaying: true,
            currentTime: 0
          });
        }
      },

      // Historial y favoritos
      addToRecentlyPlayed: (track) => {
        const { recentlyPlayed } = get();
        const filtered = recentlyPlayed.filter(t => t.id !== track.id);
        const updated = [track, ...filtered].slice(0, 20); // Mantener solo 20 tracks
        set({ recentlyPlayed: updated });
      },

      toggleFavorite: (track) => {
        const { favorites } = get();
        const isFavorite = favorites.some(t => t.id === track.id);

        if (isFavorite) {
          const filtered = favorites.filter(t => t.id !== track.id);
          set({ favorites: filtered });
        } else {
          set({ favorites: [...favorites, track] });
        }
      },

      removeFromFavorites: (trackId) => {
        const { favorites } = get();
        const filtered = favorites.filter(t => t.id !== trackId);
        set({ favorites: filtered });
      },

      // Configuración
      setRepeatMode: (mode) => set({ repeatMode: mode }),
      toggleShuffle: () => set((state) => ({ shuffleMode: !state.shuffleMode })),
      setAutoPlay: (autoPlay) => set({ autoPlay }),

      // Utilidades
      clearPlaylist: () => set({
        playlist: [],
        currentTrack: null,
        currentIndex: -1,
        isPlaying: false
      }),

      removeFromPlaylist: (trackId) => {
        const { playlist, currentIndex, currentTrack } = get();
        const filtered = playlist.filter(t => t.id !== trackId);
        let newIndex = currentIndex;
        let newTrack = currentTrack;

        // Ajustar el índice si es necesario
        if (currentTrack?.id === trackId) {
          newTrack = null;
          newIndex = -1;
        } else if (currentIndex > filtered.findIndex(t => t.id === currentTrack?.id)) {
          newIndex = currentIndex - 1;
        }

        set({
          playlist: filtered,
          currentIndex: newIndex,
          currentTrack: newTrack
        });
      },

      reorderPlaylist: (fromIndex, toIndex) => {
        const { playlist, currentIndex } = get();
        const newPlaylist = [...playlist];
        const [moved] = newPlaylist.splice(fromIndex, 1);
        newPlaylist.splice(toIndex, 0, moved);

        let newCurrentIndex = currentIndex;
        if (currentIndex === fromIndex) {
          newCurrentIndex = toIndex;
        } else if (currentIndex > fromIndex && currentIndex <= toIndex) {
          newCurrentIndex = currentIndex - 1;
        } else if (currentIndex < fromIndex && currentIndex >= toIndex) {
          newCurrentIndex = currentIndex + 1;
        }

        set({
          playlist: newPlaylist,
          currentIndex: newCurrentIndex
        });
      },
    }),
    {
      name: 'audio-player-storage',
      partialize: (state) => ({
        volume: state.volume,
        favorites: state.favorites,
        recentlyPlayed: state.recentlyPlayed,
        repeatMode: state.repeatMode,
        shuffleMode: state.shuffleMode,
        autoPlay: state.autoPlay,
      }),
      skipHydration: true,
    }
  )
);

// Selectores útiles
export const useCurrentTrack = () => useAudioPlayerStore((state) => state.currentTrack);
export const useIsPlaying = () => useAudioPlayerStore((state) => state.isPlaying);
export const usePlaylist = () => useAudioPlayerStore((state) => state.playlist);
export const useFavorites = () => useAudioPlayerStore((state) => state.favorites);
export const useRecentlyPlayed = () => useAudioPlayerStore((state) => state.recentlyPlayed);

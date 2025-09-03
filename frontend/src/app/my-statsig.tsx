"use client";

import React, { createContext, useContext } from "react";

// Definir tipos para Statsig
interface StatsigClient {
  logEvent: (eventName: string, metadata?: Record<string, string | number | boolean>) => void;
  checkGate: (gateName: string) => boolean;
}

interface StatsigContextType {
  client: StatsigClient | null;
}

// Crear un contexto simple para Statsig
const StatsigContext = createContext<StatsigContextType | null>(null);

// Hook personalizado para usar Statsig
export const useStatsigClient = () => {
  const context = useContext(StatsigContext);
  return context || { client: null };
};

// Componente de provider simplificado
export default function MyStatsig({ children }: { children: React.ReactNode }) {
  // Cliente mock para desarrollo
  const mockClient: StatsigClient = {
    logEvent: (eventName: string, metadata?: Record<string, string | number | boolean>) => {
      console.log('Statsig Event:', eventName, metadata);
    },
    checkGate: (gateName: string) => {
      console.log('Statsig Gate Check:', gateName);
      return false;
    }
  };

  return (
    <StatsigContext.Provider value={{ client: mockClient }}>
      {children}
    </StatsigContext.Provider>
  );
}

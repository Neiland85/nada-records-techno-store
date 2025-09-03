'use client';

import { Header } from '@/components';
import { AudioPlayerProvider } from '@/contexts';
import { ReactNode } from 'react';

interface RootLayoutProps {
  children: ReactNode;
}

export function RootLayout({ children }: RootLayoutProps) {
  return (
    <AudioPlayerProvider>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black">
        <Header />
        <main className="flex-1">
          {children}
        </main>
        {/* Aquí puedes agregar un footer si es necesario */}
      </div>
    </AudioPlayerProvider>
  );
}

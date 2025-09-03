import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { AudioPlayerProvider } from '../contexts/AudioPlayerContext';
import './globals.css';
import MyStatsig from './my-statsig';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Nada Records Techno Store',
  description: 'Tienda de música techno y vinilos',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <MyStatsig>
          <AudioPlayerProvider>
            {children}
          </AudioPlayerProvider>
        </MyStatsig>
      </body>
    </html>
  );
}

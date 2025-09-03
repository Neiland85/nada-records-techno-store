import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Configuración moderna para Next.js 15
  experimental: {
    // Configuración actualizada - movido de experimental.serverComponentsExternalPackages
  },

  // Nueva configuración para paquetes externos del servidor (Next.js 15+)
  serverExternalPackages: ['@vercel/blob', 'wavesurfer.js'],

  // Configuración de imágenes
  images: {
    domains: ['mismxnqktkjxmccf.public.blob.vercel-storage.com'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '*.vercel-storage.com',
        port: '',
        pathname: '**',
      },
    ],
  },

  // Configuración de TypeScript
  typescript: {
    ignoreBuildErrors: false,
  },

  // Configuración de ESLint
  eslint: {
    ignoreDuringBuilds: false,
  },
};

export default nextConfig;

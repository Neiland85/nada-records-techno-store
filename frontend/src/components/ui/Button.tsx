'use client';

import { ButtonHTMLAttributes, ReactNode } from 'react';
import { cn } from '../../utils';

type ButtonVariant = 'default' | 'secondary' | 'outline' | 'ghost' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg' | 'xl';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
}

const variantClasses: Record<ButtonVariant, string> = {
  default: 'bg-techno-primary text-white hover:bg-techno-primary/80 focus:ring-techno-primary',
  secondary: 'bg-techno-secondary text-white hover:bg-techno-secondary/80 focus:ring-techno-secondary',
  outline: 'border-2 border-techno-primary text-techno-primary hover:bg-techno-primary hover:text-white focus:ring-techno-primary',
  ghost: 'text-gray-300 hover:text-techno-primary hover:bg-techno-primary/10 focus:ring-techno-primary',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-600',
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'h-8 px-3 text-sm',
  md: 'h-10 px-4 text-base',
  lg: 'h-12 px-6 text-lg',
  xl: 'h-14 px-8 text-xl',
};

export function Button({
  className = '',
  variant = 'default',
  size = 'md',
  isLoading,
  children,
  disabled,
  ...props
}: ButtonProps) {
  const baseClasses = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';

  return (
    <button
      className={cn(baseClasses, variantClasses[variant], sizeClasses[size], className)}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          <span>Cargando...</span>
        </div>
      ) : (
        children
      )}
    </button>
  );
}

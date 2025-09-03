import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Re-export for convenience
export { clsx } from 'clsx';
export { twMerge } from 'tailwind-merge';


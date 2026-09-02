import React from 'react';

export function Card({ children, className = '', ...props }) {
  return (
    <div 
      className={`bg-[var(--color-bg-card)] border border-[var(--color-border)] rounded-xl shadow-sm overflow-hidden ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }) {
  return (
    <div className={`px-6 py-4 border-b border-[var(--color-border)] ${className}`}>
      {children}
    </div>
  );
}

export function CardContent({ children, className = '' }) {
  return (
    <div className={`p-6 ${className}`}>
      {children}
    </div>
  );
}

export function CardFooter({ children, className = '' }) {
  return (
    <div className={`px-6 py-4 bg-gray-50 border-t border-[var(--color-border)] ${className}`}>
      {children}
    </div>
  );
}

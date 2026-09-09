import React from 'react';

export function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  className = '', 
  ...props 
}) {
  const baseStyle = "inline-flex items-center justify-center font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";
  
  const variants = {
    primary: "bg-[var(--color-brand-orange)] text-white hover:bg-[#d96a1a] focus:ring-[var(--color-brand-orange)]",
    secondary: "bg-[var(--color-brand-orange-light)] text-[var(--color-brand-orange)] hover:bg-[#fce6d8] focus:ring-[var(--color-brand-orange)]",
    outline: "border border-[var(--color-border)] text-[var(--color-text-main)] hover:bg-gray-50 focus:ring-gray-200",
    ghost: "text-[var(--color-text-secondary)] hover:text-[var(--color-text-main)] hover:bg-gray-100 focus:ring-gray-200"
  };
  
  const sizes = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-sm",
    lg: "px-6 py-3 text-base"
  };

  return (
    <button 
      className={`${baseStyle} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}

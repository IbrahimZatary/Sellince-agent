import React, { forwardRef } from 'react';

export const Input = forwardRef(({ 
  label, 
  error, 
  type = 'text', 
  className = '', 
  ...props 
}, ref) => {
  return (
    <div className="flex flex-col mb-4">
      {label && (
        <label className="mb-1.5 text-sm font-medium text-[var(--color-text-main)]">
          {label}
        </label>
      )}
      <input
        ref={ref}
        type={type}
        className={`px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors ${
          error 
            ? 'border-red-500 focus:ring-red-200' 
            : 'border-[var(--color-border)] focus:border-[var(--color-brand-orange)] focus:ring-[var(--color-brand-orange-light)]'
        } ${className}`}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
});

Input.displayName = 'Input';

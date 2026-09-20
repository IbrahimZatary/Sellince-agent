import React from 'react';
import { Check } from 'lucide-react';

export function StepIndicator({ steps, currentStep }) {
  return (
    <div className="flex items-center justify-center w-full mb-8">
      {steps.map((step, index) => {
        const isCompleted = index < currentStep;
        const isActive = index === currentStep;

        return (
          <React.Fragment key={step.id}>
            {/* Step Circle */}
            <div className="flex flex-col items-center relative">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-colors ${
                  isCompleted
                    ? 'bg-[var(--color-success)] text-white'
                    : isActive
                    ? 'bg-[var(--color-brand-orange)] text-white ring-4 ring-[var(--color-brand-orange-light)]'
                    : 'bg-gray-100 text-[var(--color-text-muted)] border border-gray-200'
                }`}
              >
                {isCompleted ? <Check className="w-5 h-5" /> : index + 1}
              </div>
              <span 
                className={`absolute top-12 text-xs font-medium w-32 text-center ${
                  isActive || isCompleted ? 'text-[var(--color-text-main)]' : 'text-[var(--color-text-muted)]'
                }`}
              >
                {step.title}
              </span>
            </div>

            {/* Connecting Line */}
            {index < steps.length - 1 && (
              <div className="w-16 md:w-24 h-1 mx-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-[var(--color-success)] transition-all duration-300"
                  style={{ width: isCompleted ? '100%' : '0%' }}
                />
              </div>
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}

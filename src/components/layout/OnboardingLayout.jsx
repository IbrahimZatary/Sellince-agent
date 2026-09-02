import { Outlet, useLocation } from 'react-router-dom';
import { StepIndicator } from '../../components/ui/StepIndicator';

const ONBOARDING_STEPS = [
  { id: 'company', title: 'Company Details', path: '/onboarding/company' },
  { id: 'agent', title: 'Agent Behavior', path: '/onboarding/agent' },
  { id: 'complete', title: 'Setup Complete', path: '/onboarding/complete' }
];

export default function OnboardingLayout() {
  const location = useLocation();
  
  // Determine current step index based on path
  const currentStep = ONBOARDING_STEPS.findIndex(step => location.pathname.includes(step.path));
  const activeStepIndex = currentStep === -1 ? 0 : currentStep;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-3xl mb-8 flex justify-center">
        <h1 className="text-3xl font-bold text-[var(--color-brand-orange)] tracking-wider">SELLINCE</h1>
      </div>
      
      <div className="w-full max-w-3xl">
        <StepIndicator steps={ONBOARDING_STEPS} currentStep={activeStepIndex} />
      </div>

      <div className="w-full max-w-2xl mt-8">
        <Outlet />
      </div>
    </div>
  );
}

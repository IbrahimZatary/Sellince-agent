import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Phone, Building2 } from 'lucide-react';

const INDUSTRIES = [
  { id: 'telecom', name: 'Telecommunications', description: 'Configure AI agent for telecom support and sales.', icon: Phone },
  { id: 'banking', name: 'Banking', description: 'Configure AI agent for banking services and financial support.', icon: Building2 }
];

export default function AgentBehavior() {
  const navigate = useNavigate();
  const [selectedIndustry, setSelectedIndustry] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedIndustry) return;
    navigate('/onboarding/complete');
  };

  return (
    <Card className="w-full">
      <CardHeader className="text-center border-b-0 pb-0">
        <h2 className="text-2xl font-bold text-[var(--color-text-main)]">Agent Behavior</h2>
        <p className="text-[var(--color-text-secondary)] mt-2">Select your industry to configure initial AI agent behavior</p>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {INDUSTRIES.map((industry) => (
              <div 
                key={industry.id}
                onClick={() => setSelectedIndustry(industry.id)}
                className={`p-4 border-2 rounded-xl cursor-pointer transition-all ${
                  selectedIndustry === industry.id 
                    ? 'border-[var(--color-brand-orange)] bg-[var(--color-brand-orange-light)]' 
                    : 'border-[var(--color-border)] hover:border-gray-300'
                }`}
              >
                <div className="flex flex-col items-center text-center space-y-3">
                  <div className={`p-3 rounded-full ${selectedIndustry === industry.id ? 'bg-[var(--color-brand-orange)] text-white' : 'bg-gray-100 text-gray-500'}`}>
                    <industry.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-[var(--color-text-main)]">{industry.name}</h3>
                    <p className="text-sm text-[var(--color-text-secondary)] mt-1">{industry.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-between pt-4">
            <Button type="button" variant="ghost" onClick={() => navigate('/onboarding/company')}>
              Back
            </Button>
            <Button type="submit" disabled={!selectedIndustry}>
              Complete Setup
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

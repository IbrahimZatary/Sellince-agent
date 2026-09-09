import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';

export default function CompanyInfo() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    website: '',
    teamSize: '1-10',
    primaryGoal: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate saving company info
    navigate('/onboarding/agent');
  };

  return (
    <Card className="w-full">
      <CardHeader className="text-center border-b-0 pb-0">
        <h2 className="text-2xl font-bold text-[var(--color-text-main)]">Tell us about your company</h2>
        <p className="text-[var(--color-text-secondary)] mt-2">This helps us tailor your AI agent's experience</p>
      </CardHeader>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <Input
            label="Company Website"
            type="url"
            value={formData.website}
            onChange={(e) => setFormData({ ...formData, website: e.target.value })}
            placeholder="https://www.example.com"
          />

          <div className="flex flex-col mb-4">
            <label className="mb-1.5 text-sm font-medium text-[var(--color-text-main)]">Team Size</label>
            <select
              value={formData.teamSize}
              onChange={(e) => setFormData({ ...formData, teamSize: e.target.value })}
              className="px-4 py-2 border border-[var(--color-border)] rounded-lg focus:outline-none focus:ring-2 focus:border-[var(--color-brand-orange)] focus:ring-[var(--color-brand-orange-light)] bg-white"
            >
              <option value="1-10">1-10 employees</option>
              <option value="11-50">11-50 employees</option>
              <option value="51-200">51-200 employees</option>
              <option value="201+">201+ employees</option>
            </select>
          </div>

          <Input
            label="Primary Goal"
            value={formData.primaryGoal}
            onChange={(e) => setFormData({ ...formData, primaryGoal: e.target.value })}
            placeholder="e.g. Increase sales conversions"
          />

          <div className="flex justify-end pt-4">
            <Button type="submit">
              Continue to Agent Behavior
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

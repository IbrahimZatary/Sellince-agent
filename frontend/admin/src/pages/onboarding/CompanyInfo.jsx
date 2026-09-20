import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { useAuth } from '../../app/providers/AuthContext';

const SECTORS = [
  { value: 'telecom', label: 'Telecom' },
  { value: 'banking', label: 'Banking' },
];

const PLANS = [
  { value: 'pilot', label: 'Pilot' },
  { value: 'standard', label: 'Standard' },
  { value: 'enterprise', label: 'Enterprise' },
];

export default function CompanyInfo() {
  const navigate = useNavigate();
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    companyName: user?.company_name || '',
    sector: user?.sector || 'telecom',
    subscriptionTier: user?.subscription_tier || 'standard',
  });
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    try {
      await updateProfile({
        company_name: formData.companyName,
        sector: formData.sector,
        subscription_tier: formData.subscriptionTier,
      });
      navigate('/onboarding/agent');
    } catch (err) {
      setError(err.response?.data?.message || 'Could not save company details. Please try again.');
    } finally {
      setSaving(false);
    }
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
            label="Company Name"
            required
            value={formData.companyName}
            onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
            placeholder="e.g. Orange Jordan"
          />

          <div className="flex flex-col mb-4">
            <label className="mb-1.5 text-sm font-medium text-[var(--color-text-main)]">Industry</label>
            <select
              value={formData.sector}
              onChange={(e) => setFormData({ ...formData, sector: e.target.value })}
              className="px-4 py-2 border border-[var(--color-border)] rounded-lg focus:outline-none focus:ring-2 focus:border-[var(--color-brand-orange)] focus:ring-[var(--color-brand-orange-light)] bg-white"
            >
              {SECTORS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="flex flex-col mb-4">
            <label className="mb-1.5 text-sm font-medium text-[var(--color-text-main)]">Subscription Plan</label>
            <select
              value={formData.subscriptionTier}
              onChange={(e) => setFormData({ ...formData, subscriptionTier: e.target.value })}
              className="px-4 py-2 border border-[var(--color-border)] rounded-lg focus:outline-none focus:ring-2 focus:border-[var(--color-brand-orange)] focus:ring-[var(--color-brand-orange-light)] bg-white"
            >
              {PLANS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
              {error}
            </p>
          )}

          <div className="flex justify-end pt-4">
            <Button type="submit" disabled={saving}>
              {saving ? 'Saving…' : 'Continue to Agent Behavior'}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
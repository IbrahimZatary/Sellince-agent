import { useState } from 'react';
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

export default function Settings() {
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    fullName: user?.full_name || '',
    companyName: user?.company_name || '',
    sector: user?.sector || 'telecom',
    subscriptionTier: user?.subscription_tier || 'standard',
  });
  const [status, setStatus] = useState('idle'); // 'idle' | 'saving' | 'saved' | 'error'
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('saving');
    setError('');
    try {
      await updateProfile({
        full_name: formData.fullName,
        company_name: formData.companyName,
        sector: formData.sector,
        subscription_tier: formData.subscriptionTier,
      });
      setStatus('saved');
      setTimeout(() => setStatus('idle'), 2500);
    } catch (err) {
      setError(err.response?.data?.message || 'Could not save your changes.');
      setStatus('error');
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-[var(--color-text-main)]">Settings</h1>
        <p className="text-[var(--color-text-secondary)] mt-1">Your profile and company details</p>
      </div>

      <Card className="max-w-2xl">
        <CardHeader>
          <h3 className="text-lg font-medium text-[var(--color-text-main)]">Company Profile</h3>
          <p className="text-sm text-[var(--color-text-secondary)]">
            These are stored with your account and shown across the app.
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Your Name"
              value={formData.fullName}
              onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
              placeholder="Your full name"
            />

            <Input
              label="Email"
              value={user?.email || ''}
              disabled
              readOnly
            />

            <Input
              label="Company Name"
              value={formData.companyName}
              onChange={(e) => setFormData({ ...formData, companyName: e.target.value })}
              placeholder="e.g. Orange Jordan"
            />

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="flex flex-col">
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
              <div className="flex flex-col">
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
            </div>

            {error && (
              <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
                {error}
              </p>
            )}

            <div className="flex items-center gap-4 pt-2">
              <Button type="submit" disabled={status === 'saving'}>
                {status === 'saving' ? 'Saving…' : 'Save changes'}
              </Button>
              {status === 'saved' && (
                <span className="text-sm text-[var(--color-success)]">Saved</span>
              )}
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
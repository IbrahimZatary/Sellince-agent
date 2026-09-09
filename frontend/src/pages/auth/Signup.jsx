import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { signup } from '../../services/api/auth.api';

export default function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    companyName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords don't match");
      setIsLoading(false);
      return;
    }

    try {
      await signup(formData);
      // Navigate to the next step in onboarding
      navigate('/onboarding/agent');
    } catch (err) {
      setError('An error occurred during signup');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center pb-2">
          <h1 className="text-2xl font-bold text-[var(--color-brand-orange)] tracking-wider mb-2">SELLINCE</h1>
          <h2 className="text-xl font-semibold text-[var(--color-text-main)]">Create an account</h2>
          <p className="text-sm text-[var(--color-text-secondary)] mt-1">Start automating your customer engagement</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg border border-red-100">
                {error}
              </div>
            )}
            
            <Input
              label="Company Name"
              name="companyName"
              required
              value={formData.companyName}
              onChange={handleChange}
              placeholder="Acme Corp"
            />

            <Input
              label="Company Email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              placeholder="admin@company.com"
            />
            
            <Input
              label="Password"
              name="password"
              type="password"
              required
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
            />

            <Input
              label="Confirm Password"
              name="confirmPassword"
              type="password"
              required
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
            />
            
            <Button type="submit" className="w-full mt-6" disabled={isLoading}>
              {isLoading ? 'Creating account...' : 'Create account'}
            </Button>
            
            <p className="text-center text-sm text-[var(--color-text-secondary)] mt-4">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-[var(--color-brand-orange)] hover:underline">
                Sign in
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

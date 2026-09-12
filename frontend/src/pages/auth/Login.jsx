import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card, CardContent, CardHeader } from '../../components/ui/Card';
import { Input } from '../../components/ui/Input';
import { Button } from '../../components/ui/Button';
import { login } from '../../services/api/auth.api';
import { tokenStore } from '../../services/api/tokenStore';

export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const data = await login(formData);
      tokenStore.set(data.access_token);
      // Navigate to dashboard after successful login
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.message || 'Invalid email or password');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center pb-2">
          <h1 className="text-2xl font-bold text-[var(--color-brand-orange)] tracking-wider mb-2">SELLINCE</h1>
          <h2 className="text-xl font-semibold text-[var(--color-text-main)]">Welcome back</h2>
          <p className="text-sm text-[var(--color-text-secondary)] mt-1">Sign in to manage your AI agents</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 text-sm text-red-600 bg-red-50 rounded-lg border border-red-100">
                {error}
              </div>
            )}
            
            <Input
              label="Company email"
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              placeholder="admin@company.com"
            />
            
            <Input
              label="Password"
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              placeholder="••••••••"
            />
            
            <div className="flex items-center justify-between text-sm">
              <label className="flex items-center text-[var(--color-text-secondary)]">
                <input type="checkbox" className="mr-2 rounded border-gray-300 text-[var(--color-brand-orange)] focus:ring-[var(--color-brand-orange)]" />
                Remember me
              </label>
              <a href="#" className="font-medium text-[var(--color-brand-orange)] hover:underline">
                Forgot password?
              </a>
            </div>
            
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign in'}
            </Button>
            
            <p className="text-center text-sm text-[var(--color-text-secondary)] mt-4">
              Don't have an account?{' '}
              <Link to="/signup" className="font-medium text-[var(--color-brand-orange)] hover:underline">
                Sign up
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}

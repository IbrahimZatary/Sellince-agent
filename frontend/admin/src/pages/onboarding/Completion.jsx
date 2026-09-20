import { useNavigate } from 'react-router-dom';
import { Card, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { CheckCircle2, Rocket } from 'lucide-react';

export default function Completion() {
  const navigate = useNavigate();

  return (
    <Card className="w-full">
      <CardContent className="pt-10 pb-8 text-center flex flex-col items-center">
        <div className="w-20 h-20 bg-[var(--color-success-light)] rounded-full flex items-center justify-center mb-6">
          <CheckCircle2 className="w-10 h-10 text-[var(--color-success)]" />
        </div>
        
        <h2 className="text-3xl font-bold text-[var(--color-text-main)] mb-2">You're all set!</h2>
        <p className="text-[var(--color-text-secondary)] mb-8 max-w-md">
          Your company profile and AI agent behavior have been configured successfully. Let's take a quick tour of the platform.
        </p>
        
        <div className="space-y-4 w-full max-w-xs">
          <Button 
            className="w-full flex items-center justify-center gap-2"
            onClick={() => navigate('/demo')}
          >
            <Rocket className="w-5 h-5" />
            Start Product Tour
          </Button>
          
          <Button 
            variant="ghost" 
            className="w-full"
            onClick={() => navigate('/dashboard')}
          >
            Skip to Dashboard
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

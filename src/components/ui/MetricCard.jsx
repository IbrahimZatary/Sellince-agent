import { ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { Card, CardContent } from './Card';

export function MetricCard({ title, value, trend, trendDirection }) {
  const isPositive = trendDirection === 'up';

  return (
    <Card>
      <CardContent className="p-6">
        <h3 className="text-sm font-medium text-[var(--color-text-secondary)]">{title}</h3>
        <div className="mt-2 flex items-baseline gap-4">
          <p className="text-3xl font-semibold text-[var(--color-text-main)]">{value}</p>
          {trend !== undefined && (
            <span className={`inline-flex items-center text-sm font-medium ${isPositive ? 'text-[var(--color-success)]' : 'text-red-600'}`}>
              {isPositive ? <ArrowUpRight className="w-4 h-4 mr-1" /> : <ArrowDownRight className="w-4 h-4 mr-1" />}
              {Math.abs(trend)}%
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

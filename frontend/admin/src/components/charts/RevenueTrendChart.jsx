import { Card, CardHeader, CardContent } from '../ui/Card';

export function RevenueTrendChart({ data }) {
  const maxRevenue = Math.max(...data.map(d => d.revenue));

  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Revenue Trend</h3>
      </CardHeader>
      <CardContent>
        <div className="h-64 flex items-end justify-between pt-4 pb-2">
          {data.map((item, index) => {
            const heightPercentage = (item.revenue / maxRevenue) * 100;
            return (
              <div key={index} className="flex flex-col items-center flex-1 mx-1 group">
                <div 
                  className="w-full max-w-[40px] bg-[var(--color-brand-orange-light)] hover:bg-[var(--color-brand-orange)] transition-colors rounded-t-sm relative flex flex-col justify-end"
                  style={{ height: `${heightPercentage}%`, minHeight: '10%' }}
                >
                  {/* Tooltip on hover (simple version) */}
                  <div className="opacity-0 group-hover:opacity-100 absolute bottom-full mb-2 bg-gray-900 text-white text-xs px-2 py-1 rounded whitespace-nowrap pointer-events-none transition-opacity">
                    ${item.revenue.toLocaleString()}
                  </div>
                </div>
                <span className="text-xs text-[var(--color-text-secondary)] mt-2">{item.date}</span>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

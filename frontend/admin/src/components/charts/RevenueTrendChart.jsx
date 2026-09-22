import { Card, CardHeader, CardContent } from '../ui/Card';

export function RevenueTrendChart({ data }) {
  const maxRevenue = Math.max(...data.map(d => d.revenue), 1);
  const CHART_HEIGHT = 220; // px - inner chart area height (excluding labels)

  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Revenue Trend</h3>
      </CardHeader>
      <CardContent>
        <div className="h-64 pt-4 pb-2">
          <div className="h-[220px] flex items-end justify-between">
            {data.map((item, index) => {
              const heightPx = item.revenue > 0 ? Math.max((item.revenue / maxRevenue) * CHART_HEIGHT, 20) : 0;
              return (
                <div key={index} className="flex flex-col items-center flex-1 mx-1">
                  <div
                    className="w-full max-w-[40px] bg-[var(--color-brand-orange)] rounded-t-sm relative flex flex-col justify-end"
                    style={{ height: `${heightPx}px` }}
                  >
                    {/* Revenue label on top of bar */}
                    {item.revenue > 0 && (
                      <div className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-medium text-[var(--color-text-main)] whitespace-nowrap">
                        ${item.revenue.toLocaleString()}
                      </div>
                    )}
                  </div>
                  <span className="text-xs text-[var(--color-text-secondary)] mt-2">{item.date}</span>
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

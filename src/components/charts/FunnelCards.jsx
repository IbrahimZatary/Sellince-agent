import { Card, CardHeader, CardContent } from '../ui/Card';

export function ConversionFunnelCard({ data }) {
  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Conversion Funnel</h3>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((item, index) => (
            <div key={index} className="flex flex-col">
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-[var(--color-text-main)]">{item.stage}</span>
                <span className="text-[var(--color-text-secondary)]">{item.count.toLocaleString()} ({item.percentage}%)</span>
              </div>
              <div className="w-full bg-gray-100 h-6 flex rounded overflow-hidden">
                <div 
                  className="bg-[var(--color-brand-orange)] transition-all flex items-center justify-end px-2"
                  style={{ width: `${item.percentage}%` }}
                >
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export function RevenueByOfferCard({ data }) {
  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Revenue by Offer Type</h3>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 mt-2">
          {data.map((item, index) => (
            <div key={index}>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-[var(--color-text-secondary)]">{item.category}</span>
                <span className="font-medium text-[var(--color-text-main)]">{item.value}%</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{ width: `${item.value}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

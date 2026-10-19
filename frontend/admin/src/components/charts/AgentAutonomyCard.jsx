import { Card, CardHeader, CardContent } from '../ui/Card';

export function AgentAutonomyCard({ data }) {
  return (
    <Card>
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Agent Autonomy</h3>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {data.map((item, index) => (
            <div key={index}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-[var(--color-text-main)]">{item.status}</span>
                <span className="text-[var(--color-text-secondary)]">{item.percentage}%</span>
              </div>
              <div className="w-full bg-gray-100 rounded-full h-2.5">
                <div 
                  className={`h-2.5 rounded-full ${item.color}`} 
                  style={{ width: `${item.percentage}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

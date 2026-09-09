import { Card, CardHeader, CardContent } from '../ui/Card';

export function RecentActivityTable({ activities }) {
  return (
    <Card className="col-span-1 lg:col-span-2">
      <CardHeader>
        <h3 className="text-lg font-medium text-[var(--color-text-main)]">Recent Agent Activity</h3>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-[var(--color-text-secondary)] uppercase bg-gray-50 border-b border-[var(--color-border)]">
              <tr>
                <th className="px-6 py-3 font-medium">Customer</th>
                <th className="px-6 py-3 font-medium">Signal</th>
                <th className="px-6 py-3 font-medium">Action/Offer</th>
                <th className="px-6 py-3 font-medium">Status</th>
                <th className="px-6 py-3 font-medium text-right">Time</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity) => (
                <tr key={activity.id} className="border-b border-[var(--color-border)] last:border-0 hover:bg-gray-50/50">
                  <td className="px-6 py-4">
                    <div className="font-medium text-[var(--color-text-main)]">{activity.customer}</div>
                    <div className="text-[var(--color-text-muted)] text-xs">{activity.identifier}</div>
                  </td>
                  <td className="px-6 py-4 text-[var(--color-text-secondary)]">{activity.signal}</td>
                  <td className="px-6 py-4 text-[var(--color-text-main)] font-medium">{activity.action}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      activity.status === 'Won' ? 'bg-[var(--color-success-light)] text-[var(--color-success)]' :
                      activity.status === 'Handed to human' ? 'bg-orange-100 text-orange-700' :
                      activity.status === 'In progress' ? 'bg-blue-100 text-blue-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {activity.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-[var(--color-text-muted)] whitespace-nowrap">
                    {activity.timestamp}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

import { useCallback, useEffect, useState } from 'react';
import { getDashboardSummary } from '../../services/api/dashboard.api';

const AUTONOMY_COLORS = {
  'Auto-resolved': 'bg-green-500',
  'Handed to human': 'bg-orange-500',
  'Follow-up queued': 'bg-gray-400',
};

const ACTIVITY_STATUS_LABELS = {
  open: 'In progress',
  closed: 'Closed',
};

const mapStatusLabel = (activity) => ({
  ...activity,
  status: ACTIVITY_STATUS_LABELS[activity.status] || activity.status,
});

const withUndefinedTrend = (metric) => ({ ...metric, trend: metric.trend ?? undefined });

export function useDashboard() {
  const [data, setData] = useState(null);
  const [status, setStatus] = useState('loading');
  const [error, setError] = useState('');

  const load = useCallback(async () => {
    setStatus('loading');
    setError('');
    try {
      const summary = await getDashboardSummary();
      setData({
        ...summary,
        overviewMetrics: summary.overviewMetrics.map(withUndefinedTrend),
        agentAutonomy: summary.agentAutonomy.map((slice) => ({
          ...slice,
          color: AUTONOMY_COLORS[slice.status] || 'bg-gray-400',
        })),
        recentActivity: summary.recentActivity.map(mapStatusLabel),
      });
      setStatus('ready');
    } catch (err) {
      setError(err.response?.data?.message || err.response?.data?.detail?.[0]?.msg || 'Failed to load dashboard');
      setStatus('error');
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  return { data, status, error, retry: load };
}
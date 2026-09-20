import { useDashboard } from '../../app/hooks/useDashboard';
import { MetricCard } from '../../components/ui/MetricCard';
import { RecentActivityTable } from '../../components/tables/RecentActivityTable';
import { AgentAutonomyCard } from '../../components/charts/AgentAutonomyCard';
import { ConversionFunnelCard, RevenueByOfferCard } from '../../components/charts/FunnelCards';
import { RevenueTrendChart } from '../../components/charts/RevenueTrendChart';

export default function Dashboard() {
  const { data, status, error, retry } = useDashboard();

  if (status === 'loading') {
    return (
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 className="text-2xl font-bold text-[var(--color-text-main)]">Dashboard</h1>
            <p className="text-[var(--color-text-secondary)] mt-1">
              Loading your AI agent's performance…
            </p>
          </div>
        </div>
        <div className="animate-pulse grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-32 rounded-lg bg-[var(--color-border)]/40" />
          ))}
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h1 className="text-2xl font-bold text-[var(--color-text-main)]">Dashboard</h1>
            <p className="text-[var(--color-text-secondary)] mt-1">
              Overview of your AI agent's performance
            </p>
          </div>
        </div>
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-red-700 font-medium">{error}</p>
          <p className="text-red-500 text-sm mt-1">Could not reach the backend.</p>
          <button
            onClick={retry}
            className="mt-4 px-4 py-2 rounded-md bg-[var(--color-brand-orange)] text-white text-sm hover:opacity-90"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const { overviewMetrics, revenueTrend, conversionFunnel, revenueByOffer, agentAutonomy, recentActivity } = data;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h1 className="text-2xl font-bold text-[var(--color-text-main)]">Dashboard</h1>
          <p className="text-[var(--color-text-secondary)] mt-1">Overview of your AI agent's performance</p>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {overviewMetrics.map((metric) => (
          <MetricCard 
            key={metric.id}
            title={metric.label}
            value={metric.value}
            trend={metric.trend}
            trendDirection={metric.trendDirection}
          />
        ))}
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <RevenueTrendChart data={revenueTrend} />
        <AgentAutonomyCard data={agentAutonomy} />
      </div>

      {/* Secondary Data & Funnel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RecentActivityTable activities={recentActivity} />
        </div>
        <div className="space-y-6">
          <ConversionFunnelCard data={conversionFunnel} />
          <RevenueByOfferCard data={revenueByOffer} />
        </div>
      </div>
    </div>
  );
}

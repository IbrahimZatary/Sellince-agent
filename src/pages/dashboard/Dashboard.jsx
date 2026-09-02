import { dashboardMocks } from '../../mocks/dashboard.mock';
import { MetricCard } from '../../components/ui/MetricCard';
import { RecentActivityTable } from '../../components/tables/RecentActivityTable';
import { AgentAutonomyCard } from '../../components/charts/AgentAutonomyCard';
import { ConversionFunnelCard, RevenueByOfferCard } from '../../components/charts/FunnelCards';
import { RevenueTrendChart } from '../../components/charts/RevenueTrendChart';

export default function Dashboard() {
  const { overviewMetrics, revenueTrend, conversionFunnel, revenueByOffer, agentAutonomy, recentActivity } = dashboardMocks;

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

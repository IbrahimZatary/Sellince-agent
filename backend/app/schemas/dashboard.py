from pydantic import BaseModel


class OverviewMetric(BaseModel):
    id: str
    label: str
    value: int | str
    trend: int | None = None
    trendDirection: str = "up"


class TrendPoint(BaseModel):
    date: str
    revenue: float
    arpu: float | None = None


class FunnelStage(BaseModel):
    stage: str
    count: int
    percentage: int


class OfferShare(BaseModel):
    category: str
    value: int


class AutonomySlice(BaseModel):
    status: str
    percentage: int


class ActivityRow(BaseModel):
    id: int
    customer: str
    identifier: str
    signal: str
    action: str
    status: str
    timestamp: str


class DashboardSummary(BaseModel):
    overviewMetrics: list[OverviewMetric]
    revenueTrend: list[TrendPoint]
    conversionFunnel: list[FunnelStage]
    revenueByOffer: list[OfferShare]
    agentAutonomy: list[AutonomySlice]
    recentActivity: list[ActivityRow]
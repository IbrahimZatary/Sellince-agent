export const dashboardMocks = {
  overviewMetrics: [
    { id: 'conversations', label: 'Conversations Handled', value: '12,450', trend: 15, trendDirection: 'up' },
    { id: 'revenue', label: 'Revenue Generated', value: '$184,300', trend: 22.4, trendDirection: 'up' },
    { id: 'conversion', label: 'Conversion Rate', value: '14.2%', trend: 4.1, trendDirection: 'up' },
    { id: 'churn', label: 'Churn Prevented', value: '85', trend: -2, trendDirection: 'down' } // fewer churn is good, but usually presented as positive if "prevented"
  ],
  revenueTrend: [
    { date: 'Mon', revenue: 4000, arpu: 24 },
    { date: 'Tue', revenue: 3000, arpu: 22 },
    { date: 'Wed', revenue: 5000, arpu: 28 },
    { date: 'Thu', revenue: 2780, arpu: 20 },
    { date: 'Fri', revenue: 6890, arpu: 35 },
    { date: 'Sat', revenue: 2390, arpu: 18 },
    { date: 'Sun', revenue: 3490, arpu: 25 },
  ],
  conversionFunnel: [
    { stage: 'Engaged', count: 12450, percentage: 100 },
    { stage: 'Replied', count: 8300, percentage: 66 },
    { stage: 'Offer Presented', count: 3100, percentage: 25 },
    { stage: 'Closed', count: 1767, percentage: 14 }
  ],
  revenueByOffer: [
    { category: 'Data Upgrades', value: 45 },
    { category: 'Device Upsell', value: 30 },
    { category: 'Add-ons', value: 15 },
    { category: 'Retention Saves', value: 10 }
  ],
  agentAutonomy: [
    { status: 'Auto-resolved', percentage: 75, color: 'bg-green-500' },
    { status: 'Handed to human', percentage: 15, color: 'bg-orange-500' },
    { status: 'Follow-up queued', percentage: 10, color: 'bg-gray-400' }
  ],
  recentActivity: [
    { id: 1, customer: 'John Doe', identifier: '+1 234 567 8900', signal: 'High Data Usage', action: 'Offered 5GB Plan', status: 'Won', timestamp: '2 mins ago' },
    { id: 2, customer: 'Jane Smith', identifier: '+1 987 654 3210', signal: 'Complaint', action: 'Apology & Discount', status: 'Handed to human', timestamp: '15 mins ago' },
    { id: 3, customer: 'Alice Johnson', identifier: '+1 555 123 4567', signal: 'Contract Expiring', action: 'Renewal Offer', status: 'In progress', timestamp: '1 hour ago' },
    { id: 4, customer: 'Bob Brown', identifier: '+1 444 987 6543', signal: 'Browsing Upgrades', action: 'Device Upsell', status: 'Closed', timestamp: '2 hours ago' }
  ]
};

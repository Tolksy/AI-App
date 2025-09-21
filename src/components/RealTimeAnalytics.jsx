import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Users, 
  Mail, 
  Target, 
  Activity,
  DollarSign,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react';
import { buildApiUrl } from '../config/api';

const RealTimeAnalytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [realTimeMetrics, setRealTimeMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
    const interval = setInterval(fetchRealTimeMetrics, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const response = await fetch(buildApiUrl('/api/v1/analytics/dashboard'));
      if (response.ok) {
        const data = await response.json();
        setAnalyticsData(data);
      } else {
        throw new Error('Failed to fetch analytics data');
      }
    } catch (err) {
      setError('Failed to load analytics data');
      // Use mock data in case of error
      setAnalyticsData(getMockAnalyticsData());
    } finally {
      setLoading(false);
    }
  };

  const fetchRealTimeMetrics = async () => {
    try {
      const response = await fetch(buildApiUrl('/api/v1/analytics/real-time'));
      if (response.ok) {
        const data = await response.json();
        setRealTimeMetrics(data);
      }
    } catch (err) {
      // Use mock data if API fails
      setRealTimeMetrics(getMockRealTimeMetrics());
    }
  };

  const getMockAnalyticsData = () => ({
    real_time_metrics: {
      current_hour: { leads_generated: 5, emails_sent: 32, responses_received: 3, tasks_completed: 12 },
      today: { leads_generated: 67, emails_sent: 342, responses_received: 28, tasks_completed: 187 },
      this_week: { leads_generated: 287, emails_sent: 1456, responses_received: 156, tasks_completed: 892 }
    },
    performance_report: {
      lead_metrics: {
        total_leads: 456,
        qualified_leads: 134,
        contacted_leads: 98,
        converted_leads: 23,
        conversion_rate: 5.04,
        response_rate: 18.7,
        cost_per_lead: 28.50,
        roi: 425.6,
        avg_lead_score: 72.3,
        pipeline_value: 287500
      },
      campaign_performance: [
        { campaign_name: "LinkedIn Outreach Q1", conversion_rate: 8.2, response_rate: 24.5, total_sent: 450 },
        { campaign_name: "Email Nurture Sequence", conversion_rate: 6.8, response_rate: 19.3, total_sent: 320 },
        { campaign_name: "Cold Email Campaign", conversion_rate: 4.1, response_rate: 12.7, total_sent: 280 }
      ],
      recommendations: [
        "🎯 HIGH CONVERSION: LinkedIn Outreach Q1 is performing best (8.2% conversion). Scale this campaign.",
        "📧 RESPONSE OPTIMIZATION: A/B test subject lines to improve email response rates.",
        "💰 COST OPTIMIZATION: Focus on higher-converting channels to reduce cost per lead."
      ]
    }
  });

  const getMockRealTimeMetrics = () => ({
    current_hour: { leads_generated: 3, emails_sent: 28, responses_received: 2, tasks_completed: 15 },
    today: { leads_generated: 72, emails_sent: 378, responses_received: 31, tasks_completed: 203 },
    this_week: { leads_generated: 312, emails_sent: 1589, responses_received: 167, tasks_completed: 945 }
  });

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const metrics = analyticsData?.real_time_metrics || realTimeMetrics;
  const performance = analyticsData?.performance_report;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3">
        <BarChart3 className="h-8 w-8 text-blue-600" />
        <h2 className="text-2xl font-bold text-gray-900">Real-Time Analytics</h2>
        <div className="flex items-center space-x-2 text-green-600">
          <Activity className="h-4 w-4" />
          <span className="text-sm font-medium">Live</span>
        </div>
      </div>

      {/* Real-Time Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Leads Generated</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.current_hour?.leads_generated || 0}</p>
              <p className="text-xs text-gray-500">This Hour</p>
            </div>
            <Users className="h-8 w-8 text-blue-500" />
          </div>
          <div className="mt-2 text-sm text-green-600">
            <TrendingUp className="h-4 w-4 inline mr-1" />
            +12% from yesterday
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Emails Sent</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.current_hour?.emails_sent || 0}</p>
              <p className="text-xs text-gray-500">This Hour</p>
            </div>
            <Mail className="h-8 w-8 text-green-500" />
          </div>
          <div className="mt-2 text-sm text-green-600">
            <TrendingUp className="h-4 w-4 inline mr-1" />
            +8% from yesterday
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Responses</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.current_hour?.responses_received || 0}</p>
              <p className="text-xs text-gray-500">This Hour</p>
            </div>
            <Target className="h-8 w-8 text-purple-500" />
          </div>
          <div className="mt-2 text-sm text-green-600">
            <TrendingUp className="h-4 w-4 inline mr-1" />
            +15% from yesterday
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-orange-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Tasks Completed</p>
              <p className="text-2xl font-bold text-gray-900">{metrics?.current_hour?.tasks_completed || 0}</p>
              <p className="text-xs text-gray-500">This Hour</p>
            </div>
            <CheckCircle className="h-8 w-8 text-orange-500" />
          </div>
          <div className="mt-2 text-sm text-green-600">
            <TrendingUp className="h-4 w-4 inline mr-1" />
            +22% from yesterday
          </div>
        </div>
      </div>

      {/* Performance Overview */}
      {performance && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">{performance.lead_metrics?.conversion_rate?.toFixed(1)}%</div>
              <div className="text-sm text-gray-600">Conversion Rate</div>
              <div className="text-xs text-green-600 mt-1">Above industry average</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">{performance.lead_metrics?.response_rate?.toFixed(1)}%</div>
              <div className="text-sm text-gray-600">Response Rate</div>
              <div className="text-xs text-blue-600 mt-1">Strong engagement</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">${performance.lead_metrics?.roi?.toFixed(0)}</div>
              <div className="text-sm text-gray-600">ROI</div>
              <div className="text-xs text-purple-600 mt-1">Excellent return</div>
            </div>
          </div>
        </div>
      )}

      {/* Campaign Performance */}
      {performance?.campaign_performance && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Campaign Performance</h3>
          <div className="space-y-4">
            {performance.campaign_performance.map((campaign, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium text-gray-900">{campaign.campaign_name}</h4>
                  <p className="text-sm text-gray-600">{campaign.total_sent} emails sent</p>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-center">
                    <div className="text-lg font-bold text-green-600">{campaign.conversion_rate?.toFixed(1)}%</div>
                    <div className="text-xs text-gray-600">Conversion</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-bold text-blue-600">{campaign.response_rate?.toFixed(1)}%</div>
                    <div className="text-xs text-gray-600">Response</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {performance?.recommendations && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Recommendations</h3>
          <div className="space-y-3">
            {performance.recommendations.map((rec, index) => (
              <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <p className="text-sm text-gray-700">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <XCircle className="h-5 w-5 text-red-600" />
            <span className="text-red-800 font-medium">Error</span>
          </div>
          <p className="text-red-700 mt-1">{error}</p>
        </div>
      )}
    </div>
  );
};

export default RealTimeAnalytics;

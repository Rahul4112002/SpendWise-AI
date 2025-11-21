import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../../hooks/useAuth';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [analytics, setAnalytics] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      
      // Fetch analytics summary
      const analyticsResponse = await axios.get('/api/v1/analytics/summary?days=30', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(analyticsResponse.data);

      // Fetch AI insights
      const insightsResponse = await axios.get('/api/v1/ai/insights?days=7', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setInsights(insightsResponse.data);

      setLoading(false);
    } catch (err) {
      setError('Failed to load dashboard data');
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="dashboard-loading">Loading your financial insights...</div>;
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.name || 'User'}!</h1>
        <p className="subtitle">Your Financial Overview - Last 30 Days</p>
      </div>

      {/* Financial Summary Cards */}
      <div className="summary-cards">
        <div className="summary-card income">
          <div className="card-icon">💰</div>
          <div className="card-content">
            <h3>Total Income</h3>
            <p className="amount">₹{analytics?.total_income?.toLocaleString() || '0'}</p>
          </div>
        </div>

        <div className="summary-card expenses">
          <div className="card-icon">💸</div>
          <div className="card-content">
            <h3>Total Expenses</h3>
            <p className="amount">₹{analytics?.total_expenses?.toLocaleString() || '0'}</p>
          </div>
        </div>

        <div className="summary-card savings">
          <div className="card-icon">🏦</div>
          <div className="card-content">
            <h3>Net Savings</h3>
            <p className="amount">₹{analytics?.net_savings?.toLocaleString() || '0'}</p>
            <span className="percentage">{analytics?.savings_rate?.toFixed(1)}% savings rate</span>
          </div>
        </div>

        <div className="summary-card transactions">
          <div className="card-icon">📊</div>
          <div className="card-content">
            <h3>Transactions</h3>
            <p className="amount">{analytics?.transaction_count || 0}</p>
            <span className="average">Avg: ₹{analytics?.average_transaction?.toFixed(0)}</span>
          </div>
        </div>
      </div>

      {/* Top Categories */}
      <div className="section">
        <h2>Top Spending Categories</h2>
        <div className="categories-list">
          {analytics?.top_categories?.map((cat, index) => (
            <div key={index} className="category-item">
              <div className="category-info">
                <h4>{cat.category}</h4>
                <p>{cat.transaction_count} transactions</p>
              </div>
              <div className="category-amount">
                <p className="amount">₹{cat.total.toLocaleString()}</p>
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{width: `${cat.percentage}%`}}
                  ></div>
                </div>
                <span className="percentage">{cat.percentage.toFixed(1)}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* AI Insights */}
      {insights.length > 0 && (
        <div className="section">
          <h2>🤖 AI Insights & Recommendations</h2>
          <div className="insights-list">
            {insights.slice(0, 3).map((insight) => (
              <div key={insight.id} className={`insight-card ${insight.priority}`}>
                <div className="insight-header">
                  <h4>{insight.title}</h4>
                  <span className={`badge ${insight.priority}`}>{insight.priority}</span>
                </div>
                <p>{insight.description}</p>
                <span className="insight-time">{new Date(insight.created_at).toLocaleDateString()}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Monthly Trends */}
      <div className="section">
        <h2>Monthly Trends</h2>
        <div className="trends-chart">
          {analytics?.monthly_trends?.map((month, index) => (
            <div key={index} className="trend-month">
              <h5>{month.month}</h5>
              <div className="trend-bars">
                <div className="bar income-bar" style={{height: `${(month.income / 100000) * 100}px`}}>
                  <span>₹{(month.income / 1000).toFixed(0)}k</span>
                </div>
                <div className="bar expense-bar" style={{height: `${(month.expenses / 100000) * 100}px`}}>
                  <span>₹{(month.expenses / 1000).toFixed(0)}k</span>
                </div>
              </div>
              <div className="trend-legend">
                <span className="legend-income">Income</span>
                <span className="legend-expense">Expenses</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <button className="action-btn" onClick={() => window.location.href = '/transactions/new'}>
          ➕ Add Transaction
        </button>
        <button className="action-btn" onClick={() => window.location.href = '/upload'}>
          📄 Upload Statement
        </button>
        <button className="action-btn" onClick={() => window.location.href = '/ai-chat'}>
          💬 Chat with AI
        </button>
        <button className="action-btn" onClick={() => window.location.href = '/budgets'}>
          📊 Manage Budgets
        </button>
      </div>
    </div>
  );
};

export default Dashboard;

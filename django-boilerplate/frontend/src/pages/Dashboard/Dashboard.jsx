/**
 * Dashboard Page - Main landing page with district selector and performance summary
 */

import React, { useState, useEffect } from 'react';
import { districtsAPI } from '../../services/api';
import { formatIndianNumber, formatCurrency, formatMonthYear, getStatusColor } from '../../utils/helpers';
import Card from '../../components/Card/Card';
import LoadingSpinner from '../../components/LoadingSpinner/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage/ErrorMessage';
import StatusBadge from '../../components/StatusBadge/StatusBadge';
import { FaUsers, FaRupeeSign, FaBriefcase, FaChartLine } from 'react-icons/fa';
import './Dashboard.css';

const Dashboard = () => {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedState, setSelectedState] = useState('');

  // Fetch all districts on mount
  useEffect(() => {
    fetchDistricts();
  }, []);

  // Fetch summary when district is selected
  useEffect(() => {
    if (selectedDistrict) {
      fetchSummary(selectedDistrict.id);
    }
  }, [selectedDistrict]);

  const fetchDistricts = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await districtsAPI.getAll();
      setDistricts(data.results || data);
      
      // Auto-select first district if available
      if (data.results && data.results.length > 0) {
        setSelectedDistrict(data.results[0]);
      } else if (data.length > 0) {
        setSelectedDistrict(data[0]);
      }
    } catch (err) {
      setError(err.message || 'Failed to load districts');
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async (districtId) => {
    try {
      setSummaryLoading(true);
      const data = await districtsAPI.getSummary(districtId);
      setSummary(data);
    } catch (err) {
      console.error('Failed to load summary:', err);
      setSummary(null);
    } finally {
      setSummaryLoading(false);
    }
  };

  const handleDistrictChange = (e) => {
    const districtId = parseInt(e.target.value);
    const district = districts.find(d => d.id === districtId);
    setSelectedDistrict(district);
  };

  // Get unique states for filter
  const states = [...new Set(districts.map(d => d.state))].sort();

  // Filter districts based on search and state
  const filteredDistricts = districts.filter(d => {
    const matchesSearch = d.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         d.code.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesState = !selectedState || d.state === selectedState;
    return matchesSearch && matchesState;
  });

  if (loading) {
    return <LoadingSpinner message="Loading districts..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchDistricts} />;
  }

  return (
    <div className="dashboard-page">
      <div className="container">
        <div className="dashboard-header">
          <h1>MGNREGA Performance Dashboard</h1>
          <p className="dashboard-description">
            Track and analyze MGNREGA implementation across Indian districts
          </p>
        </div>

        {/* District Selector */}
        <Card title="Select District" className="selector-card">
          <div className="selector-filters">
            <div className="filter-group">
              <label htmlFor="state-filter">Filter by State:</label>
              <select
                id="state-filter"
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="filter-select"
              >
                <option value="">All States</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="search-input">Search District:</label>
              <input
                id="search-input"
                type="text"
                placeholder="Search by name or code..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            <div className="filter-group">
              <label htmlFor="district-select">District:</label>
              <select
                id="district-select"
                value={selectedDistrict?.id || ''}
                onChange={handleDistrictChange}
                className="district-select"
              >
                {filteredDistricts.map(district => (
                  <option key={district.id} value={district.id}>
                    {district.name}, {district.state} ({district.code})
                  </option>
                ))}
              </select>
            </div>
          </div>
        </Card>

        {/* Performance Summary */}
        {selectedDistrict && (
          <>
            {summaryLoading ? (
              <LoadingSpinner message="Loading performance data..." />
            ) : summary ? (
              <div className="summary-section">
                <div className="summary-header">
                  <div>
                    <h2>{summary.district?.name || selectedDistrict.name}</h2>
                    <p className="summary-subtitle">
                      {summary.district?.state || selectedDistrict.state} • {' '}
                      {summary.period?.display || formatMonthYear(summary.period?.year, summary.period?.month)}
                    </p>
                  </div>
                </div>

                <div className="metrics-grid">
                  <MetricCard
                    icon={<FaUsers />}
                    title="Person Days"
                    value={formatIndianNumber(summary.metrics?.personDays)}
                    status={summary.status?.personDays}
                    change={summary.comparisonToPreviousMonth?.personDays}
                  />
                  <MetricCard
                    icon={<FaBriefcase />}
                    title="Households Worked"
                    value={formatIndianNumber(summary.metrics?.householdsWorked)}
                    status={summary.status?.householdsWorked}
                    change={summary.comparisonToPreviousMonth?.householdsWorked}
                  />
                  <MetricCard
                    icon={<FaRupeeSign />}
                    title="Total Wages"
                    value={formatCurrency(summary.metrics?.totalWages)}
                    status={summary.status?.totalWages}
                    change={summary.comparisonToPreviousMonth?.totalWages}
                  />
                  <MetricCard
                    icon={<FaChartLine />}
                    title="Material Expenditure"
                    value={formatCurrency(summary.metrics?.materialExpenditure)}
                    status={summary.status?.materialExpenditure}
                    change={summary.comparisonToPreviousMonth?.materialExpenditure}
                  />
                </div>

                <div className="performance-note">
                  <div>
                    <strong>Performance Indicators:</strong> 
                    <StatusBadge status="good" /> Good (≥80% of state avg) • 
                    <StatusBadge status="average" /> Average (50-79%) • 
                    <StatusBadge status="poor" /> Poor (&lt;50%)
                  </div>
                </div>
              </div>
            ) : (
              <Card>
                <p className="no-data">No performance data available for this district.</p>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
};

// MetricCard Component
const MetricCard = ({ icon, title, value, status, change }) => {
  const changeValue = change ? parseFloat(change) : null;
  const isPositive = changeValue && changeValue > 0;
  const isNegative = changeValue && changeValue < 0;

  return (
    <Card className="metric-card">
      <div className="metric-icon" style={{ color: getStatusColor(status) }}>
        {icon}
      </div>
      <div className="metric-content">
        <h4 className="metric-title">{title}</h4>
        <p className="metric-value">{value}</p>
        <div className="metric-footer">
          <StatusBadge status={status} size="small" />
          {changeValue !== null && (
            <span className={`metric-change ${isPositive ? 'positive' : isNegative ? 'negative' : ''}`}>
              {isPositive && '+'}{changeValue.toFixed(1)}% vs last month
            </span>
          )}
        </div>
      </div>
    </Card>
  );
};

export default Dashboard;

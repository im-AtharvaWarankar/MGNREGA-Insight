/**
 * Historical Trends Page
 * Display performance trends over time with line charts
 */

import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { districtsAPI } from '../../services/api';
import { formatMonthYear, formatIndianNumber } from '../../utils/helpers';
import Card from '../../components/Card/Card';
import LoadingSpinner from '../../components/LoadingSpinner/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage/ErrorMessage';
import './Historical.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Historical = () => {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [dataLoading, setDataLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('personDays');
  const [period, setPeriod] = useState(12);

  const metrics = [
    { value: 'personDays', label: 'Person Days', color: '#2563eb' },
    { value: 'householdsWorked', label: 'Households Worked', color: '#10b981' },
    { value: 'totalWages', label: 'Total Wages (₹)', color: '#f59e0b' },
    { value: 'materialExpenditure', label: 'Material Expenditure (₹)', color: '#ef4444' }
  ];

  useEffect(() => {
    fetchDistricts();
  }, []);

  useEffect(() => {
    if (selectedDistrict) {
      fetchHistoricalData(selectedDistrict.id, period);
    }
  }, [selectedDistrict, period]);

  const fetchDistricts = async () => {
    try {
      setLoading(true);
      const data = await districtsAPI.getAll();
      setDistricts(data.results || data);
      if (data.results && data.results.length > 0) {
        setSelectedDistrict(data.results[0]);
      } else if (data.length > 0) {
        setSelectedDistrict(data[0]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistoricalData = async (districtId, months) => {
    try {
      setDataLoading(true);
      const data = await districtsAPI.getHistory(districtId, { period: months });
      setHistoricalData(data);
    } catch (err) {
      console.error('Failed to load historical data:', err);
      setHistoricalData(null);
    } finally {
      setDataLoading(false);
    }
  };

  const handleDistrictChange = (e) => {
    const districtId = parseInt(e.target.value);
    const district = districts.find(d => d.id === districtId);
    setSelectedDistrict(district);
  };

  // Prepare chart data
  const getChartData = () => {
    if (!historicalData || !historicalData.data) {
      return null;
    }

    const currentMetric = metrics.find(m => m.value === selectedMetric);
    
    return {
      labels: historicalData.data.map(item => 
        formatMonthYear(item.year, item.month)
      ),
      datasets: [
        {
          label: currentMetric.label,
          data: historicalData.data.map(item => item[selectedMetric] || 0),
          borderColor: currentMetric.color,
          backgroundColor: `${currentMetric.color}20`,
          fill: true,
          tension: 0.4
        }
      ]
    };
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const value = context.parsed.y;
            if (selectedMetric.includes('Wages') || selectedMetric.includes('Expenditure')) {
              return `₹${formatIndianNumber(value)}`;
            }
            return formatIndianNumber(value);
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => formatIndianNumber(value)
        }
      }
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading districts..." />;
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchDistricts} />;
  }

  const chartData = getChartData();

  return (
    <div className="historical-page">
      <div className="container">
        <div className="historical-header">
          <h1>Performance Trends</h1>
          <p className="historical-description">
            Track performance metrics over time for selected district
          </p>
        </div>

        <Card title="Select District and Metrics">
          <div className="historical-filters">
            <div className="filter-group">
              <label htmlFor="district-select">District:</label>
              <select
                id="district-select"
                value={selectedDistrict?.id || ''}
                onChange={handleDistrictChange}
                className="filter-select"
              >
                {districts.map(district => (
                  <option key={district.id} value={district.id}>
                    {district.name}, {district.state}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="metric-select">Metric:</label>
              <select
                id="metric-select"
                value={selectedMetric}
                onChange={(e) => setSelectedMetric(e.target.value)}
                className="filter-select"
              >
                {metrics.map(metric => (
                  <option key={metric.value} value={metric.value}>
                    {metric.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="period-select">Time Period:</label>
              <select
                id="period-select"
                value={period}
                onChange={(e) => setPeriod(parseInt(e.target.value))}
                className="filter-select"
              >
                <option value={6}>Last 6 Months</option>
                <option value={12}>Last 12 Months</option>
                <option value={24}>Last 24 Months</option>
                <option value={36}>Last 36 Months</option>
              </select>
            </div>
          </div>
        </Card>

        {dataLoading ? (
          <LoadingSpinner message="Loading trend data..." />
        ) : chartData ? (
          <Card title={`${metrics.find(m => m.value === selectedMetric).label} Trend`} className="chart-card">
            <div className="chart-container">
              <Line data={chartData} options={chartOptions} />
            </div>
          </Card>
        ) : (
          <Card>
            <p className="no-data">No historical data available for this district.</p>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Historical;

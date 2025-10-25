/**
 * Comparison Page
 * Compare performance across multiple districts
 */

import React, { useState, useEffect } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { districtsAPI, comparisonAPI } from '../../services/api';
import { formatIndianNumber, formatMonthYear } from '../../utils/helpers';
import Card from '../../components/Card/Card';
import LoadingSpinner from '../../components/LoadingSpinner/LoadingSpinner';
import ErrorMessage from '../../components/ErrorMessage/ErrorMessage';
import './Comparison.css';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const Comparison = () => {
  const [districts, setDistricts] = useState([]);
  const [selectedDistricts, setSelectedDistricts] = useState([]);
  const [comparisonData, setComparisonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [compareLoading, setCompareLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedMetric, setSelectedMetric] = useState('personDays');
  
  // Set default to current month/year
  const now = new Date();
  const [selectedYear, setSelectedYear] = useState(now.getFullYear());
  const [selectedMonth, setSelectedMonth] = useState(now.getMonth() + 1);

  const metrics = [
    { value: 'personDays', label: 'Person Days', color: '#2563eb' },
    { value: 'householdsWorked', label: 'Households Worked', color: '#10b981' },
    { value: 'totalWages', label: 'Total Wages', color: '#f59e0b' },
    { value: 'materialExpenditure', label: 'Material Expenditure', color: '#ef4444' }
  ];

  useEffect(() => {
    fetchDistricts();
  }, []);

  const fetchDistricts = async () => {
    try {
      setLoading(true);
      const data = await districtsAPI.getAll();
      setDistricts(data.results || data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDistrictToggle = (districtId) => {
    setSelectedDistricts(prev => {
      if (prev.includes(districtId)) {
        return prev.filter(id => id !== districtId);
      } else if (prev.length < 5) {
        return [...prev, districtId];
      }
      return prev;
    });
  };

  const handleCompare = async () => {
    if (selectedDistricts.length < 2) {
      alert('Please select at least 2 districts to compare');
      return;
    }

    try {
      setCompareLoading(true);
      const data = await comparisonAPI.compare({
        districtIds: selectedDistricts,
        year: selectedYear,
        month: selectedMonth
      });
      setComparisonData(data);
    } catch (err) {
      alert('Failed to compare districts: ' + err.message);
    } finally {
      setCompareLoading(false);
    }
  };

  // Prepare chart data
  const getChartData = () => {
    if (!comparisonData || !comparisonData.districts) {
      return null;
    }

    const currentMetric = metrics.find(m => m.value === selectedMetric);
    
    return {
      labels: comparisonData.districts.map(d => d.name),
      datasets: [
        {
          label: currentMetric.label,
          data: comparisonData.districts.map(d => d.value || 0),
          backgroundColor: currentMetric.color,
          borderColor: currentMetric.color,
          borderWidth: 1
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
    <div className="comparison-page">
      <div className="container">
        <div className="comparison-header">
          <h1>District Comparison</h1>
          <p className="comparison-description">
            Compare performance metrics across multiple districts (select 2-5 districts)
          </p>
        </div>

        <Card title="Select Districts to Compare">
          <div className="district-selection">
            <p className="selection-count">
              Selected: {selectedDistricts.length} / 5
            </p>
            
            {/* Month/Year Selection */}
            <div className="period-selection">
              <label>
                Month:
                <select 
                  value={selectedMonth} 
                  onChange={(e) => setSelectedMonth(Number(e.target.value))}
                  className="month-select"
                >
                  {[...Array(12)].map((_, i) => (
                    <option key={i + 1} value={i + 1}>
                      {new Date(2000, i, 1).toLocaleString('default', { month: 'long' })}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                Year:
                <select 
                  value={selectedYear} 
                  onChange={(e) => setSelectedYear(Number(e.target.value))}
                  className="year-select"
                >
                  {[2025, 2024, 2023, 2022].map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </label>
            </div>
            
            <div className="district-checkboxes">
              {districts.map(district => (
                <label key={district.id} className="district-checkbox">
                  <input
                    type="checkbox"
                    checked={selectedDistricts.includes(district.id)}
                    onChange={() => handleDistrictToggle(district.id)}
                    disabled={
                      !selectedDistricts.includes(district.id) && 
                      selectedDistricts.length >= 5
                    }
                  />
                  <span>{district.name}, {district.state}</span>
                </label>
              ))}
            </div>
            <button
              className="compare-button"
              onClick={handleCompare}
              disabled={selectedDistricts.length < 2 || compareLoading}
            >
              {compareLoading ? 'Comparing...' : 'Compare Districts'}
            </button>
          </div>
        </Card>

        {comparisonData && (
          <>
            <Card title="Comparison Details" className="mt-lg">
              <p className="comparison-period">
                Period: {comparisonData.period?.display || 'Latest available data'}
              </p>
            </Card>

            <Card title="Select Metric">
              <div className="metric-selector">
                {metrics.map(metric => (
                  <button
                    key={metric.value}
                    className={`metric-button ${selectedMetric === metric.value ? 'active' : ''}`}
                    onClick={() => setSelectedMetric(metric.value)}
                    style={{
                      borderColor: selectedMetric === metric.value ? metric.color : 'transparent',
                      color: selectedMetric === metric.value ? metric.color : 'inherit'
                    }}
                  >
                    {metric.label}
                  </button>
                ))}
              </div>
            </Card>

            {chartData && (
              <Card title={`${metrics.find(m => m.value === selectedMetric).label} Comparison`} className="chart-card">
                <div className="chart-container">
                  <Bar data={chartData} options={chartOptions} />
                </div>
              </Card>
            )}

            <Card title="Detailed Comparison" className="table-card">
              <div className="comparison-table-wrapper">
                <table className="comparison-table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>District</th>
                      <th>State</th>
                      <th>{metrics.find(m => m.value === selectedMetric)?.label}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonData.districts.map(district => (
                      <tr key={district.id}>
                        <td>#{district.rank}</td>
                        <td>{district.name}</td>
                        <td>{district.state}</td>
                        <td>
                          {selectedMetric.includes('Wages') || selectedMetric.includes('Expenditure')
                            ? `₹${formatIndianNumber(district.value)}`
                            : formatIndianNumber(district.value)
                          }
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default Comparison;

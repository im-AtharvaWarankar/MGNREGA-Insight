/**
 * Utility Functions - CivicView MGNREGA Dashboard
 */

/**
 * Format large numbers with Indian numbering system (Lakh, Crore)
 * Example: 1234567 => "12.35 Lakh"
 */
export const formatIndianNumber = (num) => {
  if (num === null || num === undefined) return 'N/A';
  
  const absNum = Math.abs(num);
  
  if (absNum >= 10000000) {
    // Crore
    return `${(num / 10000000).toFixed(2)} Cr`;
  } else if (absNum >= 100000) {
    // Lakh
    return `${(num / 100000).toFixed(2)} Lakh`;
  } else if (absNum >= 1000) {
    // Thousand
    return `${(num / 1000).toFixed(2)}K`;
  }
  
  return num.toLocaleString('en-IN');
};

/**
 * Format currency in Indian Rupees
 * Example: 1234567 => "₹12.35 Lakh"
 */
export const formatCurrency = (amount) => {
  if (amount === null || amount === undefined) return 'N/A';
  return `₹${formatIndianNumber(amount)}`;
};

/**
 * Format percentage with 2 decimal places
 */
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined) return 'N/A';
  return `${value.toFixed(decimals)}%`;
};

/**
 * Format date to readable string
 * Example: "2024-10-25" => "25 Oct 2024"
 */
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  
  const date = new Date(dateString);
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return date.toLocaleDateString('en-IN', options);
};

/**
 * Format month-year for display
 * Example: (2024, 10) => "October 2024"
 */
export const formatMonthYear = (year, month) => {
  if (!year || !month) return 'N/A';
  
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  
  return `${months[month - 1]} ${year}`;
};

/**
 * Get status color based on performance indicator
 * Matches backend logic: good >= 80%, average 50-79%, poor < 50%
 */
export const getStatusColor = (status) => {
  const colors = {
    good: '#10b981',    // Green
    average: '#f59e0b', // Amber
    poor: '#ef4444',    // Red
    neutral: '#6b7280'  // Gray
  };
  
  return colors[status] || colors.neutral;
};

/**
 * Get status label
 */
export const getStatusLabel = (status) => {
  const labels = {
    good: 'Good',
    average: 'Average',
    poor: 'Poor',
    neutral: 'N/A'
  };
  
  return labels[status] || 'N/A';
};

/**
 * Calculate percentage change between two values
 */
export const calculatePercentageChange = (current, previous) => {
  if (!previous || previous === 0) return null;
  return ((current - previous) / previous) * 100;
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text, maxLength = 50) => {
  if (!text || text.length <= maxLength) return text;
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Debounce function for search inputs
 */
export const debounce = (func, wait = 300) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

/**
 * Group array by key
 */
export const groupBy = (array, key) => {
  return array.reduce((result, item) => {
    const group = item[key];
    if (!result[group]) {
      result[group] = [];
    }
    result[group].push(item);
    return result;
  }, {});
};

/**
 * Sort array by key
 */
export const sortBy = (array, key, order = 'asc') => {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return order === 'asc' ? -1 : 1;
    if (aVal > bVal) return order === 'asc' ? 1 : -1;
    return 0;
  });
};

/**
 * Get unique values from array
 */
export const getUniqueValues = (array, key) => {
  return [...new Set(array.map(item => item[key]))];
};

/**
 * Download data as JSON file
 */
export const downloadJSON = (data, filename = 'data.json') => {
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: 'application/json'
  });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

/**
 * Download data as CSV file
 */
export const downloadCSV = (data, filename = 'data.csv') => {
  if (!data || data.length === 0) return;
  
  const headers = Object.keys(data[0]);
  const csvContent = [
    headers.join(','),
    ...data.map(row => 
      headers.map(header => {
        const value = row[header];
        return typeof value === 'string' && value.includes(',') 
          ? `"${value}"` 
          : value;
      }).join(',')
    )
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

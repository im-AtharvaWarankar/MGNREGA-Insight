/**
 * API Service - CivicView MGNREGA Dashboard
 * 
 * Axios-based API client matching Django backend endpoints:
 * - GET /api/health/ - Health check
 * - GET /api/districts/ - List all districts
 * - GET /api/districts/:id/ - District detail
 * - GET /api/districts/:id/summary/ - Performance summary
 * - GET /api/districts/:id/history/ - Historical performance
 * - POST /api/compare/ - Compare districts
 */

import axios from 'axios';

// Create axios instance with default config
// Use Vite environment variable if provided, otherwise default to local backend
// This avoids accidental https/proxy issues in some dev environments.
const API_BASE = import.meta?.env?.VITE_API_BASE || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed in future
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Backend wraps responses in { data: {...}, error: {}, isSuccess: true }
    // Extract the actual data from the wrapper
    if (response.data && response.data.data !== undefined) {
      return response.data.data;
    }
    return response.data;
  },
  (error) => {
    // Handle errors globally
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.detail ||
                        error.message || 
                        'An error occurred';
    
    console.error('API Error:', errorMessage);
    return Promise.reject({
      message: errorMessage,
      status: error.response?.status,
      data: error.response?.data
    });
  }
);

/**
 * Health Check API
 */
export const healthAPI = {
  /**
   * Check system health
   * GET /api/health/
   */
  check: () => api.get('/health/')
};

/**
 * Districts API
 */
export const districtsAPI = {
  /**
   * Get all districts with optional filters
   * GET /api/districts/?state=Karnataka&search=Bangalore
   */
  getAll: (params = {}) => api.get('/districts/', { params }),
  
  /**
   * Get district by ID
   * GET /api/districts/:id/
   */
  getById: (id) => api.get(`/districts/${id}/`),
  
  /**
   * Get district performance summary
   * GET /api/districts/:id/summary/?year=2024&month=10
   */
  getSummary: (id, params = {}) => api.get(`/districts/${id}/summary/`, { params }),
  
  /**
   * Get historical performance data
   * GET /api/districts/:id/history/?from=YYYY-MM&to=YYYY-MM
   */
  getHistory: (id, params = {}) => {
    // Convert period (number of months) to from/to dates
    if (params.period) {
      const now = new Date();
      const toYear = now.getFullYear();
      const toMonth = now.getMonth() + 1; // JS months are 0-indexed
      
      // Calculate 'from' date by going back 'period' months
      const fromDate = new Date(now);
      fromDate.setMonth(fromDate.getMonth() - params.period + 1);
      const fromYear = fromDate.getFullYear();
      const fromMonth = fromDate.getMonth() + 1;
      
      const newParams = {
        from: `${fromYear}-${String(fromMonth).padStart(2, '0')}`,
        to: `${toYear}-${String(toMonth).padStart(2, '0')}`
      };
      
      return api.get(`/districts/${id}/history/`, { params: newParams });
    }
    
    return api.get(`/districts/${id}/history/`, { params });
  }
};

/**
 * Comparison API
 */
export const comparisonAPI = {
  /**
   * Compare multiple districts
   * GET /api/compare/?districts=1,2,3&metric=person_days&period=YYYY-MM
   */
  compare: ({ districtIds, metric = 'personDays', year, month }) => {
    // Convert camelCase to snake_case for backend
    const metricMap = {
      'personDays': 'person_days',
      'householdsWorked': 'households_worked',
      'totalWages': 'total_wages',
      'materialExpenditure': 'material_expenditure'
    };
    
    const period = `${year}-${String(month).padStart(2, '0')}`;
    const districts = districtIds.join(',');
    const backendMetric = metricMap[metric] || 'person_days';
    
    return api.get(`/compare/?districts=${districts}&metric=${backendMetric}&period=${period}`);
  }
};

/**
 * Utility functions
 */

/**
 * Format error message for display
 */
export const formatErrorMessage = (error) => {
  if (typeof error === 'string') return error;
  if (error?.message) return error.message;
  return 'An unexpected error occurred';
};

/**
 * Check if response indicates success
 */
export const isSuccessResponse = (response) => {
  return response && (
    response.status === 'ok' || 
    response.status === 200 ||
    Array.isArray(response) ||
    typeof response === 'object'
  );
};

export default api;

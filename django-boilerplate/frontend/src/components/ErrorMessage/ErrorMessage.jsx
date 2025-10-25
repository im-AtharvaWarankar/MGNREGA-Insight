/**
 * ErrorMessage Component
 * Display error messages to users
 */

import React from 'react';
import { FaExclamationTriangle } from 'react-icons/fa';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onRetry }) => {
  return (
    <div className="error-message">
      <div className="error-icon">
        <FaExclamationTriangle />
      </div>
      <p className="error-text">{message || 'An error occurred'}</p>
      {onRetry && (
        <button className="error-retry-button" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  );
};

export default ErrorMessage;

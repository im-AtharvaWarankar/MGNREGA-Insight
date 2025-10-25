/**
 * StatusBadge Component
 * Display color-coded status indicators matching backend logic
 */

import React from 'react';
import { getStatusColor, getStatusLabel } from '../../utils/helpers';
import './StatusBadge.css';

const StatusBadge = ({ status, showLabel = true, size = 'medium' }) => {
  const color = getStatusColor(status);
  const label = getStatusLabel(status);
  
  return (
    <div className={`status-badge status-badge-${size}`}>
      <span
        className="status-indicator"
        style={{ backgroundColor: color }}
      />
      {showLabel && <span className="status-label">{label}</span>}
    </div>
  );
};

export default StatusBadge;

/**
 * Card Component
 * Reusable card container
 */

import React from 'react';
import './Card.css';

const Card = ({ children, title, subtitle, className = '', noPadding = false }) => {
  return (
    <div className={`card ${className}`}>
      {(title || subtitle) && (
        <div className="card-header">
          {title && <h3 className="card-title">{title}</h3>}
          {subtitle && <p className="card-subtitle">{subtitle}</p>}
        </div>
      )}
      <div className={`card-content ${noPadding ? 'no-padding' : ''}`}>
        {children}
      </div>
    </div>
  );
};

export default Card;

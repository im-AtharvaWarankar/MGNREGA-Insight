/**
 * Footer Component
 */

import React from 'react';
import './Footer.css';

const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <p className="footer-text">
            © {currentYear} CivicView. Data sourced from{' '}
            <a
              href="https://data.gov.in"
              target="_blank"
              rel="noopener noreferrer"
              className="footer-link"
            >
              data.gov.in
            </a>
            {' '}and official MGNREGA records.
          </p>
          <p className="footer-disclaimer">
            This is a public transparency initiative. For official information, visit{' '}
            <a
              href="https://nrega.nic.in"
              target="_blank"
              rel="noopener noreferrer"
              className="footer-link"
            >
              nrega.nic.in
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

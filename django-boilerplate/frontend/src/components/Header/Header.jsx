/**
 * Header Component - CivicView Navigation
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaChartLine, FaHistory, FaBalanceScale } from 'react-icons/fa';
import './Header.css';

const Header = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: <FaChartLine /> },
    { path: '/historical', label: 'Trends', icon: <FaHistory /> },
    { path: '/compare', label: 'Compare', icon: <FaBalanceScale /> }
  ];
  
  const isActive = (path) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };
  
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="header-brand">
            <Link to="/" className="brand-link">
              <h1 className="brand-title">CivicView</h1>
              <p className="brand-subtitle">MGNREGA Performance Dashboard</p>
            </Link>
          </div>
          
          <nav className="header-nav">
            <ul className="nav-list">
              {navItems.map((item) => (
                <li key={item.path} className="nav-item">
                  <Link
                    to={item.path}
                    className={`nav-link ${isActive(item.path) ? 'active' : ''}`}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    <span className="nav-label">{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;

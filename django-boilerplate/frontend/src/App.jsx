/**
 * Main App Component - CivicView MGNREGA Dashboard
 */

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import Dashboard from './pages/Dashboard/Dashboard';
import Historical from './pages/Historical/Historical';
import Comparison from './pages/Comparison/Comparison';
import './App.css';

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/historical" element={<Historical />} />
          <Route path="/compare" element={<Comparison />} />
        </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;

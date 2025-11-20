import React, { useState } from 'react';
import './App.css';
import { API_BASE_URL } from './config';

function SimpleApp() {
  const [numStocks, setNumStocks] = useState(5);
  const [targetBeta, setTargetBeta] = useState(1.0);
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const optimizePortfolio = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/optimize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          num_stocks: parseInt(numStocks),
          target_beta: parseFloat(targetBeta)
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPortfolioData(data);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to optimize portfolio');
      }
    } catch (err) {
      setError('Cannot connect to backend. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>Simple Portfolio Optimizer</h1>
        <p>No external APIs required - uses sample data for demonstration</p>
        
        <div className="input-section">
          <div className="input-group">
            <label>Number of Stocks:</label>
            <input
              type="number"
              value={numStocks}
              onChange={(e) => setNumStocks(e.target.value)}
              min="1"
              max="10"
            />
          </div>

          <div className="input-group">
            <label>Target Beta:</label>
            <input
              type="number"
              step="0.1"
              value={targetBeta}
              onChange={(e) => setTargetBeta(e.target.value)}
              min="0.1"
              max="3.0"
            />
          </div>

          <button 
            onClick={optimizePortfolio} 
            disabled={loading}
            className="optimize-btn"
          >
            {loading ? 'Optimizing...' : 'Optimize Portfolio'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            <h3>Error:</h3>
            <p>{error}</p>
          </div>
        )}

        {portfolioData && (
          <div className="results">
            <h2>Portfolio Results</h2>
            <div className="metrics">
              <div className="metric">
                <label>Expected Return:</label>
                <span>{(portfolioData.expected_return * 100).toFixed(2)}%</span>
              </div>
              <div className="metric">
                <label>Volatility:</label>
                <span>{(portfolioData.volatility * 100).toFixed(2)}%</span>
              </div>
              <div className="metric">
                <label>Sharpe Ratio:</label>
                <span>{portfolioData.sharpe_ratio.toFixed(3)}</span>
              </div>
              <div className="metric">
                <label>Portfolio Beta:</label>
                <span>{portfolioData.actual_beta.toFixed(2)}</span>
              </div>
            </div>

            <h3>Stock Weights:</h3>
            <div className="weights">
              {Object.entries(portfolioData.weights).map(([symbol, weight]) => (
                <div key={symbol} className="weight-item">
                  <span className="symbol">{symbol}</span>
                  <span className="weight">{(weight * 100).toFixed(1)}%</span>
                </div>
              ))}
            </div>

            <p className="message">{portfolioData.message}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default SimpleApp;

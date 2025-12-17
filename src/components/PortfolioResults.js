import React from 'react';

function PortfolioResults({ data }) {
  if (!data) return null;

  return (
    <div className="portfolio-results">
      <h3>Optimization Results</h3>
      
      <div className="results-grid">
        <div className="result-card">
          <h4>Portfolio Weights & Returns</h4>
          <div className="weights-list">
            {data.weights && Object.entries(data.weights)
              .filter(([, weight]) => weight > 0.001) // Only show stocks with weight > 0%
              .sort(([,a], [,b]) => b - a) // Sort by weight descending
              .map(([stock, weight]) => {
                const stockInfo = data.stocks?.find(s => s.symbol === stock);
                const individualReturn = data.individual_returns?.[stock];
                return (
                  <div key={stock} className="weight-item">
                    <div className="stock-info">
                      <span className="stock-symbol">{stock}</span>
                      {stockInfo && (
                        <span className="stock-name">{stockInfo.name}</span>
                      )}
                    </div>
                    <div className="stock-metrics">
                      <div className="weight-metric">
                        <span className="metric-label">Weight:</span>
                        <span className="weight-value">{(weight * 100).toFixed(1)}%</span>
                      </div>
                      {individualReturn && (
                        <div className="return-metric">
                          <span className="metric-label">Expected Return:</span>
                          <span className="return-value">{(individualReturn * 100).toFixed(1)}%</span>
                        </div>
                      )}
                      {stockInfo && (
                        <div className="beta-metric">
                          <span className="metric-label">Beta:</span>
                          <span className="beta-value">{stockInfo.beta}</span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
          </div>
        </div>

        <div className="result-card">
          <h4>Portfolio Metrics</h4>
          <div className="metrics-list">
            <div className="metric-item">
              <span className="metric-label">Expected Return:</span>
              <span className="metric-value">{(data.expected_return * 100).toFixed(2)}%</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Volatility:</span>
              <span className="metric-value">{(data.volatility * 100).toFixed(2)}%</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Sharpe Ratio:</span>
              <span className="metric-value">{data.sharpe_ratio?.toFixed(3) || 'N/A'}</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Target Beta:</span>
              <span className="metric-value">{data.target_beta?.toFixed(3) || 'N/A'}</span>
            </div>
            {data.target_performance && (
              <div className="metric-item">
                <span className="metric-label">Target Performance:</span>
                <span className="metric-value">{(data.target_performance * 100).toFixed(2)}%</span>
              </div>
            )}
            {data.performance_criteria && (
              <div className="metric-item">
                <span className="metric-label">Performance Criteria:</span>
                <span className="metric-value">{data.performance_criteria}</span>
              </div>
            )}
            {data.performance_achievable !== undefined && (
              <div className="metric-item">
                <span className="metric-label">Performance Achievable:</span>
                <span className="metric-value" style={{ color: data.performance_achievable ? '#27ae60' : '#e74c3c' }}>
                  {data.performance_achievable ? 'Yes' : 'No'}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {data.message && (
        <div className={`optimization-message ${data.performance_achievable === false ? 'performance-warning' : ''}`}>
          <p>{data.message}</p>
        </div>
      )}
    </div>
  );
}

export default PortfolioResults;

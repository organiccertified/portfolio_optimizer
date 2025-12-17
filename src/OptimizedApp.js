import React, { useState, useEffect, useCallback, useMemo } from 'react';
import './App.css';
import { API_BASE_URL } from './config';

function OptimizedApp() {
  // State management
  const [numStocks, setNumStocks] = useState(10);
  const [targetBeta, setTargetBeta] = useState(1.0);
  const [targetReturn, setTargetReturn] = useState('');
  const [strategy, setStrategy] = useState('diversified');
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [stocks, setStocks] = useState([]);
  const [sectors, setSectors] = useState([]);
  const [stats, setStats] = useState(null);

  // Memoized validation
  const validation = useMemo(() => {
    const errors = [];
    // For target_return strategy, numStocks validation is not required
    if (strategy !== 'target_return') {
      if (numStocks < 1 || numStocks > 50) {
        errors.push('Number of stocks must be between 1 and 50');
      }
    }
    if (targetBeta < 0.1 || targetBeta > 3.0) {
      errors.push('Target beta must be between 0.1 and 3.0');
    }
    if (targetReturn && (isNaN(parseFloat(targetReturn)) || parseFloat(targetReturn) < 1 || parseFloat(targetReturn) > 50)) {
      errors.push('Target return must be between 1% and 50%');
    }
    // Target return is required for target_return strategy
    if (strategy === 'target_return' && !targetReturn) {
      errors.push('Target Return strategy requires a target return to be specified');
    }
    return {
      isValid: errors.length === 0,
      errors
    };
  }, [numStocks, targetBeta, targetReturn, strategy]);

  // Load initial data
  useEffect(() => {
    loadStocks();
    loadStats();
  }, []);

  const loadStocks = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stocks`);
      if (response.ok) {
        const data = await response.json();
        setStocks(data.stocks);
        setSectors(data.sectors);
      }
    } catch (err) {
      console.error('Failed to load stocks:', err);
    }
  }, []);

  const loadStats = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stats`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  }, []);

  const optimizePortfolio = useCallback(async () => {
    if (!validation.isValid) {
      setError(validation.errors.join(', '));
      return;
    }

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
          target_beta: parseFloat(targetBeta),
          target_return: targetReturn ? parseFloat(targetReturn) : null,
          strategy: strategy
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPortfolioData(data);
        loadStats(); // Refresh stats
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to optimize portfolio');
      }
    } catch (err) {
      setError('Cannot connect to backend. Please check your connection.');
    } finally {
      setLoading(false);
    }
  }, [numStocks, targetBeta, strategy, validation, loadStats]);

  const clearCache = useCallback(async () => {
    try {
      await fetch(`${API_BASE_URL}/api/clear-cache`, { method: 'POST' });
      loadStats();
    } catch (err) {
      console.error('Failed to clear cache:', err);
    }
  }, [loadStats]);

  const resetForm = useCallback(() => {
    setNumStocks(10);
    setTargetBeta(1.0);
    setTargetReturn('');
    setStrategy('diversified');
    setPortfolioData(null);
    setError('');
  }, []);

  // Memoized portfolio summary
  const portfolioSummary = useMemo(() => {
    if (!portfolioData) return null;
    
    const totalWeight = Object.values(portfolioData.weights).reduce((sum, weight) => sum + weight, 0);
    const isBalanced = Math.abs(totalWeight - 1.0) < 0.01;
    
    return {
      totalWeight: totalWeight.toFixed(3),
      isBalanced,
      stockCount: Object.keys(portfolioData.weights).length,
      topStock: Object.entries(portfolioData.weights)
        .sort(([,a], [,b]) => b - a)[0]
    };
  }, [portfolioData]);

  return (
    <div className="App">
      <div className="container">
        <header className="app-header">
          <h1>Portfolio Optimizer</h1>
          <p>Advanced portfolio optimization with intelligent stock selection</p>
          {stats && (
            <div className="stats-bar">
              <span>📊 {stats.total_stocks} stocks available</span>
              <span>💾 Cache: {stats.cache_size} entries</span>
              <button onClick={clearCache} className="clear-cache-btn">Clear Cache</button>
            </div>
          )}
        </header>
        
        <div className="input-section">
          <div className="input-grid">
            <div className="input-group">
              <label htmlFor="numStocks">Number of Stocks</label>
              <input
                id="numStocks"
                type="number"
                value={numStocks}
                onChange={(e) => setNumStocks(parseInt(e.target.value) || 0)}
                min="1"
                max="50"
                disabled={strategy === 'target_return'}
                className={validation.isValid ? '' : 'error'}
                style={strategy === 'target_return' ? {opacity: 0.6, cursor: 'not-allowed'} : {}}
              />
              <small>
                {strategy === 'target_return' 
                  ? 'Ignored for Target Return strategy'
                  : 'Choose 1-50 stocks for your portfolio'}
              </small>
            </div>

            <div className="input-group">
              <label htmlFor="targetBeta">Target Beta</label>
              <input
                id="targetBeta"
                type="number"
                step="0.1"
                value={targetBeta}
                onChange={(e) => setTargetBeta(parseFloat(e.target.value) || 0)}
                min="0.1"
                max="3.0"
                className={validation.isValid ? '' : 'error'}
              />
              <small>Risk level: 0.1 (conservative) to 3.0 (aggressive)</small>
            </div>

            <div className="input-group">
              <label htmlFor="targetReturn">Target Return (Optional)</label>
              <input
                id="targetReturn"
                type="number"
                step="0.1"
                value={targetReturn}
                onChange={(e) => setTargetReturn(e.target.value)}
                min="1"
                max="50"
                placeholder="e.g., 12"
                className={validation.isValid ? '' : 'error'}
              />
              <small>Expected annual return: 1% to 50% (leave empty for auto-optimization)</small>
            </div>

            <div className="input-group">
              <label htmlFor="strategy">Selection Strategy</label>
              <select
                id="strategy"
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}
              >
                <option value="diversified">Diversified (Recommended)</option>
                <option value="random">Random Selection</option>
                <option value="top">Top Stocks</option>
                <option value="target_return">Target Return (Ignores stock count)</option>
              </select>
              <small>
                {strategy === 'target_return' 
                  ? 'Finds optimal mix to achieve target return (ignores number of stocks)'
                  : 'How to select stocks for optimization'}
              </small>
            </div>
          </div>

          {!validation.isValid && (
            <div className="validation-errors">
              {validation.errors.map((error, index) => (
                <div key={index} className="error-message">⚠️ {error}</div>
              ))}
            </div>
          )}

          <div className="action-buttons">
            <button 
              onClick={optimizePortfolio} 
              disabled={loading || !validation.isValid}
              className="optimize-btn"
            >
              {loading ? '🔄 Optimizing...' : '⚡ Optimize Portfolio'}
            </button>
            <button 
              onClick={resetForm}
              className="reset-btn"
            >
              🔄 Reset
            </button>
          </div>
        </div>

        {error && (
          <div className="error-section">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {portfolioData && (
          <div className="results">
            <div className="results-header">
              <h2>📈 Portfolio Results</h2>
              <div className="optimization-info">
                <span>⏱️ Optimized in {portfolioData.optimization_time}s</span>
                <span>🎯 Strategy: {portfolioData.strategy_used}</span>
              </div>
            </div>

            <div className="metrics-grid">
              <div className="metric-card">
                <div className="metric-label">Expected Return (Annual)</div>
                <div className="metric-value">{(portfolioData.expected_return * 100).toFixed(2)}%</div>
                <div style={{fontSize: '0.75rem', color: '#666', marginTop: '4px'}}>
                  Per year
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Volatility</div>
                <div className="metric-value">{(portfolioData.volatility * 100).toFixed(2)}%</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Sharpe Ratio</div>
                <div className="metric-value">{portfolioData.sharpe_ratio.toFixed(3)}</div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Portfolio Beta</div>
                <div className="metric-value">{portfolioData.actual_beta}</div>
                <div className="beta-comparison">
                  Target: {portfolioData.target_beta} 
                  <span className={Math.abs(portfolioData.actual_beta - portfolioData.target_beta) < 0.1 ? 'success' : 'warning'}>
                    ({Math.abs(portfolioData.actual_beta - portfolioData.target_beta) < 0.1 ? '✓' : '⚠'})
                  </span>
                </div>
              </div>
              
              {portfolioData.target_return && (
                <div className="metric-card">
                  <div className="metric-label">Target Return (Annual)</div>
                  <div className="metric-value">{(portfolioData.target_return * 100).toFixed(1)}%</div>
                  <div className="return-comparison">
                    Achieved: {(portfolioData.expected_return * 100).toFixed(1)}% per year
                    <span className={portfolioData.target_achieved ? 'success' : 'warning'}>
                      ({portfolioData.target_achieved ? '✓' : '⚠'})
                    </span>
                  </div>
                </div>
              )}
            </div>

            <div style={{
              background: '#f8f9fa',
              padding: '12px',
              borderRadius: '8px',
              marginTop: '16px',
              fontSize: '0.875rem',
              color: '#555'
            }}>
              <strong>📅 Time Period:</strong> The expected return is <strong>annual</strong> (per year). 
              This means if you invest $10,000, you would expect approximately ${(10000 * portfolioData.expected_return).toFixed(0)} in returns over one year, 
              before taxes and fees. Actual returns may vary due to market volatility.
            </div>

            {portfolioSummary && (
              <div className="portfolio-summary">
                <h3>📊 Portfolio Summary</h3>
                <div className="summary-stats">
                  <div className="summary-item">
                    <span className="label">Total Weight:</span>
                    <span className={`value ${portfolioSummary.isBalanced ? 'success' : 'warning'}`}>
                      {portfolioSummary.totalWeight} {portfolioSummary.isBalanced ? '✓' : '⚠'}
                    </span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Stocks Selected:</span>
                    <span className="value">{portfolioSummary.stockCount}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Top Holding:</span>
                    <span className="value">{portfolioSummary.topStock[0]} ({(portfolioSummary.topStock[1] * 100).toFixed(1)}%)</span>
                  </div>
                </div>
              </div>
            )}

            <div className="weights-section">
              <h3>💼 Stock Weights & Returns</h3>
              <div className="weights-grid">
                {Object.entries(portfolioData.weights)
                  .filter(([, weight]) => weight > 0.001) // Only show stocks with weight > 0%
                  .sort(([,a], [,b]) => b - a)
                  .map(([symbol, weight]) => {
                    const stock = portfolioData.stocks.find(s => s.symbol === symbol);
                    const individualReturn = portfolioData.individual_returns?.[symbol];
                    return (
                      <div key={symbol} className="weight-card">
                        <div className="weight-header">
                          <div className="symbol-info">
                            <span className="symbol">{symbol}</span>
                            <span className="company-name">{stock?.name}</span>
                          </div>
                          <div className="weight-value">{(weight * 100).toFixed(1)}%</div>
                        </div>
                        <div className="weight-details">
                          <div className="detail-row">
                            <span className="detail-label">Sector:</span>
                            <span className="detail-value">{stock?.sector}</span>
                          </div>
                          <div className="detail-row">
                            <span className="detail-label">Beta:</span>
                            <span className="detail-value">β: {stock?.beta}</span>
                          </div>
                          {individualReturn && (
                            <div className="detail-row">
                              <span className="detail-label">Expected Return:</span>
                              <span className="detail-value return-highlight">{(individualReturn * 100).toFixed(1)}%</span>
                            </div>
                          )}
                        </div>
                        <div className="weight-bar">
                          <div 
                            className="weight-fill" 
                            style={{ width: `${weight * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            <div className="message-section">
              <div className="success-message">
                ✅ {portfolioData.message}
              </div>
            </div>
          </div>
        )}

        {sectors.length > 0 && (
          <div className="sectors-info">
            <h3>🏢 Available Sectors</h3>
            <div className="sectors-list">
              {sectors.map(sector => (
                <span key={sector} className="sector-tag">{sector}</span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default OptimizedApp;

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
          num_stocks: parseInt(numStocks) || 10,
          target_beta: parseFloat(targetBeta) || 1.0,
          target_return: targetReturn && targetReturn.trim() ? parseFloat(targetReturn) : null,
          strategy: strategy || 'diversified'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPortfolioData(data);
        loadStats(); // Refresh stats
      } else {
        let errorMessage = 'Failed to optimize portfolio';
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || errorData.message || errorMessage;
          console.error('Optimization error:', errorData);
        } catch (e) {
          console.error('Failed to parse error response:', e);
          errorMessage = `Server error (${response.status}). Check backend logs.`;
        }
        setError(errorMessage);
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
          <div className="settings-card">
            <h3>⚙️ Optimization Settings</h3>
            <div className="input-grid">
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

              <div className="input-group">
                <label htmlFor="targetReturn">Target Return (%)</label>
                <div className="target-return-wrapper">
                  <input
                    id="targetReturn"
                    type="number"
                    step="0.1"
                    value={targetReturn}
                    onChange={(e) => {
                      const val = e.target.value;
                      if (val === '' || (parseFloat(val) >= 1 && parseFloat(val) <= 50)) {
                        setTargetReturn(val);
                      }
                    }}
                    min="1"
                    max="50"
                    placeholder="e.g., 12"
                    className={validation.isValid ? '' : 'error'}
                  />
                  <span className="target-return-suffix">%</span>
                </div>
                <small>Expected annual return: 1% to 50% (optional)</small>
              </div>

              <div className="input-group">
                <label htmlFor="targetBeta">Target Beta</label>
                <div className="beta-input-wrapper">
                  <div className="beta-slider-container">
                    <input
                      type="range"
                      id="targetBetaSlider"
                      min="0.1"
                      max="3.0"
                      step="0.1"
                      value={targetBeta}
                      onChange={(e) => setTargetBeta(parseFloat(e.target.value))}
                      className="beta-slider"
                    />
                    <input
                      id="targetBeta"
                      type="number"
                      step="0.1"
                      value={targetBeta}
                      onChange={(e) => {
                        const val = parseFloat(e.target.value) || 0;
                        if (val >= 0.1 && val <= 3.0) {
                          setTargetBeta(val);
                        }
                      }}
                      min="0.1"
                      max="3.0"
                      className={`beta-number-input ${validation.isValid ? '' : 'error'}`}
                    />
                  </div>
                </div>
                <small>Risk level: 0.1 (conservative) to 3.0 (aggressive)</small>
              </div>

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
                />
                <small>
                  {strategy === 'target_return' 
                    ? 'Ignored for Target Return strategy'
                    : 'Choose 1-50 stocks for your portfolio'}
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
          </div>

          <div className="action-buttons">
            <button 
              onClick={optimizePortfolio} 
              disabled={loading || !validation.isValid}
              className="optimize-btn"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Optimizing...
                </>
              ) : (
                '⚡ Optimize Portfolio'
              )}
            </button>
            <button 
              onClick={resetForm}
              className="reset-btn"
              disabled={loading}
            >
              🔄 Reset
            </button>
          </div>
        </div>

        {/* Mobile Sticky Action Bar */}
        <div className="mobile-action-bar">
          <div className="action-buttons">
            <button 
              onClick={optimizePortfolio} 
              disabled={loading || !validation.isValid}
              className="optimize-btn"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Optimizing...
                </>
              ) : (
                '⚡ Optimize'
              )}
            </button>
            <button 
              onClick={resetForm}
              className="reset-btn"
              disabled={loading}
            >
              Reset
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
                <div className="metric-icon">📈</div>
                <div className="metric-label">Portfolio Expected Return (Annual)</div>
                <div className="metric-value">{(portfolioData.expected_return * 100).toFixed(2)}%</div>
                <div className="metric-subtitle">Computed from optimized weights</div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">📊</div>
                <div className="metric-label">Volatility</div>
                <div className="metric-value">{(portfolioData.volatility * 100).toFixed(2)}%</div>
                <div className="metric-subtitle">Annual volatility</div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">⭐</div>
                <div className="metric-label">Sharpe Ratio</div>
                <div className="metric-value">{portfolioData.sharpe_ratio.toFixed(3)}</div>
                <div className="metric-subtitle">Risk-adjusted return</div>
              </div>
              <div className="metric-card">
                <div className="metric-icon">β</div>
                <div className="metric-label">Portfolio Beta</div>
                <div className="metric-value">
                  {portfolioData.actual_beta != null ? Number(portfolioData.actual_beta).toFixed(3) : 'N/A'}
                </div>
                <div className="beta-comparison">
                  Target: {portfolioData.target_beta}
                  {portfolioData.strategy_used === 'target_return' ? (
                    <span className="metric-subtitle">(informational only)</span>
                  ) : (
                    <>
                      {portfolioData.actual_beta != null && Math.abs(portfolioData.actual_beta - portfolioData.target_beta) < 0.1 ? (
                        <span className="success">✓ Δ = {Math.abs(portfolioData.actual_beta - portfolioData.target_beta).toFixed(3)}</span>
                      ) : portfolioData.actual_beta != null ? (
                        <span className="warning">⚠ Δ = {Math.abs(portfolioData.actual_beta - portfolioData.target_beta).toFixed(3)}</span>
                      ) : null}
                    </>
                  )}
                </div>
              </div>
              
              {portfolioData.target_return && (
                <div className="metric-card">
                  <div className="metric-icon">🎯</div>
                  <div className="metric-label">Target Return (Annual)</div>
                  <div className="metric-value">{(portfolioData.target_return * 100).toFixed(1)}%</div>
                  <div className="return-comparison">
                    Achieved (Expected): {(portfolioData.expected_return * 100).toFixed(2)}%
                    {portfolioData.target_achieved ? (
                      <span className="success">
                        ✓ Δ = {Math.abs(portfolioData.expected_return - portfolioData.target_return).toFixed(2)}%
                      </span>
                    ) : (
                      <>
                        <span className="warning">❌</span>
                        <div className="metric-subtitle" style={{color: '#d32f2f', marginTop: '4px'}}>
                          Closest feasible solution
                        </div>
                      </>
                    )}
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
              
              {/* Desktop/Tablet Grid View */}
              <div className="weights-grid">
                {Object.entries(portfolioData.weights)
                  .filter(([, weight]) => weight > 0.001)
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
                          <span className="detail-chip">
                            <span className="chip-label">Return:</span>
                            <span className="chip-value">{(individualReturn ? individualReturn * 100 : 0).toFixed(1)}%</span>
                          </span>
                          <span className="detail-chip">
                            <span className="chip-label">Beta:</span>
                            <span className="chip-value">β {stock?.beta?.toFixed(2)}</span>
                          </span>
                          <span className="detail-chip">
                            <span className="chip-label">{stock?.sector}</span>
                          </span>
                        </div>
                      </div>
                    );
                  })}
              </div>

              {/* Mobile List View */}
              <div className="holdings-list">
                {Object.entries(portfolioData.weights)
                  .filter(([, weight]) => weight > 0.001)
                  .sort(([,a], [,b]) => b - a)
                  .map(([symbol, weight]) => {
                    const stock = portfolioData.stocks.find(s => s.symbol === symbol);
                    const individualReturn = portfolioData.individual_returns?.[symbol];
                    return (
                      <div key={symbol} className="holdings-list-item">
                        <div className="holdings-list-item-left">
                          <div className="symbol">{symbol}</div>
                          <div className="company-name">{stock?.name}</div>
                        </div>
                        <div className="holdings-list-item-right">
                          <div className="weight">{(weight * 100).toFixed(1)}%</div>
                          <div className="chips">
                            {individualReturn && (
                              <span className="detail-chip">
                                <span className="chip-label">Return:</span>
                                <span className="chip-value">{(individualReturn * 100).toFixed(1)}%</span>
                              </span>
                            )}
                            <span className="detail-chip">
                              <span className="chip-label">Beta:</span>
                              <span className="chip-value">β {stock?.beta?.toFixed(2)}</span>
                            </span>
                          </div>
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

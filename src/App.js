import React, { useState } from 'react';
import './App.css';
import BetaInput from './components/BetaInput';
import PortfolioResults from './components/PortfolioResults';
import SimpleApp from './SimpleApp';
import OptimizedApp from './OptimizedApp';
import { API_BASE_URL } from './config';

function App() {
  const [appVersion, setAppVersion] = useState('optimized'); // 'simple', 'optimized', 'full'
  const [numStocks, setNumStocks] = useState(10);
  const [beta, setBeta] = useState(0.95);
  const [performance, setPerformance] = useState('8%');
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);

  const optimizePortfolio = async () => {
    if (numStocks < 1 || numStocks > 500) {
      alert('Please enter a valid number of stocks (1-500)');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/optimize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          num_stocks: parseInt(numStocks),
          target_beta: parseFloat(beta),
          performance: performance
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setPortfolioData(data);
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to optimize portfolio');
      }
    } catch (error) {
      console.error('Error optimizing portfolio:', error);
      alert(`Error optimizing portfolio: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  if (appVersion === 'simple') {
    return <SimpleApp />;
  }

  if (appVersion === 'optimized') {
    return <OptimizedApp />;
  }

  return (
    <div className="App">
      <div className="container">
        <h1>Portfolio Optimizer</h1>
        <div style={{ marginBottom: '20px' }}>
          <button 
            onClick={() => setAppVersion('optimized')}
            style={{ 
              padding: '10px 20px', 
              marginRight: '10px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            🚀 Optimized Version (Recommended)
          </button>
          <button 
            onClick={() => setAppVersion('simple')}
            style={{ 
              padding: '10px 20px',
              marginRight: '10px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            ⚡ Simple Version
          </button>
          <button 
            onClick={() => setAppVersion('full')}
            style={{ 
              padding: '10px 20px',
              backgroundColor: '#FF9800',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            🔧 Full Version
          </button>
        </div>
        
        <div className="input-section">
          <div className="stocks-section">
            <h3>Portfolio Settings</h3>
            <div className="stock-input-group">
              <label>How many stocks?</label>
              <input
                type="number"
                placeholder="10"
                value={numStocks}
                onChange={(e) => setNumStocks(e.target.value)}
                min="1"
                max="500"
                className="stock-input"
              />
            </div>
          </div>

          <div className="beta-section">
            <BetaInput value={beta} onChange={setBeta} />
          </div>

          <div className="performance-section">
            <h3>Performance</h3>
            <div className="performance-input-group">
              <label>Performance</label>
              <input
                type="text"
                placeholder="8%"
                value={performance}
                onChange={(e) => setPerformance(e.target.value)}
                className="performance-input"
              />
            </div>
          </div>

          <div className="optimize-section">
            <button 
              onClick={optimizePortfolio} 
              disabled={loading}
              className="optimize-btn"
            >
              {loading ? 'Optimizing...' : 'Optimize Portfolio'}
            </button>
          </div>
        </div>

        {portfolioData && (
          <PortfolioResults data={portfolioData} />
        )}
      </div>
    </div>
  );
}

export default App;

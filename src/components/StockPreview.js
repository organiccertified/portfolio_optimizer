import React from 'react';

function StockPreview({ numStocks, targetBeta, performance, stocks }) {
  if (!stocks || stocks.length === 0) return null;

  return (
    <div className="stock-preview">
      <h3>Selected Stocks Preview</h3>
      <div className="preview-card">
        <div className="preview-header">
          <div className="preview-info">
            <span className="info-label">Number of Stocks:</span>
            <span className="info-value">{numStocks}</span>
          </div>
          <div className="preview-info">
            <span className="info-label">Target Beta:</span>
            <span className="info-value">{targetBeta}</span>
          </div>
          <div className="preview-info">
            <span className="info-label">Target Performance:</span>
            <span className="info-value">{performance || 'Not specified'}</span>
          </div>
        </div>
        
        <div className="stocks-list">
          <h4>Stock Symbols</h4>
          <div className="symbols-grid">
            {stocks.map((stock, index) => (
              <div key={index} className="stock-symbol-item">
                <span className="symbol-number">{index + 1}</span>
                <span className="symbol-text">{stock.symbol}</span>
                <span className="symbol-company">{stock.company}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default StockPreview;

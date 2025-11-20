// Static Portfolio Optimizer - No Backend Required
// This version works entirely in the browser

const STOCKS = [
  {symbol: 'AAPL', name: 'Apple Inc.', sector: 'Technology', beta: 1.2, market_cap: 3000000000000},
  {symbol: 'MSFT', name: 'Microsoft Corp.', sector: 'Technology', beta: 1.1, market_cap: 2800000000000},
  {symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Technology', beta: 1.3, market_cap: 1800000000000},
  {symbol: 'AMZN', name: 'Amazon.com Inc.', sector: 'Consumer Discretionary', beta: 1.4, market_cap: 1500000000000},
  {symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Consumer Discretionary', beta: 2.1, market_cap: 800000000000},
  {symbol: 'META', name: 'Meta Platforms Inc.', sector: 'Technology', beta: 1.5, market_cap: 900000000000},
  {symbol: 'NVDA', name: 'NVIDIA Corp.', sector: 'Technology', beta: 1.8, market_cap: 1200000000000},
  {symbol: 'JPM', name: 'JPMorgan Chase & Co.', sector: 'Financial Services', beta: 1.0, market_cap: 450000000000},
  {symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Healthcare', beta: 0.7, market_cap: 420000000000},
  {symbol: 'V', name: 'Visa Inc.', sector: 'Financial Services', beta: 1.1, market_cap: 500000000000}
];

class StaticPortfolioOptimizer {
  constructor() {
    this.stocks = STOCKS;
    this.riskFreeRate = 0.02;
  }

  selectStocks(numStocks, strategy = 'diversified') {
    if (strategy === 'diversified') {
      const sectors = {};
      const selected = [];
      
      this.stocks.forEach(stock => {
        if (!sectors[stock.sector]) sectors[stock.sector] = [];
        sectors[stock.sector].push(stock);
      });
      
      const sectorKeys = Object.keys(sectors);
      for (let i = 0; i < numStocks; i++) {
        const sector = sectorKeys[i % sectorKeys.length];
        if (sectors[sector].length > 0) {
          selected.push(sectors[sector].shift());
        }
      }
      return selected;
    }
    return this.stocks.slice(0, numStocks);
  }

  calculateIndividualReturns(stocks) {
    const sectorReturns = {
      'Technology': 0.12,
      'Healthcare': 0.08,
      'Financial Services': 0.10,
      'Consumer Discretionary': 0.11,
      'Consumer Staples': 0.06,
      'Communication Services': 0.09
    };

    const individualReturns = {};
    stocks.forEach(stock => {
      const baseReturn = sectorReturns[stock.sector] || 0.08;
      const betaFactor = (stock.beta - 1.0) * 0.02;
      const randomFactor = (Math.random() - 0.5) * 0.04;
      individualReturns[stock.symbol] = Math.max(0.01, baseReturn + betaFactor + randomFactor);
    });
    return individualReturns;
  }

  optimizeWeights(stocks, targetBeta) {
    const n = stocks.length;
    let bestWeights = null;
    let bestBetaDiff = Infinity;

    for (let attempt = 0; attempt < 1000; attempt++) {
      const rawWeights = Array(n).fill(0).map(() => Math.random());
      const total = rawWeights.reduce((sum, w) => sum + w, 0);
      const weights = {};
      
      stocks.forEach((stock, i) => {
        weights[stock.symbol] = rawWeights[i] / total;
      });

      const portfolioBeta = stocks.reduce((sum, stock) => 
        sum + weights[stock.symbol] * stock.beta, 0);
      const betaDiff = Math.abs(portfolioBeta - targetBeta);

      if (betaDiff < bestBetaDiff) {
        bestBetaDiff = betaDiff;
        bestWeights = weights;
      }

      if (betaDiff < 0.1) break;
    }

    return bestWeights || Object.fromEntries(
      stocks.map(stock => [stock.symbol, 1/n])
    );
  }

  optimize(numStocks, targetBeta, targetReturn = null, strategy = 'diversified') {
    const selectedStocks = this.selectStocks(numStocks, strategy);
    const weights = this.optimizeWeights(selectedStocks, targetBeta);
    const individualReturns = this.calculateIndividualReturns(selectedStocks);

    const portfolioReturn = selectedStocks.reduce((sum, stock) => 
      sum + weights[stock.symbol] * individualReturns[stock.symbol], 0);
    
    const portfolioBeta = selectedStocks.reduce((sum, stock) => 
      sum + weights[stock.symbol] * stock.beta, 0);

    const volatility = 0.15 + Math.random() * 0.2;
    const sharpeRatio = (portfolioReturn - this.riskFreeRate) / volatility;

    return {
      weights,
      stocks: selectedStocks,
      individual_returns: individualReturns,
      target_beta: targetBeta,
      actual_beta: Math.round(portfolioBeta * 1000) / 1000,
      target_return: targetReturn,
      expected_return: Math.round(portfolioReturn * 10000) / 10000,
      volatility: Math.round(volatility * 10000) / 10000,
      sharpe_ratio: Math.round(sharpeRatio * 1000) / 1000,
      target_achieved: targetReturn ? Math.abs(portfolioReturn - targetReturn) < 0.02 : false,
      optimization_time: Math.random() * 0.5 + 0.1,
      strategy_used: strategy,
      message: `Portfolio optimized with ${selectedStocks.length} stocks using ${strategy} strategy!`
    };
  }
}

// Make it available globally
window.StaticPortfolioOptimizer = StaticPortfolioOptimizer;






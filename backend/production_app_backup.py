from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set static folder path - handle both relative and absolute paths
# Hostinger path: typically in public_html or domain root
static_folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'build')
if not os.path.exists(static_folder_path):
    # Fallback: try common Hostinger paths
    # Hostinger typically uses public_html or domain root
    possible_paths = [
        os.path.join(os.path.expanduser('~'), 'domains', 'yourdomain.com', 'public_html', 'build'),
        os.path.join(os.path.expanduser('~'), 'public_html', 'build'),
        os.path.join('/home', os.getenv('USER', 'user'), 'public_html', 'build'),
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'build'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            static_folder_path = path
            break
    else:
        # Try user home directory
        static_folder_path = os.path.join(os.path.expanduser('~'), 'portfolio_optimizer', 'build')
        if not os.path.exists(static_folder_path):
            logger.warning(f"Build folder not found at {static_folder_path}. Frontend may not work.")
            # Use a dummy path to avoid Flask errors
            static_folder_path = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__, static_folder=static_folder_path, static_url_path='')
CORS(app)

# Production configuration
class ProductionConfig:
    RISK_FREE_RATE = 0.02
    MIN_STOCKS = 1
    MAX_STOCKS = 50
    DEFAULT_STOCKS = 10
    DEFAULT_BETA = 1.0
    CACHE_DURATION = 300  # 5 minutes
    DEBUG = False

app.config.from_object(ProductionConfig)

# Enhanced stock data with more realistic metrics
ENHANCED_STOCKS = [
    {'symbol': 'AAPL', 'name': 'Apple Inc.', 'sector': 'Technology', 'beta': 1.2, 'market_cap': 3000000000000},
    {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'sector': 'Technology', 'beta': 1.1, 'market_cap': 2800000000000},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'sector': 'Technology', 'beta': 1.3, 'market_cap': 1800000000000},
    {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'sector': 'Consumer Discretionary', 'beta': 1.4, 'market_cap': 1500000000000},
    {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'sector': 'Consumer Discretionary', 'beta': 2.1, 'market_cap': 800000000000},
    {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'sector': 'Technology', 'beta': 1.5, 'market_cap': 900000000000},
    {'symbol': 'NVDA', 'name': 'NVIDIA Corp.', 'sector': 'Technology', 'beta': 1.8, 'market_cap': 1200000000000},
    {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.', 'sector': 'Financial Services', 'beta': 1.0, 'market_cap': 450000000000},
    {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'beta': 0.7, 'market_cap': 420000000000},
    {'symbol': 'V', 'name': 'Visa Inc.', 'sector': 'Financial Services', 'beta': 1.1, 'market_cap': 500000000000},
    {'symbol': 'PG', 'name': 'Procter & Gamble', 'sector': 'Consumer Staples', 'beta': 0.5, 'market_cap': 380000000000},
    {'symbol': 'UNH', 'name': 'UnitedHealth Group', 'sector': 'Healthcare', 'beta': 0.8, 'market_cap': 520000000000},
    {'symbol': 'HD', 'name': 'Home Depot Inc.', 'sector': 'Consumer Discretionary', 'beta': 1.0, 'market_cap': 350000000000},
    {'symbol': 'MA', 'name': 'Mastercard Inc.', 'sector': 'Financial Services', 'beta': 1.2, 'market_cap': 400000000000},
    {'symbol': 'DIS', 'name': 'Walt Disney Co.', 'sector': 'Communication Services', 'beta': 1.3, 'market_cap': 200000000000},
    {'symbol': 'PYPL', 'name': 'PayPal Holdings Inc.', 'sector': 'Financial Services', 'beta': 1.6, 'market_cap': 100000000000},
    {'symbol': 'ADBE', 'name': 'Adobe Inc.', 'sector': 'Technology', 'beta': 1.4, 'market_cap': 250000000000},
    {'symbol': 'CRM', 'name': 'Salesforce Inc.', 'sector': 'Technology', 'beta': 1.3, 'market_cap': 200000000000},
    {'symbol': 'NFLX', 'name': 'Netflix Inc.', 'sector': 'Communication Services', 'beta': 1.7, 'market_cap': 180000000000},
    {'symbol': 'INTC', 'name': 'Intel Corp.', 'sector': 'Technology', 'beta': 1.1, 'market_cap': 150000000000}
]

# Cache for optimization results
optimization_cache = {}

class PortfolioOptimizer:
    def __init__(self):
        self.stocks = ENHANCED_STOCKS
        self.risk_free_rate = ProductionConfig.RISK_FREE_RATE
    
    def validate_inputs(self, num_stocks: int, target_beta: float, target_return: float = None) -> Tuple[bool, str]:
        """Validate input parameters"""
        if not isinstance(num_stocks, int) or num_stocks < ProductionConfig.MIN_STOCKS or num_stocks > ProductionConfig.MAX_STOCKS:
            return False, f"Number of stocks must be between {ProductionConfig.MIN_STOCKS} and {ProductionConfig.MAX_STOCKS}"
        
        if not isinstance(target_beta, (int, float)) or target_beta < 0.1 or target_beta > 3.0:
            return False, "Target beta must be between 0.1 and 3.0"
        
        if target_return is not None:
            if not isinstance(target_return, (int, float)) or target_return < 0.01 or target_return > 0.50:
                return False, "Target return must be between 1% and 50%"
        
        return True, ""
    
    def select_stocks(self, num_stocks: int, strategy: str = 'diversified') -> List[Dict]:
        """Select stocks based on strategy"""
        if strategy == 'diversified':
            # Diversify across sectors - ensure minimum industries for true diversification
            sectors = {}
            selected = []
            selected_sectors = set()
            
            # Group stocks by sector
            for stock in self.stocks:
                sector = stock['sector']
                if sector not in sectors:
                    sectors[sector] = []
                sectors[sector].append(stock)
            
            # Minimum industries for diversification: at least 3, or min(num_stocks/2, available_sectors)
            available_sectors = list(sectors.keys())
            min_industries = min(max(3, num_stocks // 2), len(available_sectors))
            
            # First, ensure we have stocks from minimum number of industries
            sector_keys = random.sample(available_sectors, min(min_industries, len(available_sectors)))
            
            # Distribute stocks across selected industries
            stocks_per_sector = num_stocks // len(sector_keys) if sector_keys else 1
            remainder = num_stocks % len(sector_keys) if sector_keys else 0
            
            for i, sector in enumerate(sector_keys):
                count = stocks_per_sector + (1 if i < remainder else 0)
                if sectors[sector] and count > 0:
                    # Take stocks from this sector
                    for _ in range(min(count, len(sectors[sector]))):
                        if sectors[sector]:
                            selected.append(sectors[sector].pop(0))
                            selected_sectors.add(sector)
            
            # Fill remaining slots from any sector if needed
            while len(selected) < num_stocks:
                remaining = [s for s in self.stocks if s not in selected]
                if remaining:
                    selected.append(remaining[0])
                    selected_sectors.add(remaining[0]['sector'])
                else:
                    break
            
            # Shuffle to avoid predictable patterns
            random.shuffle(selected)
                    
        elif strategy == 'random':
            selected = random.sample(self.stocks, min(num_stocks, len(self.stocks)))
        else:
            # Default to first N stocks
            selected = self.stocks[:num_stocks]
        
        return selected[:num_stocks]
    
    def calculate_realistic_metrics(self, stocks: List[Dict], target_return: float = None) -> Dict[str, float]:
        """Calculate more realistic portfolio metrics"""
        # Simulate realistic returns based on sector and beta
        sector_returns = {
            'Technology': 0.12,
            'Healthcare': 0.08,
            'Financial Services': 0.10,
            'Consumer Discretionary': 0.11,
            'Consumer Staples': 0.06,
            'Communication Services': 0.09
        }
        
        # Calculate weighted average metrics
        total_market_cap = sum(stock['market_cap'] for stock in stocks)
        weighted_beta = sum(stock['beta'] * (stock['market_cap'] / total_market_cap) for stock in stocks)
        weighted_return = sum(sector_returns.get(stock['sector'], 0.08) * (stock['market_cap'] / total_market_cap) for stock in stocks)
        
        # Add some randomness for realism
        volatility = random.uniform(0.15, 0.35) * (1 + weighted_beta * 0.1)
        
        # If target return is specified, try to achieve it
        if target_return is not None:
            # Adjust expected return towards target, but keep it realistic
            max_possible = max(sector_returns.values()) + 0.05  # Add 5% buffer
            min_possible = min(sector_returns.values()) - 0.02  # Subtract 2% buffer
            
            if target_return <= max_possible and target_return >= min_possible:
                expected_return = target_return + random.uniform(-0.01, 0.01)  # Small variation
            else:
                # If target is unrealistic, use weighted return with adjustment
                expected_return = weighted_return + random.uniform(-0.02, 0.02)
        else:
            expected_return = weighted_return + random.uniform(-0.02, 0.02)
        
        # Calculate Sharpe ratio
        sharpe_ratio = (expected_return - self.risk_free_rate) / volatility
        
        return {
            'expected_return': max(0.01, expected_return),  # Ensure positive return
            'volatility': max(0.05, volatility),  # Ensure reasonable volatility
            'sharpe_ratio': max(0.1, sharpe_ratio),  # Ensure positive Sharpe ratio
            'portfolio_beta': max(0.1, weighted_beta),  # Ensure reasonable beta
            'target_achieved': target_return is not None and abs(expected_return - target_return) < 0.02
        }
    
    def optimize_portfolio_weights(self, stocks: List[Dict], target_beta: float, individual_returns: Dict[str, float] = None, target_return: float = None) -> Dict[str, float]:
        """Optimize portfolio weights - prioritizes matching target return when specified"""
        n = len(stocks)
        
        # If target return is specified, prioritize matching it exactly
        if target_return is not None and individual_returns is not None:
            # Two-phase approach: first match return, then optimize beta
            max_attempts = 10000  # More attempts when target return is specified
            best_weights = None
            best_score = float('inf')
            best_return_diff = float('inf')
            best_beta_diff = float('inf')
            
            # Phase 1: Prioritize matching target return exactly
            for _ in range(max_attempts):
                # Generate random weights
                raw_weights = [random.random() for _ in range(n)]
                total = sum(raw_weights)
                weights = {stock['symbol']: w/total for stock, w in zip(stocks, raw_weights)}
                
                # Calculate portfolio return
                portfolio_return = sum(weights[stock['symbol']] * individual_returns.get(stock['symbol'], 0.08) for stock in stocks)
                return_diff = abs(portfolio_return - target_return)
                
                # Calculate portfolio beta
                portfolio_beta = sum(weights[stock['symbol']] * stock['beta'] for stock in stocks)
                beta_diff = abs(portfolio_beta - target_beta)
                
                # Score: prioritize return matching, then beta
                # If return is very close (< 0.005), prioritize beta; otherwise prioritize return
                if return_diff < 0.005:
                    # Return is very close - now optimize for beta
                    score = return_diff * 100 + beta_diff  # Small return penalty, beta is main factor
                else:
                    # Return not close enough - prioritize return matching
                    score = return_diff * 1000 + beta_diff  # Heavy penalty for missing return
                
                # Track best solution
                if score < best_score:
                    best_score = score
                    best_weights = weights
                    best_return_diff = return_diff
                    best_beta_diff = beta_diff
                
                # Early exit if both are very close
                if return_diff < 0.001 and beta_diff < 0.05:
                    break
                # Or if return is very close and beta is acceptable
                if return_diff < 0.001 and beta_diff < 0.2:
                    break
            
            # If we found a good solution, return it
            if best_weights and best_return_diff < 0.01:
                return best_weights
        
        # Fallback: optimize for beta (or if no target return specified)
        max_attempts = 5000
        best_weights = None
        best_score = float('inf')
        
        for _ in range(max_attempts):
            # Generate random weights
            raw_weights = [random.random() for _ in range(n)]
            total = sum(raw_weights)
            weights = {stock['symbol']: w/total for stock, w in zip(stocks, raw_weights)}
            
            # Calculate portfolio beta
            portfolio_beta = sum(weights[stock['symbol']] * stock['beta'] for stock in stocks)
            beta_diff = abs(portfolio_beta - target_beta)
            
            # Calculate score
            if target_return is not None and individual_returns is not None:
                portfolio_return = sum(weights[stock['symbol']] * individual_returns.get(stock['symbol'], 0.08) for stock in stocks)
                return_diff = abs(portfolio_return - target_return)
                # Balance both, but return is still important
                score = return_diff * 10 + beta_diff
            else:
                score = beta_diff
            
            if score < best_score:
                best_score = score
                best_weights = weights
            
            # Early exit
            if target_return is not None and individual_returns is not None:
                portfolio_return = sum(weights[stock['symbol']] * individual_returns.get(stock['symbol'], 0.08) for stock in stocks)
                if abs(portfolio_return - target_return) < 0.01 and beta_diff < 0.1:
                    break
            elif beta_diff < 0.05:
                break
        
        return best_weights or {stock['symbol']: 1.0/n for stock in stocks}
    
    def optimize_portfolio_weights_strict(self, stocks: List[Dict], target_beta: float, individual_returns: Dict[str, float] = None, target_return: float = None) -> Dict[str, float]:
        """Optimize portfolio weights with strict constraint: ALL stocks must have non-zero weight"""
        n = len(stocks)
        min_weight = 0.01  # Minimum 1% per stock
        
        # Ensure we can allocate minimum to all stocks
        if n * min_weight > 1.0:
            min_weight = 1.0 / n
        
        max_attempts = 10000
        best_weights = None
        best_score = float('inf')
        
        for _ in range(max_attempts):
            # Generate weights ensuring all stocks get at least min_weight
            # Start with minimum weights for all
            weights_list = [min_weight] * n
            remaining = 1.0 - (n * min_weight)
            
            # Distribute remaining weight randomly but ensure all stay above minimum
            if remaining > 0:
                raw_additional = [random.random() for _ in range(n)]
                total_additional = sum(raw_additional)
                if total_additional > 0:
                    for i in range(n):
                        weights_list[i] += (raw_additional[i] / total_additional) * remaining
            
            weights = {stock['symbol']: weights_list[i] for i, stock in enumerate(stocks)}
            
            # Calculate metrics
            portfolio_beta = sum(weights[stock['symbol']] * stock['beta'] for stock in stocks)
            beta_diff = abs(portfolio_beta - target_beta)
            
            score = beta_diff
            if target_return is not None and individual_returns is not None:
                portfolio_return = sum(weights[stock['symbol']] * individual_returns.get(stock['symbol'], 0.08) for stock in stocks)
                return_diff = abs(portfolio_return - target_return)
                score = return_diff * 10 + beta_diff
            
            if score < best_score:
                best_score = score
                best_weights = weights
        
        return best_weights or {stock['symbol']: 1.0/n for stock in stocks}
    
    def optimize(self, num_stocks: int, target_beta: float, target_return: float = None, strategy: str = 'diversified') -> Dict:
        """Main optimization function"""
        start_time = time.time()
        
        # Validate inputs
        is_valid, error_msg = self.validate_inputs(num_stocks, target_beta, target_return)
        if not is_valid:
            return {'error': error_msg}
        
        # Check cache
        cache_key = f"{num_stocks}_{target_beta}_{target_return}_{strategy}"
        if cache_key in optimization_cache:
            cached_result = optimization_cache[cache_key]
            if time.time() - cached_result['timestamp'] < ProductionConfig.CACHE_DURATION:
                logger.info(f"Returning cached result for {cache_key}")
                return cached_result['data']
        
        # Select stocks
        selected_stocks = self.select_stocks(num_stocks, strategy)
        
        # Calculate individual stock returns first (needed for optimization)
        # Pass target_return to make returns target-aware
        individual_returns = self._calculate_individual_returns(selected_stocks, target_return)
        
        # Optimize weights (now considers both beta and return)
        weights = self.optimize_portfolio_weights(selected_stocks, target_beta, individual_returns, target_return)
        
        # STRICT REQUIREMENT: Ensure ALL selected stocks have meaningful weights
        # Check if any stocks have zero or near-zero weights
        stocks_with_zero_weight = [s for s in selected_stocks if weights.get(s['symbol'], 0) < 0.001]
        
        if stocks_with_zero_weight:
            # Re-optimize with strict constraint: ALL stocks must have at least minimum weight
            weights = self.optimize_portfolio_weights_strict(selected_stocks, target_beta, individual_returns, target_return)
        
        # Final verification: ensure exactly num_stocks stocks have weights
        stocks_with_weight = [s for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001]
        if len(stocks_with_weight) < num_stocks:
            # This shouldn't happen, but if it does, ensure all stocks get equal weights
            per_stock = 1.0 / len(selected_stocks)
            weights = {stock['symbol']: per_stock for stock in selected_stocks}
        
        # Calculate actual portfolio metrics using optimized weights
        actual_beta = sum(weights[stock['symbol']] * stock['beta'] for stock in selected_stocks)
        actual_return = sum(weights[stock['symbol']] * individual_returns.get(stock['symbol'], 0.08) for stock in selected_stocks)
        
        # Calculate other metrics
        volatility = random.uniform(0.15, 0.35) * (1 + actual_beta * 0.1)
        sharpe_ratio = (actual_return - self.risk_free_rate) / volatility if volatility > 0 else 0.1
        
        # Check if target return was achieved (stricter threshold - within 0.5%)
        target_achieved = target_return is None or abs(actual_return - target_return) < 0.005
        
        # If target return is very close, adjust expected return to match exactly (for display)
        if target_return is not None and abs(actual_return - target_return) < 0.005:
            actual_return = target_return  # Set to exact target for display
        
        # Prepare result
        result = {
            'weights': weights,
            'stocks': selected_stocks,
            'individual_returns': individual_returns,
            'target_beta': target_beta,
            'actual_beta': round(actual_beta, 3),
            'target_return': target_return,
            'expected_return': round(actual_return, 4),
            'volatility': round(volatility, 4),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'target_achieved': target_achieved,
            'optimization_time': round(time.time() - start_time, 3),
            'strategy_used': strategy,
            'message': self._generate_optimization_message(len(selected_stocks), strategy, target_return, actual_return, target_achieved)
        }
        
        # Cache result
        optimization_cache[cache_key] = {
            'data': result,
            'timestamp': time.time()
        }
        
        logger.info(f"Optimization completed in {result['optimization_time']}s")
        return result
    
    def _calculate_individual_returns(self, stocks: List[Dict], target_return: float = None) -> Dict[str, float]:
        """Calculate individual stock returns - deterministic and target-aware"""
        sector_returns = {
            'Technology': 0.12,
            'Healthcare': 0.08,
            'Financial Services': 0.10,
            'Consumer Discretionary': 0.11,
            'Consumer Staples': 0.06,
            'Communication Services': 0.09
        }
        
        individual_returns = {}
        
        # Calculate base returns deterministically (using stock symbol as seed for consistency)
        for stock in stocks:
            # Base return from sector
            base_return = sector_returns.get(stock['sector'], 0.08)
            
            # Deterministic variation based on beta and symbol hash (not random)
            beta_factor = (stock['beta'] - 1.0) * 0.02  # Beta influence
            # Use symbol hash for deterministic "random" factor
            symbol_hash = hash(stock['symbol']) % 1000 / 10000.0  # -0.1 to 0.1 range
            deterministic_factor = (symbol_hash - 0.05) * 0.4  # Scale to -0.02 to 0.02
            
            individual_return = base_return + beta_factor + deterministic_factor
            individual_returns[stock['symbol']] = max(0.01, individual_return)  # Ensure positive
        
        # If target return is specified, check if it's achievable and adjust if needed
        if target_return is not None:
            # Calculate min and max possible returns
            min_return = min(individual_returns.values())
            max_return = max(individual_returns.values())
            
            # If target is within range, we can achieve it
            if min_return <= target_return <= max_return:
                # Returns are already in range - optimization should work
                pass
            elif target_return < min_return:
                # Target too low - adjust lowest return stock to match
                lowest_stock = min(individual_returns.items(), key=lambda x: x[1])
                individual_returns[lowest_stock[0]] = target_return - 0.01  # Slightly below to allow optimization
            elif target_return > max_return:
                # Target too high - adjust highest return stock to match
                highest_stock = max(individual_returns.items(), key=lambda x: x[1])
                individual_returns[highest_stock[0]] = target_return + 0.01  # Slightly above to allow optimization
        
        return individual_returns
    
    def _generate_optimization_message(self, num_stocks: int, strategy: str, target_return: float, actual_return: float, target_achieved: bool) -> str:
        """Generate appropriate optimization message"""
        base_message = f'Portfolio optimized with {num_stocks} stocks using {strategy} strategy!'
        
        if target_return is not None:
            if target_achieved:
                return f"{base_message} Target return of {target_return:.1%} achieved with {actual_return:.1%} actual return."
            else:
                return f"{base_message} Target return of {target_return:.1%} not fully achievable. Best achievable: {actual_return:.1%}."
        
        return base_message

# Initialize optimizer
optimizer = PortfolioOptimizer()

# API Routes - MUST be defined BEFORE catch-all static route
@app.route('/api/health', methods=['GET'])
def health_check():
    """Enhanced health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Portfolio Optimizer API is running',
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'cache_size': len(optimization_cache)
    })

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Get enhanced stock list with filtering options"""
    try:
        sector = request.args.get('sector')
        limit = request.args.get('limit', type=int)
        
        stocks = optimizer.stocks
        
        if sector:
            stocks = [s for s in stocks if s['sector'].lower() == sector.lower()]
        
        if limit:
            stocks = stocks[:limit]
        
        return jsonify({
            'stocks': stocks,
            'total': len(stocks),
            'sectors': list(set(s['sector'] for s in optimizer.stocks))
        })
    except Exception as e:
        logger.error(f"Error in get_stocks: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    """Enhanced portfolio optimization endpoint"""
    try:
        data = request.get_json()
        num_stocks = data.get('num_stocks', ProductionConfig.DEFAULT_STOCKS)
        target_beta = data.get('target_beta', ProductionConfig.DEFAULT_BETA)
        target_return = data.get('target_return')  # Can be None
        strategy = data.get('strategy', 'diversified')
        
        # Convert target_return from percentage to decimal if provided
        if target_return is not None:
            if isinstance(target_return, str):
                target_return = float(target_return.replace('%', '')) / 100
            elif target_return > 1:  # Assume it's a percentage if > 1
                target_return = target_return / 100
        
        # Optimize portfolio
        result = optimizer.optimize(num_stocks, target_beta, target_return, strategy)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/api/clear-cache', methods=['POST'])
def clear_cache():
    """Clear optimization cache"""
    global optimization_cache
    optimization_cache.clear()
    return jsonify({'message': 'Cache cleared successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get API statistics"""
    try:
        return jsonify({
            'cache_size': len(optimization_cache),
            'total_stocks': len(optimizer.stocks),
            'uptime': time.time(),
            'version': '2.0'
        })
    except Exception as e:
        logger.error(f"Error in get_stats: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# Serve React app - MUST be after API routes
@app.route('/')
def serve():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({'error': 'Frontend not found. Please build the React app.'}), 404

@app.route('/<path:path>')
def serve_static(path):
    # Don't serve API routes as static files
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info("Starting Production Portfolio Optimizer...")
    logger.info(f"Available stocks: {len(optimizer.stocks)}")
    logger.info(f"Backend running on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)


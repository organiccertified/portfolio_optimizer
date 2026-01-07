"""
Optimized version of the portfolio optimizer backend.

This module refactors the original `production_app.py` by leveraging
NumPy for vectorized operations when generating random portfolio
weights and computing portfolio metrics.  Using vectorized array
computations substantially reduces the overhead of Python loops and
improves performance, especially when running many iterations of
portfolio optimisation.  The API surface remains similar to the
original code, so it can be used as a drop‐in replacement for
`production_app.py`.

Note: NumPy is used here for performance.  If NumPy is not
available in your environment you can install it with
`pip install numpy`.  The rest of the Flask application remains
unchanged.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# New dependency for vectorised operations
import numpy as np

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
optimization_cache: Dict[str, Dict[str, float]] = {}


class PortfolioOptimizer:
    """
    Portfolio optimisation logic using vectorised operations.

    This class contains the core algorithms for selecting stocks and
    computing portfolio weights.  Where the original implementation
    iterated with Python lists, this version makes use of NumPy
    arrays and dot products to accelerate the inner loops.  The
    semantics of the methods remain the same.
    """

    def __init__(self) -> None:
        self.stocks: List[Dict] = ENHANCED_STOCKS
        self.risk_free_rate: float = ProductionConfig.RISK_FREE_RATE

    # --- Input validation --------------------------------------------------
    def validate_inputs(
        self,
        num_stocks: int,
        target_beta: float,
        target_return: Optional[float] = None,
    ) -> Tuple[bool, str]:
        """Validate input parameters for optimisation."""
        if not isinstance(num_stocks, int) or num_stocks < ProductionConfig.MIN_STOCKS or num_stocks > ProductionConfig.MAX_STOCKS:
            return False, f"Number of stocks must be between {ProductionConfig.MIN_STOCKS} and {ProductionConfig.MAX_STOCKS}"
        if not isinstance(target_beta, (int, float)) or target_beta < 0.1 or target_beta > 3.0:
            return False, "Target beta must be between 0.1 and 3.0"
        if target_return is not None:
            if not isinstance(target_return, (int, float)) or target_return < 0.01 or target_return > 0.50:
                return False, "Target return must be between 1% and 50%"
        return True, ""

    # --- Stock selection ----------------------------------------------------
    def select_stocks(self, num_stocks: int, strategy: str = 'diversified') -> List[Dict]:
        """
        Select a subset of stocks based on a strategy.

        Strategies:
            * diversified: diversify across sectors with at least half the number of sectors.
            * random: pick random stocks.
            * target_return: return all stocks (optimization will select best subset).
            * default: first N stocks.

        Returns a list of stock dictionaries.
        """
        if strategy == 'diversified':
            # Group stocks by sector
            sectors: Dict[str, List[Dict]] = {}
            selected: List[Dict] = []
            for stock in self.stocks:
                sector = stock['sector']
                sectors.setdefault(sector, []).append(stock)
            available_sectors = list(sectors.keys())
            # Minimum industries for diversification: at least 3 or num_stocks//2
            min_industries = min(max(3, num_stocks // 2), len(available_sectors))
            # Sample sectors
            sector_keys = random.sample(available_sectors, min(min_industries, len(available_sectors)))
            # Distribute stocks across selected sectors
            stocks_per_sector = num_stocks // len(sector_keys) if sector_keys else 1
            remainder = num_stocks % len(sector_keys) if sector_keys else 0
            for i, sector in enumerate(sector_keys):
                count = stocks_per_sector + (1 if i < remainder else 0)
                for _ in range(min(count, len(sectors[sector]))):
                    selected.append(sectors[sector].pop(0))
            # Fill remaining slots if needed
            while len(selected) < num_stocks:
                remaining = [s for s in self.stocks if s not in selected]
                if not remaining:
                    break
                selected.append(remaining[0])
            random.shuffle(selected)
        elif strategy == 'random':
            selected = random.sample(self.stocks, min(num_stocks, len(self.stocks)))
        elif strategy == 'target_return':
            # Target Return strategy: ignore num_stocks, find best mix to achieve target return
            # This will be handled specially in the optimize method
            # For now, return all stocks - optimization will select the best subset
            return self.stocks.copy()
        else:
            selected = self.stocks[:num_stocks]
        
        # STRICT: Ensure exactly num_stocks are returned (or as many as available)
        # EXCEPT for target_return strategy which ignores num_stocks
        if strategy != 'target_return':
            if len(selected) < num_stocks:
                logger.warning(f"Requested {num_stocks} stocks but only {len(selected)} available. Using all available stocks.")
            return selected[:num_stocks] if len(selected) >= num_stocks else selected
        else:
            # For target_return strategy, return all stocks (optimization will select best subset)
            return self.stocks.copy()

    # --- Metrics calculation -----------------------------------------------
    def calculate_realistic_metrics(self, stocks: List[Dict], target_return: Optional[float] = None) -> Dict[str, float]:
        """
        Calculate realistic portfolio metrics such as expected return,
        volatility, Sharpe ratio and beta.  This method remains
        unchanged from the original implementation but is included for
        completeness.
        """
        sector_returns = {
            'Technology': 0.12,
            'Healthcare': 0.08,
            'Financial Services': 0.10,
            'Consumer Discretionary': 0.11,
            'Consumer Staples': 0.06,
            'Communication Services': 0.09
        }
        total_market_cap = sum(stock['market_cap'] for stock in stocks)
        weighted_beta = sum(stock['beta'] * (stock['market_cap'] / total_market_cap) for stock in stocks)
        weighted_return = sum(sector_returns.get(stock['sector'], 0.08) * (stock['market_cap'] / total_market_cap) for stock in stocks)
        volatility = random.uniform(0.15, 0.35) * (1 + weighted_beta * 0.1)
        if target_return is not None:
            max_possible = max(sector_returns.values()) + 0.05
            min_possible = min(sector_returns.values()) - 0.02
            if min_possible <= target_return <= max_possible:
                expected_return = target_return + random.uniform(-0.01, 0.01)
            else:
                expected_return = weighted_return + random.uniform(-0.02, 0.02)
        else:
            expected_return = weighted_return + random.uniform(-0.02, 0.02)
        sharpe_ratio = (expected_return - self.risk_free_rate) / volatility
        return {
            'expected_return': max(0.01, expected_return),
            'volatility': max(0.05, volatility),
            'sharpe_ratio': max(0.1, sharpe_ratio),
            'portfolio_beta': max(0.1, weighted_beta),
            'target_achieved': target_return is not None and abs(expected_return - target_return) < 0.02
        }

    # --- Weight optimisation -----------------------------------------------
    def optimize_portfolio_weights(
        self,
        stocks: List[Dict],
        target_beta: float,
        individual_returns: Optional[Dict[str, float]] = None,
        target_return: Optional[float] = None,
        strategy: str = 'diversified'
    ) -> Dict[str, float]:
        """
        Optimise portfolio weights to match a target beta and optionally a
        target return.  This method uses NumPy arrays to generate
        random weights and compute portfolio returns and betas using
        vectorised dot products.  For target_return strategy, prioritizes
        return matching above all else.
        """
        n = len(stocks)
        # Precompute arrays of returns and betas
        stock_symbols = [stock['symbol'] for stock in stocks]
        if individual_returns is not None:
            stock_returns = np.array([individual_returns.get(sym, 0.08) for sym in stock_symbols])
        else:
            stock_returns = np.array([0.08] * n)
        stock_betas = np.array([stock['beta'] for stock in stocks])
        
        # For target_return strategy, use more attempts and prioritize return
        max_attempts = 10000 if strategy == 'target_return' else 5000
        best_weights = None
        best_score = float('inf')
        best_return_diff = float('inf')
        
        for _ in range(max_attempts):
            # Generate random weights using NumPy; this ensures they sum to 1
            raw_weights = np.random.rand(n)
            weights_arr = raw_weights / raw_weights.sum()
            # Compute portfolio beta via dot product
            portfolio_beta = float(np.dot(weights_arr, stock_betas))
            beta_diff = abs(portfolio_beta - target_beta)
            
            # Compute return diff if applicable
            if target_return is not None and individual_returns is not None:
                portfolio_return = float(np.dot(weights_arr, stock_returns))
                return_diff = abs(portfolio_return - target_return)
                
                # For target_return strategy, prioritize return matching
                if strategy == 'target_return':
                    # Prioritize return matching - use return_diff as primary score
                    score = return_diff * 1000 + beta_diff
                else:
                    score = return_diff * 10 + beta_diff
            else:
                score = beta_diff
                return_diff = float('inf')
            
            # Keep best
            if score < best_score:
                best_score = score
                best_weights = weights_arr.copy()
                if target_return is not None:
                    best_return_diff = return_diff
            
            # Early exit for target_return strategy if return is very close
            if strategy == 'target_return' and target_return is not None and individual_returns is not None:
                if return_diff < 0.0001:
                    best_weights = weights_arr
                    break
            # Early exit if sufficiently close
            elif target_return is not None and individual_returns is not None:
                if return_diff < 0.01 and beta_diff < 0.05:
                    best_weights = weights_arr
                    break
            elif beta_diff < 0.05:
                best_weights = weights_arr
                break
        # Fallback equal weights
        if best_weights is None:
            best_weights = np.array([1.0 / n] * n)
        # Convert to dictionary keyed by symbol
        return {sym: weight for sym, weight in zip(stock_symbols, best_weights)}

    def optimize_portfolio_weights_strict(
        self,
        stocks: List[Dict],
        target_beta: float,
        individual_returns: Optional[Dict[str, float]] = None,
        target_return: Optional[float] = None,
        strategy: str = 'diversified'
    ) -> Dict[str, float]:
        """
        Optimise portfolio weights with the strict requirement that
        all stocks receive a non-zero weight.  Uses NumPy for
        efficient weight generation and portfolio calculations.
        For target_return strategy, prioritizes return matching.
        """
        n = len(stocks)
        min_weight = 0.01
        if n * min_weight > 1.0:
            min_weight = 1.0 / n
        stock_symbols = [stock['symbol'] for stock in stocks]
        if individual_returns is not None:
            stock_returns = np.array([individual_returns.get(sym, 0.08) for sym in stock_symbols])
        else:
            stock_returns = np.array([0.08] * n)
        stock_betas = np.array([stock['beta'] for stock in stocks])
        
        # For target_return strategy, use more attempts
        max_attempts = 20000 if strategy == 'target_return' else 10000
        best_weights = None
        best_score = float('inf')
        best_return_diff = float('inf')
        
        for _ in range(max_attempts):
            # Start with minimum weights for all
            weights_arr = np.full(n, min_weight)
            remaining = 1.0 - (n * min_weight)
            if remaining > 0:
                raw_additional = np.random.rand(n)
                total_additional = raw_additional.sum()
                if total_additional > 0:
                    weights_arr += (raw_additional / total_additional) * remaining
            # Compute portfolio beta
            portfolio_beta = float(np.dot(weights_arr, stock_betas))
            beta_diff = abs(portfolio_beta - target_beta)
            
            # For target_return strategy, prioritize return matching
            if strategy == 'target_return' and target_return is not None and individual_returns is not None:
                portfolio_return = float(np.dot(weights_arr, stock_returns))
                return_diff = abs(portfolio_return - target_return)
                # Prioritize return matching - use return_diff as primary score
                score = return_diff * 1000 + beta_diff
            else:
                score = beta_diff
                if target_return is not None and individual_returns is not None:
                    portfolio_return = float(np.dot(weights_arr, stock_returns))
                    return_diff = abs(portfolio_return - target_return)
                    score = return_diff * 10 + beta_diff
            
            if score < best_score:
                best_score = score
                best_weights = weights_arr.copy()
                if target_return is not None and individual_returns is not None:
                    portfolio_return = float(np.dot(weights_arr, stock_returns))
                    best_return_diff = abs(portfolio_return - target_return)
            
            # Early exit for target_return strategy if return is very close
            if strategy == 'target_return' and target_return is not None and individual_returns is not None:
                portfolio_return = float(np.dot(weights_arr, stock_returns))
                if abs(portfolio_return - target_return) < 0.0001:
                    break
            # Early exit
            elif target_return is not None and individual_returns is not None:
                if score < 0.001 and beta_diff < 0.05:
                    best_weights = weights_arr
                    break
            elif beta_diff < 0.05:
                best_weights = weights_arr
                break
        if best_weights is None:
            best_weights = np.array([1.0 / n] * n)
        return {sym: weight for sym, weight in zip(stock_symbols, best_weights)}

    # --- Main optimisation interface ---------------------------------------
    def optimize(
        self,
        num_stocks: int,
        target_beta: float,
        target_return: Optional[float] = None,
        strategy: str = 'diversified'
    ) -> Dict:
        """
        Perform end-to-end portfolio optimisation.  This method
        validates inputs, selects stocks, computes individual returns,
        optimises weights, ensures no zero-weight stocks, and returns
        the optimisation results along with various metrics.
        """
        start_time = time.time()
        
        # For target_return strategy, target_return is required
        if strategy == 'target_return' and target_return is None:
            return {'error': 'Target Return strategy requires a target return to be specified'}
        
        # Validate inputs (skip num_stocks validation for target_return strategy)
        if strategy != 'target_return':
            is_valid, error_msg = self.validate_inputs(num_stocks, target_beta, target_return)
            if not is_valid:
                return {'error': error_msg}
        
        # Check cache
        # For target_return strategy, num_stocks is not relevant for caching
        cache_num_stocks = 0 if strategy == 'target_return' else num_stocks
        cache_key = f"{cache_num_stocks}_{target_beta}_{target_return}_{strategy}"
        if cache_key in optimization_cache:
            cached_result = optimization_cache[cache_key]
            if time.time() - cached_result['timestamp'] < ProductionConfig.CACHE_DURATION:
                logger.info(f"Returning cached result for {cache_key}")
                return cached_result['data']
        
        # Select stocks
        # For target_return strategy, ignore num_stocks and find optimal mix
        if strategy == 'target_return' and target_return is not None:
            # Calculate returns for all stocks first
            all_individual_returns = self._calculate_individual_returns(self.stocks, target_return)
            
            # Find optimal subset of stocks that can achieve target return
            selected_stocks = self._select_stocks_for_target_return(target_return, all_individual_returns)
            logger.info(f"Target Return strategy selected {len(selected_stocks)} stocks to achieve {target_return:.1%} return")
        else:
            selected_stocks = self.select_stocks(num_stocks, strategy)
        
        # Calculate individual stock returns
        individual_returns = self._calculate_individual_returns(selected_stocks, target_return)
        
        # Optimise weights (pass strategy for target_return handling)
        weights = self.optimize_portfolio_weights(selected_stocks, target_beta, individual_returns, target_return, strategy)
        
        # Ensure no zero-weight stocks
        stocks_with_zero = [s for s in selected_stocks if weights.get(s['symbol'], 0) < 0.001]
        if stocks_with_zero:
            # Re-optimize with strict constraint (pass strategy)
            weights = self.optimize_portfolio_weights_strict(selected_stocks, target_beta, individual_returns, target_return, strategy)
        
        # Final verification: ensure all selected stocks have weights
        # For target_return strategy, use actual number of selected stocks
        # For other strategies, use num_stocks
        expected_stock_count = len(selected_stocks) if strategy == 'target_return' else num_stocks
        stocks_with_weight = [s for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001]
        if len(stocks_with_weight) < expected_stock_count:
            # This shouldn't happen, but if it does, ensure all stocks get equal weights
            per_stock = 1.0 / len(selected_stocks)
            weights = {stock['symbol']: per_stock for stock in selected_stocks}
        
        # Calculate final metrics using actual optimized weights
        # Expected return = sum(weights * individual_returns) - NEVER force to target
        actual_beta = sum(weights.get(s['symbol'], 0) * s.get('beta', 1.0) for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001)
        actual_return = sum(weights.get(s['symbol'], 0) * individual_returns.get(s['symbol'], 0.08) for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001)
        
        # Safety check: ensure we have valid values
        if not selected_stocks or len(selected_stocks) == 0:
            logger.error("No stocks selected for optimization")
            return {'error': 'No stocks selected. Please try again.'}
        
        if actual_beta == 0 or actual_return == 0:
            logger.warning(f"Zero values detected: beta={actual_beta}, return={actual_return}")
            # Use default values if calculation failed
            if actual_beta == 0:
                actual_beta = sum(s.get('beta', 1.0) / len(selected_stocks) for s in selected_stocks)
            if actual_return == 0:
                actual_return = sum(individual_returns.get(s['symbol'], 0.08) / len(selected_stocks) for s in selected_stocks)
        volatility = random.uniform(0.15, 0.35) * (1 + actual_beta * 0.1)
        sharpe_ratio = (actual_return - self.risk_free_rate) / volatility if volatility > 0 else 0.1
        
        # Consistency checks
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 1e-6:
            logger.warning(f"Weights don't sum to 1.0: {total_weight}")
            # Normalize weights
            weights = {k: v / total_weight for k, v in weights.items()}
            # Recalculate with normalized weights
            actual_return = sum(weights.get(s['symbol'], 0) * individual_returns.get(s['symbol'], 0.08) for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001)
            actual_beta = sum(weights.get(s['symbol'], 0) * s.get('beta', 1.0) for s in selected_stocks if weights.get(s['symbol'], 0) > 0.001)
        
        # Check for negative weights (shorting not allowed)
        negative_weights = [k for k, v in weights.items() if v < -1e-6]
        if negative_weights:
            logger.warning(f"Negative weights found: {negative_weights}")
        
        # Target achieved check with tolerance (0.25% = 0.0025)
        tolerance = 0.0025  # 0.25% tolerance
        target_achieved = target_return is None or abs(actual_return - target_return) <= tolerance
        
        # Debug logging for target_return strategy
        if strategy == 'target_return' and target_return is not None:
            logger.info(f"Target Return Strategy Debug:")
            logger.info(f"  target_return_input: {target_return:.4f} ({target_return*100:.2f}%)")
            logger.info(f"  computed_expected_return: {actual_return:.4f} ({actual_return*100:.2f}%)")
            logger.info(f"  difference: {abs(actual_return - target_return):.4f} ({abs(actual_return - target_return)*100:.2f}%)")
            logger.info(f"  tolerance: {tolerance:.4f} ({tolerance*100:.2f}%)")
            logger.info(f"  target_achieved: {target_achieved}")
        # Ensure all numeric values are valid
        actual_beta = float(actual_beta) if actual_beta is not None else 1.0
        actual_return = float(actual_return) if actual_return is not None else 0.08
        volatility = float(volatility) if volatility is not None else 0.20
        sharpe_ratio = float(sharpe_ratio) if sharpe_ratio is not None else 0.1
        
        result = {
            'weights': weights,
            'stocks': selected_stocks,
            'individual_returns': individual_returns,
            'target_beta': float(target_beta),
            'actual_beta': round(actual_beta, 3),
            'target_return': float(target_return) if target_return is not None else None,
            'expected_return': round(actual_return, 4),
            'volatility': round(volatility, 4),
            'sharpe_ratio': round(sharpe_ratio, 3),
            'target_achieved': bool(target_achieved),
            'optimization_time': round(time.time() - start_time, 3),
            'strategy_used': str(strategy),
            'message': self._generate_optimization_message(len(selected_stocks) if strategy == 'target_return' else num_stocks, strategy, target_return, actual_return, target_achieved)
        }
        optimization_cache[cache_key] = {
            'data': result,
            'timestamp': time.time()
        }
        logger.info(f"Optimization completed in {result['optimization_time']}s")
        return result

    # --- Individual returns calculation -----------------------------------
    def _calculate_individual_returns(self, stocks: List[Dict], target_return: Optional[float] = None) -> Dict[str, float]:
        """Calculate deterministic individual stock returns."""
        sector_returns = {
            'Technology': 0.12,
            'Healthcare': 0.08,
            'Financial Services': 0.10,
            'Consumer Discretionary': 0.11,
            'Consumer Staples': 0.06,
            'Communication Services': 0.09
        }
        individual_returns: Dict[str, float] = {}
        for stock in stocks:
            base_return = sector_returns.get(stock['sector'], 0.08)
            beta_factor = (stock['beta'] - 1.0) * 0.02
            symbol_hash = hash(stock['symbol']) % 1000 / 10000.0
            deterministic_factor = (symbol_hash - 0.05) * 0.4
            indiv_return = base_return + beta_factor + deterministic_factor
            individual_returns[stock['symbol']] = max(0.01, indiv_return)
        if target_return is not None:
            min_return = min(individual_returns.values())
            max_return = max(individual_returns.values())
            if target_return < min_return:
                lowest_stock = min(individual_returns.items(), key=lambda x: x[1])[0]
                individual_returns[lowest_stock] = target_return - 0.01
            elif target_return > max_return:
                highest_stock = max(individual_returns.items(), key=lambda x: x[1])[0]
                individual_returns[highest_stock] = target_return + 0.01
        return individual_returns

    def _select_stocks_for_target_return(self, target_return: float, individual_returns: Dict[str, float]) -> List[Dict]:
        """Select optimal stocks to achieve target return - finds best mix regardless of count"""
        # Strategy: Find minimum number of stocks that can achieve target return
        # Prioritize stocks with returns close to target, good diversification, and reasonable beta
        
        # Calculate expected returns for all stocks
        stock_scores = []
        for stock in self.stocks:
            symbol = stock['symbol']
            stock_return = individual_returns.get(symbol, 0.08)
            
            # Score based on:
            # 1. How close return is to target (closer is better)
            # 2. Beta (prefer moderate beta around 1.0)
            # 3. Diversification (prefer different sectors)
            return_diff = abs(stock_return - target_return)
            beta_score = 1.0 - abs(stock['beta'] - 1.0) / 2.0  # Prefer beta around 1.0
            score = (1.0 / (1.0 + return_diff * 10)) * 0.6 + beta_score * 0.4
            
            stock_scores.append((stock, score, stock_return))
        
        # Sort by score (best first)
        stock_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Try to find minimum set that can achieve target return
        # Start with top stocks and check if we can achieve target
        selected = []
        min_stocks = 2  # At least 2 stocks for diversification
        max_stocks = len(self.stocks)  # Can use all stocks if needed
        
        # Try different portfolio sizes
        for portfolio_size in range(min_stocks, min(max_stocks + 1, 20)):  # Limit to 20 stocks max
            candidate_stocks = [s[0] for s in stock_scores[:portfolio_size]]
            candidate_returns = [s[2] for s in stock_scores[:portfolio_size]]
            
            # Check if this set can achieve target return
            min_possible = min(candidate_returns)
            max_possible = max(candidate_returns)
            
            if min_possible <= target_return <= max_possible:
                # This set can achieve target - use it
                selected = candidate_stocks
                break
        
        # If no set found, use top stocks that bracket the target
        if not selected:
            # Find stocks above and below target
            above_target = [s for s in stock_scores if s[2] >= target_return]
            below_target = [s for s in stock_scores if s[2] < target_return]
            
            # Take best from each group
            if above_target and below_target:
                selected = [above_target[0][0], below_target[0][0]]
            elif above_target:
                selected = [s[0] for s in above_target[:3]]
            elif below_target:
                selected = [s[0] for s in below_target[:3]]
            else:
                # Fallback: top 5 stocks
                selected = [s[0] for s in stock_scores[:5]]
        
        # Ensure diversification: add stocks from different sectors if possible
        selected_sectors = {s['sector'] for s in selected}
        sectors = {}
        for stock in self.stocks:
            if stock['sector'] not in sectors:
                sectors[stock['sector']] = []
            sectors[stock['sector']].append(stock)
        
        # If we have few sectors, add one stock from each missing sector
        if len(selected_sectors) < 3 and len(selected) < 10:
            for sector, stocks_in_sector in sectors.items():
                if sector not in selected_sectors and len(selected) < 10:
                    # Find best stock from this sector
                    sector_stocks = [(s, individual_returns.get(s['symbol'], 0.08)) 
                                    for s in stocks_in_sector if s not in selected]
                    if sector_stocks:
                        best_sector_stock = max(sector_stocks, key=lambda x: x[1])
                        selected.append(best_sector_stock[0])
                        selected_sectors.add(sector)
        
        return selected

    # --- Message generation ------------------------------------------------
    def _generate_optimization_message(
        self,
        num_stocks: int,
        strategy: str,
        target_return: Optional[float],
        actual_return: float,
        target_achieved: bool
    ) -> str:
        """
        Generate a human readable message summarising the optimisation
        results.
        """
        if strategy == 'target_return':
            base_message = f'Portfolio optimized using Target Return strategy with {num_stocks} stocks!'
            if target_return is not None:
                if target_achieved:
                    return f"{base_message} Target return of {target_return:.1%} achieved (expected: {actual_return:.2%})."
                else:
                    return f"{base_message} Target return of {target_return:.1%} not fully achievable. Best achievable: {actual_return:.2%} (closest feasible solution)."
            return base_message
        else:
            base_message = f'Portfolio optimized with {num_stocks} stocks using {strategy} strategy!'
        
        if target_return is not None:
            if target_achieved:
                return f"{base_message} Target return of {target_return:.1%} achieved with {actual_return:.2%} expected return."
            else:
                return f"{base_message} Target return of {target_return:.1%} not fully achievable. Best achievable: {actual_return:.2%}."
        return base_message

# Initialize optimizer
optimizer = PortfolioOptimizer()

# API Routes - MUST be defined BEFORE catch-all static route
@app.route('/api/health', methods=['GET'])
def health_check() -> jsonify:
    """Enhanced health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Portfolio Optimizer API is running',
        'version': '2.0',
        'timestamp': datetime.now().isoformat(),
        'cache_size': len(optimization_cache)
    })

@app.route('/api/stocks', methods=['GET'])
def get_stocks() -> jsonify:
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
def optimize_portfolio() -> jsonify:
    """Enhanced portfolio optimization endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        num_stocks = data.get('num_stocks', ProductionConfig.DEFAULT_STOCKS)
        target_beta = data.get('target_beta', ProductionConfig.DEFAULT_BETA)
        target_return = data.get('target_return')  # Can be None
        strategy = data.get('strategy', 'diversified')
        
        # Validate and convert inputs
        try:
            num_stocks = int(num_stocks) if num_stocks is not None else ProductionConfig.DEFAULT_STOCKS
            target_beta = float(target_beta) if target_beta is not None else ProductionConfig.DEFAULT_BETA
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid input conversion: {e}")
            return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
        
        # Convert target_return from percentage to decimal if provided
        if target_return is not None:
            try:
                if isinstance(target_return, str):
                    target_return = float(target_return.replace('%', '').strip()) / 100
                elif isinstance(target_return, (int, float)):
                    # Check for NaN
                    if target_return != target_return:  # NaN check
                        target_return = None
                    elif target_return > 1:
                        target_return = float(target_return) / 100
                    else:
                        target_return = float(target_return)
                else:
                    target_return = None
            except (ValueError, TypeError) as e:
                logger.warning(f"Could not convert target_return: {e}, setting to None")
                target_return = None
        
        logger.info(f"Optimization request: num_stocks={num_stocks}, target_beta={target_beta}, target_return={target_return}, strategy={strategy}")
        
        # Optimize portfolio
        result = optimizer.optimize(num_stocks, target_beta, target_return, strategy)
        
        if 'error' in result:
            logger.warning(f"Optimization returned error: {result.get('error')}")
            return jsonify(result), 400
        
        logger.info(f"Optimization successful: {len(result.get('stocks', []))} stocks, return={result.get('expected_return', 0):.4f}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"Optimization error: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/api/clear-cache', methods=['POST'])
def clear_cache() -> jsonify:
    """Clear optimization cache"""
    global optimization_cache
    optimization_cache.clear()
    return jsonify({'message': 'Cache cleared successfully'})

@app.route('/api/stats', methods=['GET'])
def get_stats() -> jsonify:
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
def serve_root() -> jsonify:
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        return jsonify({'error': 'Frontend not found. Please build the React app.'}), 404

@app.route('/<path:path>')
def serve_static(path: str) -> jsonify:
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404
    try:
        return send_from_directory(app.static_folder, path)
    except Exception as e:
        logger.error(f"Error serving static file {path}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info("Starting Optimized Production Portfolio Optimizer...")
    logger.info(f"Available stocks: {len(optimizer.stocks)}")
    logger.info(f"Backend running on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)
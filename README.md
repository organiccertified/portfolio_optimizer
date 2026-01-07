# Portfolio Optimizer

A React-based web application that helps users optimize their stock portfolio by finding the optimal combination of stocks that maximizes returns while respecting a target beta risk level.

## Features

- **Dynamic Stock Management**: Add or remove stocks from your portfolio
- **Beta Risk Control**: Set your desired beta risk level (0.1 by default)
- **S&P 500 Integration**: Automatically fetches the latest S&P 500 stock list
- **Historical Data Analysis**: Uses 3 years of historical data for optimization
- **Portfolio Optimization**: Finds optimal weights for maximum Sharpe ratio
- **Real-time Results**: Displays portfolio weights, expected returns, volatility, and Sharpe ratio

## Technology Stack

### Frontend
- React 18
- Modern CSS with responsive design
- Chart.js for data visualization

### Backend
- Python Flask
- Pandas for data manipulation
- NumPy for numerical computations
- yfinance for stock data
- scikit-learn for beta calculations
- scipy for portfolio optimization

## Installation

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start (Recommended)

**Windows:**
```bash
# Double-click or run:
start_optimized.bat
```

**Mac/Linux:**
```bash
chmod +x start_optimized.sh
./start_optimized.sh
```

This will automatically:
1. Install Python dependencies
2. Start the backend server on http://localhost:5000
3. Start the frontend server on http://localhost:3000
4. Open the app in your browser

### Manual Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd portfolioOptimizer
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r optimized_requirements.txt
   cd ..
   ```

4. **Start the Backend Server** (Terminal 1)
   ```bash
   cd backend
   python optimized_app.py
   ```
   The backend will start on http://localhost:5000
   You should see: `Running on http://0.0.0.0:5000`

5. **Start the Frontend Development Server** (Terminal 2)
   ```bash
   npm start
   ```
   The frontend will start on http://localhost:3000
   Your browser should automatically open to http://localhost:3000

6. **Alternative: Run Both Simultaneously** (Single Terminal)
   ```bash
   npm run dev
   ```
   Note: This uses the old `backend/app.py`. For the optimized version, use the manual setup above.

## Usage

1. **Add Stocks**: Click "Add another stock" to add more stocks to your portfolio
2. **Enter Stock Symbols**: Type stock symbols (e.g., NVDA, AAPL, MSFT)
3. **Set Beta Risk**: Adjust the beta risk level (default: 0.1)
4. **Optimize**: Click "Optimize Portfolio" to find the optimal weights
5. **View Results**: See the optimal portfolio weights and performance metrics

## API Endpoints

- `GET /api/stocks` - Get list of S&P 500 stocks
- `POST /api/optimize` - Optimize portfolio with given stocks and beta
- `GET /api/health` - Health check endpoint

## Portfolio Optimization Algorithm

The application uses the following approach:

1. **Data Collection**: Fetches 3 years of historical data for selected stocks and SPY
2. **Beta Calculation**: Calculates individual stock betas relative to the market
3. **Optimization**: Uses scipy's SLSQP optimizer to maximize Sharpe ratio
4. **Constraints**: Ensures portfolio beta matches target and weights sum to 1
5. **Results**: Returns optimal weights and portfolio metrics

## Features in Detail

### Stock Management
- Dynamic addition/removal of stocks
- Input validation for stock symbols
- Automatic uppercase conversion

### Beta Risk Control
- Float input validation
- Real-time beta constraint enforcement
- Portfolio optimization respecting target beta

### Data Sources
- **S&P 500 List**: Dynamically scraped from Wikipedia
- **Stock Data**: Real-time data from Yahoo Finance via yfinance
- **Market Data**: SPY ETF data for market comparison

## Error Handling

- Graceful fallback to predefined S&P 500 list if web scraping fails
- Comprehensive error messages for optimization failures
- Input validation for all user inputs
- Network error handling for API calls

## Performance Considerations

- Efficient data fetching with yfinance
- Optimized portfolio calculations using NumPy
- Responsive UI with modern React patterns
- Caching of S&P 500 stock list

## Deployment

### Hostinger Deployment

**Quick Start:**
```bash
# Windows
deploy_hostinger.bat

# Linux/Mac
chmod +x deploy_hostinger.sh
./deploy_hostinger.sh
```

This creates a `production` folder with all files ready for Hostinger. Upload contents to `public_html`.

**Detailed Instructions:**
- Quick guide: See `HOSTINGER_QUICK_START.md`
- Full guide: See `HOSTINGER_DEPLOYMENT.md`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Disclaimer

This application is for educational and informational purposes only. It does not constitute financial advice. Always consult with a qualified financial advisor before making investment decisions. Past performance does not guarantee future results.

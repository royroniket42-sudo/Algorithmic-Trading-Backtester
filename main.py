from core.data import DataFeed
from core.strategy import MovingAverageCrossover
from core.portfolio import Portfolio
import pandas as pd

def run_backtest():
    # 1. Initialization
    ticker = "AAPL"
    print("--- Starting Backtest Engine ---")
    data_feed = DataFeed(ticker, "2020-01-01", "2023-01-01")
    market_data = data_feed.fetch_data()
    
    portfolio = Portfolio(initial_capital=10000.0, transaction_cost=0.001) # 0.1% fee
    strategy = MovingAverageCrossover(short_window=20, long_window=50)

    # 2. Event-Driven Loop
    print("Executing strategy...")
    for date, row in market_data.iterrows():
        current_price = float(row['Close'].iloc[0]) if isinstance(row['Close'], pd.Series) else float(row['Close'])
        
        # Generate signal
        signal = strategy.generate_signal(current_price)
        
        # Execute Trade
        portfolio.execute_trade(signal, current_price, date)
        
        # Mark to market (Update daily equity)
        portfolio.update_equity(current_price, date)

    # 3. Analytics & Output
    print("\n--- Backtest Results ---")
    results = portfolio.get_performance_summary()
    for metric, value in results.items():
        print(f"{metric}: {value}")

if __name__ == "__main__":
    run_backtest()
import pandas as pd
from core.metrics import calculate_sharpe_ratio, calculate_max_drawdown

class Portfolio:
    def __init__(self, initial_capital=10000.0, transaction_cost=0.001):
        self.initial_capital = initial_capital
        self.current_cash = initial_capital
        self.holdings = 0
        self.transaction_cost = transaction_cost
        self.equity_curve = []

    def execute_trade(self, signal, price, date):
        # signal: 1 (Buy), -1 (Sell), 0 (Hold)
        if signal == 1 and self.current_cash >= price:
            # Buy maximum whole shares possible
            shares_to_buy = int(self.current_cash // (price * (1 + self.transaction_cost)))
            if shares_to_buy > 0:
                cost = (shares_to_buy * price) * (1 + self.transaction_cost)
                self.current_cash -= cost
                self.holdings += shares_to_buy
                
        elif signal == -1 and self.holdings > 0:
            # Sell all holdings
            revenue = (self.holdings * price) * (1 - self.transaction_cost)
            self.current_cash += revenue
            self.holdings = 0

    def update_equity(self, price, date):
        total_value = self.current_cash + (self.holdings * price)
        self.equity_curve.append({'Date': date, 'Equity': total_value})

    def get_performance_summary(self):
        df = pd.DataFrame(self.equity_curve).set_index('Date')
        df['Returns'] = df['Equity'].pct_change().dropna()
        
        total_return = (df['Equity'].iloc[-1] - self.initial_capital) / self.initial_capital
        sharpe = calculate_sharpe_ratio(df['Returns'])
        mdd = calculate_max_drawdown(df['Equity'])

        return {
            "Initial Capital": f"${self.initial_capital:,.2f}",
            "Final Equity": f"${df['Equity'].iloc[-1]:,.2f}",
            "Total Return": f"{total_return * 100:.2f}%",
            "Sharpe Ratio": f"{sharpe:.2f}",
            "Max Drawdown": f"{mdd * 100:.2f}%"
        }
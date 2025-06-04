import tkinter as tk
from tkinter import messagebox
import pandas as pd
try:
    import MetaTrader5 as mt5
except ModuleNotFoundError:  # pragma: no cover - only occurs without package
    mt5 = None

try:
    from .main import apply_strategy
except ImportError:  # allow running as a script
    import os
    import sys
    sys.path.append(os.path.dirname(__file__))
    from main import apply_strategy

class TradingGUI:
    def __init__(self, master):
        self.master = master
        master.title("NewTrain AI Bot")

        tk.Label(master, text="Login").grid(row=0, column=0)
        tk.Label(master, text="Password").grid(row=1, column=0)
        tk.Label(master, text="Server").grid(row=2, column=0)
        tk.Label(master, text="Symbol").grid(row=3, column=0)
        tk.Label(master, text="Lot Size").grid(row=4, column=0)

        self.login_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master, show='*')
        self.server_entry = tk.Entry(master)
        self.symbol_entry = tk.Entry(master)
        self.lot_entry = tk.Entry(master)

        self.login_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.server_entry.grid(row=2, column=1)
        self.symbol_entry.grid(row=3, column=1)
        self.lot_entry.grid(row=4, column=1)

        tk.Button(master, text="Connect", command=self.connect).grid(row=5, column=0)
        tk.Button(master, text="Start Trading", command=self.start_trading).grid(row=5, column=1)

    def connect(self):
        login = int(self.login_entry.get())
        password = self.password_entry.get()
        server = self.server_entry.get()
        if mt5 is None:
            messagebox.showerror(
                "Unavailable",
                "MetaTrader5 package is not installed."
            )
            return
        if not mt5.initialize(login=login, password=password, server=server):
            messagebox.showerror(
                "Error", f"initialize() failed: {mt5.last_error()}"
            )
            return
        messagebox.showinfo("Connected", "Connected to MT5")

    def fetch_data(self, symbol, bars=500):
        if mt5 is None:
            raise RuntimeError("MetaTrader5 package is not installed")
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, bars)
        if rates is None:
            raise RuntimeError("Failed to get rates")
        df = pd.DataFrame(rates)
        df['Date'] = pd.to_datetime(df['time'], unit='s')
        df.rename(columns={'close':'Close'}, inplace=True)
        return df[['Date', 'Close']]

    def start_trading(self):
        symbol = self.symbol_entry.get()
        lot = float(self.lot_entry.get())
        try:
            df = self.fetch_data(symbol)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        df_sig = apply_strategy(df)
        last_signal = df_sig['Signal'].iloc[-1]
        if last_signal == 1:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(symbol).ask,
                "deviation": 10,
                "magic": 234000,
                "comment": "NewTrain buy"}
        elif last_signal == -1:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(symbol).bid,
                "deviation": 10,
                "magic": 234000,
                "comment": "NewTrain sell"}
        else:
            messagebox.showinfo("No Signal", "No trade signal.")
            return
        if mt5 is None:
            messagebox.showerror(
                "Unavailable",
                "MetaTrader5 package is not installed."
            )
            return
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            messagebox.showerror("Trade Failed", f"retcode={result.retcode}")
        else:
            messagebox.showinfo("Trade Placed", f"Order successful: {result.order}")


def main():
    root = tk.Tk()
    app = TradingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

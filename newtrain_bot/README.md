# NewTrain AI Trading Bot

This project demonstrates a simple moving average crossover bot and provides a small GUI to connect to MetaTrader 5.

## Description
The bot loads market data either from a CSV file or directly from the MT5 platform and trades on the last signal generated from 1‑minute candles.

## Setup
1. Install Python 3.
2. Create a virtual environment (optional).
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. To run the example strategy on sample data:
   ```bash
   python main.py
   ```
5. To launch the GUI and connect to MT5:
   ```bash
   python -m newtrain_bot.gui
   ```

## Files
- `main.py` – core trading logic and simple moving average strategy.
- `gui.py` – Tkinter GUI that connects to MT5 and places trades based on the strategy.
- `data/sample_prices.csv` – example historical price data for offline testing.
- `requirements.txt` – Python dependencies.

This project is for demonstration purposes only. Use with caution when trading live accounts.

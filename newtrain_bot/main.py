import pandas as pd

# Parameters for moving averages
SHORT_WINDOW = 3
LONG_WINDOW = 5

def load_data(path: str) -> pd.DataFrame:
    """Load price data from a CSV file."""
    df = pd.read_csv(path, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)
    return df


def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """Apply moving average crossover strategy."""
    df = df.copy()
    df['SMA_short'] = df['Close'].rolling(window=SHORT_WINDOW).mean()
    df['SMA_long'] = df['Close'].rolling(window=LONG_WINDOW).mean()
    df['Signal'] = 0
    df.loc[df['SMA_short'] > df['SMA_long'], 'Signal'] = 1
    df.loc[df['SMA_short'] < df['SMA_long'], 'Signal'] = -1
    return df


def main():
    df = load_data('data/sample_prices.csv')
    df_with_signals = apply_strategy(df)
    print(df_with_signals[['Date', 'Close', 'SMA_short', 'SMA_long', 'Signal']])


if __name__ == '__main__':
    main()

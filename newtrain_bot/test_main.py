import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from main import apply_strategy

def test_apply_strategy():
    data = {
        'Date': pd.date_range(start='2021-01-01', periods=6, freq='D'),
        'Close': [1, 2, 3, 4, 5, 6],
    }
    df = pd.DataFrame(data)
    result = apply_strategy(df)
    assert 'Signal' in result.columns
    assert result['Signal'].iloc[-1] == 1


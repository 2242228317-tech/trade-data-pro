import baostock as bs
import pandas as pd

# Login
lg = bs.login()
print(f"Login result: {lg.error_msg}")

# Query data for 嘉美包装 (002969)
rs = bs.query_history_k_data_plus(
    '002969.sz',
    'date,code,open,high,low,close,volume',
    start_date='2024-01-01',
    end_date='2026-03-14',
    frequency='d'
)

print(f"Query result: {rs.error_msg}")

# Get data
data_list = []
while (rs.error_code == '0') and rs.next():
    data_list.append(rs.get_row_data())

print(f"Got {len(data_list)} records")

if len(data_list) > 0:
    df = pd.DataFrame(data_list, columns=['date', 'code', 'open', 'high', 'low', 'close', 'volume'])
    print("\nLatest 5 records:")
    print(df.tail())
else:
    print("No data retrieved")

# Logout
bs.logout()

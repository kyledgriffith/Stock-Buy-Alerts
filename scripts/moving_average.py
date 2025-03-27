# %%
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
file_path = "C:/Users/kyleg/OneDrive/Documents/Stocks Forecasting/TSLA.csv"
df = pd.read_csv(file_path)

# Rename the first column to 'Datetime'
df.rename(columns={df.columns[0]: 'Datetime'}, inplace=True)

# Ensure Datetime column is in datetime format and sorted
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values(by='Datetime')

# Define moving averages
short_window = 3
long_window = 10

df['short_ma'] = df['close'].rolling(window=short_window, min_periods=1).mean()
df['long_ma'] = df['close'].rolling(window=long_window, min_periods=1).mean()

# Identify points where short MA crosses above long MA
df['signal'] = (df['short_ma'] > df['long_ma']) & (df['short_ma'].shift(1) <= df['long_ma'].shift(1))

# Extract hour and minute to filter time
df['time'] = df['Datetime'].dt.time

# Define valid time range (9:35 AM to 3:50 PM)
start_time = pd.to_datetime("09:35:00").time()
end_time = pd.to_datetime("15:50:00").time()

# Apply time filter
df['valid_time'] = df['time'].between(start_time, end_time)

# Generate alerts only if the signal is true and within valid time
alerts = df[(df['signal']) & (df['valid_time'])]

# Display alerts
print("Alerts:")
print(alerts[['Datetime', 'close']])
# %%
# Plot
plt.figure(figsize=(12, 6))
plt.plot(df['Datetime'], df['close'], label='Stock Price', alpha=0.5)
plt.plot(df['Datetime'], df['short_ma'], label=f'Short MA ({short_window})', linestyle='dashed')
plt.plot(df['Datetime'], df['long_ma'], label=f'Long MA ({long_window})', linestyle='dotted')
plt.scatter(alerts['Datetime'], alerts['close'], color='red', label='Buy Signal', marker='^', alpha=1)
plt.legend()
plt.xlabel('Datetime')
plt.ylabel('Price')
plt.title('Stock Price with Moving Averages and Buy Signals')
plt.xticks(rotation=45)
plt.show()

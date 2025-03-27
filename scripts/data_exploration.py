# %%
import pandas as pd

# Define the correct column names (adjust as needed)
column_names = ["timestamp", "open", "high", "low", "close", "volume", "symbol"]

# Load the CSV file
file_path = "C:/Users/kyleg/OneDrive/Documents/Stocks Forecasting/TSLA.csv"  # Change this as needed
df = pd.read_csv(file_path, names=column_names, header=0)

# Display the first few rows
print(df.info())
print(df.head())
# %%
# Convert the timestamp column (update column name if needed)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Ensure numeric values are properly formatted
df = df.apply(pd.to_numeric, errors='ignore')

# Check for missing values
print(df.isnull().sum())

# %%
import matplotlib.pyplot as plt  

plt.figure(figsize=(10,5))
plt.plot(df['timestamp'], df['close'], label='Close Price', color='blue')  
plt.xlabel('Time')  
plt.ylabel('Stock Price')  
plt.title('Stock Price Trend')  
plt.legend()  
plt.show()

# %%

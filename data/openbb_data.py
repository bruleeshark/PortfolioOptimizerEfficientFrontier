# Create openbb_data.py file
# Use OpenBB Terminal API to collect real-time data on USDC, FTM, and WETH prices and market caps
# Store data in CSV file @ ./data/historical_data.csv

# uses the OpenBB Terminal API (available at https://api.openbase.com/v1/assets/historicalData)
# to retrieve historical data for user-specified assets.

# Note that this code assumes that you have already set up an OpenBB account and have an API key
# that you can use to access the OpenBB Terminal API. You will also need to replace the assets list 
# with a list of user-specified assets.

import csv
import time
import requests

# Define function to get historical data for an asset
def get_historical_data(asset):
    url = f"https://api.openbase.com/v1/assets/historicalData?asset={asset}&period=1y&interval=1d"
    response = requests.get(url)
    data = response.json()
    return data["data"]

# Define function to write data to CSV file
def write_data_to_csv(data):
    with open("historical_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

# Main function to retrieve historical data for multiple assets
def main():
    assets = ["USDC", "FTM", "WETH"]  # Replace with user-specified assets
    for asset in assets:
        data = get_historical_data(asset)
        write_data_to_csv(data)
        time.sleep(5)  # Wait 5 seconds between API requests

if __name__ == "__main__":
    main()

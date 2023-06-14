import os
from datetime import datetime
import requests
import csv
import configparser


class BinanceAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, symbol, interval):
        url = f"{self.base_url}/klines?symbol={symbol}&interval={interval}"
        response = requests.get(url)
        data = response.json()
        return data

    def get_market_caps(self, symbol):
        url = f"{self.base_url}/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        return data


class CSVWriter:
    def __init__(self, header):
        self.header = header

    def save_data(self, data, filename):
        parent_directory = os.path.dirname(os.getcwd())  # Get the parent directory
        filepath = os.path.join(parent_directory, filename)
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            for row in data:
                writer.writerow(
                    row[:6]
                )  # Save only the first 6 columns (ignore the rest)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("../config.ini")
    BASE_URL = config.get("Binance", "base_url")
    # Set the symbol and interval
    symbol = "BTCUSDT"
    interval = "1d"

    binance_api = BinanceAPI(BASE_URL)
    csv_writer = CSVWriter(
        ["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time"]
    )

    data = binance_api.get_data(symbol, interval)

    filename = f"{symbol}_{interval}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"
    csv_writer.save_data(data, filename)

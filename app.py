from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd
import configparser

from binance_data.binance import BinanceAPI

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")


class CandlestickDataProvider:
    def __init__(self, filename):
        self.filename = filename

    def get_candlestick_data(self):
        candlestick_data = pd.read_csv(self.filename)
        candlestick_data["Open Time"] = pd.to_datetime(
            candlestick_data["Open Time"], unit="ms"
        )
        return candlestick_data


class PieChartDataProvider:
    def __init__(self, symbols):
        self.symbols = symbols

    def get_market_caps(self):
        binance_data = BinanceAPI()
        market_caps = [
            binance_data.get_market_caps(symbol)["quoteVolume"]
            for symbol in self.symbols
        ]
        return market_caps


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/candlestick")
def candlestick():
    filename = config.get("Providers", "candlestick_data_file")
    provider = CandlestickDataProvider(filename)
    candlestick_data = provider.get_candlestick_data()

    fig = go.Figure(
        data=go.Candlestick(
            x=candlestick_data["Open Time"],
            open=candlestick_data["Open"],
            high=candlestick_data["High"],
            low=candlestick_data["Low"],
            close=candlestick_data["Close"],
        )
    )

    fig.update_layout(
        title="Candlestick Chart", xaxis_title="Date", yaxis_title="Price"
    )
    return fig.to_html(full_html=False)


@app.route("/market_caps")
def market_caps_chart():
    symbols = config.get("PieChart", "symbols").split(",")
    provider = PieChartDataProvider(symbols)
    market_caps = provider.get_market_caps()

    fig = go.Figure(data=go.Pie(labels=provider.symbols, values=market_caps, hole=0.4))
    fig.update_layout(title="Market Caps")
    return fig.to_html(full_html=False)


if __name__ == "__main__":
    app.run(debug=True)

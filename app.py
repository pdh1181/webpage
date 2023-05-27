from flask import Flask, render_template, request
import yfinance as yf
import plotly.graph_objs as go

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the stock symbol from the form input
        stock_symbol = request.form['symbol']
        
        # Fetch stock data using yfinance
        stock_data = yf.download(stock_symbol)
        
        # Extract the required data for candlestick plot
        candlestick_data = stock_data[['Open', 'High', 'Low', 'Close']].copy()
        candlestick_data.reset_index(inplace=True)
        
        # Create the candlestick plot
        candlestick = go.Candlestick(
            x=candlestick_data['Date'],
            open=candlestick_data['Open'],
            high=candlestick_data['High'],
            low=candlestick_data['Low'],
            close=candlestick_data['Close'],
            name=stock_symbol
        )
        
        # Create the plot layout
        layout = go.Layout(
            title=f'Candlestick Plot for {stock_symbol}',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Price')
        )
        
        # Create the plot figure
        fig = go.Figure(data=[candlestick], layout=layout)
        
        # Convert the plot figure to JSON for passing to the frontend
        plot_json = fig.to_json()
        
        return render_template('index.html', plot_json=plot_json)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import yfinance as yf
# import mplfinance as mpf
# import pandas as pd
# from io import BytesIO
# import plotly.graph_objects as go
# from datetime import date


def generate_stock_graph(request,symbol,start='2024-10-20',end='2024-12-20'):
    # Download stock data using yfinance
    data = yf.download(symbol, start=start, end=end)

    # Prepare the data for Plotly
    open_values = data['Open'].values.tolist()
    high_values = data['High'].values.tolist()
    low_values = data['Low'].values.tolist()
    close_values = data['Close'].values.tolist()
    dates = data.index.strftime('%Y-%m-%d').tolist()

    fig_data = [{
        'x': dates,
        'open': open_values,
        'high': high_values,
        'low': low_values,
        'close': close_values,
    }]

    layout = {
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Price'},
        'xaxis_rangeslider_visible': False
    }

    return JsonResponse({'data': fig_data, 'layout': layout, 'symbol':symbol})




def getData(sym):
    data = yf.Ticker(sym).history(period="5d")
    cur = data.iloc[-1]
    prev = data.iloc[-2]

    return {'val':cur['Open'],
            'diff':cur['Open']-prev['Close']}





def home(request):
    try:
        stockSNX = yf.Ticker('^BSESN')
        dataSNX = stockSNX.history(period="5d")
        stockNFT = yf.Ticker('^NSEI')
        dataNFT  = stockNFT.history(period="5d")

        if len(dataSNX) < 2 or len(dataNFT) < 2:
            if len(dataSNX) == 0 or len(dataNFT) == 0:
                return JsonResponse({'error': 'Market is currently closed, and no data is available.'}, status=400)
            return JsonResponse({'error': 'Not enough data for the last 2 days'}, status=400)
        
        latest_dataSNX = dataSNX.iloc[-1]
        previous_dataSNX = dataSNX.iloc[-2]

        latest_dataNFT = dataNFT.iloc[-1]
        previous_dataNFT = dataNFT.iloc[-2]

        sensex_ = latest_dataSNX['Open']
        nifty_ = latest_dataNFT['Close']
        sensex_diff = latest_dataSNX['Open']-previous_dataSNX['Close']
        nifty_diff = latest_dataNFT['Open']-previous_dataNFT['Close']

        AAPLdata = getData('AAPL')
        AMZNdata = getData('AMZN')
        RELIdata = getData('RELI')
        INTCdata = getData('INTC')
        NVDAdata = getData('NVDA')
        Fdata = getData('F')
        TSLAdata = getData('TSLA')
        METAdata = getData('META')
        MSFTdata = getData('MSFT')
        GOOGdata = getData('GOOG')

        sensex_data = {
            'sensex': sensex_,
            'nifty' : nifty_,
            'sensex_diff':sensex_diff,
            'nifty_diff':nifty_diff,
            'AAPL':AAPLdata['val'],
            'AMZN':AMZNdata['val'],
            'RELI':RELIdata['val'],
            'INTC':INTCdata['val'],
            'NVDA':NVDAdata['val'],
            'F':Fdata['val'],
            'TSLA':TSLAdata['val'],
            'META':METAdata['val'],
            'MSFT':MSFTdata['val'],
            'GOOG':GOOGdata['val'],
            'AAPLdiff':AAPLdata['diff'],
            'AMZNdiff':AMZNdata['diff'],
            'RELIdiff':RELIdata['diff'],
            'INTCdiff':INTCdata['diff'],
            'NVDAdiff':NVDAdata['diff'],
            'Fdiff':Fdata['diff'],
            'TSLAdiff':TSLAdata['diff'],
            'METAdiff':METAdata['diff'],
            'MSFTdiff':MSFTdata['diff'],
            'GOOGdiff':GOOGdata['diff']
        }
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Render the data to the template
    return render(request, 'homeui.html', sensex_data)
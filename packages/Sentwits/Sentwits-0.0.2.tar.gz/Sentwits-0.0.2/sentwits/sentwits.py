import requests
import collections

class COMMENTS:

    def __init__(self,ticker,timeframe,limit):
        self.ticker = ticker
        self.timeframe = timeframe
        self.limit = limit

    def stocktwits_comment_sentiment(self):
        if self.limit > 30:
            limit = 30

        sentiment = []

        url = requests.get(
            'https://api.stocktwits.com/api/2/streams/symbol/{}.json?filter=all&limit={}'.format(self.ticker, self.limit))
        api = url.json()

        for x in range(limit):
            i = ''
            if api['messages'][x]['entities']['sentiment'] is not None:
                i = api['messages'][x]['entities']['sentiment']['basic']
                sentiment.append(i)

            print(api['messages'][x]['user']['username'] + ':', api['messages'][x]['body'], "\033[1m" + i + "\033[0m")
            print('')
        return 'Bullish:', collections.Counter(sentiment)['Bullish'], 'Bearish:', collections.Counter(sentiment)[
            'Bearish']

class SENTIMENT:
    def __init__(self):
        pass


    def stocktwits_sentiment_ratio(self=True):
        tickers = []

        # Find all trending stocks today
        url = requests.get('https://api.stocktwits.com/api/2/trending/symbols.json')
        api = url.json()
        for x in api['symbols']:
            tickers.append(x['symbol'])

        # While loop for iterating through bull/bear cases
        for p in range(1):
            bull = 0
            bear = 0

            # for loop for iterating through top trending stocks,
            # then appending according to bull/bear side
            for i in tickers:
                url = requests.get(
                    'https://api.stocktwits.com/api/2/streams/symbol/{}.json?filter=all&limit=30'.format(i))
                api = url.json()

                # Max range is limited to 30 pr ticker
                for x in range(30):
                    if api['messages'][x]['entities']['sentiment'] is not None:
                        if api['messages'][x]['entities']['sentiment']['basic'] == 'Bearish':
                            bear += 1
                        else:
                            bull += 1

            # In case 'bull' divides by zero
            if bear == 0:
                bear = 1

            # Indicator
            indicator = round((bull / bear), 3)
            return indicator


        # Returns top watched tickers

        # Returns top watched tickers

    def stocktwits_top_watched(self=True):
        tickers = []
        url = requests.get('https://api.stocktwits.com/api/2/watchlists/top_watched.json')
        api = url.json()

        for x in api['top_watched']:
            tickers.append(x['symbol'])
        return tickers

        # Returns list of trending tickers today

    def stocktwits_trending(self=True):
        tickers = []
        url = requests.get('https://api.stocktwits.com/api/2/trending/symbols.json')
        api = url.json()
        for x in api['symbols']:
            tickers.append(x['symbol'])
        return tickers


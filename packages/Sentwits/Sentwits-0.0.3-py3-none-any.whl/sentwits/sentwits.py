import pandas as pd
import requests

class COMMENTS:

    def __init__(self, ticker, limit, timeframe='1-month'):
        self.ticker = ticker
        self.timeframe = timeframe
        self.limit = limit

    def GetComments(self):
        if self.limit > 30:
            limit = 30

        userid = []
        body = []

        url = requests.get('https://api.stocktwits.com/api/2/streams/symbol/{}.json?filter=all&limit={}'.format(self.ticker, self.limit))
        api = url.json()

        for x in range(self.limit):
            body.append(api['messages'][x]['body'])
            userid.append(api['messages'][x]['user']['username'])

        return pd.DataFrame({'Username': userid, 'Message': body})

    def GetSentiment(self):
        if self.limit > 30:
            limit = 30

        bull = []
        bear = []

        url = requests.get(
            'https://api.stocktwits.com/api/2/streams/symbol/{}.json?filter=all&limit={}'.format(self.ticker, self.limit))
        api = url.json()

        for x in range(self.limit):
            if api['messages'][x]['entities']['sentiment'] is not None:
                i = api['messages'][x]['entities']['sentiment']['basic']
                if i == 'Bullish':
                    bull.append(i)
                if i == 'Bearish':
                    bear.append(i)

        df = pd.DataFrame.from_dict({'Bullish': [len(bull)],
                                     'Bearish': [len(bear)]})
        return df

class SENTIMENT:

    def __init__(self):
        pass

    def GetSentimentRatio(self=True):
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

class USER:

    def __init__(self, userid, limit):
        self.userid = userid
        self.limit = limit

    def GetComments(self):

        body = []
        times = []
        url = requests.get('https://api.stocktwits.com/api/2/streams/user/{}.json?filter=all&limit={}'.format(self.userid, self.limit))
        api = url.json()
        for x in range(self.limit):
            body.append(api['messages'][x]['body'])
            times.append(api['messages'][x]['created_at'])

        return pd.DataFrame({'Message': body, 'Datetime': times})

    def GetFollow(self):
        url = requests.get('https://api.stocktwits.com/api/2/streams/user/{}.json?filter=all&limit={}'.format(self.userid, self.limit))
        api = url.json()
        followers = api['user']['followers']
        following = api['user']['following']

        return pd.DataFrame({'Followers': [followers], 'Following': [following]})

class GENERAL:
    def __init__(self):
        pass

    def GetTopWatched(self=True):
        tickers = []
        url = requests.get('https://api.stocktwits.com/api/2/watchlists/top_watched.json')
        api = url.json()

        for x in api['top_watched']:
            tickers.append(x['symbol'])
        return pd.DataFrame({'Tickers': tickers})

        # Returns list of trending tickers today

    def GetTrending(self=True):
        tickers = []
        url = requests.get('https://api.stocktwits.com/api/2/trending/symbols.json')
        api = url.json()
        for x in api['symbols']:
            tickers.append(x['symbol'])
        return pd.DataFrame({'Tickers': tickers})

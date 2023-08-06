Sentwits: Stocktwits Sentiment Analysis Tool.
--------------------------------------------

Sentwits is a python 3 library, build to scrape sentiment data directly from Stocktwits.
Get live sentiment data and comment updates for: Stocks, crypto and other assets offered by Stocktwits.
Minimal input is required from the user, so user friendliness is at its best.

Installation
------------
Simply

.. code-block:: bash

    $ pip install sentwits

Usage
-----

SENTIMENT:

 Trending:
  
 .. code-block:: Python

    from sentwits import COMMENTS, SENTIMENT

    >>> s = SENTIMENT.stocktwits_trending()

    >>> print(s)

    >>> ['ADGI', 'DOGE.X', 'BYND', 'CLSK', 'XRP.X', 'BTC.X', 'XAIR', 'CRSP', 'ESSC', 'RICK', 'RUN', 'LII', 'FBHS', 'STRN', 'RRD', 'BEN', 'SKIL', 'COHU', 'BOXD', 'AUPH', 'LVLU', 'MYGN', 'NC', 'LMAT', 'CYN', 'NWLI', 'SMLP', 'IPOF', 'VFF', 'PL']
  
 Top Watched:
  
 .. code-block:: Python

    from sentwits import COMMENTS, SENTIMENT

    >>> s = SENTIMENT.stocktwits_top_watched()

    >>> print(s)
    
    >>> ['AAPL', 'TSLA', 'AMZN', 'BTC.X', 'FB', 'NFLX', 'SPY', 'AMD', 'MSFT', 'AMC', 'BABA', 'NVDA', 'NIO', 'DOGE.X', 'TWTR', 'DIS', 'ETH.X', 'GME', 'GOOG', 'SNDL', 'SNAP', 'LCID', 'PLTR', 'BA', 'PLUG', 'SQ', 'OCGN', 'F', 'SHIB.X', 'GE', 'BB', 'FCEL', 'XRP.X', 'SPCE', 'TLRY', 'ZOM', 'MU', 'WKHS', 'BAC', 'QQQ', 'GOOGL', 'GEVO', 'NAKD', 'ACB', 'INTC', 'ROKU', 'PYPL', 'IDEX', 'MARA', 'ADA.X', 'BNGO', 'NOK', 'RIOT', 'WMT', 'GNUS', 'DKNG', 'LTC.X', 'AAL', 'CEI', 'MRNA', 'SBUX', 'SHOP', 'IBIO', 'INO', 'T', 'NKE', 'UBER', 'GPRO', 'NKLA', 'CTRM', 'CLOV', 'NVAX', 'MVIS', 'SOS', 'HCMC', 'PFE', 'CGC', 'BYND', 'COIN', 'VXRT', 'V', 'JNUG', 'SPX', 'TOPS', 'FSR', 'JAGX', 'CCL', 'XSPA', 'GILD', 'XOM', 'WISH', 'NNDM', 'DJIA', 'SRNE', 'JPM', 'DAL', 'UVXY', 'ATOS', 'CRON', 'VISL']
  
 Sentiment Ratio:
  
 .. code-block:: Python

    from sentwits import COMMENTS, SENTIMENT

    >>> s = SENTIMENT.stocktwits_sentiment_ratio())

    >>> print(s)
    
    >>> 6.316

COMMENTS:

.. code-block:: Python

    from sentwits import COMMENTS, SENTIMENT

    >>> s = COMMENTS('TSLA',limit=30).stocktwits_comment_sentiment()

    >>> print(s)
    
OUTPUT:
  Limited to the last 30 comments.
  
.. text-block:: Python
    XiaYao: $TSLA not a horrible day 😎 Bullish

    bendrobidow: $TSLA btw, Bernie and Karen Warren simply use Elon&#39;s name as click bait. Same strategy as in every news outlet.
    Nobody cares about Bernie and Karen, nobody want&#39;s to hear anything they r saying, but as soon as they mention Musk, everyone is talking about them again

    Not sure if Elon&#39;s strategy is helpful. He answers and helps their major goal, they just want to stay relevant 

    TradeNetWork: $BTC.X $TSLA very green added in 940s 

    Epic_Economics: $TSLA Elon!!! Tweet something for the crypto kiddos. Quick 

    BangHussleTheGreat: $LCID my only concern is quality. I’m hoping LUCID doesn’t have these issues. From what I understand a lot of the employees are already owners of other EV’s so they should try their best to prevent the types of issues seen here. This is not a shot at Tesla by posting this, I believe in trial and error. If it wouldn’t have been for $TSLA ’s trials we’d be in for major errors. https://fb.watch/9UNStCKnKg/ Bullish

    BannedGecko: $TSLA If you&#39;re up 10x on Tesla.  It&#39;s time to start winding down positions.  $TM $GM and every single car manufacturer on the planet has just released their new EV concepts.  And the analyst reception is unbelievable.

    Anything is possible where money is manipulated.  But it is quite interesting to see the back channel forecasts for Tesla at sub 500.

    I wonder what&#39;s cooking. Bearish

    Vinnyhuynh: $TSLA if you don’t  Buy now, don’t buy later at $1,000 Bullish

    InsiderFinance: 5-Day Equity Sentiment Recap: $TSLA is the #3 stock that institutions are trading over rolling 5 day window with 128.6K options contracts.

    Market analysis included in screenshot of dashboard from http://insiderfinance.io. 

    Vinnyhuynh: $TSLA speaking of inflation, did we already had that episode back in May?? 

    Cashhew: $TSLA 🤣🤣🤣 

    Arkoo: $TSLA inflation shit is already priced in elon is almost done selling what&#39;s your excuse? Bullish

    iAndigotmyback: $TSLA We have two more weeks to buy the diP 

    takinglosses: $TSLA Anybody know if Blackrock owns any tesla shares? 

    randomtrader07: @Street_Insider her ass got kicked hard.. had not for $TSLA she would be down like 70% in year..feel bad for retail investors who followed her 

    alps: $TSLA $IWM $MSFT PUTS paid nicely 

    PUNCHYOFACE: $LUCD $DOGE.X Should get some collateral love in Lucid from Doge and $TSLA and Elon funboys. 

    Sjacob99: @MemphisBelle2020 nice to see $LCID break away from $RIVN and $TSLA chart today.  Looking forward to a steady run back up to $50… Bullish

    Tradr78: $TSLA think this rises tomorrow at least above 1k. it ain’t headed down short term 

    ShortyMcFly: $SPY PARTY for the countdown tomorrow!!! This FOMC is the SUPERBOWL of the Year End!! Calls are on the losing side of the Tape for odds!! 😂📉💀💦🎲 $tsla $msft $aapl $adgi 

    &quot;JPOW JPOW JPOW JPOW&quot; - RATE HIKE RATE HIKE RATE HIKE!🤣😭✅ Bearish

    PUNCHYOFACE: $LUCD Only positive stock I have ... even $TSLA not green today 

    earthgabe: $TSLA my calls look like inflation numbers rn 

    allcharts: $TSLA TSLA 2021-12-14 Dark Pool &amp; Short Interest Data: 
    https://www.youtube.com/watch?v=xZHlBkUgmss 

    madnessofcrowds: $TSLA well there&#39;s no denying that bounce 

    WinderLiquor: $AMC $gme $TSLA  $SPY  and yes, you too Bill at $MSFT just so everyone knows Bullish

    FunCouponCodes: $TSLA Pretty much check on it to see how everyone’s feeling. $929 to I have no idea but a +$100 and IF holds end of week would say a lot GL 🍀✌️ 

    kamranl: $TSLA still maintain my 750 end of month target Bearish

    ineverleft1: $TSLA HIGHEST MARGINS THE NEXT DECADE! Bullish

    Mysticx213: $TSLA back over 1k EOW Bullish

    FlipperFastDaBull: $TSLA This is how to recoup some bear attacks.... $AAPL Bulls...some big money moves are on the way tomorrow!  Covid news had to cross the tape so there isn&#39;t a tapper tantrum, but a SURGE tantrum tomorrow!  Stocks, 700 Point day tomorrow GAINER, you heard it here first.  Chinese stocks are still declining, and Mega&#39;s will get their Santa Rally if you played your cards right.  $AAPL 175-190 calls will print tomorrow, loaded the dip with TSLA.  New highs before year end! Bullish

    HotStuff: $GRAB had a nice comeback from below $6 to $6.75. Not the best stock since its IPO earlier this month. Will definitely keep an eye on this one.
    $TSLA rebounded from a $930 low to over $960 before the close. Was able to get quite a few in the mid $930&#39;s.
    $PTPI received a major haircut as shares were trading at $4.38 yesterday and declined to $2.56 today. Stock has very nice volatility for good trading opportunities. Not for the faint of heart but a lot of fun.
    $ADGI did wash out at $6.30 with a 81% selloff today recovering to $7.26 at the close, up 15% from today&#39;s washout low. Evaluating a possible rebound potential to maybe $10-$11 which could be doable. Bullish

    ('Bullish:', 10, 'Bearish:', 3)


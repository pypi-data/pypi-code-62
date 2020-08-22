"""Contains functions for getting market level data."""
import robin_stocks.helper as helper
import robin_stocks.urls as urls
import robin_stocks.stocks as stocks

def get_top_movers_sp500(direction, info=None):
    """Returns a list of the top S&P500 movers up or down for the day.

    :param direction: The direction of movement either 'up' or 'down'
    :type direction: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * instrument_url
                      * symbol
                      * updated_at
                      * price_movement
                      * description

    """
    try:
        direction = direction.lower().strip()
    except AttributeError as message:
        print(message)
        return None

    if (direction != 'up' and direction != 'down'):
        print('Error: direction must be "up" or "down"')
        return([None])

    url = urls.movers_sp500()
    payload = {'direction': direction}
    data = helper.request_get(url, 'pagination', payload)

    return(helper.filter(data, info))

def get_top_100(info=None):
    """Returns a list of the Top 100 stocks on Robin Hood.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument

    """
    url = urls.get_100_most_popular()
    data = helper.request_get(url, 'regular')
    data = helper.filter(data, 'instruments')

    symbols = [stocks.get_symbol_by_url(x) for x in data]
    data = stocks.get_quotes(symbols)

    return(helper.filter(data, info))

def get_top_movers(info=None):
    """Returns a list of the Top 20 movers on Robin Hood.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument

    """
    url = urls.movers_top()
    data = helper.request_get(url, 'regular')
    data = helper.filter(data, 'instruments')

    symbols = [stocks.get_symbol_by_url(x) for x in data]
    data = stocks.get_quotes(symbols)

    return(helper.filter(data, info))

def get_all_stocks_from_market_tag(tag, info=None):
    """Returns all the stock quote information that matches a tag category.

    :param tag: The category to filter for. Examples include 'biopharmaceutical', 'upcoming-earnings', 'most-popular-under-25', and 'technology'.
    :type tag: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each mover. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * ask_price
                      * ask_size
                      * bid_price
                      * bid_size
                      * last_trade_price
                      * last_extended_hours_trade_price
                      * previous_close
                      * adjusted_previous_close
                      * previous_close_date
                      * symbol
                      * trading_halted
                      * has_traded
                      * last_trade_price_source
                      * updated_at
                      * instrument

    """
    url = urls.market_category(tag)
    data = helper.request_get(url, 'regular')
    data = helper.filter(data, 'instruments')

    if not data:
        print('ERROR: "{}" is not a valid tag'.format(tag))
        return [None]

    symbols = [stocks.get_symbol_by_url(x) for x in data]
    data = stocks.get_quotes(symbols)

    return(helper.filter(data, info))

def get_markets(info=None):
    """Returns a list of available markets.

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each market. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * url
                      * todays_hours
                      * mic
                      * operating_mic
                      * acronym
                      * name
                      * city
                      * country
                      * timezone
                      * website

    """
    url = urls.markets()
    data = helper.request_get(url, 'pagination')
    return(helper.filter(data, info))

def get_market_today_hours(market, info=None):
    """Returns the opening and closing hours of a specific market for today. Also will tell you if market is
    market is open on that date.

    :param market: The 'mic' value for the market. Can be found using get_markets().
    :type market: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the specific market. If info parameter is provided, \
    the string value for the corresponding key will be provided.
    :Dictionary Keys: * date
                      * is_open
                      * opens_at
                      * closes_at
                      * extended_opens_at
                      * extended_closes_at
                      * previous_open_hours
                      * next_open_hours

    """
    markets = get_markets()
    result = next((x for x in markets if x['mic'] == market), None)
    if not result:
        raise Exception('Not a valid market name. Check get_markets() for a list of market information.')

    url = result['todays_hours']
    data = helper.request_get(url, 'regular')
    return(helper.filter(data, info))

def get_market_next_open_hours(market, info=None):
    """Returns the opening and closing hours for the next open trading day after today. Also will tell you if market is
    market is open on that date.

    :param market: The 'mic' value for the market. Can be found using get_markets().
    :type market: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the specific market. If info parameter is provided, \
    the string value for the corresponding key will be provided.
    :Dictionary Keys: * date
                      * is_open
                      * opens_at
                      * closes_at
                      * extended_opens_at
                      * extended_closes_at
                      * previous_open_hours
                      * next_open_hours

    """
    url = get_market_today_hours(market, info='next_open_hours')
    data = helper.request_get(url, 'regular')
    return(helper.filter(data, info))

def get_market_next_open_hours_after_date(market, date, info=None):
    """Returns the opening and closing hours for the next open trading day after a date that is specified. Also will tell you if market is
    market is open on that date.

    :param market: The 'mic' value for the market. Can be found using get_markets().
    :type market: str
    :param date: The date you want to find the next available trading day after. format is YYYY-MM-DD.
    :type date: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the specific market. If info parameter is provided, \
    the string value for the corresponding key will be provided.
    :Dictionary Keys: * date
                      * is_open
                      * opens_at
                      * closes_at
                      * extended_opens_at
                      * extended_closes_at
                      * previous_open_hours
                      * next_open_hours

    """
    url = get_market_hours(market, date, info='next_open_hours')
    data = helper.request_get(url, 'regular')
    return(helper.filter(data, info))

def get_market_hours(market, date, info=None):
    """Returns the opening and closing hours of a specific market on a specific date. Also will tell you if market is
    market is open on that date. Can be used with past or future dates.

    :param market: The 'mic' value for the market. Can be found using get_markets().
    :type market: str
    :param date: The date you want to get information for. format is YYYY-MM-DD.
    :type date: str
    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a dictionary of key/value pairs for the specific market. If info parameter is provided, \
    the string value for the corresponding key will be provided.
    :Dictionary Keys: * date
                      * is_open
                      * opens_at
                      * closes_at
                      * extended_opens_at
                      * extended_closes_at
                      * previous_open_hours
                      * next_open_hours

    """
    url = urls.market_hours(market, date)
    data = helper.request_get(url, 'regular')
    return(helper.filter(data, info))


def get_currency_pairs(info=None):
    """Returns currency pairs

    :param info: Will filter the results to get a specific value.
    :type info: Optional[str]
    :returns: Returns a list of dictionaries of key/value pairs for each currency pair. If info parameter is provided, \
    a list of strings is returned where the strings are the value of the key that matches info.
    :Dictionary Keys: * asset_currency
                      * display_only
                      * id
                      * max_order_size
                      * min_order_size
                      * min_order_price_increment
                      * min_order_quantity_increment
                      * name
                      * quote_currency
                      * symbol
                      * tradability

    """
    url = urls.currency()
    data = helper.request_get(url, 'results')
    return(helper.filter(data, info))

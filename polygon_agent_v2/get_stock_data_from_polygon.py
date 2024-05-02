import os
import json
from polygon import RESTClient
from dotenv import load_dotenv

"""
Description of the function and it's parameters.
These description are passed to the Agents so that
Agent can figure out when to call this function and with
what parametrs
"""

get_stock_data_from_Polygon_description = """
    This function can retrieve the historical stock price from Polygon API.
    It will store the retrieved the data in json format and will save it in a file on disk.
    It will return the filename of the data file.

    The schema for the data is as follows:
    open = daily open price
    high = highest price for the day,
    low = lowest price for the day,
    close = daily closing price,
    volume = daily trading volume,
    vwap = volume weighted average price,
    timestamp = Integer type.  Date in Unix Msec timestamp format,
    transactions = Number of transactions,
    otc = Whether or not this aggregate is for an OTC ticker

    """

param_ticker_description = (
    "ticker symbol for which historical stock data is to be downloaded"
)
param_from_date_description = (
    "Date when to start the download from in YYYY-mm-dd format"
)
param_to_date_description = "Date when to stop the download in YYYY-mm-dd format"


def get_stock_data_from_polygon(
    ticker: str,
    from_date: str,
    to_date: str,
    multiplier: int = 1,
    timespan: str = "day",
):
    load_dotenv()

    try:

        client = RESTClient(api_key=os.getenv("POLYGON_API_KEY"))

        data = client.get_aggs(
            ticker=ticker,
            multiplier=multiplier,
            timespan=timespan,
            from_=from_date,
            to=to_date,
        )

        # create working dir if doesn't exist
        working_dir = os.getenv("WORK_DIR")
        os.makedirs(working_dir, exist_ok=True)

        # save to disk
        filename = f"{ticker}_{from_date}_{to_date}.json"
        full_path = f"{working_dir}/{filename}"
        with open(full_path, "w") as f:
            f.write(json.dumps(data, default=lambda o: o.__dict__))
    except Exception as e:
        print(f"Exception: {e}")

    return filename


# for testing purposes
if __name__ == "__main__":
    print(
        get_stock_data_from_polygon(
            ticker="AAPL", from_date="2023-01-01", to_date="2023-12-31"
        )
    )

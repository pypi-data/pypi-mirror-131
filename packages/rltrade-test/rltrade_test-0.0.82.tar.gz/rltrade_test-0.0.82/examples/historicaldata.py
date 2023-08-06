import asyncio
from metaapi_cloud_sdk import MetaApi
from datetime import datetime

token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYTI0YzMwYzFkNDRmZGFmZGI3NmVmYTUxZmQ2MDJmMCIsInBlcm1pc3Npb25zIjpbXSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaWF0IjoxNjM5NDkwMzEzLCJyZWFsVXNlcklkIjoiM2EyNGMzMGMxZDQ0ZmRhZmRiNzZlZmE1MWZkNjAyZjAifQ.DhA6Q-AlWNssi8ScOaWy2Bxo4Hebgw94BDE6PiT9J-TvsuF7OqvdYBQ1IWYEMtsYsg3Ij8p8Wpvn8ZdZeHRkR3vLcQnMH-GZj3DyYkeqovQKk6U3uOobV-GS3meJPZYfw2zItuTDBWxuHDZsVW1ZvF4sItBDmsWIe2svF0NmKE1nu-ephcYVzYo9grr93de_h-QwlP-yeZFeGEqrz3-q5gYWcARJsIR1BX63zePuDHkUK9k5W9Rm28WdB87MHEyMSWhcAZDf8si5MwsPYC3wpzNtzGqORF3UY-w5EmolCtSPMBqM7AI0LKc1n8GPS3ZhnvHkfGhWEdb5gKlCWwshk30tICN24C1bZG06zfs450oLm8ih9ls5oyshcg_xwawNvsA305D7Siz0Pzqr1xnUA8zMz8cVUFZtjdBWCfot05_ziVO0x_mApVyAVC2OA-Sh61RtkwNNpg4bTCzK30OpdiS9GO0HLgnepnuwWOO0T9DTzTAJUxyJcXOzcWcXGdMTWaGAp5ranytU97k8GxDHa5jOS_WvphL24C8QA6of0pYZwHM3Ul5Aw351H1SbJLIqs2AChDoUnpJb9OZb-27ESLZgM1mhU6rwzt8lRRbxUHaXSv5QpM29nPm3k5KrFSv-UTXiX6oU9c1nNh3qLb6FKV_B1CQarcvyx66iUg-1DcU'
login = '7083590'
password = 'Marines791!'
account_id = 'a0366018-a4bd-4d1f-8ca3-1b069b1dd134'
server_name = 'OANDA-v20 Live-1'
broker_srv_file = '/home/maunish/Upwork Projects/rl-trade/examples/OANDA-v20 Live-1.srv' #change this path for your PC

domain = 'agiliumtrade.agiliumtrade.ai'
symbol = 'EURUSD'

async def retrieve_historical_candles():
    api = MetaApi(token, {'domain': domain})
    try:
        account = await api.metatrader_account_api.get_account(account_id)

        #  wait until account is deployed and connected to broker
        print('Deploying account')
        if account.state != 'DEPLOYED':
            await account.deploy()
        else:
            print('Account already deployed')
        print('Waiting for API server to connect to broker (may take couple of minutes)')
        if account.connection_status != 'CONNECTED':
            await account.wait_connected()

        # retrieve last 10K 1m candles
        pages = 1
        print(f'Downloading {pages}K latest candles for {symbol}')
        started_at = datetime.now().timestamp()
        start_time = None
        candles = None
        for i in range(pages):
            # the API to retrieve historical market data is currently available for G1 only
            new_candles = await account.get_historical_candles(symbol, '1m', start_time)
            print(f'Downloaded {len(new_candles) if new_candles else 0} historical candles for {symbol}')
            if new_candles and len(new_candles):
                candles = new_candles
            if candles and len(candles):
                start_time = candles[0]['time']
                start_time.replace(minute=start_time.minute - 1)
                print(f'First candle time is {start_time}')
        if candles:
            print(f'First candle is', candles[0])
        print(f'Took {(datetime.now().timestamp() - started_at) * 1000}ms')

    except Exception as err:
        print(api.format_error(err))
    exit()

asyncio.run(retrieve_historical_candles())
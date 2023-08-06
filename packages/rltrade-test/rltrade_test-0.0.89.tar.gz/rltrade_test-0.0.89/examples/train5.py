import asyncio
from rltrade import config
from metaapi_cloud_sdk import MetaApi
from rltrade.data import OandaDownloader
from rltrade.backtests import backtest_stats
from rltrade.models import SmartDayTradeAgent3

# token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYTI0YzMwYzFkNDRmZGFmZGI3NmVmYTUxZmQ2MDJmMCIsInBlcm1pc3Npb25zIjpbXSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaWF0IjoxNjM5NDkwMzEzLCJyZWFsVXNlcklkIjoiM2EyNGMzMGMxZDQ0ZmRhZmRiNzZlZmE1MWZkNjAyZjAifQ.DhA6Q-AlWNssi8ScOaWy2Bxo4Hebgw94BDE6PiT9J-TvsuF7OqvdYBQ1IWYEMtsYsg3Ij8p8Wpvn8ZdZeHRkR3vLcQnMH-GZj3DyYkeqovQKk6U3uOobV-GS3meJPZYfw2zItuTDBWxuHDZsVW1ZvF4sItBDmsWIe2svF0NmKE1nu-ephcYVzYo9grr93de_h-QwlP-yeZFeGEqrz3-q5gYWcARJsIR1BX63zePuDHkUK9k5W9Rm28WdB87MHEyMSWhcAZDf8si5MwsPYC3wpzNtzGqORF3UY-w5EmolCtSPMBqM7AI0LKc1n8GPS3ZhnvHkfGhWEdb5gKlCWwshk30tICN24C1bZG06zfs450oLm8ih9ls5oyshcg_xwawNvsA305D7Siz0Pzqr1xnUA8zMz8cVUFZtjdBWCfot05_ziVO0x_mApVyAVC2OA-Sh61RtkwNNpg4bTCzK30OpdiS9GO0HLgnepnuwWOO0T9DTzTAJUxyJcXOzcWcXGdMTWaGAp5ranytU97k8GxDHa5jOS_WvphL24C8QA6of0pYZwHM3Ul5Aw351H1SbJLIqs2AChDoUnpJb9OZb-27ESLZgM1mhU6rwzt8lRRbxUHaXSv5QpM29nPm3k5KrFSv-UTXiX6oU9c1nNh3qLb6FKV_B1CQarcvyx66iUg-1DcU'
# login = '7083590'
# password = 'Marines791!'
# account_id = 'a0366018-a4bd-4d1f-8ca3-1b069b1dd134'
# server_name = 'OANDA-v20 Live-1'
# broker_srv_file = '/home/maunish/Upwork Projects/rl-trade/examples/OANDA-v20 Live-1.srv'
# domain = 'agiliumtrade.agiliumtrade.ai'

"""
time_frame - last date available
4h  - '2021-04-23'
1h  - '2021-10-19'
30m - '2021-11-18'
15m - '2021-12-03'
5m -  '2021-12-08'
"""

time_frame = "4h" # available 5m, 15m, 30m, 1h, 4h
train_period = ('2021-04-23','2021-12-15') #for training the model
test_period = ('2021-12-15','2021-12-18') 
start_time = "00:00:00"
end_time = "23:55:00" 
path = 'models/daytrades/forex'

token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYTI0YzMwYzFkNDRmZGFmZGI3NmVmYTUxZmQ2MDJmMCIsInBlcm1pc3Npb25zIjpbXSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaWF0IjoxNjM5NDkwMzEzLCJyZWFsVXNlcklkIjoiM2EyNGMzMGMxZDQ0ZmRhZmRiNzZlZmE1MWZkNjAyZjAifQ.DhA6Q-AlWNssi8ScOaWy2Bxo4Hebgw94BDE6PiT9J-TvsuF7OqvdYBQ1IWYEMtsYsg3Ij8p8Wpvn8ZdZeHRkR3vLcQnMH-GZj3DyYkeqovQKk6U3uOobV-GS3meJPZYfw2zItuTDBWxuHDZsVW1ZvF4sItBDmsWIe2svF0NmKE1nu-ephcYVzYo9grr93de_h-QwlP-yeZFeGEqrz3-q5gYWcARJsIR1BX63zePuDHkUK9k5W9Rm28WdB87MHEyMSWhcAZDf8si5MwsPYC3wpzNtzGqORF3UY-w5EmolCtSPMBqM7AI0LKc1n8GPS3ZhnvHkfGhWEdb5gKlCWwshk30tICN24C1bZG06zfs450oLm8ih9ls5oyshcg_xwawNvsA305D7Siz0Pzqr1xnUA8zMz8cVUFZtjdBWCfot05_ziVO0x_mApVyAVC2OA-Sh61RtkwNNpg4bTCzK30OpdiS9GO0HLgnepnuwWOO0T9DTzTAJUxyJcXOzcWcXGdMTWaGAp5ranytU97k8GxDHa5jOS_WvphL24C8QA6of0pYZwHM3Ul5Aw351H1SbJLIqs2AChDoUnpJb9OZb-27ESLZgM1mhU6rwzt8lRRbxUHaXSv5QpM29nPm3k5KrFSv-UTXiX6oU9c1nNh3qLb6FKV_B1CQarcvyx66iUg-1DcU'
login = '3648098'
password = 'Marines791!'
account_id = '75e3c45c-8aab-4f76-9e4e-4c7cf55c35c6'
server_name = 'OANDA-v20 Demo-1'
broker_srv_file = '/home/maunish/Upwork Projects/rl-trade/examples/OANDA-Demo-1.srv'
domain = 'agiliumtrade.agiliumtrade.ai'

ticker_list = ['AUDUSD','EURUSD','NZDUSD','USDCAD','USDCHF','GBPUSD']
sec_types = ['-','-','-','-','-','-']
exchanges = ['-','-','-','-','-','-']


tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
additional_indicators = config.ADDITIONAL_DAYTRADE_INDICATORS
# additional_indicators = config.ADDITIONAL_STOCK_INDICATORS

env_kwargs = {
    "initial_amount": 50_000, #this does not matter as we are making decision for lots and not money.
    "ticker_col_name":"tic",
    "stop_loss":0.015,
    "filter_threshold":1, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "transaction_cost":0, #transaction cost per order
    "tech_indicator_list":tech_indicators + additional_indicators, 
    "reward_scaling": 1}

PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.01,
            'batch_size':522}

async def train_model():
    api = MetaApi(token,{'domain':domain})

    try:
        account = await api.metatrader_account_api.get_account(account_id)

        if account.state != 'DEPLOYED':
            await account.deploy()
        else:
            print('Account already deployed')
        if account.connection_status != 'CONNECTED':
            await account.wait_connected()
    
        oa = OandaDownloader(
            account = account,
            time_frame=time_frame,
            start_date=train_period[0],
            end_date=test_period[1],
            start_time=start_time,
            end_time=end_time,
            ticker_list=ticker_list)

        df = await oa.fetch_data()

        agent = SmartDayTradeAgent3("ppo",
                            df=df,
                            account=account,
                            time_frame=time_frame,
                            ticker_list=ticker_list,
                            sec_types = sec_types,
                            exchanges=exchanges,
                            ticker_col_name="tic",
                            tech_indicators=tech_indicators,
                            additional_indicators=additional_indicators,
                            train_period=train_period,
                            test_period=test_period,
                            start_time=start_time,
                            end_time=end_time,
                            env_kwargs=env_kwargs,
                            model_kwargs=PPO_PARAMS,
                            tb_log_name='ppo',
                            epochs=2)

        agent.train_model()
        agent.save_model(path) #save the model for trading

        df_daily_return,df_actions = agent.make_prediction() #testing model on testing period

    except Exception as err:
        print(api.format_error(err))


asyncio.run(train_model())
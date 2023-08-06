from rltrade import config
from rltrade.data import OandaDownloader
from rltrade.backtests import backtest_stats
from rltrade.models import SmartDayTradeAgent3



# Data is set to 5 min bar size
demo = True
# can not go before 6th dec
train_period = ('2021-12-06','2021-12-08') #for training the model
test_period = ('2021-12-08','2021-12-14') 
"""
start_time  = 00:00:00 to end_time 23:55:00 is used for trading whole day,
it will automatically filter the data to after 1am on Monday and before 330pm on Friday.

you can also limit trade period by using start_time and end_time.
It will download no data for weekend
"""
start_time = "00:00:00"
end_time = "23:55:00" 
path = 'models/daytrades/forex'
token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIzYTI0YzMwYzFkNDRmZGFmZGI3NmVmYTUxZmQ2MDJmMCIsInBlcm1pc3Npb25zIjpbXSwidG9rZW5JZCI6IjIwMjEwMjEzIiwiaWF0IjoxNjM5NDkwMzEzLCJyZWFsVXNlcklkIjoiM2EyNGMzMGMxZDQ0ZmRhZmRiNzZlZmE1MWZkNjAyZjAifQ.DhA6Q-AlWNssi8ScOaWy2Bxo4Hebgw94BDE6PiT9J-TvsuF7OqvdYBQ1IWYEMtsYsg3Ij8p8Wpvn8ZdZeHRkR3vLcQnMH-GZj3DyYkeqovQKk6U3uOobV-GS3meJPZYfw2zItuTDBWxuHDZsVW1ZvF4sItBDmsWIe2svF0NmKE1nu-ephcYVzYo9grr93de_h-QwlP-yeZFeGEqrz3-q5gYWcARJsIR1BX63zePuDHkUK9k5W9Rm28WdB87MHEyMSWhcAZDf8si5MwsPYC3wpzNtzGqORF3UY-w5EmolCtSPMBqM7AI0LKc1n8GPS3ZhnvHkfGhWEdb5gKlCWwshk30tICN24C1bZG06zfs450oLm8ih9ls5oyshcg_xwawNvsA305D7Siz0Pzqr1xnUA8zMz8cVUFZtjdBWCfot05_ziVO0x_mApVyAVC2OA-Sh61RtkwNNpg4bTCzK30OpdiS9GO0HLgnepnuwWOO0T9DTzTAJUxyJcXOzcWcXGdMTWaGAp5ranytU97k8GxDHa5jOS_WvphL24C8QA6of0pYZwHM3Ul5Aw351H1SbJLIqs2AChDoUnpJb9OZb-27ESLZgM1mhU6rwzt8lRRbxUHaXSv5QpM29nPm3k5KrFSv-UTXiX6oU9c1nNh3qLb6FKV_B1CQarcvyx66iUg-1DcU'
login = '7083590'
password = 'Marines791!'
account_id = 'a0366018-a4bd-4d1f-8ca3-1b069b1dd134'
server_name = 'OANDA-v20 Live-1'
"""
this file is in the examples folder "change the path accordingly in you PC
"""
broker_srv_file = '/home/maunish/Upwork Projects/rl-trade/examples/OANDA-v20 Live-1.srv'
domain = 'agiliumtrade.agiliumtrade.ai'

ticker_list = ['AUDUSD','EURUSD','NZDUSD','USDCAD','USDCHF','GBPUSD']
sec_types = ['-','-','-','-','-','-']
exchanges = ['-','-','-','-','-','-']

tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
additional_indicators = config.ADDITIONAL_DAYTRADE_INDICATORS

env_kwargs = {
    "initial_amount": 50_000, #this does not matter as we are making decision for lots and not money.
    "ticker_col_name":"tic",
    "mode":'min',
    "filter_threshold":1, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "transaction_cost":0, #transaction cost per order
    "tech_indicator_list":tech_indicators + additional_indicators, 
    "reward_scaling": 1}

PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.01,
            'batch_size':2000}

df = OandaDownloader(
    token=token,
    login=login,
    password=password,
    account_id=account_id,
    server_name=server_name,
    broker_srv_file=broker_srv_file,
    domain=domain,
    start_date=train_period[0],
    end_date=test_period[1],
    start_time=start_time,
    end_time=end_time,
    ticker_list=ticker_list
).fetch_min_data()

agent = SmartDayTradeAgent3("ppo",
                    df=df,
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
                    demo=demo,
                    mode='min', # daily or min
                    epochs=10)

# agent.train_model() #training model on trading period
agent.train_model_filter()
agent.save_model(path) #save the model for trading

df_daily_return,df_actions = agent.make_prediction() #testing model on testing period

"""
backtesting is not working will fix it.
"""
# perf_stats_all = backtest_stats(df=df_daily_return,
#                                 baseline_ticker=agent.ticker_list,
#                                 sec_types= agent.sec_types,
#                                 exchanges=agent.exchanges,
#                                 value_col_name="daily_return",
#                                 baseline_start = test_period[0], 
#                                 baseline_end = test_period[1],
#                                 start_time=start_time,
#                                 end_time=end_time,
#                                 demo=demo,
#                                 mode='min')
# print(perf_stats_all)
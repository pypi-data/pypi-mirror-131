from rltrade import config
from rltrade.data import IBKRDownloader
from rltrade.backtests import backtest_stats
from rltrade.models import SmartDayTradeAgent2


demo = True
train_period = ('2021-11-22','2021-11-30') #for training the model
test_period = ('2021-11-30','2021-12-10') 
start_time = "09:30:00"
end_time = "10:00:00" 
path = 'models/daytrades/ESNQ'
ticker_list = ['ESZ1','NQZ1']
sec_types = ['FUT','FUT']
exchanges = ['GLOBEX','GLOBEX']
# path = 'models/daytrades/AAPLMSFT'
# ticker_list = ['AAPL','MSFT']
# sec_types = ['STK','STK']
# exchanges = ['SMART','SMART']
tech_indicators = config.STOCK_INDICATORS_LIST # indicators from stockstats
additional_indicators = config.ADDITIONAL_DAYTRADE_INDICATORS

env_kwargs = {
    "initial_amount": 50_000, #this does not matter as we are making decision for contract and not money.
    "ticker_col_name":"tic",
    "mode":'min',
    "filter_threshold":1, #between 0.1 to 1, select percentage of top stocks 0.3 means 30% of top stocks
    "target_metrics":['asset','calamar','skew','kurtosis'], #asset, cagr, sortino, calamar, skew and kurtosis are available options.
    "transaction_cost":0, #transaction cost per order
    "tech_indicator_list":tech_indicators + additional_indicators, 
    "reward_scaling": 1}

PPO_PARAMS = {'ent_coef':0.005,
            'learning_rate':0.01,
            'batch_size':2000}

print('Downloading Data')
df = IBKRDownloader(start_date = train_period[0], # first date
                    end_date = test_period[1], #last date
                    ticker_list = ticker_list,
                    sec_types=sec_types,
                    exchanges=exchanges,
                    start_time=start_time,
                    end_time=end_time,
                    demo=demo,
                    ).fetch_min_data()

agent = SmartDayTradeAgent2("ppo",
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

perf_stats_all = backtest_stats(df=df_daily_return,
                                baseline_ticker=agent.ticker_list,
                                sec_types= agent.sec_types,
                                exchanges=agent.exchanges,
                                value_col_name="daily_return",
                                baseline_start = test_period[0], 
                                baseline_end = test_period[1],
                                start_time=start_time,
                                end_time=end_time,
                                demo=demo,
                                mode='min')
print(perf_stats_all)
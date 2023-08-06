import time
import threading
import numpy as np
import pandas as pd
from pytz import timezone
from datetime import datetime
from stockstats import StockDataFrame as Sdf
from rltrade.ibkr import IBapi, api_connect,stock_contract,future_contract

#Meta api
import asyncio
from metaapi_cloud_sdk import MetaApi

class IBKRDownloader:

    def __init__(self,start_date:str,end_date:str,
                ticker_list:list,sec_types:list,exchanges:list,
                start_time="09:30:00",end_time="15:59:00",demo=True):
        self.start_date = start_date.replace('-','')
        self.end_date = end_date.replace('-','')
        self.ticker_list = ticker_list
        self.sec_types = sec_types
        self.exchanges = exchanges
        self.start_date_dt = datetime.strptime(self.start_date,"%Y%m%d")
        self.end_date_dt = datetime.strptime(self.end_date,"%Y%m%d")
        self.date_delta =  (self.end_date_dt-self.start_date_dt)
        self.days = self.date_delta.days
        self.years = int(self.days / 365)
        self.dates = pd.date_range(start=self.start_date_dt,end =self.end_date_dt,freq='2D')
        self.dates = [''.join(str(x).split('-'))[:8] for x in self.dates]
        self.start_time = start_time
        self.end_time = end_time
        self.demo = demo
        self.count = 0
            
    def download_data(self,app:IBapi,id:int,ticker:str,sectype:str,exchange:str):
        def run_loop():
            app.run()
        thread = threading.Thread(target=run_loop,daemon=True)
        thread.start()
        while True:
            if isinstance(app.nextorderId, int):
                break
            else:
                print('waiting for connection')
                time.sleep(1)
        duration = f"{self.years} Y" if self.years > 0 else f"{self.days} D"
        if sectype == 'STK':
            cnt = stock_contract(ticker,secType=sectype,exchange=exchange)
        elif sectype == 'FUT':
            cnt = future_contract(ticker,secType=sectype,exchange=exchange)
        app.reqHistoricalData(id,cnt,self.end_date+" "+ self.end_time + " est", duration,'1 day','TRADES',1,2,False,[])
        app.nextorderId += 1
        return app

    def fetch_data(self):
        df = pd.DataFrame()
        not_downloaded = list()
        print("connecting to server...")
        app = api_connect(demo=self.demo)
        for i,tic in enumerate(self.ticker_list):
            print("Trying to download: ",tic)
            sec = self.sec_types[i]
            exchange = self.exchanges[i]
            try:
                temp_df = self.download_data(app,i,tic,sec,exchange)
                time.sleep(5)
                temp_df = app.get_df()
                temp_df['tic'] = tic
                temp_df['sec'] = sec
                temp_df['exchange'] = exchange
                app.reset_df()
                df = df.append(temp_df)
            except:
                print("Not able to download",tic)
                not_downloaded.append(tic)
        app.disconnect()
        time.sleep(5)
        if len(not_downloaded) > 0:
            print("IB was not able to download this ticker",not_downloaded)
        
        df = df.reset_index()
        df["date"] = pd.to_datetime(df['date'],format='%Y%m%d')
        df["day"] = df["date"].dt.dayofweek
        df["date"] = df["date"].apply(lambda x: x.strftime("%Y-%m-%d"))
        return df
    
    def download_min_data(self,app:IBapi,id:int,ticker:str,sectype:str,exchange:str,end:str):
        def run_loop():
            app.run()
        thread = threading.Thread(target=run_loop,daemon=True)
        thread.start()
        while True:
            if isinstance(app.nextorderId, int):
                break
            else:
                print('waiting for connection')
                time.sleep(1)
        if sectype == 'STK':
            cnt = stock_contract(ticker,secType=sectype,exchange=exchange)
        elif sectype == 'FUT':
            cnt = future_contract(ticker,secType=sectype,exchange=exchange)

        app.reqHistoricalData(id,cnt ,end+" "+ self.end_time + " est","2 D",'1 min','TRADES',1,1,False,[])
        app.nextorderId += 1
        return app
    
    def fetch_min_data(self):
        df = pd.DataFrame()
        not_downloaded = list()
        print("connecting to server...")
        app = api_connect(demo=self.demo)
        for i,tic in enumerate(self.ticker_list):
            print("Trying to download: ",tic)
            sec = self.sec_types[i]
            exchange  = self.exchanges[i]
            for end in self.dates[1:]:
                self.count += 1
                try:
                    app = self.download_min_data(app,self.count,tic,sec,exchange,end)
                    time.sleep(10)
                    temp_df = app.get_df()
                    temp_df['tic'] = tic
                    temp_df['sec'] = sec
                    temp_df['exchange'] = exchange
                    app.reset_df()
                    df = df.append(temp_df)
                except:
                    print("Not able to download",tic)
                    not_downloaded.append(tic)
        app.disconnect()
        time.sleep(5)
        if len(not_downloaded) > 0:
            print("IB was not able to download this ticker",not_downloaded)
        
        df["date"] = pd.to_datetime(df['date'],format='%Y%m%d  %H:%M:%S')
        df['time'] = df['date'].dt.time
        df['only date'] = df['date'].dt.date
        df = df[(df['time']>=datetime.strptime(self.start_time,"%H:%M:%S").time()) & 
                (df['time']<=datetime.strptime(self.end_time,"%H:%M:%S").time())]
        
        df['market closed'] = df.groupby('only date')['time'].transform(lambda x:(x==x.max()))
        df['market closed'] = df['market closed'] | df['market closed'].shift(-1).fillna(True)
        return df
    
    def download_todays_min_data(self,app:IBapi,id:int,ticker:str,sectype:str,exchange:str,end:str,duration:str):
        def run_loop():
            app.run()
        thread = threading.Thread(target=run_loop,daemon=True)
        thread.start()
        while True:
            if isinstance(app.nextorderId, int):
                break
            else:
                print('waiting for connection')
                time.sleep(1)
        if sectype == 'STK':
            cnt = stock_contract(ticker,secType=sectype,exchange=exchange)
        elif sectype == 'FUT':
            cnt = future_contract(ticker,secType=sectype,exchange=exchange)

        app.reqHistoricalData(id,cnt ,"", duration,'1 min','TRADES',1,1,True,[])
        time.sleep(5)
        app.nextorderId += 1
        return app
    
    def fetch_todays_min_data(self,end,duration):
        df = pd.DataFrame()
        not_downloaded = list()
        print("connecting to server...")
        app = api_connect(demo=self.demo)
        for i,tic in enumerate(self.ticker_list):
            self.count +=1
            sec = self.sec_types[i]
            exchange = self.exchanges[i]
            try:
                temp_df = self.download_todays_min_data(app,self.count,tic,sec,exchange,end,duration)
                time.sleep(1)
                temp_df = app.get_df()
                temp_df['tic'] = tic
                temp_df['sec'] = sec
                temp_df['exchange'] = exchange
                app.reset_df()
                df = df.append(temp_df)
            except:
                print("Not able to download",tic)
                not_downloaded.append(tic)   
        app.disconnect()
        time.sleep(5)
        if len(not_downloaded) > 0:
            print("IB was not able to download this ticker",not_downloaded)
        
        df["date"] = pd.to_datetime(df['date'],format='%Y%m%d  %H:%M:%S')
        df['time'] = df['date'].dt.time
        df['only date'] = df['date'].dt.date
        df = df[(df['time']>=datetime.strptime(self.start_time,"%H:%M:%S").time()) & 
                (df['time']<=datetime.strptime(self.end_time,"%H:%M:%S").time())]
        df['market closed'] = False
        return df

class OandaDownloader:
    def __init__(self,
    account,
    time_frame:str,
    start_date:str,
    end_date:str,
    ticker_list:list,
    start_time="09:30:00",
    end_time="15:59:00",
    ):
        self.account = account
        self.time_frame = time_frame
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.ticker_list = ticker_list
        tz = timezone('EST')
        self.start_date_st = tz.localize(datetime.strptime(self.start_date+self.start_time,"%Y-%m-%d%H:%M:%S")).astimezone(tz)
        self.start_date_et = tz.localize(datetime.strptime(self.start_date+self.end_time,"%Y-%m-%d%H:%M:%S")).astimezone(tz)
        self.end_date_st = tz.localize(datetime.strptime(self.end_date+self.start_time,"%Y-%m-%d%H:%M:%S")).astimezone(tz)
        self.end_date_et = tz.localize(datetime.strptime(self.end_date+self.end_time,"%Y-%m-%d%H:%M:%S")).astimezone(tz)
        
        self.time_value = int(self.time_frame[:-1])
        self.time_format = self.time_frame[-1]

        if self.time_format == 'm':
            freq = f'{self.time_value * 1000} min' 
        elif self.time_format == 'h':
            freq = f'{self.time_value * 1000} H'
        elif self.time_format == 'd':
            freq = f'{self.time_value * 1000} D'

        self.date_range = pd.date_range(start=self.start_date_st,end=self.end_date_et,freq=freq)
        self.date_range = [tz.localize(datetime.strptime(str(x)[:-6],"%Y-%m-%d %H:%M:%S")).astimezone(tz) for x in self.date_range]
        self.date_range.append(self.end_date_et)
        self.date_range = self.date_range[1:]
        self.time_delta = (self.start_date_et-self.start_date_st)

        
    async def fetch_data(self):
            
        df = pd.DataFrame()
        for tic in self.ticker_list:
            for date in self.date_range:
                # if date.weekday() < 5:
                new_data = await self.account.get_historical_candles(tic,self.time_frame,date,limit=1000)
                print(f'Downloaded {len(new_data) if new_data else 0} historical data for {tic}')
                temp_df = pd.DataFrame(new_data)
                temp_df.columns = ['date','open','high','low','close','volume']
                temp_df['date'] = temp_df['date'].dt.tz_convert('EST')
                temp_df["date"] = pd.to_datetime(temp_df['date'],format='%Y%m%d  %H:%M:%S')
                temp_df['tic'] = tic
                temp_df['sec'] = '-'
                temp_df['exchange'] = '-'
                # if date.weekday() == 0:
                #     temp_df['time'] = temp_df['date'].dt.time
                #     temp_df = temp_df[(temp_df['time']>=datetime.strptime("01:00:00","%H:%M:%S").time())]
                #     temp_df.drop('time',inplace=True,axis=1)
                # elif date.weekday() == 4:
                #     temp_df['time'] = temp_df['date'].dt.time
                #     temp_df = temp_df[(temp_df['time']<=datetime.strptime("03:30:00","%H:%M:%S").time())]
                #     temp_df.drop('time',inplace=True,axis=1)
                df = df.append(temp_df)
        
        df['only date'] = df['date'].dt.date
        df['time'] = df['date'].dt.time
        df = df[(df['time']>=datetime.strptime(self.start_time,"%H:%M:%S").time()) & 
                (df['time']<=datetime.strptime(self.end_time,"%H:%M:%S").time())]
        df['market closed'] = df.groupby('only date')['time'].transform(lambda x:(x==x.max()))
        df['market closed'] = df['market closed'] | df['market closed'].shift(-1).fillna(True)
        df = df.reset_index(drop=True)
        return df
    
    async def fetch_todays_data(self,time_now,duration):
        df = pd.DataFrame()
        if self.time_format == 'm':
            duration = duration / (60 * self.time_value)
        elif self.time_format == 'h':
            duration = duration / (3600 * self.time_value)

        for tic in self.ticker_list:
            # if time_now.weekday() < 5:
            new_data = await self.account.get_historical_candles(tic,self.time_frame,time_now,limit=duration)
            print(f'Downloaded {len(new_data) if new_data else 0} historical data for {tic}')
            temp_df = pd.DataFrame(new_data)
            temp_df.columns = ['date','open','high','low','close','volume']
            temp_df['date'] = temp_df['date'].dt.tz_convert('EST')
            temp_df["date"] = pd.to_datetime(temp_df['date'],format='%Y%m%d  %H:%M:%S')
            temp_df['tic'] = tic
            temp_df['sec'] = '-'
            temp_df['exchange'] = '-'
            # if time_now.weekday() == 0:
            #     temp_df['time'] = temp_df['date'].dt.time
            #     temp_df = temp_df[(temp_df['time']>=datetime.strptime("01:00:00","%H:%M:%S").time())]
            #     temp_df.drop('time',inplace=True,axis=1)
            # elif time_now.weekday() == 4:
            #     temp_df['time'] = temp_df['date'].dt.time
            #     temp_df = temp_df[(temp_df['time']<=datetime.strptime("03:30:00","%H:%M:%S").time())]
            #     temp_df.drop('time',inplace=True,axis=1)
            df = df.append(temp_df)

        df['only date'] = df['date'].dt.date
        df['time'] = df['date'].dt.time
        df = df[(df['time']>=datetime.strptime(self.start_time,"%H:%M:%S").time()) & 
                (df['time']<=datetime.strptime(self.end_time,"%H:%M:%S").time())]
        df['market closed'] = False
        df = df.reset_index(drop=True)

        return df

    async def fetch_daily_data(self):
            
        df = pd.DataFrame()
        for tic in self.ticker_list:
            for date in self.date_range:
                # if date.weekday() < 5:
                new_data = await self.account.get_historical_candles(tic,self.time_frame,date,limit=1000)
                print(f'Downloaded {len(new_data) if new_data else 0} historical data for {tic}')
                temp_df = pd.DataFrame(new_data)
                temp_df.columns = ['date','open','high','low','close','volume']
                temp_df['date'] = temp_df['date'].dt.tz_convert('EST')
                temp_df["date"] = pd.to_datetime(temp_df['date'],format='%Y%m%d  %H:%M:%S')
                temp_df['tic'] = tic
                temp_df['sec'] = '-'
                temp_df['exchange'] = '-'
                # if date.weekday() == 0:
                #     temp_df['time'] = temp_df['date'].dt.time
                #     temp_df = temp_df[(temp_df['time']>=datetime.strptime("01:00:00","%H:%M:%S").time())]
                #     temp_df.drop('time',inplace=True,axis=1)
                # elif date.weekday() == 4:
                #     temp_df['time'] = temp_df['date'].dt.time
                #     temp_df = temp_df[(temp_df['time']<=datetime.strptime("03:30:00","%H:%M:%S").time())]
                #     temp_df.drop('time',inplace=True,axis=1)
                df = df.append(temp_df)
        
        df['only date'] = df['date'].dt.date
        df = df.reset_index(drop=True)
        return df


class FeatureEngineer:

    def __init__(self,
                stock_indicator_list = [],
                additional_indicators = [],
                cov_matrix = False):
        self.stock_indicator_list = stock_indicator_list
        self.additional_indicators = additional_indicators
        self.indicators = self.stock_indicator_list + self.additional_indicators
        self.cov_matrix = cov_matrix
    
    def create_data(self,df):
        df = self.clean_data(df)

        if self.cov_matrix:
            df = self.add_cov_matrix(df)

        if 'hurst_exp' in self.additional_indicators:
            df = self.add_hurst_exponent(df)
        if 'half_hour_time' in self.additional_indicators:
            df = self.add_half_hour_time(df)

        if 'vix_fix_1year' in self.additional_indicators:
            df = self.add_vix_fix(df,1)
        if 'sharpe_1year' in self.additional_indicators:
            df = self.add_sharpe(df,1)
        if 'sortino_1year' in self.additional_indicators:
            df = self.add_sortino(df,1)
        if 'calamar_1year' in self.additional_indicators:
            df = self.add_clamar(df,1)
        
        if 'vix_fix_3year' in self.additional_indicators:
            df = self.add_vix_fix(df,3)
        if 'sharpe_3year' in self.additional_indicators:
            df = self.add_sharpe(df,3)
        if 'sortino_3year' in self.additional_indicators:
            df = self.add_sortino(df,3)
        if 'calamar_3year' in self.additional_indicators:
            df = self.add_clamar(df,3)
        
        if 'vix_fix_5year' in self.additional_indicators:
            df = self.add_vix_fix(df,5)
        if 'sharpe_5year' in self.additional_indicators:
            df = self.add_sharpe(df,5)
        if 'sortino_5year' in self.additional_indicators:
            df = self.add_sortino(df,5)
        if 'calamar_5year' in self.additional_indicators:
            df = self.add_clamar(df,5)

        if len(self.stock_indicator_list)>0:
            df = self.add_stock_indicators(df)

        df.loc[:,self.indicators] = df[self.indicators].replace([np.inf, -np.inf], np.nan)
        df = df.fillna(method="ffill").fillna(method="bfill")
        df = df.sort_values(["date", "tic"], ignore_index=True)
        df.index = df["date"].factorize()[0]
        return df
    
    def time_series_split(self,df, start, end, target_date_col="date"):
        df = df.copy()
        data = df[(df[target_date_col] >= start) & (df[target_date_col] < end)]
        data.index = data[target_date_col].factorize()[0]
        return data
        
    def train_test_split(self,df,train_period,test_period):
        df = self.create_data(df)
        train = self.time_series_split(df, start = train_period[0], end = train_period[1])
        test = self.time_series_split(df, start = test_period[0], end = test_period[1])
        return train,test
    
    def clean_data(self,data):
        df = data.copy()
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(method="ffill").fillna(method="bfill")
        df = df.drop_duplicates(subset=['date','tic'])
        df = df.reset_index(drop=True)
        df = self.skip_missing_dates(df)
        df = self.remove_corrupt_ticker(df)
        df.index = df.date.factorize()[0]
        df=df.sort_values(['date','tic'],ignore_index=True)
        return df
    
    def remove_corrupt_ticker(self,df:pd.DataFrame):
        a = df.groupby('tic')['close'].apply(lambda x:sum(x==0))
        invalid_ticker = a[a>0].index.tolist()
        df = df[~df['tic'].isin(invalid_ticker)]
        df = df.reset_index(drop=True)
        print("Tickers with corrupt Data",invalid_ticker)
        print("Remaining ticker",df.tic.unique().tolist())
        return df
    
    def skip_missing_dates(self,df:pd.DataFrame):
        n_ticker = df['tic'].nunique()
        a = df.groupby('date')['tic'].count()
        invalid_dates = a[a<n_ticker].index.tolist()
        df = df[~df['date'].isin(invalid_dates)]
        df = df.reset_index(drop=True)
        return df
    
    def add_half_hour_time(self,df:pd.DataFrame):
        df['half_hour_time'] = [x.hour*2 +2 if int((x.minute//30)*30) else x.hour*2+1 for x in df['date']]
        return df
    
    def add_cov_matrix(self,df,lookback=252):
        df.index = df.date.factorize()[0]

        cov_list = []
        for i in range(lookback,len(df.index.unique())):
            data_lookback = df.loc[i-lookback:i,:]
            price_lookback=data_lookback.pivot_table(index = 'date',columns = 'tic', values = 'close')
            return_lookback = price_lookback.pct_change().dropna()
            return_lookback = return_lookback.replace([np.inf, -np.inf], np.nan)
            return_lookback = return_lookback.fillna(method="ffill").fillna(method="bfill")
            covs = return_lookback.cov().values 
            cov_list.append(covs)
        
        df_cov = pd.DataFrame({'date':df.date.unique()[lookback:],'cov_list':cov_list})
        df = df.merge(df_cov, on='date',how='left')
        return df
    
    def add_hurst_exponent(self,data,max_lag=20):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['hurst_exp'] = temp['close'].rolling(max_lag*2).apply(lambda x:self.get_hurst_exponent(x.values))
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", f'hurst_exp']], on=["tic", "date"], how="left")
        return df

    def get_hurst_exponent(self,time_series, max_lag=20):
        lags = range(2, max_lag)
        tau = [np.std(np.subtract(time_series[lag:], time_series[:-lag])) for lag in lags]
        reg = np.polyfit(np.log(lags), np.log(tau), 1)
        return reg[0]

    def add_sharpe(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[f'sharpe_{years}year'] = temp['daily_return'].rolling(days,min_periods=1).mean() / temp['daily_return'].rolling(days,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", f'sharpe_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_sortino(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True) 
            temp['daily_negative_return'] = temp['daily_return'] 
            temp.loc[(temp['daily_negative_return']>0),'daily_negative_return'] = 0
            temp[f'sortino_{years}year'] = temp['daily_negative_return'].rolling(days,min_periods=1).mean() / temp['daily_negative_return'].rolling(days,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'sortino_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_clamar(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_drawndown'] = temp['daily_return'].diff(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[f'calamar_{years}year'] = temp['daily_return'].rolling(days,min_periods=1).mean()/temp['daily_drawndown'].rolling(days,min_periods=1).min()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'calamar_{years}year']], on=["tic", "date"], how="left")
        return df
    
    def add_vix_fix(self,data,years):
        df = data.copy()
        days = years * 252
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp[f'vix_fix_{years}year'] = ((temp['close'].rolling(days,min_periods=1).max() \
                                         - temp['low'])/temp['close'].rolling(days,min_periods=1).max()) * 100
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", f'vix_fix_{years}year']], on=["tic", "date"], how="left")
        return df

    def add_stock_indicators(self,data):
        df = data.copy()
        stock = Sdf.retype(df.copy())
        unique_ticker = stock.tic.unique()
        for indicator in self.stock_indicator_list:
            indicator_df = pd.DataFrame()
            for i in range(len(unique_ticker)):
                try:
                    temp_indicator = stock[stock.tic == unique_ticker[i]][indicator]
                    temp_indicator = pd.DataFrame(temp_indicator)
                    temp_indicator["tic"] = unique_ticker[i]
                    temp_indicator["date"] = df[df.tic == unique_ticker[i]][
                        "date"
                    ].to_list()
                    indicator_df = indicator_df.append(temp_indicator, ignore_index=True)
                except Exception as e:
                    print(e)
            df = df.merge(indicator_df[["tic", "date", indicator]], on=["tic", "date"], how="left")
        return df

class DayTradeFeatureEngineer:

    def __init__(self,
                stock_indicator_list = [],
                additional_indicators = [],
                cov_matrix = False):
        self.stock_indicator_list = stock_indicator_list
        self.additional_indicators = additional_indicators
        self.indicators = self.stock_indicator_list + self.additional_indicators
        self.cov_matrix = cov_matrix
    
    def create_data(self,df):
        df = self.clean_data(df)

        if self.cov_matrix:
            df = self.add_cov_matrix(df)

        if 'hurst_exp' in self.additional_indicators:
            df = self.add_hurst_exponent(df)
        if 'half_hour_time' in self.additional_indicators:
            df = self.add_half_hour_time(df)

        if 'vix_fix_1day' in self.additional_indicators:
            df = self.add_vix_fix(df,86_400,'vix_fix_1day')
        if 'sharpe_1day' in self.additional_indicators:
            df = self.add_sharpe(df,86_400,'sharpe_1day')
        if 'sortino_1day' in self.additional_indicators:
            df = self.add_sortino(df,86_400,'sortino_1day')
        if 'calamar_1day' in self.additional_indicators:
            df = self.add_clamar(df,86_400,'calamar_1day')
        
        if 'vix_fix_4hour' in self.additional_indicators:
            df = self.add_vix_fix(df,14_400,'vix_fix_4hour')
        if 'sharpe_4hour' in self.additional_indicators:
            df = self.add_sharpe(df,14_400,'sharpe_4hour')
        if 'sortino_4hour' in self.additional_indicators:
            df = self.add_sortino(df,14_400,'sortino_4hour')
        if 'calamar_4hour' in self.additional_indicators:
            df = self.add_clamar(df,14_400,'calamar_4hour')
        
        if 'vix_fix_1hour' in self.additional_indicators:
            df = self.add_vix_fix(df,3600,'vix_fix_1hour')
        if 'sharpe_1hour' in self.additional_indicators:
            df = self.add_sharpe(df,3600,'sharpe_1hour')
        if 'sortino_1hour' in self.additional_indicators:
            df = self.add_sortino(df,3600,'sortino_1hour')
        if 'calamar_1hour' in self.additional_indicators:
            df = self.add_clamar(df,3600,'calamar_1hour')
        
        if 'vix_fix_30min' in self.additional_indicators:
            df = self.add_vix_fix(df,1800,'vix_fix_30min')
        if 'sharpe_30min' in self.additional_indicators:
            df = self.add_sharpe(df,1800,'sharpe_30min')
        if 'sortino_30min' in self.additional_indicators:
            df = self.add_sortino(df,1800,'sortino_30min')
        if 'calamar_30min' in self.additional_indicators:
            df = self.add_clamar(df,1800,'calamar_30min')
        
        if 'vix_fix_15min' in self.additional_indicators:
            df = self.add_vix_fix(df,900,'vix_fix_15min')
        if 'sharpe_15min' in self.additional_indicators:
            df = self.add_sharpe(df,900,'sharpe_15min')
        if 'sortino_15min' in self.additional_indicators:
            df = self.add_sortino(df,900,'sortino_15min')
        if 'calamar_15min' in self.additional_indicators:
            df = self.add_clamar(df,900,'calamar_15min')

        if len(self.stock_indicator_list)>0:
            df = self.add_stock_indicators(df)

        df.loc[:,self.indicators] = df[self.indicators].replace([np.inf, -np.inf], np.nan)
        df = df.fillna(method="ffill").fillna(method="bfill")
        df = df.sort_values(["date", "tic"], ignore_index=True)
        df['closing time'] = df.groupby('date')['date'].transform(lambda x:(x==x.max))
        df.index = df["date"].factorize()[0]
        return df
    
    def time_series_split(self,df, start, end, target_date_col="date"):
        df = df.copy()
        data = df[(df[target_date_col] >= start) & (df[target_date_col] < end)]
        data.index = data[target_date_col].factorize()[0]
        return data
        
    def train_test_split(self,df,train_period,test_period):
        df = self.create_data(df)
        train = self.time_series_split(df, start = train_period[0], end = train_period[1])
        test = self.time_series_split(df, start = test_period[0], end = test_period[1])
        return train,test
    
    def clean_data(self,data):
        df = data.copy()
        df = df.replace([np.inf, -np.inf], np.nan)
        df = df.fillna(method="ffill").fillna(method="bfill")
        df = df.drop_duplicates(subset=['date','tic'])
        df = df.reset_index(drop=True)
        df = self.skip_missing_dates(df)
        df = self.remove_corrupt_ticker(df)
        df.index = df.date.factorize()[0]
        df=df.sort_values(['date','tic'],ignore_index=True)
        return df
    
    def remove_corrupt_ticker(self,df:pd.DataFrame):
        a = df.groupby('tic')['close'].apply(lambda x:sum(x==0))
        invalid_ticker = a[a>0].index.tolist()
        df = df[~df['tic'].isin(invalid_ticker)]
        df = df.reset_index(drop=True)
        print("Tickers with corrupt Data",invalid_ticker)
        print("Remaining ticker",df.tic.unique().tolist())
        return df
    
    def skip_missing_dates(self,df:pd.DataFrame):
        n_ticker = df['tic'].nunique()
        a = df.groupby('date')['tic'].count()
        invalid_dates = a[a<n_ticker].index.tolist()
        df = df[~df['date'].isin(invalid_dates)]
        df = df.reset_index(drop=True)
        return df
    
    def add_half_hour_time(self,df:pd.DataFrame):
        df['half_hour_time'] = [x.hour*2 +2 if int((x.minute//30)*30) else x.hour*2+1 for x in df['date']]
        return df
    
    def add_cov_matrix(self,df,lookback=252):
        df.index = df.date.factorize()[0]

        cov_list = []
        for i in range(lookback,len(df.index.unique())):
            data_lookback = df.loc[i-lookback:i,:]
            price_lookback=data_lookback.pivot_table(index = 'date',columns = 'tic', values = 'close')
            return_lookback = price_lookback.pct_change().dropna()
            return_lookback = return_lookback.replace([np.inf, -np.inf], np.nan)
            return_lookback = return_lookback.fillna(method="ffill").fillna(method="bfill")
            covs = return_lookback.cov().values 
            cov_list.append(covs)
        
        df_cov = pd.DataFrame({'date':df.date.unique()[lookback:],'cov_list':cov_list})
        df = df.merge(df_cov, on='date',how='left')
        return df
    
    def add_hurst_exponent(self,data,max_lag=20):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['hurst_exp'] = temp['close'].rolling(max_lag*2).apply(lambda x:self.get_hurst_exponent(x.values))
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", f'hurst_exp']], on=["tic", "date"], how="left")
        return df

    def get_hurst_exponent(self,time_series, max_lag=20):
        lags = range(2, max_lag)
        tau = [np.std(np.subtract(time_series[lag:], time_series[:-lag])) for lag in lags]
        reg = np.polyfit(np.log(lags), np.log(tau), 1)
        return reg[0]

    def add_sharpe(self,data,n,name):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[name] = temp['daily_return'].rolling(n,min_periods=1).mean() / temp['daily_return'].rolling(n,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True )
        df = df.merge(indicator_df[["tic", "date", name]], on=["tic", "date"], how="left")
        return df
    
    def add_sortino(self,data,n,name):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_return'].fillna(0,inplace=True) 
            temp['daily_negative_return'] = temp['daily_return'] 
            temp.loc[(temp['daily_negative_return']>0),'daily_negative_return'] = 0
            temp[name] = temp['daily_negative_return'].rolling(n,min_periods=1).mean() / temp['daily_negative_return'].rolling(n,min_periods=1).std()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date",name]], on=["tic", "date"], how="left")
        return df
    
    def add_clamar(self,data,n,name):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp['daily_return'] = temp['close'].pct_change(1)
            temp['daily_drawndown'] = temp['daily_return'].diff(1)
            temp['daily_return'].fillna(0,inplace=True)
            temp[name] = temp['daily_return'].rolling(n,min_periods=1).mean()/temp['daily_drawndown'].rolling(n,min_periods=1).min()
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date",name]], on=["tic", "date"], how="left")
        return df
    
    def add_vix_fix(self,data,n,name):
        df = data.copy()
        unique_ticker = df.tic.unique()
        indicator_df = pd.DataFrame()
        for ticker in unique_ticker:
            temp = df[(df['tic'] == ticker)].copy()
            temp[name] = ((temp['close'].rolling(n,min_periods=1).max() \
                                         - temp['low'])/temp['close'].rolling(n,min_periods=1).max()) * 100
            indicator_df = indicator_df.append(temp, ignore_index=True)
        df = df.merge(indicator_df[["tic", "date", name]], on=["tic", "date"], how="left")
        return df

    def add_stock_indicators(self,data):
        df = data.copy()
        stock = Sdf.retype(df.copy())
        unique_ticker = stock.tic.unique()
        for indicator in self.stock_indicator_list:
            indicator_df = pd.DataFrame()
            for i in range(len(unique_ticker)):
                try:
                    temp_indicator = stock[stock.tic == unique_ticker[i]][indicator]
                    temp_indicator = pd.DataFrame(temp_indicator)
                    temp_indicator["tic"] = unique_ticker[i]
                    temp_indicator["date"] = df[df.tic == unique_ticker[i]][
                        "date"
                    ].to_list()
                    indicator_df = indicator_df.append(temp_indicator, ignore_index=True)
                except Exception as e:
                    print(e)
            df = df.merge(indicator_df[["tic", "date", indicator]], on=["tic", "date"], how="left")
        return df
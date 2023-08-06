# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pro数据接口 
Created on 2017/07/01
@author: polo,Jimmy
@group : tushare.pro
"""
import re

import pandas as pd
import simplejson as json
from functools import partial
import requests
import os
from diskcache import Cache
from tqdm import tqdm

from sharecharts.utils import get_token, set_token, DT, Code, Unit
import datetime as dt
import numpy as np

PRICE_COLS = ['open', 'close', 'high', 'low', 'pre_close']


def number_format(x):
    return '%.2f' % x


FREQUENCY = {'D': '1DAY', 'W': '1WEEK', 'Y': '1YEAR'}


def ma(series: pd.Series, window: int) -> pd.Series:
    return pd.Series.rolling(series, window).mean()


home = os.path.expanduser("~").replace("\\", "/")
cache = Cache(directory=home + "/.share_cache", timeout=60, sqlite_synchronous=0)


class DataApi:
    __token = ''
    __http_url = 'http://api.tushare.pro'

    def __init__(self, token, timeout=10):
        """
        Parameters
        ----------
        token: str
            API接口TOKEN，用于用户认证
        """
        self.__token = token
        self.__timeout = timeout

    @staticmethod
    def delete_cache(count=15):
        days = pd.date_range(dt.datetime.now() - dt.timedelta(days=count), dt.datetime.now())
        bar_keys = ["_daily_bar_cache-" + day.strftime("%Y%m%d") for day in days]
        val_keys = ["_daily_valuation_cache-" + day.strftime("%Y%m%d") for day in days]
        all_keys = bar_keys + val_keys
        cache.iterkeys()
        for key in cache.iterkeys():
            if key[0:2] == '20' or key in all_keys:
                cache.delete(key)
        return "ok"

    @staticmethod
    def normalize_code(codes) -> list:
        """规范化代码"""
        nums = [re.findall("\\d{6}", code)[0] for code in codes]
        return [num + ".SZ" if num[0] in ['0', '1', '3'] else num + ".SH" for num in nums]

    def trade_days(self, start_date=None, end_date=None, count=None) -> np.array:
        """
        获取给定区间的交易日期
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param count: 数量
        :return:
        """
        end_date = dt.datetime.now() if end_date is None else end_date
        key = "交易日_base"
        with cache:
            cached = cache.get(key)
        if cached is None:
            df = self.trade_cal(exchange='', start_date=DT(dt.datetime(2010, 1, 1)).tushare(),
                                end_date=DT(dt.datetime.now() + dt.timedelta(days=365)).tushare(),
                                is_open='1')
            days = np.array(pd.to_datetime(df['cal_date']).tolist())
            with cache:
                cache.set(key, days, expire=86400, retry=True)
            cached = days
        if start_date is None:
            return cached[cached <= pd.to_datetime(end_date.strftime("%Y-%m-%d"))][-count:]
        else:
            return cached[(cached >= pd.to_datetime(start_date.strftime("%Y-%m-%d"))) & (
                    cached <= pd.to_datetime(end_date.strftime("%Y-%m-%d")))]

    def last_closed_trade_day(self, end_date=None) -> dt.datetime:
        """最后一个收盘的交易日"""
        end_date = dt.datetime.now() if end_date is None else end_date
        trade_days = self.trade_days(end_date=end_date, count=5)
        if (dt.datetime.now() - trade_days[-1]).days == 0 and end_date.hour * 60 + end_date.minute < 901:
            # 今天是交易日，沒有收盤
            return trade_days[-2]
        else:
            return trade_days[-1]

    def is_open(self, date=None) -> bool:
        """
        给定日期是不是交易日
        :return:
        """
        date = dt.datetime.now() if date is None else date
        days = self.trade_days(end_date=date, count=1)
        return pd.to_datetime(date.strftime("%Y-%m-%d")) in days

    def __daily_bar_cache(self, date):
        """
        每日K线数据
        :param date:
        :return:
        """
        key = "_daily_bar_cache-" + date.strftime('%Y%m%d')
        with cache:
            cached = cache.get(key)
        if cached is None:
            df_price = self.daily(trade_date=DT(date).tushare())
            if df_price.shape[0] > 0:
                df_price['vol'] = df_price['vol'] * 100
                df_price['amount'] = df_price['amount'] * 1000
                df_price['ts_code'] = self.normalize_code(df_price['ts_code'])
                df_price['trade_date'] = pd.to_datetime(df_price['trade_date'])
            elif self.last_closed_trade_day().date() == date.date():
                codes = [Code(code).number() for code in self.stock_basic().index]
                dfs = []
                for i in range(0, len(codes), 80):
                    dfs.append(self.__tdx_quotes(codes[i:i + 80]))
                df = pd.concat(dfs)
                df_price = df[['code', 'price', 'open', 'high', 'low', 'vol', 'amount', 'last_close']].copy()
                df_price.columns = ['ts_code', 'close', 'open', 'high', 'low', 'vol', 'amount', 'pre_close']
                df_price['change'] = df_price['close'] - df_price['pre_close']
                df_price['pct_chg'] = df_price['close'] / df_price['pre_close'] - 1
                df_price['trade_date'] = pd.to_datetime(date.strftime('%Y-%m-%d'))
                df_price['ts_code'] = self.normalize_code(df_price['ts_code'])
                df_price['vol'] = df_price['vol'] * 100
            else:
                return None
            df_adj = self.adj_factor(trade_date=DT(date).tushare())
            df_adj['ts_code'] = self.normalize_code(df_adj['ts_code'])
            df_adj['trade_date'] = pd.to_datetime(df_adj['trade_date'])
            df_limit = self.stk_limit(trade_date=DT(date).tushare())
            df_limit['ts_code'] = self.normalize_code(df_limit['ts_code'])
            df_limit['trade_date'] = pd.to_datetime(df_limit['trade_date'])
            df_ret = df_price.merge(df_adj, left_on=['ts_code', 'trade_date'], right_on=['ts_code', 'trade_date'],
                                    how='left')
            df_ret1 = df_ret.merge(df_limit, left_on=['ts_code', 'trade_date'], right_on=['ts_code', 'trade_date'],
                                   how='left')
            df_ret2 = df_ret1[
                ['ts_code', 'trade_date', 'open', 'high', 'low', 'close', 'vol', 'amount', 'pre_close', 'change',
                 'pct_chg', 'adj_factor', 'up_limit',
                 'down_limit']].copy()
            if df_ret2.shape[0] > 0:
                with cache:
                    cache.set(key, df_ret2, retry=True)
            return df_ret2



        else:
            return cached

    def __daily_valuation_cache(self, date):
        """
        每日估值数据
        :param date:
        :return:
        """
        key = "_daily_valuation_cache-" + date.strftime('%Y%m%d')
        with cache:
            cached = cache.get(key)
        if cached is None:
            df = self.query('daily_basic', trade_date=DT(date).tushare(),
                            fields='ts_code,trade_date,turnover_rate,turnover_rate_f,volume_ratio,pe_ttm,pb,total_mv,circ_mv')
            df['total_mv'] = df['total_mv'] * 10000
            df['circ_mv'] = df['circ_mv'] * 10000
            if df.shape[0] > 0:
                with cache:
                    cache.set(key, df, retry=True)
            return df
        else:
            return cached

    @staticmethod
    def __adj_fields(df_pivot: pd.DataFrame, arr_adj: pd.DataFrame, multi=1) -> pd.DataFrame:
        '''
        针对tushare 以千,万,手为单位的字段,转换成1为单位
        :param df_pivot:
        :param arr_adj:
        :param multi:
        :return:
        '''
        return pd.DataFrame(df_pivot.values * arr_adj * multi, columns=df_pivot.columns, index=df_pivot.index)

    def panel_value(self, end_date=None, count=255, use_cache=True):
        """
        估值数据面板
        :param end_date:
        :param count:
        :param use_cache:
        :return:
        """
        end_date = dt.datetime.now() if end_date is None else end_date
        last_day = self.last_closed_trade_day(end_date)
        trade_days = self.trade_days(end_date=last_day, count=count)
        key = last_day.strftime("%Y%m%d") + "daily_valuation_panel" + str(count)
        with cache:
            cached = cache.get(key)
        if cached is None or use_cache is False:
            dfs = []
            for date in tqdm(trade_days):
                dfs.append(self.__daily_valuation_cache(date))
            df_all = pd.concat(dfs)
            df_all['ts_code'] = df_all['ts_code'].str.replace("SH", 'XSHG').str.replace('SZ', 'XSHE')
            df_all['trade_date'] = pd.to_datetime(df_all['trade_date'])
            df_turnover_rate = df_all.pivot(index='trade_date', columns='ts_code', values='turnover_rate')
            df_turnover_rate_f = df_all.pivot(index='trade_date', columns='ts_code', values='turnover_rate_f')
            df_volume_ratio = df_all.pivot(index='trade_date', columns='ts_code', values='volume_ratio')
            df_pe_ttm = df_all.pivot(index='trade_date', columns='ts_code', values='pe_ttm')
            df_pb = df_all.pivot(index='trade_date', columns='ts_code', values='pb')
            df_total_mv = df_all.pivot(index='trade_date', columns='ts_code', values='total_mv')
            df_circ_mv = df_all.pivot(index='trade_date', columns='ts_code', values='circ_mv')
            ret = {"换手率": df_turnover_rate, "流通换手率": df_turnover_rate_f,
                   '量比': df_volume_ratio, 'PE_TTM': df_pe_ttm, 'PB': df_pb,
                   '总市值(亿)': df_total_mv, '流通市值(亿)': df_circ_mv
                   }
            with cache:
                cache.set(key, ret, 28800, retry=True)
            return ret
        else:
            return cached

    @staticmethod
    def convert_tushare_df(df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            if 'time' in col:
                df[col] = pd.to_datetime(df[col])
        return df

    def panel_kline(self, end_date=None, count=255, use_cache=True):
        """
        股票K线Panel
        :param end_date:
        :param count:
        :param use_cache:
        :return:
        """
        end_date = dt.datetime.now() if end_date is None else end_date
        last_day = self.last_closed_trade_day(end_date)
        trade_days = self.trade_days(end_date=last_day, count=count)
        key = last_day.strftime("%Y%m%d") + "daily_bar_panel" + str(count)
        data_missing = False
        with cache:
            cached = cache.get(key)
        if cached is None or use_cache is False:
            with cache:
                df_old = cache.get("all_kline")
            old_days = [] if df_old is None else list(pd.to_datetime(df_old['trade_date'].unique()))
            need_update_days = set(trade_days.tolist()).difference(set(old_days))
            if df_old is None:
                dfs = []
            else:
                dfs = [df_old]
            for date in tqdm(need_update_days):
                df_day = self.__daily_bar_cache(date)
                if df_day is not None and df_day.shape[0] > 0:
                    dfs.append(df_day)
                else:
                    data_missing = True
            df_all = pd.concat(dfs)
            df_all = df_all.drop_duplicates(subset=['ts_code', 'trade_date'])
            df_all['ts_code'] = df_all['ts_code'].astype("category")
            cache.set("all_kline", df_all, 2592000)
            df_all = df_all[df_all['trade_date'] > trade_days[0]].copy()
            df_all_pivot = df_all.pivot(index='trade_date', columns='ts_code',
                                        values=['adj_factor', 'open', 'high', 'low', 'close', 'vol', 'amount',
                                                'up_limit', 'down_limit'])
            df_adj = df_all_pivot['adj_factor'].fillna(method='ffill')
            arr_adj = df_adj.values / df_adj.iloc[-1].values
            df_open = df_all_pivot['open']
            df_close = df_all_pivot['close']
            df_high = df_all_pivot['high']
            df_low = df_all_pivot['low']
            df_volume = df_all_pivot['vol'].fillna(0)
            df_money = df_all_pivot['amount'].fillna(0)
            df_up_limit = df_all_pivot['up_limit'].fillna(method='ffill')
            df_down_limit = df_all_pivot['down_limit'].fillna(method='ffill')
            df_open = self.__adj_fields(df_open, arr_adj)
            df_close = self.__adj_fields(df_close, arr_adj)
            df_pre_close = df_close.shift(1)
            df_high = self.__adj_fields(df_high, arr_adj)
            df_low = self.__adj_fields(df_low, arr_adj)
            df_high_limit = self.__adj_fields(df_up_limit,
                                              arr_adj)
            df_low_limit = self.__adj_fields(df_down_limit,
                                             arr_adj)
            df_money = pd.DataFrame(df_money.values,
                                    columns=df_volume.columns, index=df_volume.index)
            ret = {"open": df_open, "high": df_high, 'low': df_low, 'close': df_close, 'volume': df_volume,
                   'money': df_money, 'pre_close': df_pre_close, 'high_limit': df_high_limit, 'low_limit': df_low_limit
                   }
            if data_missing is False:
                with cache:
                    cache.set(key, ret, 259200, retry=True)
            return ret
        else:
            return cached

    def query(self, api_name, fields='', **kwargs):
        req_params = {
            'api_name': api_name,
            'token': self.__token,
            'params': kwargs,
            'fields': fields
        }

        res = requests.post(self.__http_url, json=req_params, timeout=self.__timeout)
        result = json.loads(res.text)
        if result['code'] != 0:
            raise Exception(result['msg'])
        data = result['data']
        columns = data['fields']
        items = data['items']

        return pd.DataFrame(items, columns=columns)

    def symbols_search(self, keyword: str, asset: str = "E") -> pd.DataFrame:
        """
        查询标的代码
        :param keyword:
        :param asset:
        :return:
        """
        asset = asset.strip().upper()
        if asset == 'E':
            df = self.query("stock_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]
        elif asset == 'E':
            df = self.query("hk_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]
        elif asset == "I":
            df = self.query("index_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]
        elif asset == "FD":
            df = self.query("fund_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]
        elif asset == "FT":
            df = self.query("fut_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]
        elif asset == "CB":
            df = self.query("cb_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['bond_short_name'].str.contains(keyword))]
        else:
            df = self.query("stock_basic")
            return df[(df['ts_code'].str.contains(keyword)) | (df['name'].str.contains(keyword))]

    def pro_bar(self, ts_code='', start_date=None, end_date=None, freq='D', asset='E',
                exchange='',
                adj=None,
                mas=[],
                contract_type='',
                retry_count=3) -> pd.DataFrame:
        """
        BAR数据
        Parameters:
        ------------
        ts_code:证券代码，支持股票,ETF/LOF,期货/期权,港股,数字货币
        start_date:开始日期  YYYYMMDD
        end_date:结束日期 YYYYMMDD
        freq:支持1/5/15/30/60分钟,周/月/季/年
        asset:证券类型 E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
        exchange:市场代码，用户数字货币行情
        adj:复权类型,None不复权,qfq:前复权,hfq:后复权
        ma:均线,支持自定义均线频度，如：ma5/ma10/ma20/ma60/maN
        factors因子数据，目前支持以下两种：
            vr:量比,默认不返回，返回需指定：factor=['vr']
            tor:换手率，默认不返回，返回需指定：factor=['tor']
                        以上两种都需要：factor=['vr', 'tor']
        retry_count:网络重试次数

        Return
        ----------
        DataFrame
        code:代码
        open：开盘close/high/low/vol成交量/amount成交额/maN均价/vr量比/tor换手率

             期货(asset='X')
        code/open/close/high/low/avg_price：均价  position：持仓量  vol：成交总量
        """
        ts_code = ts_code.strip().upper() if asset != 'E' else ts_code.strip().lower()
        for _ in range(retry_count):
            try:
                freq = freq.strip().upper()
                asset = asset.strip().upper()
                if asset == 'E':
                    if freq == 'D':
                        df = self.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
                        ds = self.daily_basic(ts_code=ts_code, start_date=start_date, end_date=end_date)[
                            ['trade_date', 'turnover_rate', 'volume_ratio', 'total_share', 'float_share', 'free_share']]
                        ds = ds.set_index('trade_date')
                        df = df.set_index('trade_date')
                        df = df.merge(ds, left_index=True, right_index=True)
                        df = df.reset_index()

                    if freq == 'W':
                        df = self.weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
                    if freq == 'M':
                        df = self.monthly(ts_code=ts_code, start_date=start_date, end_date=end_date)
                    if adj is not None:
                        fcts = self.adj_factor(ts_code=ts_code, start_date=start_date, end_date=end_date)[
                            ['trade_date', 'adj_factor']]
                        data = df.set_index('trade_date', drop=False).merge(fcts.set_index('trade_date'),
                                                                            left_index=True,
                                                                            right_index=True, how='left')
                        data['adj_factor'] = data['adj_factor'].fillna(method='bfill')
                        for col in PRICE_COLS:
                            if adj == 'hfq':
                                data[col] = data[col] * data['adj_factor']
                            else:
                                data[col] = data[col] * data['adj_factor'] / float(fcts['adj_factor'][0])
                            data[col] = data[col].map(number_format)
                        if adj == 'hfq':
                            data['vol'] = data['vol'] / data['adj_factor']
                        else:
                            data['vol'] = data['vol'] / data['adj_factor'] * float(fcts['adj_factor'][0])
                        for col in PRICE_COLS:
                            data[col] = data[col].astype(float)
                        data = data.drop('adj_factor', axis=1)
                        df['change'] = df['close'] - df['pre_close']
                        df['pct_change'] = df['close'].pct_change() * 100
                    else:
                        data = df
                elif asset == 'I':
                    if freq == 'D':
                        data = self.index_daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
                elif asset == 'FT':
                    if freq == 'D':
                        data = self.fut_daily(ts_code=ts_code, start_dae=start_date, end_date=end_date,
                                              exchange=exchange)
                elif asset == 'O':
                    if freq == 'D':
                        data = self.opt_daily(ts_code=ts_code, start_dae=start_date, end_date=end_date,
                                              exchange=exchange)
                elif asset == 'FD':
                    if freq == 'D':
                        data = self.fund_daily(ts_code=ts_code, start_dae=start_date, end_date=end_date)
                elif asset == 'HK':
                    if freq == 'D':
                        data = self.hk_daily(ts_code=ts_code, start_dae=start_date, end_date=end_date)
                if asset == 'C':
                    if freq == 'D':
                        freq = 'daily'
                    elif freq == 'W':
                        freq = 'week'
                    data = self.coinbar(exchange=exchange, symbol=ts_code, freq=freq, start_dae=start_date,
                                        end_date=end_date,
                                        contract_type=contract_type)
                if mas is not None and len(mas) > 0:
                    for a in mas:
                        if isinstance(a, int):
                            data['ma%s' % a] = mas(data['close'], a).map(number_format).shift(-(a - 1))
                            data['ma%s' % a] = data['ma%s' % a].astype(float)
                            data['ma_v_%s' % a] = mas(data['vol'], a).map(number_format).shift(-(a - 1))
                            data['ma_v_%s' % a] = data['ma_v_%s' % a].astype(float)
                data['trade_date'] = pd.to_datetime(data['trade_date'])
                data = data.set_index('trade_date', drop=True)
                return data
            except Exception as e:
                print(e)
                return None
            else:
                return
        raise IOError('ERROR.')

    def __getattr__(self, name):
        if name not in self.__dict__:
            self.__dict__[name] = partial(self.query, name)
        return partial(self.query, name)


def pro_api(token=''):
    """
    初始化pro API
    """
    if token is not None and token != '':
        set_token(token)
    else:
        token = get_token()
    if token is not None and token != '':
        return DataApi(token)
    else:
        raise Exception('api init error.')


__all__ = ['pro_api']

if __name__ == '__main__':
    pro = pro_api()
    df = pro.symbols_search('000001.SZ')
    print(df)

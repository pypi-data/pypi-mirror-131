import pandas as pd
import os


def set_token(token):
    df = pd.DataFrame([token], columns=['token'])
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, "tk.csv")
    df.to_csv(fp, index=False)


def get_token():
    user_home = os.path.expanduser('~')
    fp = os.path.join(user_home, "tk.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        return str(df.iloc[0]['token'])
    else:
        print('请设置tushare pro的token凭证码，如果没有请访问https://tushare.pro注册申请')
        return None


import datetime as dt


class Code(object):

    def __init__(self, code):
        if code.endswith('.SZ') or code.endswith('.SH') or code.endswith('.HK'):  # tushare格式
            self.code = code.replace('.SH', '.XSHG').replace('.SZ', '.XSHE')
        elif len(code) == 8 and (code.startswith('sh') or code.startswith('sz')):
            self.code = code[2:8] + code[0:2].replace('sh', '.XSHG').replace('sz', '.XSHE')
        elif len(code) == 9 and (code.startswith('sh') or code.startswith('sz')):
            self.code = code[3:9] + code[0:3].replace('sh.', '.XSHG').replace('sz.', '.XSHE')
        elif len(code) == 11 and (code.startswith('SHSE') or code.startswith('SZSE')):
            self.code == code[5:] + code[0:4].replace('SZSE', '.XSHE').replace('SHSE', '.XSHG')
        else:
            self.code = code

    @staticmethod
    def all():
        return "tushare(000001.SZ)/jq(000001.XSHE)/akshare(sz000001)/number(000001)/gm(SHSE.000001)"

    @staticmethod
    def convert_ths(s):
        return s.apply(lambda cell: cell.replace('.SH', '.XSHG').replace('.SZ', '.XSHE'))

    def tushare(self):
        return self.code.replace('.XSHE', '.SZ').replace('.XSHG', '.SH')

    def gm(self):
        return self.code[7:].replace('XSHE', 'SZSE').replace('XSHG', 'SHSE') + "." + self.code[:6]

    def jq(self):
        return self.code

    def akshare(self):
        return self.code[6, 11].replace('.XSHE', 'sz').replace('.XSHG', 'sh') + self.code[0:6]

    def number(self):
        return self.code.split(".")[0]


class DT(object):
    def __init__(self, dates: dt.datetime):
        self.dt = dates

    @staticmethod
    def all():
        return "tushare(%Y%m%d)/baostock(%Y-%m-%d)/jqdata/hkstock"

    def tushare(self) -> str:
        return self.dt.strftime("%Y%m%d")

    def baostock(self) -> str:
        return self.dt.strftime("%Y-%m-%d")

    def jqdata(self) -> str:
        return self.dt

    def gmsdk(self) -> str:
        return self.dt


class Unit(object):
    def __init__(self, unit: str):
        """1m 1d 1w 1M"""
        self.unit = unit

    @staticmethod
    def all() -> str:
        return "1m/5m/15m/30m/60m/1d/1w/1M"

    def gm(self) -> str:
        if self.unit[-1] == 'm':
            return str(int(self.unit[:-1]) * 60) + "s"
        elif self.unit[-1] == 'd':
            return "1d"

    def baostock(self) -> str:
        if self.unit[-1] == 'm':
            return self.unit[:-1]
        elif self.unit[-1] == 'd':
            return "d"
        elif self.unit[-1] == 'w':
            return "w"
        elif self.unit[-1] == 'M':
            return "m"

    def tushare(self) -> str:
        if self.unit[-1] == 'm':
            return self.unit[:-1] + "min"
        elif self.unit[-1] == 'd':
            return "D"
        elif self.unit[-1] == 'w':
            return "W"
        elif self.unit[-1] == 'M':
            return "M"

    def tdx(self) -> int:
        """
        0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线 5 周K线 6 月K线
        7 1分钟K线 8 1分钟K线 9 日K线 10 季K线 11 年K线
        :return:
        """
        if self.unit == '5m':
            return 0
        elif self.unit == '15m':
            return 1
        elif self.unit == '30m':
            return 2
        elif self.unit == '60m':
            return 3
        elif self.unit == '1m':
            return 7
        elif self.unit == '1d':
            return 9
        elif self.unit == '1w':
            return 5
        elif self.unit == '1M':
            return 6
        else:
            return 9


class Adjust(object):
    def __init__(self, adj: str):
        self.adj = adj

    @staticmethod
    def all() -> str:
        return "qfq/hfq/ "

    def baostock(self) -> str:
        if self.adj == 'qfq':
            return 2
        elif self.adj == 'hfq':
            return 1
        elif self.adj == '':
            return 3

    def tushare(self) -> str:
        if self.adj == 'qfq':
            return 'qfq'
        elif self.adj == 'hfq':
            return 'hfq'
        elif self.adj == '':
            return None

    def jqdata(self) -> str:
        if self.adj == 'qfq':
            return 'pre'
        elif self.adj == 'hfq':
            return 'post'
        elif self.adj == '':
            return None

    def gm(self) -> int:
        if self.adj == 'qfq':
            return 1
        elif self.adj == 'hfq':
            return 2
        elif self.adj == '':
            return 0


__all__ = ['Code', 'DT', 'Adjust', 'Unit', 'get_token', 'set_token']

"""
套利FOF回测模块
"""
import numpy as np
from sqlalchemy import create_engine
from hbshare.quant_research.Kevin.rm_associated.util.data_loader import get_trading_day_list
import pandas as pd
import datetime
import hbshare as hbs

sql_params = {
    "ip": "192.168.223.152",
    "user": "readonly",
    "pass": "c24mg2e6",
    "port": "3306",
    "database": "work"
}

engine_params = "mysql+pymysql://{}:{}@{}:{}/{}".format(sql_params['user'], sql_params['pass'], sql_params['ip'],
                                                        sql_params['port'], sql_params['database'])


def get_fund_data_from_sql(start_date, end_date, fund_dict):
    nav_series_list = []
    for name, fund_id in fund_dict.items():
        sql_script = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
                     "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                     "and a.jjzt not in ('3') " \
                     "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                     "order by b.jzrq".format(fund_id, start_date, end_date)
        res = hbs.db_data_query("highuser", sql_script, page_size=5000)
        data = pd.DataFrame(res['data']).set_index('TRADEDATE')['ADJ_NAV']
        data.name = name
        nav_series_list.append(data)
    df = pd.concat(nav_series_list, axis=1).sort_index()

    return df


def get_fund_data_from_work(start_date, end_date, fund_id):
    sql_script = "SELECT name, t_date, nav FROM fund_data where " \
                 "t_date >= {} and t_date <= {} and code = '{}'".format(start_date, end_date, fund_id)
    engine = create_engine(engine_params)
    data = pd.read_sql(sql_script, engine)
    data['t_date'] = data['t_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))

    return data


def cal_annual_return(return_series):
    T = len(return_series)
    annual_return = (1 + return_series).prod() ** (52 / T) - 1

    return annual_return


def cal_annual_volatility(return_series):
    vol = return_series.std() * np.sqrt(52)

    return vol


def cal_max_drawdown(nav_series):
    drawdown_series = nav_series / (nav_series.cummax()) - 1

    return drawdown_series.min()


def cal_sharpe_ratio(return_series, rf):
    annual_return = cal_annual_return(return_series)
    vol = cal_annual_volatility(return_series)
    sharpe_ratio = (annual_return - rf) / vol

    return sharpe_ratio


if __name__ == '__main__':
    s_date = '20200103'
    e_date = '20211126'

    f_dict = {
        "展弘稳进1号1期": "SE8723",
        "盛冠达股指套利3号": "SGS597",
        "稳博中睿6号": "SJB143"
    }

    date_list = get_trading_day_list(s_date, e_date, frequency='week')

    nav_df = get_fund_data_from_sql(s_date, e_date, f_dict).reindex(date_list).fillna(method='ffill')

    mx_df = pd.read_excel('D:\\蒙玺竞起6号净值.xlsx', sheet_name=0)
    mx_df['trade_date'] = mx_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
    mx_df.rename(columns={"nav": "蒙玺竞起6号"}, inplace=True)
    mx_df = mx_df.set_index('trade_date').reindex(date_list).dropna()

    nav_df = pd.concat([nav_df, mx_df], axis=1)
    return_df = nav_df.pct_change().fillna(0.)

    # 等权
    weight_df1 = pd.DataFrame(index=return_df.index, columns=return_df.columns)
    weight_df1.loc['20200103', :] = [1/3, 1/3, 1/3, 0]

    rbl_list = ['20201120']

    for i in range(1, len(return_df)):
        date = return_df.index[i]
        weight_df1.iloc[i, :] = weight_df1.iloc[i - 1, :] * (1 + return_df.iloc[i, :])
        if date in rbl_list:
            weight_df1.loc[date] = weight_df1.loc[date].mean()

    port_nav1 = weight_df1.sum(axis=1)

    # 额度加权
    weight_df2 = pd.DataFrame(index=return_df.index, columns=return_df.columns)
    weight_df2.loc['20200103', :] = [4/9, 1/9, 4/9, 0]
    weight_df2.loc['20201120', :] = [4/11, 1/11, 4/11, 2/11]

    rbl_list = ['20201120']

    for i in range(1, len(return_df)):
        date = return_df.index[i]
        weight_df2.iloc[i, :] = weight_df2.iloc[i - 1, :] * (1 + return_df.iloc[i, :])
        if date in rbl_list:
            weight_df2.loc[date] = [weight_df2.loc[date].sum() * x for x in [4/11, 1/11, 4/11, 2/11]]

    port_nav2 = weight_df2.sum(axis=1)

    # 净值
    port_nav = pd.concat([port_nav1.to_frame('等权组合'), port_nav2.to_frame('最大额度组合')], axis=1)
    # 累计收益率
    cum_return = port_nav.iloc[-1] - 1
    # 年化收益
    an_return = port_nav.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
    # 年化波动
    an_vol = port_nav.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
    # 最大回撤
    max_draw = port_nav.apply(cal_max_drawdown, axis=0)
    draw_series = port_nav.apply(lambda x: x / x.cummax() - 1)
    # sharpe
    sharpe = port_nav.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
    # # sortino
    down_std = port_nav.pct_change().dropna(how='all').apply(lambda x: x[x < 0].std() * np.sqrt(52), axis=0)
    sortino = an_return / down_std
    # calmar
    calmar = an_return / max_draw.abs()
    # 胜率
    win_ratio = port_nav.pct_change().dropna(how='all').apply(lambda x: x.gt(0).sum() / len(x), axis=0)
    # 平均损益比
    win_lose = port_nav.pct_change().dropna(how='all').apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
    # 年度累计
    ret_20 = port_nav.loc['20201231'] - 1
    ret_21 = port_nav.iloc[-1] / port_nav.loc['20201231'] - 1
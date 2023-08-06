"""
本地净值对比程序
"""
import pandas as pd
from datetime import datetime
import hbshare as hbs
from hbshare.quant_research.Kevin.rm_associated.util.data_loader import get_trading_day_list
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown
import plotly
from plotly.offline import plot as plot_ly
import plotly.graph_objs as go
import plotly.figure_factory as ff

plotly.offline.init_notebook_mode(connected=True)


# 宽投
local_nav = pd.read_excel("D:\\研究基地\\B-套利类\\宽投\\净值文件\\宽投资产-指增净值序列20211022.xls", header=1)
local_nav = local_nav.rename(
    columns={"净值日期": "tradeDate", "指数增强二号（复权累计净值）": "宽投指数增强二号"})[['tradeDate', '宽投指数增强二号']]
local_nav['tradeDate'] = local_nav['tradeDate'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
local_nav = local_nav.set_index('tradeDate')
local_nav = local_nav[local_nav.index >= '20200101']

# 概率
nav_pieces1 = pd.read_excel('D:\\研究基地\\A-机器学习类\\概率\\概率业绩数据_0903.xlsx', sheet_name=5)
nav_pieces1.rename(columns={"日期": "trade_date", "估算超额收益": "estimate_return"}, inplace=True)
nav_pieces1['trade_date'] = nav_pieces1['trade_date'].apply(lambda x: datetime.strftime(x, "%Y%m%d"))
nav_pieces1['概率500指增'] = (1 + nav_pieces1['estimate_return'] + nav_pieces1['中证500收益'])
sql_script_out = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
             "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
             "and a.jjzt not in ('3') " \
             "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
             "order by b.jzrq".format('SQT076', '20210625', '20211203')
res_out = hbs.db_data_query("highuser", sql_script_out, page_size=5000)
online_nav = pd.DataFrame(res_out['data']).set_index('TRADEDATE')['ADJ_NAV']
local_nav = pd.concat([nav_pieces1.set_index('trade_date')['概率500指增'], online_nav], axis=1)
local_nav['return'] = local_nav['ADJ_NAV'].pct_change()
local_nav['tmp'] = local_nav['概率500指增']
start_point = local_nav['return'].first_valid_index()
for k in range(local_nav.index.tolist().index(start_point), len(local_nav)):
    local_nav.loc[local_nav.index.tolist()[k], 'tmp'] = local_nav.iloc[k - 1]['tmp'] * (1 + local_nav.iloc[k]['return'])
local_nav = local_nav[['tmp']].rename(columns={"tmp": "概率500指增"})


compare_dict = {"衍复指增三号": "SJH866",
                "启林500指增": "SGY379",
                "因诺聚配500指增": "SGX346",
                "天演中证500指增": "SJU836",
                "灵均进取1号": "SW3470",
                "世纪前沿500指增": "SGP682",
                "赫富500指增一号": "SEP463",
                "九坤日享500指增": "ST9804"}


class LocalNavComparer:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        # calendar
        trading_day_list = get_trading_day_list(self.start_date, self.end_date, frequency='week')
        # nav_df
        nav_list = []
        for fund_name, fund_id in compare_dict.items():
            sql_script = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
                         "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3') " \
                         "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(fund_id, self.start_date, self.end_date)
            res = hbs.db_data_query("highuser", sql_script, page_size=5000)
            data = pd.DataFrame(res['data']).set_index('TRADEDATE')['ADJ_NAV']
            data.name = fund_name
            nav_list.append(data)
        nav_df = pd.concat(nav_list, axis=1).sort_index().reindex(trading_day_list).fillna(method='ffill', limit=1)
        nav_df = pd.merge(nav_df, local_nav, left_index=True, right_index=True, how='left').fillna(
            method='ffill', limit=1)
        nav_df = nav_df / nav_df.iloc[0]
        # benchmark
        benchmark_id = '000905'
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, self.start_date, self.end_date)
        res = hbs.db_data_query('readonly', sql_script)
        data = pd.DataFrame(res['data']).rename(columns={"TCLOSE": "benchmark"}).set_index('TRADEDATE')[['benchmark']]
        data = data.reindex(trading_day_list)

        assert (nav_df.shape[0] == data.shape[0])

        excess_return = nav_df.pct_change().sub(data.pct_change()['benchmark'].squeeze(), axis=0)
        self.excess_df = (1 + excess_return.fillna(0.)).cumprod()

    @staticmethod
    def plotly_line(df, title_text, sava_path, figsize=(1200, 500)):
        fig_width, fig_height = figsize
        data = []
        for col in df.columns:
            trace = go.Scatter(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                mode="lines"
            )
            data.append(trace)

        date_list = df.index.tolist()
        tick_vals = [i for i in range(0, len(df), 4)]
        tick_text = [date_list[i] for i in range(0, len(df), 4)]

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True, tickvals=tick_vals, ticktext=tick_text),
            template='plotly_white'
        )
        fig = go.Figure(data=data, layout=layout)

        plot_ly(fig, filename=sava_path, auto_open=False)

    def get_construct_result(self):
        # plot
        self.plotly_line(self.excess_df, "500指增产品对比", "D:\\量化产品跟踪\\新增净值走势对比\\概率.html", figsize=(1500, 800))
        # calculate
        nav_df = self.excess_df.copy()
        portfolio_index_df = pd.DataFrame(
            index=nav_df.columns, columns=['超额年化收益', '超额年化波动', '最大回撤', 'Sharpe', '胜率', '平均损益比'])
        portfolio_index_df.loc[:, '超额年化收益'] = nav_df.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
        portfolio_index_df.loc[:, '超额年化波动'] = \
            nav_df.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
        portfolio_index_df.loc[:, '最大回撤'] = nav_df.apply(cal_max_drawdown, axis=0)
        portfolio_index_df.loc[:, 'Sharpe'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
        portfolio_index_df.loc[:, '胜率'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x.gt(0).sum() / len(x), axis=0)
        portfolio_index_df.loc[:, '平均损益比'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
        portfolio_index_df.index.name = '产品名称'
        portfolio_index_df.reset_index(inplace=True)
        # 格式处理
        portfolio_index_df['超额年化收益'] = portfolio_index_df['超额年化收益'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['超额年化波动'] = portfolio_index_df['超额年化波动'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['最大回撤'] = portfolio_index_df['最大回撤'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['Sharpe'] = portfolio_index_df['Sharpe'].round(2)
        portfolio_index_df['胜率'] = portfolio_index_df['胜率'].apply(lambda x: format(x, '.1%'))
        portfolio_index_df['平均损益比'] = portfolio_index_df['平均损益比'].round(2)

        fig = ff.create_table(portfolio_index_df)
        fig.layout.autosize = False
        fig.layout.width = 1000
        fig.layout.height = 400

        plot_ly(fig, filename="D:\\量化产品跟踪\\新增净值走势对比\\概率_table.html", auto_open=False)


if __name__ == '__main__':
    LocalNavComparer("20201218", "20211203").get_construct_result()
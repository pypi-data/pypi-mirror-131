import pandas as pd
import plotly
import plotly.graph_objs as go
import  plotly.figure_factory as ff


class Untils:

    def __init__(self,val_hld,indus_info,fin_info,benchmark_info):
        from ..XZ.config import config_pfa
        configuration = config_pfa.Config()
        self.asset_type_code= configuration.Asset_type
        self.val_hld=val_hld[['Code','Name','Weight','Stamp_date','Stock_code']]
        self.indus_info=indus_info
        self.fin_info=fin_info
        self.bench_info=benchmark_info
        self.purified_stk_hld= self.cleaning_stock_hld()

    def shift_df_date(self,bench_df,df,bench_date_col,date_col):

        for date in list(set(bench_df[bench_date_col].unique()).difference(set(df[date_col].unique()))):
            date_delta=df[date_col]-date
            df .loc[date_delta.abs() == date_delta.abs().min(), date_col] = date
        return df

    def cleaning_stock_hld(self):

        rawdata=self.val_hld[~self.val_hld['Stock_code'].isnull()]

        temp_df=pd.merge(
            rawdata,self.indus_info[['SECUCODE','FIRSTINDUSTRYNAME']],how='left',left_on='Stock_code',right_on='SECUCODE'
        ).drop(['SECUCODE'],axis=1)

        #original used to shift the date that is missed in from any information table(any table except the fund valuation table)
        #this part is then abandoned by using '' for missing date
        # self.fin_info=self.shift_df_date(temp_df,self.fin_info,'Stamp_date','TRADINGDAY')
        # self.bench_info = self.shift_df_date(temp_df, self.bench_info, 'Stamp_date', 'ENDDATE')[['SECUCODE','WEIGHT','ENDDATE','Index_type']]

        self.bench_info=self.bench_info.rename(columns={'WEIGHT':'Index_Weight'})
        self.bench_info=pd.merge(temp_df[['Stamp_date', 'Stock_code','Weight']],self.bench_info,how='left',left_on=['Stock_code','Stamp_date'],right_on=['SECUCODE','ENDDATE'])
        self.bench_info['Index_type'].fillna('1800以外', inplace=True)
        self.bench_info['Index_Weight'].fillna(0, inplace=True)
        temp_df=pd.merge(temp_df,self.fin_info,how='left',left_on=['Stock_code','Stamp_date'],right_on=['SECUCODE','TRADINGDAY']).drop('ROW_ID',axis=1)

        return temp_df

    def aggregate_by(self,df,groupby,method,method_on):

        if(method=='sum'):
            output_df = df.groupby(groupby).sum(method_on).unstack().fillna(0)[
                (method_on)].fillna(0)
        elif(method=='average'):
            output_df = df.groupby(groupby).mean(method_on).unstack().fillna(0)[
                (method_on)].fillna(0)
        else:
            raise Exception
            print('Please check the aggregation method')

        output_df['日期'] = output_df.index

        return output_df

    def asset_allocation_stats(self):

        data=self.val_hld
        output_df = pd.DataFrame(columns=['日期'])
        output_df['日期']=data['Stamp_date'].unique()

        for keys in self.asset_type_code.keys():

            output_df =pd.merge(output_df,data[data['Code']==self.asset_type_code[keys]][['Weight','Stamp_date']],
                                how='left',left_on='日期',right_on='Stamp_date')
            output_df.rename(columns={'Weight':keys},inplace=True)
            output_df=output_df.drop(['Stamp_date'],axis=1)

        output_df['A股']=0
        for col in [x for x in list(self.asset_type_code.keys()) if ('上交所' in x or '深交所' in x) ]:
            output_df['A股']= output_df['A股']+output_df[col].fillna(0)
        output_df['港股']=output_df['港股通'].fillna(0)+output_df['深港通'].fillna(0)

        return output_df.fillna(0)

    def rank_filter(self,input_df,thresholds):

        index_list=['前'+str(x)+'大' for x in thresholds ]
        output_df=pd.DataFrame(columns=input_df['日期'])
        input_df=input_df.drop(['日期'],axis=1).T
        for col in input_df.columns:
            values=[]
            for rank in thresholds:
                values.append( [ input_df[col].sort_values(ascending=False).values[0:rank],
                                 input_df[col].sort_values(ascending=False).index[0:rank]] )
            output_df[col]=values
        output_df.index=index_list
        output_df=output_df.T
        output_df['日期']=output_df.index

        return  output_df

    def fund_risk_exposure(self,row_factors_df):

        left_table=self.purified_stk_hld[['Stock_code','Name','Weight','Stamp_date']].dropna()
        left_table['Stamp_date']=[ ''.join(x.split('-')) for x in left_table['Stamp_date'].astype(str)]
        factors_col=row_factors_df.columns.drop(['ticker','trade_date']).tolist()
        fund_factors=pd.merge(left_table,row_factors_df
                              ,how='left',right_on=['ticker','trade_date'],left_on=['Stock_code','Stamp_date'])\
            .drop('Stock_code',axis=1)

        for col in factors_col:
            fund_factors[col]=fund_factors[col]*fund_factors['Weight']/100
        fund_factors=fund_factors.groupby(['trade_date']).sum(factors_col)[factors_col]

        # fund_factors['Stamp_date'] = fund_factors.index
        fund_factors['JYYF']=[ x[0:6] for x in fund_factors.index]

        return fund_factors

    def generate_ret_df(self):


        ret_df=self.val_hld[self.val_hld['Code'].str.contains('今日单位净值') | self.val_hld['Code'].str.contains('基金单位净值:')]['Code'].unique()[0]
        ret_df=self.val_hld[self.val_hld['Code']==ret_df][['Code','Name','Stamp_date']]
        ret_df.rename(columns={'Name':'Net_value'},inplace=True)
        ret_df['Return']=ret_df['Net_value'].astype(float).pct_change()
        ret_df.drop('Code',axis=1,inplace=True)
        ret_df.reset_index(drop=True, inplace=True)

        return ret_df

    def iter_list(self,inputlist,iter_num):
        import itertools
        iter_list=list(itertools.combinations(inputlist,iter_num))
        return iter_list

class Plot:
    def __init__(self,fig_width,fig_height):

        self.fig_width=fig_width
        self.fig_height=fig_height

    # def plot_render(self,data,layout, **kwargs):
    #     kwargs['output_type'] = 'div'
    #     plot_str = plotly.offline.plot({"data": data, "layout": layout}, **kwargs)
    #     print('%%angular <div style="height: %ipx; width: %spx"> %s </div>' % (self.fig_height, self.fig_width, plot_str))

    def plot_render(self,data,layout):
        fig = go.Figure(data=data, layout=layout)
        fig.show()

    def plotly_style_bar(self,df, title_text,legend_x=0.30):
        fig_width, fig_height = self.fig_width,self.fig_height
        cols = df.columns.tolist()
        color_list = ['rgb(49, 130, 189)', 'rgb(204, 204, 204)', 'rgb(216, 0, 18)']
        data = []
        for i in range(len(cols)):
            col = cols[i]
            trace = go.Bar(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                # marker=dict(color=color_list[i])
            )
            data.append(trace)

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            legend=dict(orientation="h", x=legend_x),
            template='plotly_white'
        )

        #fig = go.Figure(data=data, layout=layout)

        return data, layout

    def plotly_pie(self,df, title_text):
        fig_width, fig_height = self.fig_width,self.fig_height
        labels = df.index.tolist()
        values = df.values.round(3).tolist()
        data = [go.Pie(labels=labels, values=values, hoverinfo="label+percent",
                       texttemplate="%{label}: %{percent}")]
        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height
        )

        # fig = go.Figure(data=data, layout=layout)

        return data, layout

    def plotly_area(self,df,title_text):
        fig_width, fig_height = self.fig_width,self.fig_height
        names = df.columns.to_list()
        names.remove('日期')
        cols =df['日期'].to_list()

        data = []
        for name in names:
            tmp = go.Scatter(
                x=cols,
                y=df[name].values,
                name=name,
                mode='lines',
                line=dict(width=0.5),
                fill='tonexty',
                stackgroup='one')
            data.append(tmp)

        layout = go.Layout(
            title=title_text,
            autosize=False,
            width=fig_width,
            height=fig_height,
            showlegend=True,
            xaxis=dict(type='category'),
            yaxis=dict(
                type='linear',
                range=[1, 100],
                dtick=20,
                ticksuffix='%'))

        self.plot_render(data, layout)

    def plotly_line(self,df, title_text):

        fig_width, fig_height = self.fig_width,self.fig_height
        names = df.columns.to_list()
        names.remove('日期')
        cols =df['日期'].to_list()

        data = []
        for name in names:
            trace = go.Scatter(
                x=cols,
                y=df[name].values,
                name=name,
                mode="lines+markers"
            )
            data.append(trace)

        date_list = df.index.tolist()

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            yaxis2={'anchor': 'x', "overlaying": 'y', "side": 'right'},
            template='plotly_white'
        )

        self.plot_render(data, layout)

    def plotly_scatter(self, df, title_text,fix_range=False):

        fig_width, fig_height = self.fig_width, self.fig_height
        col_x = df.columns.tolist()[0]
        col_y = df.columns.tolist()[1]

        range_x=max(abs(0-df[col_x].max()),abs(0-df[col_x].min()))

        trace0 = go.Scatter(
            x=df[col_x].values,
            y=df[col_y].values,
            mode='markers',  # 绘制纯散点图
            name='因子组合'  # 图例名称
        )

        data = [trace0]
        if (fix_range == True):
            layout = go.Layout(
                title=dict(text=title_text),
                autosize=False, width=fig_width, height=fig_height,
                yaxis=dict(tickfont=dict(size=12), showgrid=True,title_text=col_y,range=[0,1],dtick=0.5),
                xaxis=dict(tickfont=dict(size=12),showgrid=True,title_text=col_x,range=[-range_x,range_x],dtick=0),
                template='plotly_white'
            )
        else:
            layout = go.Layout(
                title=dict(text=title_text),
                autosize=False, width=fig_width, height=fig_height,
                yaxis=dict(tickfont=dict(size=12), showgrid=True,title_text=col_y),
                xaxis=dict(tickfont=dict(size=12),showgrid=True,title_text=col_x),
                template='plotly_white'
            )

        self.plot_render(data, layout)

    def plotly_line_multi_yaxis(self,df,title_text,y2_col):

        fig_width, fig_height = self.fig_width,self.fig_height
        names = df.columns.to_list()
        for name in y2_col+['日期']:
            names.remove(name)
        cols =df['日期'].to_list()

        data = []
        for name in names:
            trace = go.Scatter(
                x=cols,
                y=df[name].values,
                name=name+'(左轴)',
                mode="lines+markers"
            )
            data.append(trace)

        for name in y2_col:
            trace = go.Scatter(
                x=cols,
                y=df[name].values,
                name=name+'(右轴)',
                mode="lines+markers",
                yaxis='y2'
            )
            data.append(trace)

        date_list = df.index.tolist()

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            xaxis=dict(showgrid=True),
            yaxis2={'anchor': 'x', "overlaying": 'y', "side": 'right'},
            template='plotly_white'
        )

        self.plot_render(data, layout)

    #
    # def plotly_table(self,df,colwidth,title_text):
    #
    #     # 给首行着色
    #     headerColor = 'lightblue'
    #
    #     # 给奇数偶数行制定不同的颜色
    #     # rowEvenColor = 'lightgrey'
    #     # rowOddColor = 'white'
    #
    #     colnames=['<b>'+x+'</b>'for x in df.columns.tolist()]
    #
    #     data=[go.Table(
    #         columnwidth=colwidth,
    #         header=dict(
    #             # 制定列名称
    #             values=colnames,
    #             line_color='darkslategray',
    #             fill_color=headerColor,
    #             align=['left', 'center'],
    #             font=dict(color='Black', size=16)
    #         ),
    #         cells=dict(
    #             values=df.fillna('').T.values.tolist(),
    #             line_color='darkslategray',
    #             # 2-D list of colors for alternating rows
    #             #fill_color=[[rowOddColor, rowOddColor, rowOddColor, rowOddColor, rowEvenColor] * 5],
    #             align=['left', 'center'],
    #             font=dict(color='darkslategray', size=16),
    #             height=30
    #         ))
    #     ]
    #
    #     layout = go.Layout(
    #         title=dict(text=title_text),
    #         autosize=True,
    #         yaxis=dict(tickfont=dict(size=12), showgrid=True),
    #         xaxis=dict(showgrid=True),
    #         template='plotly_white'
    #     )
    #
    #
    #     self.plot_render( data, layout)

    def plotly_table(self, df, table_width, title_text):

        fig=ff.create_table(df)
        fig.layout.width=table_width
        fig.layout.title=title_text
        self.plot_render(fig.data,fig.layout )
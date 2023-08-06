import numpy as np
import pandas as pd
from ..XZ import functionality
from ..XZ import db_engine as dben


class Projects:

    def __init__(self):

        from ..XZ.config import config_pfa as config
        self.config_pfa=config.Config()

    # 1.资产配置时序：A股 / 港股 / 债券 / 基金 / 现金等类别时序的累计区域图；
    def asset_allocation_pic(self,plot,asset_allocation_df):

        # 1.资产配置时序：A股 / 港股 / 债券 / 基金 / 现金等类别时序的累计区域图；
        plot.plotly_area(asset_allocation_df[['活期存款', '债券', '基金', '权证', '其他', 'A股',
                                              '港股', '日期']], '资产配置时序')

    # 2.行业配置时序：基于申万一级行业分别规则，对持仓的行业分布做一个时序统计；
    def industry_allocation_pic(self,plot,ind_hld):
        plot.plotly_area(ind_hld, '行业配置时序')

    # 3. 行业集中度时序：持仓前一 / 三 / 五大行业的权重时序
    def industry_centralization_pci(self,plot,indutry_allocation_df_ranked):

        # 3. 行业集中度时序：持仓前一 / 三 / 五大行业的权重时序
        inputdf = indutry_allocation_df_ranked.copy()
        cols = inputdf.columns.tolist()
        cols.remove('日期')
        for col in cols:
            inputdf[col] = [x[0].sum() for x in inputdf[col]]
        plot.plotly_line(inputdf, '行业集中度时序')

    # 4.重仓明细：时序上各个时间点的持仓明细（表格）；
    def stock_holding_pic(self,plot,stk_hld):
        # 4.重仓明细：时序上各个时间点的持仓明细（表格）；
        tempdf = stk_hld.drop('日期',axis=1).T
        input_df=pd.DataFrame()
        for date in tempdf.columns:
            input_df[date]=tempdf[date].sort_values(ascending=False).index[0:20]\
                           +'( '+tempdf[date].sort_values(ascending=False).values[0:20].astype(str)+' )'

        plot.plotly_table(input_df, 5000, '持仓明细')

    # 5.持股集中度时序：持仓前三 / 五 / 十大权重和的时序折线图；
    def stock_centralization_pic(self,plot,asset_allocation_df_ranked):
        # 5.持股集中度时序：持仓前三 / 五 / 十大权重和的时序折线图；
        inputdf = asset_allocation_df_ranked.copy()
        cols = inputdf.columns.tolist()
        cols.remove('日期')
        for col in cols:
            inputdf[col] = [x[0].sum() for x in inputdf[col]]
        plot.plotly_line(inputdf, '持股集中度时序')

    # 6.组合中A股持仓的平均PE / PB / 股息率的折线图；
    def valuation_pic(self,plot,fin_hld,stk_hld,date_list):
        # 6.组合中A股持仓的平均PE / PB / 股息率的折线图；
        tempdf = pd.DataFrame()
        for item in ['PE', 'PB', 'DIVIDENDRATIO']:
            tempdf[item] = ((fin_hld.loc[:, (item, slice(None))].values) * (stk_hld.drop('日期', axis=1).values)).sum(
                axis=1) / stk_hld.drop('日期', axis=1).values.sum(axis=1)
        tempdf['日期'] = date_list
        plot.plotly_line_multi_yaxis(tempdf, '持股估值分析', ['PB', 'DIVIDENDRATIO'])

    # 7.持股分布：所持股票在各类宽基成分股中的权重时序的折线图，包括：沪深300、中证500、中证1000、1800以外。
    def hodling_in_benchmark(self,plot,ben_hld):
        # 7.持股分布：所持股票在各类宽基成分股中的权重时序的折线图，包括：沪深300、中证500、中证1000、1800以外。
        plot.plotly_area(ben_hld, '宽基成分股配置走势')

    # 8 单只基金Alpha R_Square 散点图
    def alpha_rsquare_pic(self,plot,fun,df1,date_list,Jydb):

        #read the factors information from hb database
        sec_code_A=df1['Stock_code'].dropna()[~df1['Stock_code'].dropna().str.contains('H')].unique()
        raw_factors=Jydb.extract_factors(sec_code_A,date_list)

        #calcualte the risk exposure for the fund as a whole
        fund_factors=fun.fund_risk_exposure(fun.purified_stk_hld[['Stock_code','Name','Weight','Stamp_date']].dropna(),
                                            raw_factors,
                                            ['Stamp_date','Stock_code','Weight'])

        #get the return of benchmark index as factors
        index_list=['000905','000300']
        factors_benchmark=Jydb.extract_benchmark_return(date_list,index_list+['000012'])
        factors_benchmark=fun.aggregate_by(factors_benchmark,['TJYF','ZQDM'],'sum','HB')

        #join the classical risk factors with benchmark factors
        fund_factors=pd.merge(fund_factors,factors_benchmark,how='inner',left_on='JYYF',right_on='日期').drop('日期',axis=1)
        factors_list=fund_factors.columns.drop(['JYYF']+index_list).tolist()

        #get the return of the fund by valuation table as the y input for the ols model
        ret_df=fun.generate_ret_df()
        ret_df['JYYF'] = [x.split('-')[0] + x.split('-')[1] for x in ret_df['Stamp_date'].astype(str)]
        ret_df.drop('Stamp_date',axis=1,inplace=True)
        ret_df['Return']=ret_df['Return'].shift(-1)
        ret_df.drop(ret_df.index[-1], axis=0, inplace=True)

        #combine all the data for ols in one dataframe
        ols_df=pd.merge(fund_factors,ret_df,how='inner',left_on='JYYF',right_on='JYYF')
        ols_df['const']=1
        del fund_factors,ret_df,raw_factors

        #8 单只基金Alpha R_Square 散点图

        for num_factors in [6]:
            # pick 6 factors for each round of run as suggested by the research paper of haitong security
            summary_df,simulated_df,selected_factors=fun.calculate_alpha(ols_df, factors_list, num_factors,
                                                                         ret_col= 'Return',date_col='JYYF',
                                                                         bench_factor=index_list)

            plot.plotly_scatter(summary_df[['alpha','rsquar']],'因子组合Alpha_R_square散点图',fix_range=True)

            plot.plotly_line(simulated_df[['simulated_ret', 'real_ret', '日期']], '基金多因子模型拟合效果_因子：{0}'.format(selected_factors))
            # plot.plotly_scatter(simulated_df[['simulated_ret','real_ret']].sort_values('real_ret'), '基金多因子模型拟合效果')

    def prv_hld_analysis (self,prd_name,tablename,pic_list=None):

        ########################################Collecting data########################################
        config=self.config_pfa

        # initial the temp database class
        Pfdb = dben.PrvFunDB()

        # write fold files to DB
        # Pfdb.write2DB(table_name='prvfund',fold_dir="E:\私募主观\主观股多估值表基地",increment=0)

        # initial the class
        Jydb = dben.HBDB()

        # extra data from the temp database
        df1 = Pfdb.extract_from_db(prd_name=prd_name, columns='*', tablename=tablename)

        # get the unique date list and stock code list
        date_list = df1['Stamp_date'].dropna().unique()
        sec_code = df1['Stock_code'].dropna().unique()

        # extra industry data from the JY database
        df2 = Jydb.extract_industry(sec_code)

        # extra financial data from the JY database
        df3 = Jydb.extract_fin_info(sec_code,date_list)

        # extra benchmark data from the JY database
        df4 = Jydb.extract_benchmark(config.Index_type, sec_code=sec_code,date_list=date_list)

        fun = functionality.Untils(df1[['Code','Name','Weight','Stamp_date','Stock_code']], df2, df3, df4)

        asset_allocation_df = fun.asset_allocation_stats()

        ind_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'FIRSTINDUSTRYNAME'], method='sum',
                                   method_on='Weight')
        indutry_allocation_df_ranked = fun.rank_filter(ind_hld, [1, 3, 5])

        stk_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'Name'], method='sum',
                                   method_on='Weight')
        asset_allocation_df_ranked = fun.rank_filter(stk_hld, [3, 5, 10])

        fin_hld = fun.aggregate_by(fun.purified_stk_hld, groupby=['Stamp_date', 'Name'], method='sum',
                                   method_on=['PE', 'PB', 'DIVIDENDRATIO'])
        ben_hld = fun.aggregate_by(fun.bench_info, groupby=['Stamp_date', 'Index_type'], method='sum',
                                   method_on='Weight')

        ########################################Drawing Pictures ########################################

        # drawing the pics ,initial the instant
        plot = functionality.Plot(fig_width=1200, fig_height=600)

        if(pic_list is None):

            self.asset_allocation_pic(plot,asset_allocation_df)
            self.industry_allocation_pic(plot,ind_hld)
            self.industry_centralization_pci(plot, indutry_allocation_df_ranked)
            self.stock_holding_pic(plot, stk_hld)
            self.stock_centralization_pic(plot, asset_allocation_df_ranked)
            self.valuation_pic(plot, fin_hld, stk_hld, date_list)
            self.hodling_in_benchmark(plot,ben_hld)
            self.alpha_rsquare_pic(plot, fun, df1, date_list, Jydb)

        else:
            pic_list=[x+'_pic' for x in pic_list]

            if('asset_allocation_pic' in pic_list):
                self.asset_allocation_pic(plot, asset_allocation_df)
            if ('industry_allocation_pic' in pic_list):
                self.industry_allocation_pic(plot,ind_hld)
            if ('industry_centralization_pci' in pic_list):
                self.industry_centralization_pci(plot, indutry_allocation_df_ranked)
            if ('stock_holding_pic' in pic_list):
                self.stock_holding_pic(plot, stk_hld)
            if ('stock_centralization_pic' in pic_list):
                self.stock_centralization_pic(plot, asset_allocation_df_ranked)
            if ('valuation_pic' in pic_list):
                self.valuation_pic(plot, fin_hld, stk_hld, date_list)
            if ('hodling_in_benchmark' in pic_list):
                self.hodling_in_benchmark(plot,ben_hld)
            if ('alpha_rsquare_pic' in pic_list):
                self.alpha_rsquare_pic(plot, fun, df1, date_list, Jydb)

    def prv_fof_analysis(self,fund_code):

        hbdb=dben.HBDB()

        sql = """ 
        select d.*,b.jzrq,b.jjjz,b.ljjz  
        from 
        (
        select a.jjdm,a.jjjc,a.cpfl,a.jjfl,c.mjjdm,c.lhbz,c.sfzz,c.fofjjdl,c.fofejfl,c.tzmb,c.tzfw,c.tzcl,c.tzbz,c.fxsytz 
        from st_hedge.t_st_jjxx a, st_hedge.t_st_sm_jjxx c 
        where a.jjdm=c.jjdm and a.jjdm='{0}'
        ) d left join st_hedge.t_st_jjjz b on d.jjdm=b.jjdm """.format(fund_code)

        hld_prv=hbdb.db2df(sql,db='highuser')

        sql="select jzdm,yxj,moddt_etl from st_hedge.t_st_sm_jjbjjz a where jjdm='{}' ".format(fund_code)
        benchmark_code=hbdb.db2df(sql,db='highuser')

        print('Done')

    def fund_alpha_analysis(self,fund_list):

        fun=functionality.Untils()
        ########################################Collecting data########################################
        hbdb=dben.HBDB()
        for fund in fund_list:

            #read the holding info for the fund
            sql="select jjdm,jsrq,zqdm,zqmc,zjbl from st_fund.t_st_gm_gpzh where jjdm='{0}'".format(fund)
            fund_hld=hbdb.db2df(sql,db='funduser')

            #read the net value info for the fund
            sql="select jjdm,tjyf,hb1y from st_fund.t_st_gm_yhb where jjdm='{0}'".format(fund)
            ret_df=hbdb.db2df(sql,db='funduser')
            ret_df['hb1y']=ret_df['hb1y'] / 100
            ret_df['tjyf']=ret_df['tjyf'].astype(str)


            # read the factors information from hb database
            sec_code= fund_hld['zqdm'][~fund_hld['zqdm'].dropna().str.contains('H')].unique()
            date_list=fund_hld['jsrq'].unique()
            raw_factors = hbdb.extract_factors(sec_code, date_list)

            industry=False
            if(industry==True):
                #add the industry factors if necessary, i am not using the industry factors in the st_ashare.r_st_barra_style_factor
                #because it contains too many industries i am using the 中证指数行业分类2016版 which is less to reduce the computing burder

                sql = """
                select a.SecuCode,b.FirstIndustryName,b.XGRQ from HSJY_GG.SecuMain a 
                left join HSJY_GG.LC_ExgIndustry b on a.CompanyCode=b.CompanyCode  
                where Standard=28 and a.SecuCode in({0}) """.format("'"+"','".join(sec_code)+"'")
                industry_factors=hbdb.db2df(sql,db='readonly').sort_values('XGRQ').drop(['ROW_ID','XGRQ'],axis=1)
                industry_factors.drop_duplicates('SECUCODE',keep='last',inplace=True)

                # sql = """
                # select a.SecuCode,b.FirstIndustryName,b.UpdateTime from HSJY_GG.SecuMain a
                # left join HSJY_GP.LC_STIBExgIndustry b on a.CompanyCode=b.CompanyCode
                # where Standard=28 and a.SecuCode in({0}) """.format("'"+"','".join(sec_code)+"'")
                # industry_factors2=hbdb.db2df(sql,db='readonly').sort_values('UpdateTime').drop(['ROW_ID','UpdateTime'],axis=1)
                # industry_factors2.drop_duplicates('SECUCODE',keep='last',inplace=True)

                industry_factors=pd.concat([industry_factors,pd.get_dummies(industry_factors['FIRSTINDUSTRYNAME'])],axis=1).drop('FIRSTINDUSTRYNAME',axis=1)

                raw_factors=pd.merge(raw_factors,industry_factors,how='left',left_on='ticker',right_on=['SECUCODE']).drop('SECUCODE',axis=1)

            # calcualte the risk exposure for the fund as a whole
            fund_factors = fun.fund_risk_exposure(fund_hld,raw_factors,['jsrq','zqdm','zjbl'])

            jjfl=hbdb.db2df("select jjfl from st_fund.t_st_gm_flls where jjdm='{0}' ".format(fund),db='funduser')['jjfl'][0]
            jzdm_list=hbdb.db2df("select jzdm from st_hedge.t_st_sm_jjflbjjz where jjfl='{}' and jzdm not like 'H%%' ".format(jjfl),db='highuser')['jzdm']\
                .values.tolist()

            sql="select hb1y,zqdm,tjyf from st_market.t_st_zs_yhb  where zqdm in ({0}) ".format(','.join(jzdm_list+['000012']))
            benchmark_df=hbdb.db2df(sql,db='alluser')
            benchmark_df=benchmark_df[benchmark_df['hb1y']!=999]
            benchmark_df=benchmark_df.groupby(['zqdm', 'tjyf']).sum('hb1y').unstack().T
            benchmark_df['日期']=benchmark_df.index.get_level_values(1).astype(str)

            fund_factors=pd.merge(fund_factors,benchmark_df,how='inner',left_on='JYYF',right_on='日期').drop('日期',axis=1)

            factors_list=fund_factors.columns.drop(['JYYF']+jzdm_list).tolist()

            #standardlize the factors to be mean 1 std 1
            for col in factors_list:
                mean=fund_factors[col].mean()
                std=fund_factors[col].std()
                fund_factors[col]=fund_factors[col]/std+1-mean

            # combine all the data for ols in one dataframe
            ols_df = pd.merge(fund_factors, ret_df, how='inner', left_on='JYYF', right_on='tjyf')
            ols_df['const'] = 1
            del fund_factors, ret_df, raw_factors

            plot = functionality.Plot(fig_width=1200, fig_height=600)

            for num_factors in [6]:
                # pick 6 factors for each round of run as suggested by the research paper of haitong security
                summary_df, simulated_df,selected_factors = fun.calculate_alpha(ols_df, factors_list, num_factors, ret_col='hb1y',
                                                               date_col='JYYF',bench_factor=jzdm_list)

                fund_name=hbdb.db2df("select jjjc from st_fund.t_st_gm_jjxx where jjdm='{0}'".format(fund),db='funduser').values[0]
                plot.plotly_scatter(summary_df[['alpha', 'rsquar']], '因子组合Alpha_R_square散点图_{0}'.format(fund_name), fix_range=True)

                plot.plotly_line(simulated_df[['simulated_ret', 'real_ret', '日期']], '基金多因子模型拟合效果_{0}_因子：{1}'.format(fund_name,selected_factors))

    def bl_model(self,end_date,asset_list):

        from ..AAM.blmodel import  blmodel

        blm=blmodel.BL_Model()
        #get last 10 years trade month date
        trade_date_month=blm.get_trade_date(end_date,fre='M')[-121:]

        #last 6 years data is needed for calculating the cov martix
        begin_date=str(int(end_date[0:4])-6)+end_date[4:6]+'01'
        trade_date_week=blm.get_trade_date(end_date=end_date,fre='W',begin_date=begin_date)

        #calcualte the Cov matrix based on weekly return for the laset 6years
        cov_matrix=blm.cov_mat_from_return(trade_date_week,asset_list)

        #calcualte the risk_aversion
        risk_aversion=blm.get_risk_aversion()

        #calculate the prio return based on the market value weights, COV matrix and risk aversion

        #mkt_val=blm.get_weight(end_date,asset_list)
        #since we do not have the market value data from db, mannually input the market value here
        # mkt_val=[277355929574535,189126278507110,26909992142220,46865702805647,12784724380556,
        #          7377133769326,91204018181995]
        mkt_val = [277355929574535, 189126278507110, 26909992142220,
                   7377133769326, 91204018181995]

        prio_return=blm.implied_return_from_weight(mkt_val=mkt_val,risk_aversion=risk_aversion,
            end_date=trade_date_week[-1],asset_list=asset_list,cov_matrix=cov_matrix)

        tau=0.05
        #the cov matrix of average return is a shrink of the cov matrix of return itself
        cov_matrix=tau*cov_matrix

        # calculate the view return if necessary
        # use the last 10 years data for calculating view return
        view_ret = []
        for asset in asset_list:
            view_ret.append(blm.calculate_view_return(trade_date_month, asset))

        views = np.eye(len(asset_list))

        # calculate the view confidence if not read from database directlly
        view_confidence =np.dot(np.dot(views, cov_matrix), views.T)*np.eye(len(views))

        #set upper and lower bound
        lb=[-0.1]*len(asset_list)
        ub=[0.5]*len(asset_list)
        constrains=blm.set_boundary(len(asset_list), lb, ub)

        opt_weight=blm.blm_solver(sigma=cov_matrix,mu=prio_return,P=views,Q=view_ret,
                             Omega=view_confidence,delta=risk_aversion,constrains=constrains)

        opt_restul=pd.DataFrame()
        opt_restul['Asset']=asset_list
        opt_restul['Weight']=opt_weight

        return opt_restul




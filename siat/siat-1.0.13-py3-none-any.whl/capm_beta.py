﻿# -*- coding: utf-8 -*-
"""
本模块功能：CAPM模型贝塔系数计算
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2018年7月16日
最新修订日期：2020年1月15日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
def get_price(ticker,fromdate,todate):
    """
    功能：抓取股价
    输出：指定收盘价格序列，最新日期的股价排列在前
    ticker: 股票代码。大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    fromdate: 样本开始日期，尽量远的日期，以便取得足够多的原始样本，mm/dd/yyyy
    todate: 样本结束日期，既可以是今天日期，也可以是一个历史日期，mm/dd/yyyy
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #ticker='000300.SS'
    #fromdate='01/01/2018'
    #todate='06/30/2019'
    #---------------------------------------------
    
    #抓取雅虎股票价格
    from pandas_datareader import data
    try:
        price=data.DataReader(ticker,'yahoo',fromdate,todate)
    except:
        print("Error #1(get_price): failed to crawl stock prices")        
        print("Information:",ticker,fromdate,todate)  
        return None            
    
    #去掉比起始日期更早的样本
    price2=price[price.index >= fromdate]

    #去掉比结束日期更晚的样本
    #price2=price2[price2.index <= todate]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    #提取日期和星期几
    #sortedprice['Date']=sortedprice.index.date
    #sortedprice['Date']=sortedprice.index.strftime("%Y-%m-%d")
    sortedprice['Date']=sortedprice.index.strftime("%m/%d/%Y")
    sortedprice['Weekday']=sortedprice.index.weekday+1
    
    #生成输出数据格式：日期，星期几，收盘价
    dfprice=sortedprice[['Date','Weekday','Close']]

    #返回日期升序的股票收盘价序列    
    return dfprice
    

if __name__=='__main__':
    df601857=get_price('601857.SS','2012-01-01','2019-12-31')
    dfprice=get_price('MSFT','01/01/2015','06/30/2019')
    dfprice.head(5)
    dfprice.tail(3)
    dfprice[dfprice.Date == '06/28/2019']
    dfprice[(dfprice.Date>='03/20/2019') & (dfprice.Date<='03/29/2019')]
    
    dfindex=get_price('^GSPC','1/1/2015','6/30/2019')
    
    dfprice002504=get_price('002504.SZ','01/01/2015','06/30/2019')
    dfprice000001=get_price('000001.SS','01/01/2015','07/16/2019')
    dfprice000001.tail(3)
    
    dfprice00700=get_price('0700.HK','01/01/2015','06/30/2019')

#==============================================================================
def get_price_excel(ticker,fromdate,todate,excelfile,sheetname='Sheet1'):
    """
    功能：抓取股价，保存到Excel文件中
    输出：指定收盘价格序列，最新日期的股价排列在前
    ticker: 股票代码。大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    fromdate: 样本开始日期，尽量远的日期，以便取得足够多的原始样本
    todate: 样本结束日期，既可以是今天日期，也可以是一个历史日期
    excelfile：保存到Excel文件名，含目录。如果目录不存在，将会导致错误。
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #ticker='000300.SS'
    #fromdate='01/01/2018'
    #todate='06/30/2019'
    #---------------------------------------------
    
    #仅为测试使用
    #ticker='601857.SS'
    #fromdate='2019-1-1'
    #todate='2019-8-31'
    #excelfile='C:/temp/myexcel1.xlsx'
    #sheetname='601857.SS'
    
    price=get_price(ticker,fromdate,todate)
    if price is None:
        print("Error #1(get_price_excel): failed to crawl stock data")
        print("Information:",ticker,fromdate,todate) 
        return
    try:
        price.to_excel(excelfile,sheetname,encoding='utf-8')             
    except:
        print("Error #2((get_price_excel): failed to stock data to excel file")        
        print("Information:",excelfile,sheetname)
        return
    print("***Results saved in",excelfile,"with sheet",sheetname)
    return 
    

if __name__=='__main__':
    df601857=get_price_excel('601857.SS','2019-1-1','2019-12-31', \
                             'C:/temp/myexcel1.xlsx','601857.SS')


#==============================================================================
def prepare_capm_data(stkcd,mktidx,start,end):
    """
    函数功能：准备计算一只股票CAPM模型贝塔系数的数据，并标记年度
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    start：使用股票价格数据的开始日期，MM/DD/YYYY
    end：使用股票价格数据的结束日期，MM/DD/YYYY
    输出数据：
    返回数据：带年度标记的可直接用于capm回归的股票收益率数据
    """
        
    #仅用于调试，正式使用前应注释掉
    #stkcd='600028.SS'; mktidx='000001.SS'
    #start="12/31/2011"; end="12/31/2018"

    #抓取股价和指数
    stock=get_price(stkcd,start,end)
    if stock is None:
        print("Error #1(prepare_capm_data): failed to get stock price")
        print("Information:",stkcd,start,end)              
        return None    
    market=get_price(mktidx,start,end)
    if market is None:
        print("Error #2(prepare_capm_data): failed to get market index")
        print("Information:",mktidx,start,end)              
        return None

    #计算日收益率
    import pandas as pd
    stkret=pd.DataFrame(stock['Close'].pct_change())
    mktret=pd.DataFrame(market['Close'].pct_change())

    #合并，去掉空缺
    R=pd.merge(mktret,stkret,how='left',left_index=True,right_index=True)
    R=R.dropna()

    #标记各个年度
    R['Year']=R.index.strftime("%Y")

    #返回带年份的股票收益率序列
    return R

#==============================================================================
def capm_beta(stkcd,mktidx,start,end):
    """
    函数功能：计算一只股票的静态CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    start：使用股票价格数据的开始日期，MM/DD/YYYY
    end：使用股票价格数据的结束日期，MM/DD/YYYY
    输出数据：
    显示CAPM市场模型回归的alpha, beta, 以及显著性和拟合优度
    无返回数据
    """
        
    #读取股价并准备好收益率数据
    R=prepare_capm_data(stkcd,mktidx,start,end)
    if R is None:
        print("#Error(capm_beta): failed to prepare capm data")
        print("Info:",stkcd,mktidx,start,end)              
        return   

    #全数据OLS回归
    from scipy import stats 
    (beta,alpha,r_value,p_value,std_err)= \
        stats.linregress(R['Close_x'],R['Close_y'])

    #显示回归结果
    print(" \n***** CAPM Beta Coefficient *****")
    print(" Regression formula: Market Model")
    print(" Stock code        :",stkcd)
    print(" Market index      :",mktidx)
    print(" Data period start :",start)
    print(" Data period end   :",end)
    print(" Intercept         :",round(alpha,4))
    print(" Beta coefficient  :",round(beta,4))
    print(" R-square          :",round(r_value**2,4))
    print(" p-value           :",round(p_value,4))
    
    #import datetime
    #today = datetime.date.today()
    #print("*** Source: Yahoo Finance,",today)
    print("*** Source: Yahoo Finance")

    return  beta  
    
if __name__=='__main__':
    capm_beta('002504.SZ','000001.SS','12/31/2011','12/31/2018')    

#==============================================================================
def gen_yearlist(start_year,end_year):
    """
    功能：产生从start_year到end_year的一个年度列表
    输入参数：
    start_year: 开始年份，字符串
    end_year：截止年份
    输出参数：
    年份字符串列表    
    """
    #仅为测试使用，完成后应注释掉
    #start_year='2010'
    #end_year='2019'    
    
    import numpy as np
    start=int(start_year)
    end=int(end_year)
    num=end-start+1    
    ylist=np.linspace(start,end,num=num,endpoint=True)
    
    yearlist=[]
    for y in ylist:
        yy='%d' %y
        yearlist=yearlist+[yy]
    #print(yearlist)
    
    return yearlist
#==============================================================================
def plot_trend(titletxt,footnotetxt,df,power=1):
    """
    功能：绘制散点数据的平滑曲线图及其趋势线
    titletxt: 标题
    footnotetxt：脚注
    df: 数据框，其索引为字符型年份，第1列与年份对应的数值1，
    第2列与年份对应的数值2，。。。
    power: 趋势线拟合的幂阶数，默认为三阶多项式
    """
    #将字符型年份转化为整数型
    yearstr=df.index
    year=[]
    for t in yearstr:
        tt=int(t)
        year=year+[tt]    
    
    #取得列名
    rowlist=df.columns.values.tolist()
    n=len(rowlist)
    
    import numpy as np
    import scipy.interpolate as itp
    import matplotlib.pyplot as plt

    #由于年度为连续整数，为插值方便，先将所有年度放大10倍
    year0=[]
    for t in year:
        tt=t*10
        year0=year0+[tt]

    #形成用于插值的连续整数自变量xx
    x1=year0[0]
    x2=year0[-1]+1
    xx=np.array(range(x1,x2,1))   
    
    #将用于插值的自变量缩小10倍，以便自变量在x轴上的尺度统一
    x=[]
    for t in xx:
        tt=t/10.0
        x=x+[tt]
    
    #循环处理每个因变量
    for i in np.array(range(0,n,1)):
        number=df[rowlist[i]]

        #进行插值: linear=线性插值, cubic=立方插值
        y=itp.interp1d(year0,number,kind='cubic')
        #生成插值出来的模拟数据因变量
        y2=y(xx)
        #绘图1：插值出来的大量模拟点构成的平滑曲线
        plt.plot(x,y2)
        #绘图2：原数据点

        #进行拟合: 1=线性拟合, 2=二次拟合，3=三次拟合
        p=np.polyfit(year0,number,power)
        #生成拟合出来的模拟数据因变量
        p2=np.polyval(p,xx)
        #绘图2：拟合出来的大量模拟点构成的平滑趋势曲线
        plt.plot(x,p2,linestyle=':',linewidth=3)

        #绘图3：原数据点
        plt.plot(year,number,'*',label=rowlist[i])
    
    #x轴刻度：使用原数据点的自变量
    plt.xticks(year,rotation=45)
    plt.legend(loc='best')
    plt.title(titletxt)
    plt.xlabel(footnotetxt)
    plt.show()
    
    return
#==============================================================================

def capm_beta_yearly(stkcd,mktidx,yearlist):
    """
    函数功能：分年度计算一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist: 年度列表，start日期要给第一个年份留出至少一年数据供回归使用
    输出数据：
    按年份显示CAPM市场模型回归的alpha, beta, 以及显著性和拟合优度
    无返回数据
    """
    
    #运行开始信息
    print("*** Analysing yearly CAPM betas, please wait ...")
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31' 
        
    #读取股价并准备好收益率数据
    R=prepare_capm_data(stkcd,mktidx,start,end)
    if R is None:
        print("Error #1(capm_beta_yearly): failed to prepare capm data")
        print("Information:",stkcd,mktidx,start,end)              
        return      

    #print("\n***CAPM yearly beta: Stock_return=alpha+beta*Market_return")
    #print("Stock code:",stkcd)
    #print("Market index:",mktidx)
    #print("Year Beta   R-sqr  p-value")

    #用于保存beta(CAPM)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta','alpha','R-sqr','p-value'))
    
    #分年度OLS回归
    from scipy import stats
    for year in yearlist:
        #print(year,' ',end='')
        r=R[R['Year']==year]
        if len(r)==0: continue
        try:
            output=stats.linregress(r['Close_x'],r['Close_y'])
        except:
            print("Error #2(capm_beta_yearly): no data for regression")
            print("Information:",stkcd,year,R,r)
            return             
        (beta,alpha,r_value,p_value,std_err)=output
        
        row=pd.Series({'Year':year,'Beta':beta,'alpha':alpha, \
                       'R-sqr':r_value**2,'p-value':p_value})
        betas=betas.append(row,ignore_index=True)          
        #print(year,round(beta,4),round(r_value**2,3),round(p_value,4))
    
    #设置打印标题与数据对齐
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('display.width', 180) # 设置打印宽度(**重要**)
    print("\n",betas)
    betas.set_index('Year',inplace=True)
    
    #绘图：年度贝塔系数趋势
    df=pd.DataFrame(betas['Beta'])
    title="Stock's Annual CAPM Beta: "+stkcd
    foot="\nSource: Yahoo Finance"
    plot_trend(title,foot,df,power=2)
    
    return betas   
    
if __name__=='__main__':
    yearlist=['2013','2014','2015','2016','2017','2018','2019']
    capm_beta_yearly('AAPL','^GSPC',yearlist)    

#==============================================================================
#新增投资组合贝塔系数部分
#==============================================================================
def get_price_portfolio(tickerlist,sharelist,fromdate,todate):
    """
    功能：抓取投资组合的每日价值
    输出：投资组合的收盘价格序列，最新日期的股价排列在前
    tickerlist: 股票代码列表
    sharelist：持有份额列表，与股票代码列表一一对应
    fromdate: 样本开始日期，尽量远的日期，以便取得足够多的原始样本, 'YYYY-MM-DD'
    todate: 样本结束日期，既可以是今天日期，也可以是一个历史日期
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #tickerlist=['AAPL','MSFT']
    #sharelist=[2,1]
    #fromdate='2019-1-1'
    #todate  ='2019-8-31'
    #---------------------------------------------
    
    #检查开始/结束日期的合理性
    import pandas as pd
    start=pd.to_datetime(fromdate)
    end=pd.to_datetime(todate)
    if start >= end:
        print("Error #1(get_price_portfolio): invalid start / end dates")
        return None
    
    #检查股票列表个数与份额列表个数是否一致
    if len(tickerlist) != len(sharelist):
        print("Error #2(get_price_portfolio): numbers of stocks and portions do not match")
        return None        
    
    #从雅虎财经抓取股票价格
    from pandas_datareader import data
    try:
        p=data.DataReader(tickerlist,'yahoo',fromdate,todate)
    except:
        print("Error #3(get_price_portfolio): failed to crawl stock prices")        
        print("Information:",tickerlist,fromdate,todate)  
        return None            
    cp=p['Close']
    price=pd.DataFrame(cp.dot(sharelist))
    price.rename(columns={0: 'Close'}, inplace=True)    
    
    #去掉比起始日期更早的样本
    price2=price[price.index >= fromdate]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    #提取日期和星期几
    sortedprice['Date']=sortedprice.index.strftime("%m/%d/%Y")
    sortedprice['Weekday']=sortedprice.index.weekday+1
    
    #生成输出数据格式：日期，星期几，收盘价
    dfprice=sortedprice[['Date','Weekday','Close']]

    #返回日期升序的股票收盘价序列    
    return dfprice  


#==============================================================================
def prepare_capm_portfolio(tickerlist,sharelist,mktidx,start,end):
    """
    函数功能：准备计算股票投资组合CAPM模型贝塔系数的数据，并标记年度
    输入参数：
    tickerlist: 股票代码列表
    sharelist：持有份额列表
    mktidx: 市场指数代码
    start：使用股票价格数据的开始日期，'YYYY-MM-DD'
    end：使用股票价格数据的结束日期
    输出数据：
    返回数据：带年度标记的可直接用于capm模型回归的数据表
    """
        
    #仅用于调试，正式使用前应注释掉
    #tickerlist=['AAPL','MSFT']
    #sharelist=[2,1]
    #mktidx='^GSPC'
    #start="1/1/2019"; end="8/31/2019"

    #抓取投资组合股价和指数
    stock=get_price_portfolio(tickerlist,sharelist,start,end)
    if (stock is None) or (len(stock)==0):
        print("#Error(prepare_capm_portfolio): failed to get stock prices")
        print("Info:",tickerlist,start,end)              
        return None    
    market=get_price(mktidx,start,end)
    if (market is None) or (len(market)==0):
        print("#Error(prepare_capm_portfolio): failed to get market index")
        print("Info:",mktidx,start,end)              
        return None

    #计算日收益率
    import pandas as pd
    stkret=pd.DataFrame(stock['Close'].pct_change())
    mktret=pd.DataFrame(market['Close'].pct_change())

    #合并：mktret作为Close_x，stkret作为Close_y，去掉空缺
    R=pd.merge(mktret,stkret,how='left',left_index=True,right_index=True)
    R=R.dropna()

    #标记各个年度
    R['Year']=R.index.strftime("%Y")

    #返回带年份的股票收益率序列
    return R

#==============================================================================
def capm_beta_portfolio(tickerlist,sharelist,mktidx,start,end):
    """
    函数功能：计算投资组合的静态CAPM模型贝塔系数
    输入参数：
    tickerlist: 股票代码列表
    sharelist：持有份额列表
    mktidx: 指数代码
    start：使用股票价格数据的开始日期，MM/DD/YYYY
    end：使用股票价格数据的结束日期，MM/DD/YYYY
    输出数据：
    显示CAPM市场模型回归的截距, beta, 以及显著性和拟合优度
    无返回数据
    """
        
    #读取股价并准备好收益率数据
    R=prepare_capm_portfolio(tickerlist,sharelist,mktidx,start,end)
    if R is None:
        print("Error #1(capm_beta_portfolio): failed to prepare capm data")
        print("Information:",tickerlist,sharelist,mktidx,start,end)              
        return   

    #全数据OLS回归
    from scipy import stats 
    (beta,alpha,r_value,p_value,std_err)= \
        stats.linregress(R['Close_x'],R['Close_y'])

    #显示回归结果
    print("\n *** Portfolio CAPM Beta Coefficient \
          \n Model: Stock_return=intercept + beta * Market_return")
    print(" Portfolio stocks:",tickerlist)
    print(" Stock portions  :",sharelist)
    print(" Market index    :",mktidx)
    print(" Intercept       :",round(alpha,4))
    print(" Portfolio beta  :",round(beta,4))
    print(" R-sqr       :",round(r_value**2,4))
    print(" p-value         :",round(p_value,4))

    return beta


#==============================================================================
def capm_beta_portfolio_yearly(tickerlist,sharelist,mktidx,yearlist):
    """
    函数功能：分年度计算投资组合的CAPM模型贝塔系数，并绘图
    输入参数：
    tickerlist: 投资组合中各个成分股的股票代码
    sharelist: 各个成分股的持股比例
    mktidx: 指数代码
    yearlist: 年度列表，start日期要给第一个年份留出至少一年数据供回归使用
    输出数据：
    按年份绘图beta
    无返回数据
    """
    
    #运行开始信息
    print("*** Analysing yearly portfolio CAPM betas, please wait ...")
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31' 
        
    #读取股价并准备好收益率数据
    R=prepare_capm_portfolio(tickerlist,sharelist,mktidx,start,end)
    if (R is None) or (len(R)==0):
        print("#Error(capm_beta_portfolio_yearly): failed to prepare capm data")
        print("Info:",tickerlist,sharelist,mktidx,start,end)              
        return      

    #用于保存beta(CAPM)和beta
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta','intercept','R-sqr','p-value'))
    
    #分年度OLS回归
    from scipy import stats
    for year in yearlist:
        #print(year,' ',end='')
        r=R[R['Year']==year]
        if len(r)==0: continue
        try:
            output=stats.linregress(r['Close_x'],r['Close_y'])
        except:
            print("Error #2(capm_beta_portfolio_yearly): no data for regression")
            print("Information:",year,R,r)
            return         
        (beta,alpha,r_value,p_value,std_err)=output
        
        row=pd.Series({'Year':year,'Beta':beta,'intercept':alpha, \
                       'R-sqr':r_value**2,'p-value':p_value})
        betas=betas.append(row,ignore_index=True)          
        
    print("\n",betas)
    betas.set_index('Year',inplace=True)
    
    #绘图：年度贝塔系数变化
    df=pd.DataFrame(betas['Beta'])
    title="Investment Portfolio's Annual CAPM Betas"+ \
            "\nPortfolio: "+str(tickerlist)+"\nComposition: "+str(sharelist)
    foot="\nSource: Yahoo Finance"
    plot_trend(title,foot,df,power=2)
    
    return  betas  
    
if __name__=='__main__':
    yearlist=['2013','2014','2015','2016','2017','2018','2019']
    capm_beta_portfolio_yearly(['AAPL','MSFT'],[2,1],'^GSPC',yearlist)
    capm_beta_portfolio_yearly(['600028.SS','600036.SS'],[2,1],'000001.SS',yearlist)    

#==============================================================================
def capm_beta_portfolio_yearly_excel(tickerlist,sharelist,mktidx,yearlist, \
                                     excelfile,sheetname='Sheet1'):
    """
    函数功能：分年度计算投资组合的CAPM模型贝塔系数，绘图，结果保存到Excel
    输入参数：
    tickerlist: 投资组合中各个成分股的股票代码
    sharelist: 各个成分股的持股比例
    mktidx: 指数代码
    yearlist: 年度列表
    excelfile: 带目录的Excel文件名，如果目录不存在则出错
    sheetname：Excel文件中的sheet名
    输出：
    按年份绘图beta系数, 并保存到Excel文件
    无返回数据
    """
    
    #运行开始信息
    print("\n*** Analysing yearly portfolio CAPM betas, please wait ...")
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31' 
        
    #读取股价并准备好收益率数据
    R=prepare_capm_portfolio(tickerlist,sharelist,mktidx,start,end)
    if R is None:
        print("Error #1(capm_beta_portfolioyearly_excel): failed to prepare capm data")
        print("Information:",tickerlist,sharelist,mktidx,start,end)              
        return      

    #用于保存beta(CAPM)和beta
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta','intercept','R-sqr','p-value'))
    
    #分年度OLS回归
    from scipy import stats
    for year in yearlist:
        #print(year,' ',end='')
        r=R[R['Year']==year]
        if len(r)==0: continue
        try:
            output=stats.linregress(r['Close_x'],r['Close_y'])
        except:
            print("Error #2(capm_beta_portfolio_yearly_excel): no data available for regressing beta")
            print("Information:",year,R,r)
            return         
        (beta,alpha,r_value,p_value,std_err)=output
        
        row=pd.Series({'Year':year,'Beta':beta,'intercept':alpha, \
                       'R-sqr':r_value**2,'p-value':p_value})
        betas=betas.append(row,ignore_index=True)          
        
    betas2=betas.copy() #用于保存excel   
    betas2['Year']=betas2['Year'].astype('int')
    betas2['Portfolio']=str(tickerlist)
    betas2['Share Ratio']=str(sharelist)
    betas2['Market Index']=mktidx
    
    betas.set_index('Year',inplace=True)    #用于绘图
    
    #绘图：年度贝塔系数变化
    df=pd.DataFrame(betas['Beta'])
    title="Investment Portfolio's Annual CAPM Betas"+ \
            "\nPortfolio: "+str(tickerlist)+"\nComposition: "+str(sharelist)
    foot="\nSource: Yahoo Finance"
    plot_trend(title,foot,df,power=2)
    
    """
    #为折线加数据标签
    import matplotlib.pyplot as plt
    for a,b in zip(betas.index,betas['Beta']):
        plt.text(a,b+0.02,str(round(b,2)),ha='center',va='bottom',fontsize=7)
    plt.show()
    """
    
    #保存到Excel   
    import pandas as pd
    try:
        file1=pd.ExcelFile(excelfile)
    except:
        #不存在excelfile文件，直接写入
        betas2.to_excel(excelfile,sheet_name=sheetname, \
                       header=True,encoding='utf-8')
        print("***Results saved in",excelfile,"@ sheet",sheetname)
        return
    else:
        #已存在excelfile文件，先将所有已有内容读出        
        dict=pd.read_excel(file1, None)
    file1.close()
    
    #获得所有sheet名字
    sheetlist=list(dict.keys())
    
    #检查新的sheet名字是否已存在
    try:
        pos=sheetlist.index(sheetname)
    except:
        #不存在重复
        dup=False
    else:
        #存在重复，合并内容
        dup=True
        #print(dict[sheetlist[pos]],betas2)
        df1=dict[sheetlist[pos]][['Year','Beta','intercept','R-sqr','p-value','Portfolio','Share Ratio','Market Index']]
        df=pd.concat([df1,betas2],axis=0,ignore_index=True)        
        dict[sheetlist[pos]]=df
    
    #将原有内容写回excelfile    
    result=pd.ExcelWriter(excelfile)
    for s in sheetlist:
        df1=dict[s][['Year','Beta','intercept','R-sqr','p-value','Portfolio','Share Ratio','Market Index']]
        df1.to_excel(result,s,header=True,index=True,encoding='utf-8')
    #写入新内容
    if not dup: #sheetname未重复
        betas2.to_excel(result,sheetname,header=True,index=True,encoding='utf-8')
    try:
        result.save()
        result.close()
    except:
        print("Error #3(capm_beta_portfolio_yearly_excel): writing file permission denied")
        print("Information:",excelfile)  
        return
    print("***Results saved in",excelfile,"@ sheet",sheetname)
    return  betas  
    
if __name__=='__main__':
    yearlist=['2013','2014','2015','2016','2017','2018','2019']
    excelfile='C:/temp/myexcel.xls'
    capm_beta_portfolio_yearly_excel(['AAPL','MSFT'],[2,1],'^GSPC',yearlist, excelfile,'p01')

#==============================================================================
def compare2_betas_yearly(stkcd1,stkcd2,mktidx,yearlist):
    """
    函数功能：分年度计算两只股票的CAPM模型贝塔系数，并绘图对比其风险特征的对冲性
    输入参数：
    stkcd1: 股票代码
    stkcd2: 股票代码
    mktidx: 指数代码
    yearlist: 年度列表，start日期要给第一个年份留出至少一年数据供回归使用
    输出数据：
    按年份绘图贝塔系数的变化
    无返回数据
    """
    #仅用于测试，完成后应注释掉
    #stkcd1='600028.SS'
    #stkcd2='600036.SS'
    #mktidx='000001.SS'
    #yearlist=['2013','2014','2015','2016','2017','2018','2019']

    
    #运行开始信息
    print("*** Comparing stock CAPM betas, please wait ...")
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31' 
        
    #读取股价并准备好收益率数据
    R1=prepare_capm_data(stkcd1,mktidx,start,end)
    if R1 is None:
        print("Error #1(compare2_betas_yearly): failed to prepare capm data")
        print("Information:",stkcd1,mktidx,start,end)              
        return      

    R2=prepare_capm_data(stkcd2,mktidx,start,end)
    if R2 is None:
        print("Error #2(compare2_betas_yearly): failed to prepare capm data")
        print("Information:",stkcd2,mktidx,start,end)              
        return 

    #用于保存beta(CAPM)
    import pandas as pd
    betas1=pd.DataFrame(columns=('Year','Beta','alpha','R-sqr','p-value'))
    #分年度OLS回归
    from scipy import stats
    for year in yearlist:
        r=R1[R1['Year']==year]
        if len(r)==0: continue
        try:
            output=stats.linregress(r['Close_x'],r['Close_y'])
        except:
            print("Error #3(compare2_betas_yearly): no data for regression")
            print("Information:",stkcd1,year,r,R1)
            continue         
        (beta,alpha,r_value,p_value,std_err)=output
        
        row=pd.Series({'Year':year,'Beta':beta,'alpha':alpha, \
                       'R-sqr':r_value**2,'p-value':p_value})
        betas1=betas1.append(row,ignore_index=True)          
    betas1.set_index('Year',inplace=True)

    betas2=pd.DataFrame(columns=('Year','Beta','alpha','R-sqr','p-value'))
    for year in yearlist:
        #print(year,' ',end='')
        r=R2[R2['Year']==year]
        if len(r)==0: continue
        try:
            output=stats.linregress(r['Close_x'],r['Close_y'])
        except:
            print("Error #4(compare2_betas_yearly): no data for regression")
            print("Information:",stkcd2,year,r,R2)
            continue         
        (beta,alpha,r_value,p_value,std_err)=output        
        row=pd.Series({'Year':year,'Beta':beta,'alpha':alpha, \
                       'R-sqr':r_value**2,'p-value':p_value})
        betas2=betas2.append(row,ignore_index=True)          
    betas2.set_index('Year',inplace=True)
    
    #绘图：年度贝塔系数变化
    import matplotlib.pyplot as plt
    plt.plot(betas1['Beta'],label=stkcd1,c='red',marker='o',lw=3)
    plt.plot(betas2['Beta'],label=stkcd2,c='blue',marker='o',lw=3)
    plt.axhline(y=1.0,color='b',linestyle=':',c='green',label='Market line')  
    plt.ylabel("Beta coefficient",fontweight='bold')
    plt.xticks(rotation=45,fontweight='bold')
    trtitle="Comparing Hedgeability of Stocks"+"\n"+stkcd1+" vs "+stkcd2
    plt.title(trtitle,fontweight='bold')
    plt.legend(loc='best')
    plt.show()
    
    return  betas1,betas2  
    
if __name__=='__main__':
    yearlist=['2013','2014','2015','2016','2017','2018','2019']
    compare2_betas_yearly('AMZN','WMT','^GSPC',yearlist)    
    compare2_betas_yearly('601857.SS','600036.SS','000001.SS',yearlist)

#==============================================================================
#==============================================================================
#==============================================================================
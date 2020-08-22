﻿# -*- coding: utf-8 -*-

"""
版权：王德宏，北京外国语大学国际商学院
功能：计算CAPM模型贝塔系数的调整值
版本：2.1，2019-7-25
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
#==============================================================================
def check_period(fromdate,todate):
    """
    功能：根据开始/结束日期检查期间日期的合理性
    输入参数：
    fromdate：开始日期。格式：YYYY-MM-DD
    enddate：开始日期。格式：YYYY-MM-DD
    输出参数：
    validity：期间合理性。True-合理，False-不合理
    start：开始日期。格式：datetime类型
    end：结束日期。格式：datetime类型
    """
    import pandas as pd
    try:
        start=pd.to_datetime(fromdate)
    except:
        print("Error #1(check_period): invalid date:",fromdate)
        return None,None,None         
    try:
        end=pd.to_datetime(todate)
    except:
        print("Error #2(check_period): invalid date:",todate)
        return None,None,None          
    if start >= end:
        print("Error #3(check_period): invalid period: from",fromdate,"to",todate)
        return None,None,None     

    return True,start,end
#==============================================================================
def get_price(ticker,start,end):
    """
    功能：抓取股价，使用pandas_datareader
    输出：指定收盘价格序列，最新日期的股价排列在前
    ticker: 股票代码。大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    start: 样本开始日期，尽量远的日期，以便取得足够多的原始样本，yyyy-mm-dd
    end: 样本结束日期，既可以是今天日期，也可以是一个历史日期
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #ticker='0700.HK'
    #start='2016-01-01'
    #end='2018-12-31'
    #---------------------------------------------
    
    #抓取雅虎股票价格
    from pandas_datareader import data
    try:
        price=data.DataReader(ticker,'yahoo',start,end,retry_count=3,pause=1)
    except:
        print("Error #1(get_price): server not responsed!")
        return None
    
    if len(price) == 0:
        print("Error #2(get_price): server reached but returned no data!")
        print("==>Tip: for a stock listed outside US, try a later start date!")
        return None
    
    #去掉比起始日期更早的样本
    price2=price[price.index >= start]

    #去掉比结束日期更晚的样本
    #price2=price2[price2.index <= end]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    #提取日期和星期几
    sortedprice['Date']=sortedprice.index.strftime("%Y-%m-%d")
    sortedprice['Weekday']=sortedprice.index.weekday+1
    
    #生成输出数据格式：日期，星期几，收盘价
    dfprice=sortedprice[['Date','Weekday','Close']]

    #返回日期升序的股票收盘价序列    
    return dfprice


if __name__=='__main__':
    prices1=get_price('SINA','2001-01-01','2018-12-31')
    prices2=get_price('0700.HK','2013-01-01','2018-12-31')
    index2=get_price('^HSI','2014-01-01','2018-12-31')

#==============================================================================
def get_price_yf(ticker,start,end):
    """
    功能：抓取股价，使用yfinance
    输出：指定收盘价格序列，最新日期的股价排列在前
    ticker: 股票代码。大陆股票代码加上后缀.SZ或.SS，港股代码去掉前导0加后缀.HK
    start: 样本开始日期，尽量远的日期，以便取得足够多的原始样本，yyyy-mm-dd
    end: 样本结束日期，既可以是今天日期，也可以是一个历史日期
    """
    
    #仅为调试用的函数入口参数，正式使用前需要注释掉！
    #ticker='0700.HK'
    #start='2016-01-01'
    #end='2018-12-31'
    #---------------------------------------------
    
    #转换日期
    r,startdate,enddate=check_period(start,end)
    if r is None:
        print("Error #1(get_price_yf): invalid time period")
        return None        
        
    #抓取雅虎股票价格
    import yfinance as yf
    try:
        stock=yf.Ticker(ticker)
        p=stock.history(start=start,end=end)
    except:
        print("Error #1(get_price_yf): server not responsed!")
        return None
    
    if len(p) == 0:
        print("Error #2(get_price_yf): server reached but returned no data!")
        return None
    
    #去掉比起始日期更早的样本
    price=p[p.index >= startdate]
    #去掉比结束日期更晚的样本
    price2=price[price.index <= enddate]
    
    #按日期升序排序，近期的价格排在后面
    sortedprice=price2.sort_index(axis=0,ascending=True)

    #提取日期和星期几
    sortedprice['Date']=sortedprice.index.strftime("%Y-%m-%d")
    sortedprice['Weekday']=sortedprice.index.weekday+1
    
    #生成输出数据格式：日期，星期几，收盘价
    dfprice=sortedprice[['Date','Weekday','Close']]

    #返回日期升序的股票收盘价序列    
    return dfprice


if __name__=='__main__':
    prices1=get_price_yf('SINA','2001-01-01','2018-12-31')
    prices2=get_price_yf('0700.HK','2013-01-01','2018-12-31')
    index2=get_price_yf('^HSI','2014-01-01','2018-12-31')
    
    
#==============================================================================
def prepare_capm(stkcd,mktidx,start,end):
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
    #stkcd='002504.SZ'; mktidx='000001.SS'
    #start="12/31/2011"; end="12/31/2018"

    #抓取股价和指数
    stock=get_price_yf(stkcd,start,end)
    if stock is None:
        print("Error #1(prepare_capm): no stock data retrieved from server!")
        return None
    market=get_price_yf(mktidx,start,end)
    if market is None:
        print("Error #2(prepare_capm): no index data retrieved from server!")
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

if __name__=='__main__':
    R1=prepare_capm('0700.HK','^HSI','2014-01-01','2018-12-31')

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

if __name__=='__main__':
    yearlist=gen_yearlist('2013','2019')
#==============================================================================
def get_beta_ML(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用ML方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，列出其中期间的贝塔系数
    输出数据：
    显示CAPM市场模型回归的beta, 以及ML调整后的beta系数
    返回数据:年度CAPM贝塔系数和ML调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'    
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("Error #1(get_beta_ML): Preparing CAPM data failed!")
        return None

    if (R is None):
        print("Error #2(get_beta_ML): server time out")
        print("Possible reasons:")  
        print("  1)internet connection problem")            
        print("  2)incorrect parameters for function")            
        print("  3)server too busy")            
        return None
    if (len(R) == 0):
        print("Error #3(get_beta_ML): server returned empty data")
        print("Possible reasons: data tentatively inaccessible for non-US stock")              
        return None
    
    #用于保存beta(CAPM)和beta(ML)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(ML)'))

    #计算Merrill-Lynch方法贝塔系数调整
    from scipy import stats
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta,alpha,r_value,p_value,std_err)=output
            beta_ML=beta*2.0/3.0+1.0/3.0
            #整齐输出 
            #print(year,"%6.4f "%(beta),"%6.4f "%(beta_ML))

            row=pd.Series({'Year':year,'Beta(CAPM)':beta,'Beta(ML)':beta_ML})
            betas=betas.append(row,ignore_index=True)

    betas.set_index(["Year"], inplace=True)
    
    if printout == True: printdf(betas,2)
    if graph == True:
        model="Merrill-Lynch Beta Adjustment"
        draw2_betas(model,mktidx,stkcd,betas)

    return betas

#==============================================================================
def printdf(df,decimal=2):
    """
    功能：整齐地显示数据框的内容，自动调整各列宽度
    """
    #打印时保留的小数点位数
    dec="%."+str(decimal)+"f"
    format=lambda x: dec % x
    df1=df.applymap(format)    
    
    import pandas as pd
    #调整最佳列宽
    old_width = pd.get_option('display.max_colwidth')
    pd.set_option('display.max_colwidth', -1)
    print(df1)
    pd.set_option('display.max_colwidth', old_width)

    return
    
if __name__=='__main__':
    yearlist=gen_yearlist['2010','2019']
    betas=get_beta_ML('AAPL','^GSPC',yearlist)    
    betas2=get_beta_ML('BILI','^GSPC',yearlist)
    betas3=get_beta_ML('0700.HK','^HSI',yearlist)
    yearlist1=['2015','2016','2017','2018']
    betas3=get_beta_ML('0700.HK','^HSI',yearlist1)

#==============================================================================
def draw2_betas(model,scope,ticker,betas):    
    """
    功能：绘制双曲线的贝塔因子变化图
    输入参数：
    model: 模型类型, 任意字符串(例如Merrill-Lynch Beta Adjustment)
    scope: 市场指数, 任意字符串(例如Standard & Poor 500)
    ticker：股票代码
    输出：图形
    """
    #仅用作测试，完成后应注释掉
    #model="Merrill-Lynch Beta Adjustment"
    #scope="Standard & Poor 500"
    #ticker="AAPL"

    #取得股票和指数名字，对于非美股可能耗时较长
    """
    import yfinance as yf
    mktidx= yf.Ticker(scope)
    idxinfo=mktidx.info
    idxname=idxinfo['shortName']
    stkcd=yf.Ticker(ticker)
    stkinfo=stkcd.info
    stkname=stkinfo['shortName']   
    title1="\n"+stkname+"\n"+model+"\n(Benchmark on "+idxname+")"
    """
    title1="\n"+ticker+": "+model+"\n(Benchmark on Market Index "+scope+")"
   
    #转换索引类型为DatetimeIndex，便于后续处理
    """
    import pandas as pd
    betas['Date']=betas.index
    betas['Date']=pd.to_datetime(betas['Date'])
    betas.set_index('Date',inplace=True)
    """

    #获得列明
    betalist=betas.columns.values.tolist()
    beta1=betalist[0]
    beta2=betalist[1]

    import matplotlib.pyplot as plt
    try:
        plt.plot(betas[beta1],label=beta1,marker='o',color='red')
        plt.plot(betas[beta2],label=beta2,marker='*',linewidth=4,color='blue')
    except:
        print("Error #1(draw2_betas) no available data for drawing!")
        return
    plt.axhline(y=1.0,color='b',linestyle=':',label='Market line')  
    plt.title(title1,fontsize=12,fontweight='bold')
    plt.ylabel("Betas",fontsize=12,fontweight='bold')
    plt.xticks(rotation=45)
    plt.legend(loc='best')    
    plt.show()       
    
    return

if __name__=='__main__':
    model="ML Beta Adjustment"
    scope="SP500"
    ticker="AAPL"
    draw2_betas(model,scope,ticker,betas)




#==============================================================================
def get_beta_SW(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用SW方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，列出其中期间的贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM市场模型回归的beta, 以及调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'   
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("Error #1(get_beta_SW): preparing CAPM data failed!")
        return None

    if (R is None):
        print("Error #2(get_beta_SW): server time out")
        print("Possible reasons:")  
        print("  1)internet connection problem")            
        print("  2)incorrect parameters for function")            
        print("  3)server too busy")            
        return None
    if (len(R) == 0):
        print("Error #3(get_beta_SW): server returned empty data")
        print("Possible reasons: data tentatively inaccessible for non-US stock")              
        return None

    #用于保存beta(CAPM)和beta(SW)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(SW)'))

    #计算Scholes-William调整
    R['Close_x+1']=R['Close_x'].shift(1)    
    R['Close_x-1']=R['Close_x'].shift(-1)
    R=R.dropna()    #stats.linregress不接受空缺值

    from scipy import stats    
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta0,alpha,r_value,p_value,std_err)=output

            output=stats.linregress(r['Close_x+1'],r['Close_y'])
            (beta1,alpha,r_value,p_value,std_err)=output 

            output=stats.linregress(r['Close_x-1'],r['Close_y'])
            (beta_1,alpha,r_value,p_value,std_err)=output    

            output=stats.linregress(r['Close_x-1'],r['Close_x'])
            (rou,alpha,r_value,p_value,std_err)=output    

            beta_SW=(beta_1+beta0+beta1)/(1.0+2.0*rou)
            row=pd.Series({'Year':year,'Beta(CAPM)':beta0,'Beta(SW)':beta_SW})
            betas=betas.append(row,ignore_index=True)            
    
    betas.set_index(["Year"], inplace=True)
    
    if printout == True: printdf(betas,2)
    if graph == True:
        model="Scholes-William Beta Adjustment"
        draw2_betas(model,mktidx,stkcd,betas)
    
    return betas

    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas_AAPL=get_beta_SW('AAPL','^GSPC',yearlist)
    
    model="SW Beta Adjustment"
    scope="SP500"
    ticker="AAPL"
    draw2_betas(model,scope,ticker,betas_AAPL)

#==============================================================================
def get_beta_dimson(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用Dimson(1979)方法调整一只股票的CAPM模型贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，用于计算年度贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM的beta, 以及调整后的beta系数
    """

    #仅为测试用，完成后应立即注释掉
    #stkcd='0700.HK'
    #mktidx='^HSI'
    #yearlist=['2015','2016','2017','2018']
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'  
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("Error #1(get_beta_dimson): preparing CAPM data failed!")
        return None

    if (R is None):
        print("Error #2(get_beta_dimson): server time out")
        print("Possible reasons:")  
        print("  1)internet connection problem")            
        print("  2)incorrect parameters for function")            
        print("  3)server too busy")            
        return None
    if (len(R) == 0):
        print("Error #3(get_beta_dimson): server returned empty data")
        print("Possible reasons: data tentatively inaccessible for non-US stock")              
        return None

    #用于保存beta(CAPM)和beta(Dimson)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(Dimson)'))

    #计算Dimson(1979)调整
    R['Close_x+1']=R['Close_x'].shift(1)    
    R['Close_x-1']=R['Close_x'].shift(-1)   
    R=R.dropna()

    from scipy import stats    
    import statsmodels.api as sm
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:   
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta_capm,alpha,r_value,p_value,std_err)=output               
            
            #三个解释变量
            RX=r[['Close_x-1','Close_x','Close_x+1']]
            X1=sm.add_constant(RX)	#要求回归具有截距项
            Y=r['Close_y']
            model = sm.OLS(Y,X1)	#定义回归模型，X1为多元矩阵
            results = model.fit()	#进行OLS回归

            (alpha,beta_1,beta0,beta1)=results.params	#提取回归系数
            beta_dimson=beta_1+beta0+beta1            

            row=pd.Series({'Year':year,'Beta(CAPM)':beta_capm, \
                           'Beta(Dimson)':beta_dimson})
            betas=betas.append(row,ignore_index=True)               

    betas.set_index(["Year"], inplace=True)

    if printout == True: printdf(betas,2)
    if graph == True:
        model="Dimson Beta Adjustment"
        draw2_betas(model,mktidx,stkcd,betas)

    return betas
    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas_MSFT=get_beta_dimson('MSFT','^GSPC',yearlist)
    
    model="Dimson Beta Adjustment"
    scope="SP500"
    ticker="MSFT"
    draw2_betas(model,scope,ticker,betas_MSFT)

    betas_MSFT2=get_beta_dimson('MSFT','^DJI',yearlist)
    
    model="Dimson Beta Adjustment"
    scope="DJIA"
    ticker="MSFT"
    draw2_betas(model,scope,ticker,betas_MSFT2)
#==============================================================================
def prepare_hamada_yearly_yahoo(ticker):
    """
    功能：从雅虎财经下载财报数据，计算hamada模型需要的因子
    局限：只能下载最近4年的财报
    输入：股票代码
    输出：
    数据框, CFLB，贝塔Lev对贝塔Unlev的倍数
    年度列表
    """
    #仅限测试使用    
    #ticker='AAPL'

    import yfinance as yf
    stock=yf.Ticker(ticker)    

    #利润表
    try:
        is0=stock.financials
    except:
        print("#Error(prepare_hamada_yearly_yahoo): failed to get financial info for",ticker)
        return None,None
    if len(is0)==0:
        print("#Error(prepare_hamada_yearly_yahoo): failed to get financial info for",ticker)
        return None,None
    is1=is0.T
    is1['income tax expense']=is1['Income Tax Expense'].astype('float')
    is1['income before tax']=is1['Income Before Tax'].astype('float')
    is1['tax rate']=is1['income tax expense']/is1['income before tax']

    import pandas as pd
    is1['date']=pd.to_datetime(is1.index)
    is1.set_index(["date"], inplace=True)
    is2=is1.sort_index(axis=0,ascending=True)
    tax=pd.DataFrame(is2['tax rate'])

    #资产负债表
    bs0=stock.balance_sheet
    bs1=bs0.T
    bs1['total liabilities']=bs1['Total Liab'].astype('float')
    bs1['total equities']=bs1["Total Stockholder Equity"].astype('float')
    bs1['lev ratio']=bs1['total liabilities']/bs1['total equities']
    bs1['date']=pd.to_datetime(bs1.index)
    bs1.set_index(['date'],inplace=True)
    bs2=bs1.sort_index(axis=0,ascending=True)
    lev=pd.DataFrame(bs2['lev ratio'])
    
    #合成，计算
    fac=pd.merge(lev,tax,how='left',left_index=True,right_index=True)
    fac['CFLB%']=1/(1+(1/fac['lev ratio'])*(1/abs(1-fac['tax rate'])))*100
    fac['lev_unlev']=1+fac['lev ratio']*(1-fac['tax rate'])
    fac['year']=fac.index.strftime("%Y")
    yearlist=list(fac['year'])

    return fac,yearlist

if __name__ =="__main__":
    ticker="MSFT"
    fac,yl=prepare_hamada_yearly_yahoo("MSFT")

#==============================================================================
def get_beta_hamada(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：使用Hamada(1972)方法，计算无杠杆贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，用于计算年度贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM的beta, Hamada beta，CFLB(债务融资对CAPM beta系数的贡献率)
    """

    #仅为测试用，完成后应立即注释掉
    """
    stkcd='0700.HK'
    mktidx='^HSI'
    yearlist=['2015','2016','2017','2018']
    """
    
    #计算Hamada参数，并返回可用的年度列表
    fac,yearlist=prepare_hamada_yearly_yahoo(stkcd)
    if fac is None:
        print("#Error(get_beta_hamada): no financial statements available")
        return None
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'  
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("Error #1(get_beta_hamada): preparing CAPM data failed!")
        print("Information:",stkcd,mktidx,yearlist)              
        return None

    if (R is None):
        print("Error #2(get_beta_hamada): server time out")
        print("Possible reasons:")  
        print("  1)internet connection problem")            
        print("  2)incorrect parameters for function")            
        print("  3)server too busy")            
        return None
    if (len(R) == 0):
        print("Error #3(get_beta_hamada): server returned empty data")
        print("Possible reasons: data tentatively inaccessible for non-US stock")              
        return None
    R=R.dropna()
    
    #用于保存beta(CAPM)和beta(Hamada)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(Unlevered)','CFLB%'))

    from scipy import stats    
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) != 0:   
            output=stats.linregress(r['Close_x'],r['Close_y'])
            (beta_capm,alpha,r_value,p_value,std_err)=output               
            
            #Hamada无杠杆因子
            lev_unlev=fac[fac['year']==year]['lev_unlev'].values[0]
            beta_hamada=beta_capm/lev_unlev
            cflb=fac[fac['year']==year]['CFLB%'].values[0]            

            row=pd.Series({'Year':year,'Beta(CAPM)':beta_capm, \
                           'Beta(Unlevered)':beta_hamada,'CFLB%':cflb})
            betas=betas.append(row,ignore_index=True)               

    betas.set_index(["Year"], inplace=True)

    if printout == True: 
        printdf(betas,2)
    if graph == True:
        model="Hamada Unlevered Beta"
        draw2_betas(model,mktidx,stkcd,betas)
        
        #绘制CFLB
        if len(betas)<=1: return betas
        
        import matplotlib.pyplot as plt
        plt.plot(betas['CFLB%'],marker='o',color='red',lw=3)
        
        bmin=min(list(betas['CFLB%']))
        bmax=max(list(betas['CFLB%']))
        axhmin=(int(bmin/10)+1)*10
        if bmin <= axhmin <= bmax:
            plt.axhline(y=axhmin,color='b',linestyle=':') 
        axhmax=(int(bmax/10))*10
        if bmin <= axhmax <= bmax:
            plt.axhline(y=axhmax,color='b',linestyle=':')         
        
        title1=stkcd+": Contribution of Financial Leverage to Beta"+ \
            "\n(Benchmark on Market Index "+mktidx+")"
        plt.title(title1,fontsize=12,fontweight='bold')
        plt.ylabel("CFLB %",fontsize=12,fontweight='bold')
        #plt.legend(loc='best')         
        plt.grid(ls='-.')
        #查看可用的样式：print(plt.style.available)
        #样式：bmh(好),classic,ggplot(好，图大)，tableau-colorblind10，
        #样式：seaborn-bright，seaborn-poster，seaborn-whitegrid
        plt.style.use('bmh')
        plt.show()         

    return betas
    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas1=get_beta_hamada('MSFT','^GSPC',yearlist)

#==============================================================================
def init_ts():
    """
    功能：初始化tushare pro，登录后才能下载数据
    """
    import tushare as ts
    #设置token
    token='49f134b05e668d288be43264639ac77821ab9938ff40d6013c0ed24f'
    pro=ts.pro_api(token)
    
    return pro
#==============================================================================
def convert_date_ts(y4m2d2):
    """
    功能：日期格式转换，YYYY-MM-DD-->YYYYMMDD，用于tushare
    输入：日期，格式：YYYY-MM-DD
    输出：日期，格式：YYYYMMDD
    """
    import pandas as pd
    try: date1=pd.to_datetime(y4m2d2)
    except:
        print("Error #1(convert_date_tushare): invalid date:",y4m2d2)
        return None 
    else:
        date2=date1.strftime('%Y')+date1.strftime('%m')+date1.strftime('%d')
    return date2

if __name__ == '__main__':
    convert_date_ts("2019/11/1")
#==============================================================================
def prepare_hamada_yearly_ts(ticker):
    """
    功能：从tushare下载财报数据，计算hamada模型需要的因子
    局限：
    输入：股票代码
    输出：
    数据框, CFLB，贝塔Lev对贝塔Unlev的倍数
    年度列表
    """
    #仅限测试使用    
    #ticker='600519.SS'
    
    #转换股票代码.SS为.SH(tushare使用.SH而不是雅虎的.SS)
    ticker1=ticker.upper()
    try: ticker2=ticker1.replace('.SS','.SH')
    except: pass

    #初始化tushare
    pro=init_ts() 
    
    #利润表
    is0=pro.income(ts_code=ticker2)
    
    #修改报表截止日期格式为YYYY-MM-DD
    is0['year']=is0.apply(lambda x:x['end_date'][0:4],axis=1)
    is0['MM']=is0.apply(lambda x:x['end_date'][4:6],axis=1)
    is0['DD']=is0.apply(lambda x:x['end_date'][6:8],axis=1)
    is0['date']=is0['year']+'-'+is0['MM']+'-'+is0['DD']
    
    #只取年报              
    is1=is0[is0['MM']=='12']
    #最新的合并报表
    is1=is1[is1['report_type']=='1'] 
    #去掉重复值
    is1.drop_duplicates(subset=['ts_code','end_date','report_type'], \
                        keep='first',inplace=True)
    #计算实际所得税率
    is1['income tax expense']=is1['income_tax'].astype('float')
    is1['income before tax']=is1['total_profit'].astype('float')
    is1['tax rate']=is1['income tax expense']/is1['income before tax']

    is1.set_index(["year"], inplace=True)
    is2=is1.sort_index(axis=0,ascending=True)
    import pandas as pd
    tax=pd.DataFrame(is2['tax rate'])

    #资产负债表
    bs0=pro.balancesheet(ts_code=ticker2)
    
    #修改报表截止日期格式为YYYY-MM-DD
    bs0['year']=bs0.apply(lambda x:x['end_date'][0:4],axis=1)
    bs0['MM']=bs0.apply(lambda x:x['end_date'][4:6],axis=1)
    bs0['DD']=bs0.apply(lambda x:x['end_date'][6:8],axis=1)
    bs0['date']=bs0['year']+'-'+bs0['MM']+'-'+bs0['DD']    
    
    #只取年报              
    bs1=bs0[bs0['MM']=='12']
    #最新的合并报表
    bs1=bs1[bs1['report_type']=='1'] 
    #去掉重复值
    bs1.drop_duplicates(subset=['ts_code','end_date','report_type'], \
                        keep='first',inplace=True)
    
    bs1['total liabilities']=bs1['total_liab'].astype('float')
    bs1['total equities']=(bs1["total_assets"]-bs1["total_liab"]).astype('float')
    bs1['lev ratio']=bs1['total liabilities']/bs1['total equities']
    bs1.set_index(['year'],inplace=True)
    bs2=bs1.sort_index(axis=0,ascending=True)
    lev=pd.DataFrame(bs2['lev ratio'])
    
    #合成，计算
    fac=pd.merge(lev,tax,how='left',left_index=True,right_index=True)
    fac['CFLB%']=1/(1+(1/fac['lev ratio'])*(1/abs(1-fac['tax rate'])))*100
    fac['lev_unlev']=1+fac['lev ratio']*(1-fac['tax rate'])
    fac['year']=fac.index
    yearlist=list(fac['year'])

    return fac,yearlist

if __name__ =="__main__":
    fac,yl=prepare_hamada_yearly_ts("MSFT")

#==============================================================================
def get_beta_hamada_ts(stkcd,mktidx,yearlist,printout=True,graph=True):
    """
    函数功能：基于Hamada(1972)方法，使用tushare数据，计算无杠杆贝塔系数
    输入参数：
    stkcd: 股票代码
    mktidx: 指数代码
    yearlist：年度列表，用于计算年度贝塔系数
    输出数据：显示CAPM市场模型回归的beta, 以及调整后的beta系数
    返回数据：CAPM的beta, Hamada beta，CFLB(债务融资对CAPM beta系数的贡献率)
    """

    #仅为测试用，完成后应立即注释掉
    """
    stkcd='600519.SS'
    mktidx='000001.SS'
    yearlist=gen_yearlist('2011','2019')
    """
    
    #计算Hamada参数，并返回可用的年度列表
    fac,yearlist2=prepare_hamada_yearly_ts(stkcd)
    fac=fac[fac['year']>=yearlist[0]]
    fac=fac[fac['year']<=yearlist[-1]]
    
    #生成开始结束日期
    Y4=str(int(yearlist[0])-1)
    start=Y4+'-01-01'
    end=yearlist[-1]+'-12-31'  
        
    #读取股价并准备好收益率数据
    try:
        R=prepare_capm(stkcd,mktidx,start,end)
    except:
        print("Error #1(get_beta_hamada_ts): preparing CAPM data failed!")
        print("Information:",stkcd,mktidx,yearlist)              
        return None

    if (R is None):
        print("Error #2(get_beta_hamada_ts): server time out")
        print("Possible reasons:")  
        print("  1)internet connection problem")            
        print("  2)incorrect parameters for function")            
        print("  3)server too busy")            
        return None
    if (len(R) == 0):
        print("Error #3(get_beta_hamada_ts): server returned empty data")
        print("Possible reasons: data tentatively inaccessible for non-US stock")              
        return None
    R=R.dropna()
    
    #用于保存beta(CAPM)和beta(Hamada)
    import pandas as pd
    betas=pd.DataFrame(columns=('Year','Beta(CAPM)','Beta(Unlevered)', \
                                'CFLB%','Tax Rate%','Debt Ratio%'))

    from scipy import stats    
    for year in yearlist:
        r=R[R['Year']==year]
        if len(r) == 0: continue  
        output=stats.linregress(r['Close_x'],r['Close_y'])
        (beta_capm,alpha,r_value,p_value,std_err)=output               
            
        #Hamada无杠杆因子
        try:
            lev_unlev=fac[fac['year']==year]['lev_unlev'].values[0]
        except: continue
        beta_hamada=beta_capm/lev_unlev
        cflb=fac[fac['year']==year]['CFLB%'].values[0] 
        taxrate=fac[fac['year']==year]['tax rate'].values[0]*100 
        levratio=fac[fac['year']==year]['lev ratio'].values[0]*100

        row=pd.Series({'Year':year,'Beta(CAPM)':beta_capm, \
                           'Beta(Unlevered)':beta_hamada,'CFLB%':cflb, \
                           'Tax Rate%':taxrate,'Debt Ratio%':levratio})
        betas=betas.append(row,ignore_index=True)               

    betas.set_index(["Year"], inplace=True)

    if printout == True: 
        printdf(betas,2)
    if graph == True:
        model="Hamada Unlevered Beta"
        draw2_betas(model,mktidx,stkcd,betas)
        
        #绘制Hamada影响因子
        draw_hamada_factors(stkcd,mktidx,betas)        

    return betas
    
if __name__=='__main__':
    yearlist=gen_yearlist('2010','2019')
    betas1=get_beta_hamada('MSFT','^GSPC',yearlist)
#==============================================================================
def draw_hamada_factors(stkcd,mktidx,betas):
    """
    功能：绘制Hamada模型因子的变化折线图，企业实际所得税税率，资产负债率，CFLB
    """
    if len(betas)<=1: return
    
    #计算资产负债率：由 D/E到 D/(A=D+E)
    betas['Debt/Assets%']=1/(1+1/(betas['Debt Ratio%']/100))*100

    import matplotlib.pyplot as plt
    fig=plt.figure(figsize=(12,8))
    ax1=fig.add_subplot(111)
    ax1.plot(betas['CFLB%'],marker='o',color='green',lw=3,label='CFLB%')
    ax1.plot(betas['Debt/Assets%'],marker='o',color='red',lw=2,ls='--', \
             label='Debt/Assets%')
    ax1.set_ylabel("CFLB%, Debt/Assets%")
    ax1.legend(loc='upper left') 
    ax1.set_xticklabels(betas.index,rotation=45)
    
    ax2=ax1.twinx()
    ax2.plot(betas['Tax Rate%'],marker='o',color='black',lw=2,ls='-.', \
             label='Act Income Tax%')
    ax2.set_ylabel('Income Tax%')  
    ax2.legend(loc='lower right')
    ax2.set_xticklabels(betas.index,rotation=45)
    
    title1=stkcd+": Impact of Hamada Factors on Beta"+ \
            "\n(Benchmark on Market Index "+mktidx+")"
    plt.title(title1,fontsize=12,fontweight='bold')
    plt.style.use('ggplot')
    plt.show()     
    
    return
#==============================================================================













    
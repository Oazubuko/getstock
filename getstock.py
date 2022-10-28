from pyfinviz.screener import Screener
import pandas as pd
import numpy as np
import statistics as stat


Sum =[]
list = []
class stock:
    def __init__(self, ticker, pe, fwdpe):
        self.ticker = ticker
        self.pe = pe
        self.fwdpe = fwdpe
        self.diff = pe - fwdpe

class portfol:#my portfolio
    def __init__(self, ticker, pe, fwdpe, diff):
        self.ticker = ticker
        self.pe = pe
        self.fwdpe = fwdpe
        self.diff = diff


def add_portfol(ticker, pe, fwdpe, diff):
    list.append(portfol(ticker, pe, fwdpe, diff))


def iqr(scrf):
    q75, q25 = np.percentile(scrf, [75 ,25])
    #iqr = q75 - q25
    return(q75)#no overvalued

def pages(scr_df):
    list = []
    scrf = []
    scrf_wdpe = []
    roe = []

    for y in range(0,len(scr_df)):
        if y == 1:
            continue
        scr = scr_df[y]
        for x in range(0, len(scr['PE'])):
            if scr['FwdPE'][x] == "-":
                #print("DONT BUY")\
                continue
            else:
                if float(scr['FwdPE'][x]) - float(scr['PE'][x]) < 0:#should be some growth soon; adjust for growth 
                    scrf.append(float(scr['PE'][x]))
                    scrf_wdpe.append(float(scr['FwdPE'][x]))
                    list.append(stock(scr['Ticker'][x], float(scr['PE'][x]), float(scr['FwdPE'][x])))
                    #print(scr['Ticker'][x])



    try:
        low_25 = iqr(scrf)    
    except IndexError:
        return
    else:
        for obj in list:
            if obj.pe < low_25:#only lowest valued
                #print(obj.ticker)
                add_portfol( obj.ticker, obj.pe, obj.fwdpe, obj.diff )
                #add the ticker, pe, fwd pe, diff between 2, and pct. of growth portfolio by industry, also Sum
                Sum.append(obj.diff)
            
        

def industry_sel():
    x = range(1,len(dir(Screener.IndustryOption)) - 3)
    for n in x:
        industry = dir(Screener.IndustryOption)[n-1]
        #print(industry)    
        options = [Screener.IndustryOption[industry], Screener.CountryOption.USA, Screener.PEOption.PROFITABLE_0, Screener.PEGOption.UNDER_3, Screener.DividendYieldOption.POSITIVE_0_PERCENT, Screener.ReturnOnEquityOption.VERY_POSITIVE_30_PERCENT]
        try:
            screener = Screener(filter_options=options, view_option=Screener.ViewOption.VALUATION,
                            pages=[x for x in range(1,4)])
        except AttributeError:
            continue
        else:
            scr_df = screener.data_frames
            pages(scr_df)
        
        #print("SEARCHING FOR POTENTIALLY UNDERVALUED ", industry, "STOCKS...")
        
        

    print("CONSIDER SELLING STOCKS NOT CONTAINED IN THE FOLLOWING LIST: ")
    for obj in list:
        if obj.diff-stat.median(Sum) > 1:#somewhat arbitrary; could use iqr instead
            print( obj.ticker, obj.pe, obj.fwdpe, obj.diff-stat.median(Sum), "STRONG BUY" )
        elif obj.diff-stat.median(Sum) > 0:
            print( obj.ticker, obj.pe, obj.fwdpe, obj.diff-stat.median(Sum), "BUY" )
        else:
            print( obj.ticker, obj.pe, obj.fwdpe, obj.diff-stat.median(Sum), "HOLD" )
    print("Total of", len(list), "stocks for portfolio...")
##    #print("Mean diff", stat.mean(Sum))


search = industry_sel()

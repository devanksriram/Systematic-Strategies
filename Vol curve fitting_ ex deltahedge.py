# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 13:59:01 2023

@author: dsriram.mifft2023
"""

import numpy as np
import pandas as pd
# for statistical functions
from scipy import stats
# for Matplotlib plotting
import matplotlib.pyplot as plt
# to do inline plots in the Notebook
# for Operating System operations
import os
# for some mathematical functions
import math
# for date management
import datetime as dt
import requests
import time
from pyblackscholesanalytics.market.market import MarketEnvironment
from pyblackscholesanalytics.options.options import PlainVanillaOption
from pyblackscholesanalytics.utils.utils import plot_compare
from pyblackscholesanalytics.utils.numeric_routines import NumericGreeks


#define variables

vol_start = 0.2
riskfree_rate = 0
API_KEY = {'X-API-key': 'NVP0OJPX'} #define API key from the RITC app
input_table = pd.DataFrame(index=range(0,40),columns=['ticker','type','last','size','trading_fee','max_trade_size','position']) #Portfolio tab
vol_surface_call = pd.DataFrame(index =['1m','2m'], columns = [np.arange(45,55)])
vol_surface_put = pd.DataFrame(index =['1m','2m'], columns = [np.arange(45,55)])
call_1m_timeseries = pd.DataFrame(columns = [np.arange(45,55)])
put_1m_timeseries = pd.DataFrame(columns = [np.arange(45,55)])
call_2m_timeseries = pd.DataFrame(columns = [np.arange(45,55)])
put_2m_timeseries = pd.DataFrame(columns = [np.arange(45,55)])
tick1 = 0
left_wing = 0
right_wing = 0
belly = 0
news_timeseries = pd.DataFrame(columns = ['headline'])
poly_timeseries = []
poly_put_timeseries =[]
poly2_timeseries = []
poly2_put_timeseries = []
signal = []
positions = []

#delta_numeric = NumGreeks.delta(S=S)
#delta_analytic = Vanilla_Call.delta(S=S)

#Fill in inputs from first news line news[-1] basically slice that string and define these variables
def pullnewsdata():
    with requests.Session() as s:
        s.headers.update(API_KEY)
        resp = s.get('http://localhost:9999/v1/news')
        if resp.ok:
            news = resp.json()      
            return(news[0]['body']) # print the latest news line's body- slice further for vol number store it in a vol dataframe(think?)


# Main labels needed -'ticker''type' 'last' 'size' 'trading_fee''max_trade_size'
def pullsecuritiesdata():
     with requests.Session() as s:
         s.headers.update(API_KEY)
         resp = s.get('http://localhost:9999/v1/securities')
         if resp.ok:
             securities = resp.json()
             i = 0
             while i < 41: #41 listed securities in total
                     for col in input_table.columns:
                         input_table.loc[i,col] = securities[i][col]
                     i = i + 1
       

#exec1 = {'ticker': 'RTM1C45', 'type': 'MARKET', 'quantity': 200,'action': 'BUY'} pass a dictionary into(execute)

def execute(x):
    with requests.Session() as s:
        s.headers.update(API_KEY)
        resp = s.post('http://localhost:9999/v1/orders', params=x)
        if resp.ok:
            mkt_order = resp.json()
            id = mkt_order['order_id']
            print('The market buy order was submitted and has ID', id)
        else:
            print('The order was not successfully submitted!')

def cancel_order(x):
    with requests.Session() as s:
        s.headers.update(API_KEY)
        # x = cancel_params = {'all': 0, 'query': 'ticker == RTM1C45'} # cancel all open sell orders with a price over 20.10
        resp = s.post('http://localhost:9999/v1/commands/cancel', params=x)
        if resp.ok:
            status = resp.json()
            cancelled = status['cancelled_order_ids']
            print('These orders were cancelled:', cancelled)
            
            
def server_status():
    with requests.Session() as s: # step 3
        s.headers.update(API_KEY) # step 4
        resp = s.get('http://localhost:9999/v1/case') # step 5
        if resp.ok: # step 6
            case = resp.json() # step 7
            server_status = case['status'] # accessing the 'tick' value that was returned
            return(server_status)
        
        


 
#tocall these functions in loop
# maybe look over ticks and keep pulling fresh data using this function, every tick

# Paste the new module to my working directory C:\Users\dsriram.mifft2023\.spyder-py3\pyblackscholesanalytics
# Copy from C:\Users\dsriram.mifft2023\Anaconda3\Lib\site-packages\pyblackscholesanalytics
 
#now filtering out the options and slicing the ticker

def save_timeseriescsv():
    call_1m_timeseries.to_csv('call_1m_timeseries.csv')
    put_1m_timeseries.to_csv('put_1m_timeseries.csv')
    call_2m_timeseries.to_csv('call_2m_timeseries.csv')
    put_2m_timeseries.to_csv('put_2m_timeseries.csv')
    news_timeseries.to_csv('news_timeseries.csv')

def tick():
    with requests.Session() as s: # step 3
        s.headers.update(API_KEY) # step 4
        resp = s.get('http://localhost:9999/v1/case') # step 5
        if resp.ok: # step 6                                                                                                                                                                                                                              
            case = resp.json() # step 7
            tick = case['tick'] # accessing the 'tick' value that was returned
            return tick

def period():
    with requests.Session() as s: # step 3
        s.headers.update(API_KEY) # step 4
        resp = s.get('http://localhost:9999/v1/case') # step 5
        if resp.ok: # step 6
            case = resp.json() # step 7
            period = case['period'] # accessing the 'tick' value that was returned
            return(period)
        
def volsurface_builder():
    for y in ['1m','2m']:
        
        for x in np.arange(45,55):
           
            mkt_env = MarketEnvironment(t="21-02-2023", r=riskfree_rate, S_t= input_table['last'][0], sigma=vol_start) #random date( as long as difference in T-t is 1month or 2 months
           
            if y == '1m':
                time_expiry="21-03-2023"
            else:
                time_expiry="21-04-2023"    
            
            #call vol
            Vanilla_Call = PlainVanillaOption(mkt_env,option_type='call', K= x, T=time_expiry)
            c_star = np.array(option_data[(option_data['Expiry']==int(y[0])) & (option_data['Strike'].astype(int)==x) & (option_data['Call/Put']=='C')]['last'])
            #now loop all this across option_data and store in new vol_surface dataframe 
            vol_surface_call.loc[y,x] = Vanilla_Call.implied_volatility(iv_estimated= vol_start, target_price=c_star, epsilon=1e-8, minimization_method="Least-Squares", max_iter = 300) #running the Newton's iteration algorithm
            
            #put vol
            
            Vanilla_Put = PlainVanillaOption(mkt_env,option_type='put', K= x, T=time_expiry)
            p_star = np.array(option_data[(option_data['Expiry']==int(y[0])) & (option_data['Strike'].astype(int)==x) & (option_data['Call/Put']=='P')]['last'])
            #now loop all this across option_data and store in new vol_surface dataframe 
            vol_surface_put.loc[y,x] = Vanilla_Put.implied_volatility(iv_estimated= vol_start, target_price=p_star, epsilon=1e-8, minimization_method="Least-Squares", max_iter = 300) #running the Newton's iteration algorithm

def visualise():
    
    fig,axes = plt.subplots(2,2)
    axes[0,0].plot(np.arange(45,55) ,vol_surface_call.iloc[0,:], color = 'blue')
    axes[0,0].set_title('Call option Vol surface 1m')
    axes[1,0].plot(np.arange(45,55) ,vol_surface_put.iloc[0,:], color = 'red')
    axes[1,0].set_title('Put option Vol surface 1m')
    
    axes[0,1].plot(np.arange(45,55) ,vol_surface_call.iloc[1,:], color = 'blue')
    axes[0,1].set_title('Call option Vol surface 2m')
    axes[1,1].plot(np.arange(45,55) ,vol_surface_put.iloc[1,:], color = 'red')
    axes[1,1].set_title('Put option Vol surface 2m')
    for ax in axes.flat:
        ax.label_outer()
    
    plt.show()

#option_data = input_table[input_table.type=='OPTION']
#passing boolean into dataframe

server_status = server_status()
period = period()
#main loop 
if period == 1:
    
    while int(tick1 < 280):
        pullsecuritiesdata()
        headline = str(pullnewsdata())
        option_data = input_table[input_table.type=='OPTION']
        option_data.loc[:,'Call/Put'] = option_data['ticker'].str[4]
        option_data.loc[:,'Expiry'] = option_data['ticker'].str[3]
        option_data.loc[:,'Expiry'] = option_data['Expiry'].astype(int)
        option_data = option_data.assign(Expiry_yrs = lambda x: (x['Expiry']*30/365))
        option_data.loc[:,'Strike'] = option_data['ticker'].str[-2:]
        market_price = option_data['last'][1] #loop this over rows
        volsurface_builder()
        visualise()
        pullnewsdata()
        #store data in timeseries
        call_1m_timeseries.loc[tick1] = np.array(vol_surface_call.iloc[0,:])
        put_1m_timeseries.loc[tick1] = np.array(vol_surface_put.iloc[0,:])
        call_2m_timeseries.loc[tick1] = np.array(vol_surface_call.iloc[1,:])
        put_2m_timeseries.loc[tick1] = np.array(vol_surface_put.iloc[1,:])
        news_timeseries.loc[tick1] = np.array(headline)
        
        belly = round(input_table['last'][0],0)
        if belly -3 < 45:
            left_wing = 45
        else:
            left_wing = belly - 3
        
        if belly + 3 > 54:
            right_wing = 54
        else:
            right_wing = belly + 3
        
            
        x_axis = np.array([left_wing, belly, right_wing]).astype(float)
        
        call_smile_1m = np.array([vol_surface_call.loc['1m',left_wing], vol_surface_call.loc['1m',belly], np.array(vol_surface_call.loc['1m',right_wing])]).astype(float)
        call_smile_2m = np.array([vol_surface_call.loc['2m',left_wing], vol_surface_call.loc['2m',belly], np.array(vol_surface_call.loc['2m',right_wing])]).astype(float)
        put_smile_1m = np.array([vol_surface_put.loc['1m',left_wing], vol_surface_put.loc['1m',belly], np.array(vol_surface_put.loc['1m',right_wing])]).astype(float)
        put_smile_2m = np.array([vol_surface_put.loc['2m',left_wing], vol_surface_put.loc['2m',belly], np.array(vol_surface_put.loc['2m',right_wing])]).astype(float)
        
        #fit 1m call smile
        poly = np.polyfit(np.arange(45,55).astype(float),np.array(vol_surface_call.loc['1m',:]).astype(float),2)
        z = []
        for x in np.arange(45,55):
            z.append(poly[0]*x*x + poly[1]*x + poly[2]) 
            
        #fit 1m put smile
        poly_put = np.polyfit(np.arange(45,55).astype(float),np.array(vol_surface_put.loc['1m',:]).astype(float),2)
        z_put = []
        for x in np.arange(45,55):
            z_put.append(poly_put[0]*x*x + poly_put[1]*x + poly_put[2])

        #plot volsurface fitting model
        fig,axes = plt.subplots(2,1)
        axes[0].plot(np.arange(45,55) ,z, color = 'blue')
        axes[0].set_title('Call Vol parabola fitting 1m')
        axes[1].plot(np.arange(45,55) ,z_put, color = 'red')
        axes[1].set_title('Put Vol parabola fitting 1m')
        for ax in axes.flat:
            ax.label_outer()
        plt.show()
        
        poly_timeseries.append(poly[0]-poly_put[0])
        
        if  poly[0] - poly_put[0] > np.mean(poly_timeseries) + np.std(poly_timeseries) * 2:   #int(float(poly[0])*float(poly_put[0]) < 0.0): # & int(poly[0] > poly_put[0])
            #poly[0] - poly_put[0] > np.mean(poly_timeseries) + np.std(poly_timeseries) * 2:                  #int(poly[0])/int(poly_put(0) < 0:   #np.mean(poly_timeseries):
            smile_1m_signal = 1
            exec1 = {'ticker': str('RTM1C'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
            exec2 = {'ticker': str('RTM1C'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'BUY'}
            exec3 = {'ticker': str('RTM1C'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
            exec4 = {'ticker': str('RTM1P'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
            exec5 = {'ticker': str('RTM1P'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'SELL'}
            exec6 = {'ticker': str('RTM1P'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
            
            execute(exec1)
            execute(exec2)
            execute(exec3)
            execute(exec4)
            execute(exec5)
            execute(exec6)
            
            
            
            #execute() mkt_params = {'ticker': 'RTM1C45', 'type': 'MARKET', 'quantity': 200,'action': 'BUY'}
            
        elif   poly[0] - poly_put[0] < np.mean(poly_timeseries) + np.std(poly_timeseries) * 2: 
            #int(float(poly[0])*float(poly_put[0]) < 0.0) & int(poly[0] < poly_put[0]):
                #poly[0] - poly_put[0] < np.mean(poly_timeseries) + np.std(poly_timeseries) * 2:                  #int(poly[0])/int(poly_put(0) < 0:   #np.mean(poly_timeseries):
               smile_1m_signal = 1
               exec1 = {'ticker': str('RTM1C'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
               exec2 = {'ticker': str('RTM1C'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'SELL'}
               exec3 = {'ticker': str('RTM1C'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
               exec4 = {'ticker': str('RTM1P'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
               exec5 = {'ticker': str('RTM1P'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'BUY'}
               exec6 = {'ticker': str('RTM1P'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
               execute(exec1)
               execute(exec2)
               execute(exec3)
               execute(exec4)
               execute(exec5)
               execute(exec6)
               
               
               
        else:
            # exit positions
            smile_1m_signal = 0
            positions = option_data[option_data.position!=0][['ticker','position']]
            if not positions.empty:#all avalable positions
                for x in np.array(positions.ticker):
                    if int(positions[positions.ticker ==x]['position']) < 0:
                        y = 'BUY'
                    else:
                        y = 'SELL'
                        
                    execkill = {'ticker': str(x), 'type': 'MARKET', 'quantity': int(abs(positions[positions.ticker ==x]['position'])),'action': y}
                    execute(execkill)
            #deltahedge
        
        
        #if call_smile_1m_signal = 1 execute butterfly
        signal.append(smile_1m_signal)
        print(signal)
        #check if smile is concave upward d2y/dx2 = +ve poly[0] > 0
        #update data per tick
        tick1 = tick()
        time.sleep(1)
        
    while int(279 < tick1 < 300):
        # exit positions
        smile_1m_signal = 3
        positions = option_data[option_data.position!=0][['ticker','position']]
        if not positions.empty:#all avalable positions
            for x in np.array(positions.ticker):
                if int(positions[positions.ticker ==x]['position']) < 0:
                    y = 'BUY'
                else:
                    y = 'SELL'
                        
                    execkill = {'ticker': str(x), 'type': 'MARKET', 'quantity': int(abs(positions[positions.ticker ==x]['position'])),'action': y}
                    execute(execkill)
            #deltahedge
        signal.append(smile_1m_signal)
        tick1 = tick()
        time.sleep(5)

    

else:
    while int(tick1 < 280):
        pullsecuritiesdata()
        headline = str(pullnewsdata())
        option_data = input_table[input_table.type=='OPTION']
        option_data = input_table[input_table.type=='OPTION']
        option_data.loc[:,'Call/Put'] = option_data['ticker'].str[4]
        option_data.loc[:,'Expiry'] = option_data['ticker'].str[3]
        option_data.loc[:,'Expiry'] = option_data['Expiry'].astype(int)
        option_data = option_data.assign(Expiry_yrs = lambda x: (x['Expiry']*30/365))
        option_data.loc[:,'Strike'] = option_data['ticker'].str[-2:]
        market_price = option_data['last'][1] #loop this over rows
        volsurface_builder()
        visualise()
        pullnewsdata()
        #store data in timeseries
        call_1m_timeseries.loc[tick1] = np.array(vol_surface_call.iloc[0,:])
        put_1m_timeseries.loc[tick1] = np.array(vol_surface_put.iloc[0,:])
        call_2m_timeseries.loc[tick1] = np.array(vol_surface_call.iloc[1,:])
        put_2m_timeseries.loc[tick1] = np.array(vol_surface_put.iloc[1,:])
        news_timeseries.loc[tick1] = np.array(headline)
        
        belly = round(input_table['last'][0],0)
        if belly -3 < 45:
            left_wing = 45
        else:
            left_wing = belly - 3
        
        if belly + 3 > 54:
            right_wing = 54
        else:
            right_wing = belly + 3
        
            
        x_axis = np.array([left_wing, belly, right_wing]).astype(float)
        
        call_smile_1m = np.array([vol_surface_call.loc['1m',left_wing], vol_surface_call.loc['1m',belly], np.array(vol_surface_call.loc['1m',right_wing])]).astype(float)
        call_smile_2m = np.array([vol_surface_call.loc['2m',left_wing], vol_surface_call.loc['2m',belly], np.array(vol_surface_call.loc['2m',right_wing])]).astype(float)
        put_smile_1m = np.array([vol_surface_put.loc['1m',left_wing], vol_surface_put.loc['1m',belly], np.array(vol_surface_put.loc['1m',right_wing])]).astype(float)
        put_smile_2m = np.array([vol_surface_put.loc['2m',left_wing], vol_surface_put.loc['2m',belly], np.array(vol_surface_put.loc['2m',right_wing])]).astype(float)
        
        
        poly2 = np.polyfit(np.arange(45,55).astype(float),np.array(vol_surface_call.loc['2m',:]).astype(float),2)
        z = []
        for x in np.arange(45,55):
            z.append(poly2[0]*x*x + poly2[1]*x + poly2[2])
        
        #####
        #fit 1m put smile
        poly2_put = np.polyfit(np.arange(45,55).astype(float),np.array(vol_surface_put.loc['2m',:]).astype(float),2)
        z_put = []
        for x in np.arange(45,55):
            z_put.append(poly2_put[0]*x*x + poly2_put[1]*x + poly2_put[2])

        #plot volsurface fitting model
        fig,axes = plt.subplots(2,1)
        axes[0].plot(np.arange(45,55) ,z, color = 'blue')
        axes[0].set_title('Call Vol parabola fitting 2m')
        axes[1].plot(np.arange(45,55) ,z_put, color = 'red')
        axes[1].set_title('Put Vol parabola fitting 2m')
        for ax in axes.flat:
            ax.label_outer()
        plt.show()
        
        poly2_timeseries.append(poly2[0]-poly2_put[0])
        
        

        if  poly2[0] - poly2_put[0] > np.mean(poly2_timeseries) + np.std(poly2_timeseries) * 2:  #int(float(poly2[0])*float(poly2_put[0]) < 0.0): # & int(poly2[0] > poly2_put[0])
        #poly2[0] - poly2_put[0] > np.mean(poly2_timeseries) + np.std(poly2_timeseries) * 2:                  #int(poly[0])/int(poly_put(0) < 0:   #np.mean(poly_timeseries):
            smile_2m_signal = 1
            exec1 = {'ticker': str('RTM2C'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
            exec2 = {'ticker': str('RTM2C'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'BUY'}
            exec3 = {'ticker': str('RTM2C'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
            exec4 = {'ticker': str('RTM2P'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
            exec5 = {'ticker': str('RTM2P'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'SELL'}
            exec6 = {'ticker': str('RTM2P'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
            execute(exec1)
            execute(exec2)
            execute(exec3)
            execute(exec4)
            execute(exec5)
            execute(exec6)
            
            
            
            
            #execute() mkt_params = {'ticker': 'RTM1C45', 'type': 'MARKET', 'quantity': 200,'action': 'BUY'}
        elif    poly2[0] - poly2_put[0] < np.mean(poly2_timeseries) + np.std(poly2_timeseries) * 2:#int(float(poly2[0])*float(poly2_put[0]) < 0.0) & int(poly2[0] < poly2_put[0]):
                #poly2[0] - poly2_put[0] < np.mean(poly2_timeseries) + np.std(poly2_timeseries) * 2:                  #int(poly[0])/int(poly_put(0) < 0:   #np.mean(poly_timeseries):
                #smile_2m_signal = 1
                exec1 = {'ticker': str('RTM2C'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
                exec2 = {'ticker': str('RTM2C'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'SELL'}
                exec3 = {'ticker': str('RTM2C'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
                exec4 = {'ticker': str('RTM2P'+str(int(left_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'SELL'}
                exec5 = {'ticker': str('RTM2P'+str(int(belly))), 'type': 'MARKET', 'quantity': 10,'action': 'BUY'}
                exec6 = {'ticker': str('RTM2P'+str(int(right_wing))), 'type': 'MARKET', 'quantity': 5,'action': 'BUY'}
                
                execute(exec1)
                execute(exec2)
                execute(exec3)
                execute(exec4)
                execute(exec5)
                execute(exec6)
                
                
                
                
        else:
            # exit positions
            smile_2m_signal = 0
            positions = option_data[option_data.position!=0][['ticker','position']]
            if not positions.empty:#all avalable positions
                for x in np.array(positions.ticker):
                    if int(positions[positions.ticker ==x]['position']) < 0:
                        y = 'BUY'
                    else:
                        y = 'SELL'
                        
                    execkill = {'ticker': str(x), 'type': 'MARKET', 'quantity': int(abs(positions[positions.ticker ==x]['position'])),'action': y}
                    execute(execkill)
            #deltahedge

        
        #if call_smile_1m_signal = 1 execute butterfly
        signal.append(smile_2m_signal)
        print(signal)
        #check if smile is concave upward d2y/dx2 = +ve poly[0] > 0
        #update data per tick
        tick1 = tick()
        time.sleep(1)
        
    while int(280 < tick1 < 300):
        smile_2m_signal = 3
        positions = option_data[option_data.position!=0][['ticker','position']]
        if (not positions.empty):#all avalable positions
            for x in positions.ticker:
                if int(positions[positions.ticker == x]['position']) < 0:
                    y = 'BUY'
                else:
                    y = 'SELL'
                        
                execkill = {'ticker': str(x), 'type': 'MARKET', 'quantity': int(abs(positions[positions.ticker ==x]['position'])),'action': y}
                execute(execkill)
            
        tick1 = tick()
        time.sleep(1)
            
    # underlying value, strike-price, time-to-maturity, volatility and short-rate

#tick1 is overwriting the first month data by the second month data so pause the code and start again when round 2 begins

#butterfly shape of call 1m should be same as shape of put 1m
#(a-2b+c)-(e-2f+g)


    
    
    

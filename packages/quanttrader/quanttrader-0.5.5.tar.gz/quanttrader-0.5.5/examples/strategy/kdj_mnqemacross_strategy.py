#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quanttrader.strategy.strategy_base import StrategyBase
from quanttrader.data.tick_event import TickType
from quanttrader.order.order_event import OrderEvent
from quanttrader.order.order_status import OrderStatus
from quanttrader.order.order_type import OrderType
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import logging

_logger = logging.getLogger('qtlive')


class MAcrossMNQexp(StrategyBase):
    """
    EMA indicator
    """
    def __init__(self):
        super(MAcrossMNQexp,self).__init__()
        self.bar_start_time = '00:00:01'        # bar starts earlier to accumulate bars
        self.bar_end_time = '17:00:00'          # 16:15; instead,stocks close at 16:00
        self.bar_start2_time = '18:00:00'  # 16:15; instead,stocks close at 16:00
        self.start_time = '02:00:00'     # trading starts
        self.end_time = '16:45:00'       # flat positions at 16:14:58
        self.start2_time = '18:30:00'  # trading starts

        self.profit_taking_ticks = 60.0         # 20 ticks
        self.stop_loss_ticks = 40.0       # 10 ticks

        self.profit_taking_price = 0.0
        self.stop_loss_price = 0.0

        self.cidx_5min_old = 0     # used to tell if it is a new bar
        self.cidx_5min = 0         # current bar idx
        self.nbars_5min = 0        # total bars so far
        self.ema1_5min = np.nan
        self.ema2_5min = np.nan
        self.ema3_5min = np.nan

        self.n_ema1 = 3
        self.n_ema2 = 24
        self.n_ema3 = 100
        self.n_bartime = 60*1

        _logger.info('MAcrossMNQexp initiated')

    def set_params(self,params_dict=None):
        super(MAcrossMNQexp,self).set_params(params_dict)

        today = datetime.today()
        self.bar_start_time = today.replace(hour=int(self.bar_start_time[:2]),minute=int(self.bar_start_time[3:5]),second=int(self.bar_start_time[6:]),microsecond=0)
        self.bar_end_time = today.replace(hour=int(self.bar_end_time[:2]),minute=int(self.bar_end_time[3:5]),second=int(self.bar_end_time[6:]),microsecond=0) + timedelta(days=1)
        self.start_time = today.replace(hour=int(self.start_time[:2]),minute=int(self.start_time[3:5]),second=int(self.start_time[6:]),microsecond=0)
        self.end_time = today.replace(hour=int(self.end_time[:2]),minute=int(self.end_time[3:5]),second=int(self.end_time[6:]),microsecond=0) + timedelta(days=1)

        dt_5min = np.arange(0,(self.bar_end_time-self.bar_start_time).seconds,self.n_bartime)
        idx_5min = self.bar_start_time + dt_5min * timedelta(seconds=1)
        self.df_5min_bar = pd.DataFrame(np.full((len(idx_5min),),np.nan,dtype=[('Open',np.float64),('High',np.float64),('Low',np.float64),('Close',np.float64),('Volume',np.uint8)]))
        self.df_5min_ma = pd.DataFrame(np.full((len(idx_5min),),np.nan,dtype=[('ema1',np.float64),('ema2',np.float64),('ema3',np.float64)]))
        #self.df_5min_KDJ.K = 50.0
        #self.df_5min_KDJ.D = 50.0
        self.df_5min_bar.index = idx_5min
        self.df_5min_ma.index = idx_5min
        self.midx_5min = len(idx_5min) - 1            # max idx

        self.profit_taking_ticks = self.profit_taking_ticks * 0.25        # ticks to price
        self.stop_loss_ticks = self.stop_loss_ticks * 0.25       # ticks to price

    def on_tick(self,k):
        """
        respond to tick data
        """
        super().on_tick(k)     # extra mtm calc

        if k.timestamp < self.bar_start_time or (k.timestamp < self.bar_start2_time and k.timestamp > self.bar_end_time):     # bar_start_time < start_time
            return

        current_pos = int(self._position_manager.get_position_size(k.full_symbol))        # assume this strat only has one symbol

        if k.timestamp > self.end_time and k.timestamp < self.bar_start2_time:         # flat and shutdown
            if current_pos != 0:
                o = OrderEvent()
                o.full_symbol = k.full_symbol
                o.order_type = OrderType.MARKET
                o.order_size = -current_pos
                _logger.info(f'MAcrossMNQexp EOD flat position,current size {current_pos},order size {o.order_size}')
                self.place_order(o)
                #_logger.info(f'MAcrossMNQexp-k.timestamp')
            self.active = False
            return
        
        #--- 5min bar ---#
        while (self.cidx_5min < self.midx_5min) and (self.df_5min_bar.index[self.cidx_5min+1] < k.timestamp):    # fast forward cidx,in case of empty bars
            self.cidx_5min += 1

        new_5min_bar = self.cidx_5min_old < self.cidx_5min
        if new_5min_bar:    # tick bar
            #_logger.info(f'New 5min bar {self.cidx_5min_old} {self.cidx_5min} | {self.df_5min_bar.index[self.cidx_5min]} | {k.timestamp}')
            self.nbars_5min += 1
            self.cidx_5min_old = self.cidx_5min
        else:
            #_logger.info(f'existing 5min bar {self.cidx_5min_old} {self.cidx_5min} | {self.df_5min_bar.index[self.cidx_5min]} | {k.timestamp}')
            pass
        
        if k.tick_type == TickType.TRADE:    # only aggregate trades; assume no empty bar
            if np.isnan(self.df_5min_bar.iloc[self.cidx_5min,0]):       # not initialized yet
                self.df_5min_bar.iloc[self.cidx_5min,0] = k.price      # O
                self.df_5min_bar.iloc[self.cidx_5min,1] = k.price      # H
                self.df_5min_bar.iloc[self.cidx_5min,2] = k.price      # L
                self.df_5min_bar.iloc[self.cidx_5min,3] = k.price      # C
                self.df_5min_bar.iloc[self.cidx_5min,4] = k.size       # V
            else:
                self.df_5min_bar.iloc[self.cidx_5min,1] = max(self.df_5min_bar.High[self.cidx_5min],k.price)
                self.df_5min_bar.iloc[self.cidx_5min,2] = min(self.df_5min_bar.Low[self.cidx_5min],k.price)
                self.df_5min_bar.iloc[self.cidx_5min,3] = k.price
                self.df_5min_bar.iloc[self.cidx_5min,4] = k.size + self.df_5min_bar.Volume[self.cidx_5min]

        #if self.nbars_5min < self.n_rsv_lookback+self.n_kd_lookback+self.n_kd_lookback-2:  # not enough bars
        #     return

        if new_5min_bar:     # calc KDJ. cidx_5min-1 bar is complete
            #Ln = min(self.df_5min_bar.Low[self.cidx_5min-self.n_rsv_lookback:self.cidx_5min])      # 1. not including current bar; assuming no empty bars 2. min(nan) = nan
            #Hn = max(self.df_5min_bar.High[self.cidx_5min-self.n_rsv_lookback:self.cidx_5min])
            Cn = self.df_5min_bar.Close[self.cidx_5min-1]
            if np.isnan(Cn):          # not initialized yet
                return
            
            if np.isnan(self.df_5min_ma.ema1[self.cidx_5min-1]):
                self.df_5min_ma.ema1[self.cidx_5min-1] = self.df_5min_bar.Close[self.cidx_5min-1]
                self.df_5min_ma.ema2[self.cidx_5min-1] = self.df_5min_bar.Close[self.cidx_5min-1]
                self.df_5min_ma.ema3[self.cidx_5min-1] = self.df_5min_bar.Close[self.cidx_5min-1]
            else:
                self.df_5min_ma.ema1[self.cidx_5min-1] = (2.0*self.df_5min_bar.Close[self.cidx_5min-1] + (self.n_ema1-1)*self.df_5min_ma.ema1[self.cidx_5min-1])/(self.n_ema1+1)
                #self.df_5min_bar.Close[self.cidx_5min-self.n_ema1:self.cidx_5min].mean(skipna=False)  #if sma
                self.df_5min_ma.ema2[self.cidx_5min-1] = (2.0*self.df_5min_bar.Close[self.cidx_5min-1] + (self.n_ema2-1)*self.df_5min_ma.ema2[self.cidx_5min-1]/(self.n_ema2+1)
                #self.df_5min_bar.Close[self.cidx_5min-self.n_ema2:self.cidx_5min].mean(skipna=False)  #if sma
                self.df_5min_ma.ema3[self.cidx_5min-1] = (2.0*self.df_5min_bar.Close[self.cidx_5min-1] + (self.n_ema3-1)*self.df_5min_ma.ema3[self.cidx_5min-1]/(self.n_ema3+1)
                #self.df_5min_bar.Close[self.cidx_5min-self.n_ema3:self.cidx_5min].mean(skipna=False)  #if sma

            _logger.info(f'MAcrossMNQexp tick time,{k.timestamp},tick price,{k.price},ema1,{self.df_5min_ma.ema1[self.cidx_5min-1]},ema2,{self.df_5min_ma.ema2[self.cidx_5min-1]},ema3,{self.df_5min_ma.ema3[self.cidx_5min-1]}')

            if k.timestamp < self.start_time and (k.timestamp < self.start2_time and k.timestamp > self.end_time):     # no trading time
                return
            
            if np.isnan(self.df_5min_ma.ema1[self.cidx_5min-1]):       # not enough bars
                return

            long = self.df_5min_ma.ema1[self.cidx_5min-1]>self.df_5min_ma.ema2[self.cidx_5min-1] and self.df_5min_ma.ema2[self.cidx_5min-2]<self.df_5min_ma.ema1[self.cidx_5min-2]
            short = self.df_5min_ma.ema1[self.cidx_5min-1]<self.df_5min_ma.ema2[self.cidx_5min-1] and self.df_5min_ma.ema2[self.cidx_5min-2]>self.df_5min_ma.ema1[self.cidx_5min-2]

            if long & (current_pos <= 0) & (len(self._order_manager.standing_order_set) == 0) & (self.ema2_5min >= self.ema3_5min):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = 1 - current_pos
                _logger.info(f'MAcrossMNQexp long order placed,current price,{k.price},ema1n,{self.df_5min_ma.ema1[self.cidx_5min-1]},ema2n,{self.df_5min_ma.ema2[self.cidx_5min-1]},ema3n,{self.df_5min_ma.ema3[self.cidx_5min-1]},ema1p,{self.df_5min_ma.ema1[self.cidx_5min-2]},ema2p,{self.df_5min_ma.ema2[self.cidx_5min-2]},ema3p,{self.df_5min_ma.ema3[self.cidx_5min-2]}') #,current size {current_pos},order size {o.order_size}
                #self.place_order(o)
                #_logger.info(f'MAcrossMNQexp')
            elif short & (current_pos >= 0) & (len(self._order_manager.standing_order_set) == 0) & (self.ema2_5min <= self.ema3_5min):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = -1 - current_pos
                _logger.info(f'MAcrossMNQexp short order placed,current price,{k.price},ema1n,{self.df_5min_ma.ema1[self.cidx_5min-1]},ema2n,{self.df_5min_ma.ema2[self.cidx_5min-1]},ema3n,{self.df_5min_ma.ema3[self.cidx_5min-1]},ema1p,{self.df_5min_ma.ema1[self.cidx_5min-2]},ema2p,{self.df_5min_ma.ema2[self.cidx_5min-2]},ema3p,{self.df_5min_ma.ema3[self.cidx_5min-2]}') #,current size {current_pos},order size {o.order_size}
                #self.place_order(o)
                #_logger.info(f'MAcrossMNQexp')
        
        if k.tick_type == TickType.TRADE:      # take profit and stop loss based on trade price
            if (k.price > self.profit_taking_price) & (current_pos > 0) & (len(self._order_manager.standing_order_set) == 0):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = -1
                #_logger.info(f'MAcrossMNQexp long taking profit,current price {k.price},current size {current_pos},order size {o.order_size},profit price {self.profit_taking_price}')
                #self.place_order(o)
                _logger.info(f'MAcrossMNQexp')
            elif (k.price < self.stop_loss_price) & (current_pos > 0) & (len(self._order_manager.standing_order_set) == 0):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = -1
                #_logger.info(f'MAcrossMNQexp long stop loss,current price {k.price},current size {current_pos},order size {o.order_size},stop price {self.stop_loss_price}')
                #self.place_order(o)
                _logger.info(f'MAcrossMNQexp')
            elif (k.price < self.profit_taking_price) & (current_pos < 0) & (len(self._order_manager.standing_order_set) == 0):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = 1
                #_logger.info(f'MAcrossMNQexp short taking profit,current price {k.price},current size {current_pos},order size {o.order_size},profit price {self.profit_taking_price}')
                #self.place_order(o)
                _logger.info(f'MAcrossMNQexp')
            elif (k.price > self.stop_loss_price) & (current_pos < 0) & (len(self._order_manager.standing_order_set) == 0):
                #o = OrderEvent()
                #o.full_symbol = self.symbols[0]
                #o.order_type = OrderType.MARKET
                #o.order_size = 1
                #_logger.info(f'MAcrossMNQexp short stop loss,current price {k.price},current size {current_pos},order size {o.order_size},stop price {self.stop_loss_price}')
                #self.place_order(o)
                _logger.info(f'MAcrossMNQexp')
            else:
                # _logger.info(f'MAcrossMNQexp no action,current price {k.price},current size {current_pos},standing orders {len(self._order_manager.standing_order_set)}')
                pass


    def on_fill(self,fill_event):
        """
        on order filled
        derived class call super().on_fill first
        """
        super().on_fill(fill_event)

        if fill_event.fill_size > 0:     # long
            self.profit_taking_price = fill_event.fill_price + self.profit_taking_ticks
            self.stop_loss_price = fill_event.fill_price - self.stop_loss_ticks
        else:
            self.profit_taking_price = fill_event.fill_price - self.profit_taking_ticks
            self.stop_loss_price = fill_event.fill_price + self.stop_loss_ticks

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quanttrader.strategy.strategy_base import StrategyBase
from quanttrader.data.tick_event import TickType
from quanttrader.order.order_event import OrderEvent
from quanttrader.order.order_status import OrderStatus
from quanttrader.order.order_type import OrderType
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import logging

_logger = logging.getLogger('qtlive')


class KDJStrategyV2(StrategyBase):
    """
    KDJ indicator
    """
    def __init__(self):
        super(KDJStrategyV2, self).__init__()
        self.name = 'KDJStrategyV2'
        self.bar_start_time = '08:30:00'        # bar starts earlier to accumulate bars
        self.bar_end_time = '16:15:00'          # 16:15; instead, stocks close at 16:00
        self.start_time = '09:30:00'     # trading starts
        self.end_time = '16:14:58'       # flat positions at 16:14:58

        self.levelone = 16.0
        self.profit_taking_ticks = 20.0         # 20 ticks
        self.stop_loss_ticks = 10.0       # 10 ticks
        self.profit_taking_price = 0.0
        self.stop_loss_price = 0.0

        self.cidx_5min_old = 0     # used to tell if it is a new bar
        self.cidx_5min = 0         # current bar idx
        self.nbars_5min = 0        # total bars so far
        self.n_rsv_lookback = 20            # lookback period
        self.n_k_lookback = 3            # lookback period
        self.n_d_lookback = 3            # lookback period
        self.ema_5min = np.nan
        self.n_ema = 40

        _logger.info(f'{self.name} initiated')

    def set_params(self, params_dict=None):
        super(KDJStrategyV2, self).set_params(params_dict)

        today = datetime.today()
        self.bar_start_time = today.replace(hour=int(self.bar_start_time[:2]), minute=int(self.bar_start_time[3:5]), second=int(self.bar_start_time[6:]), microsecond=0)        
        self.bar_end_time = today.replace(hour=int(self.bar_end_time[:2]), minute=int(self.bar_end_time[3:5]), second=int(self.bar_end_time[6:]), microsecond=0)    
        self.start_time = today.replace(hour=int(self.start_time[:2]), minute=int(self.start_time[3:5]), second=int(self.start_time[6:]), microsecond=0)      
        self.end_time = today.replace(hour=int(self.end_time[:2]), minute=int(self.end_time[3:5]), second=int(self.end_time[6:]), microsecond=0)          

        dt_5min = np.arange(0, (self.bar_end_time-self.bar_start_time).seconds, 60*1)
        idx_5min = self.bar_start_time + dt_5min * timedelta(seconds=1)
        self.df_5min_bar = pd.DataFrame(np.full((len(idx_5min), ), np.nan, dtype=[('Open', np.float64), ('High', np.float64), ('Low', np.float64), ('Close', np.float64), ('Volume', np.uint8)]))
        self.df_5min_KDJ = pd.DataFrame(np.full((len(idx_5min), ), np.nan, dtype=[('RSV', np.float64), ('K', np.float64), ('D', np.float64), ('J', np.float64)]))
        # self.df_5min_KDJ.K = 50.0
        # self.df_5min_KDJ.D = 50.0
        self.df_5min_bar.index = idx_5min
        self.df_5min_KDJ.index = idx_5min
        self.midx_5min = len(idx_5min) - 1            # max idx

        self.profit_taking_ticks = self.profit_taking_ticks * 0.25        # ticks to price
        self.stop_loss_ticks = self.stop_loss_ticks * 0.25       # ticks to price

    def on_tick(self, k):
        """
        respond to tick data
        """
        super().on_tick(k)     # extra mtm calc

        if k.timestamp < self.bar_start_time:     # bar_start_time < start_time
            return

        current_pos = int(self._position_manager.get_position_size(k.full_symbol))        # assume this strat only has one symbol

        if k.timestamp > self.end_time:          # flat and shutdown
            if current_pos != 0:
                o = OrderEvent()
                o.full_symbol = k.full_symbol
                o.order_type = OrderType.MARKET
                o.order_size = -current_pos
                _logger.info(f'{self.name} EOD flat position, current size {current_pos}, order size {o.order_size}')
                self.place_order(o)
            self.active = False
            return
        
        #--- 5min bar ---#
        while (self.cidx_5min < self.midx_5min) and (self.df_5min_bar.index[self.cidx_5min+1] < k.timestamp):    # fast forward cidx, in case of empty bars
            self.cidx_5min += 1

        new_5min_bar = self.cidx_5min_old < self.cidx_5min
        if new_5min_bar:    # tick bar
            #_logger.info(f'{self.name} New 5min bar {self.cidx_5min_old} {self.cidx_5min} | {self.df_5min_bar.index[self.cidx_5min]} | {k.timestamp}')
            self.nbars_5min += 1
            self.cidx_5min_old = self.cidx_5min
        else:
            #_logger.info(f'{self.name} existing 5min bar {self.cidx_5min_old} {self.cidx_5min} | {self.df_5min_bar.index[self.cidx_5min]} | {k.timestamp}')
            pass
        
        if k.tick_type == TickType.TRADE:    # only aggregate trades; assume no empty bar
            if np.isnan(self.df_5min_bar.iloc[self.cidx_5min, 0]):       # not initialized yet
                self.df_5min_bar.iloc[self.cidx_5min, 0] = k.price      # O
                self.df_5min_bar.iloc[self.cidx_5min, 1] = k.price      # H
                self.df_5min_bar.iloc[self.cidx_5min, 2] = k.price      # L
                self.df_5min_bar.iloc[self.cidx_5min, 3] = k.price      # C
                self.df_5min_bar.iloc[self.cidx_5min, 4] = k.size       # V
            else:
                self.df_5min_bar.iloc[self.cidx_5min, 1] = max(self.df_5min_bar.High[self.cidx_5min], k.price)
                self.df_5min_bar.iloc[self.cidx_5min, 2] = min(self.df_5min_bar.Low[self.cidx_5min], k.price)
                self.df_5min_bar.iloc[self.cidx_5min, 3] = k.price
                self.df_5min_bar.iloc[self.cidx_5min, 4] = k.size + self.df_5min_bar.Volume[self.cidx_5min]

        # if self.nbars_5min < self.n_rsv_lookback+self.n_k_lookback+self.n_d_lookback-2:  # not enough bars
        #     return

        if new_5min_bar:     # calc KDJ. cidx_5min-1 bar is complete
            Cn = self.df_5min_bar.Close[self.cidx_5min-1]
            if np.isnan(Cn):          # not initialized yet
                return
            
            if self.cidx_5min < self.n_rsv_lookback:         # not enough bars
                return
            
            Ln = min(self.df_5min_bar.Low[self.cidx_5min-self.n_rsv_lookback:self.cidx_5min])      # 1. not including current bar; assuming no empty bars 2. min(nan) = nan
            Hn = max(self.df_5min_bar.High[self.cidx_5min-self.n_rsv_lookback:self.cidx_5min])
            
            if np.isnan(self.ema_5min):
                self.ema_5min = Cn
            else:
                self.ema_5min = (2.0*Cn + (self.n_ema - 1)*self.ema_5min)/(self.n_ema+1)
            self.df_5min_KDJ.RSV[self.cidx_5min-1] = (Cn - Ln)/ (Hn - Ln) * 100.0
            # self.df_5min_KDJ.K[self.cidx_5min-1] = 2.0/3.0 * self.df_5min_KDJ.K[self.cidx_5min-2] + 1.0/3.0 * self.df_5min_KDJ.RSV[self.cidx_5min-1]
            # self.df_5min_KDJ.D[self.cidx_5min-1] = 2.0/3.0 * self.df_5min_KDJ.D[self.cidx_5min-2] + 1.0/3.0 * self.df_5min_KDJ.K[self.cidx_5min-1]
            self.df_5min_KDJ.K[self.cidx_5min-1] = self.df_5min_KDJ.RSV[self.cidx_5min-self.n_k_lookback:self.cidx_5min].mean(skipna=False)
            self.df_5min_KDJ.D[self.cidx_5min-1] = self.df_5min_KDJ.K[self.cidx_5min-self.n_d_lookback:self.cidx_5min].mean(skipna=False)
            self.df_5min_KDJ.J[self.cidx_5min-1] = 3.0 * self.df_5min_KDJ.K[self.cidx_5min-1] - 2.0 * self.df_5min_KDJ.D[self.cidx_5min-1]

            _logger.info(f'{self.name} tick time {k.timestamp}, tick price {k.price}, kdj bar time {self.df_5min_KDJ.index[self.cidx_5min-1]}, Ln {Ln}, Hn {Hn}, Cn {Cn}, ema {self.ema_5min}, RSV {self.df_5min_KDJ.RSV[self.cidx_5min-1]}, K {self.df_5min_KDJ.K[self.cidx_5min-1]}, D {self.df_5min_KDJ.D[self.cidx_5min-1]}, J {self.df_5min_KDJ.J[self.cidx_5min-1]}')

            if k.timestamp < self.start_time:     # no trading time
                return
            
            if np.isnan(self.df_5min_KDJ.J[self.cidx_5min-1]):       # not enough bars
                return

            long = (self.df_5min_KDJ.J[self.cidx_5min-1] > self.df_5min_KDJ.J[self.cidx_5min-2]) and (self.df_5min_KDJ.J[self.cidx_5min-2] < self.df_5min_KDJ.J[self.cidx_5min-3]) and (self.df_5min_KDJ.J[self.cidx_5min-3] < self.df_5min_KDJ.J[self.cidx_5min-4]) and (self.df_5min_KDJ.J[self.cidx_5min-1] < self.levelone)
            short = (self.df_5min_KDJ.J[self.cidx_5min-1] < self.df_5min_KDJ.J[self.cidx_5min-2]) and (self.df_5min_KDJ.J[self.cidx_5min-2] > self.df_5min_KDJ.J[self.cidx_5min-3]) and (self.df_5min_KDJ.J[self.cidx_5min-3] > self.df_5min_KDJ.J[self.cidx_5min-4]) and (self.df_5min_KDJ.J[self.cidx_5min-1] > (100.0- self.levelone))

            if long & (current_pos <= 0) & (len(self._order_manager.standing_order_set) == 0) & (k.price > self.ema_5min):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = 1 - current_pos
                _logger.info(f'{self.name} long order placed, current price {k.price}, ema {self.ema_5min}, current size {current_pos}, order size {o.order_size}')
                self.place_order(o)
            elif short & (current_pos >= 0) & (len(self._order_manager.standing_order_set) == 0) & (k.price < self.ema_5min):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = -1 - current_pos
                _logger.info(f'{self.name} short order placed, current price {k.price}, ema {self.ema_5min}, current size {current_pos}, order size {o.order_size}')
                self.place_order(o)
        
        if k.tick_type == TickType.TRADE:      # take profit and stop loss based on trade price
            if (k.price > self.profit_taking_price) & (current_pos > 0) & (len(self._order_manager.standing_order_set) == 0):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = -1
                _logger.info(f'{self.name} long taking profit, current price {k.price}, current size {current_pos}, order size {o.order_size}, profit price {self.profit_taking_price}')
                self.place_order(o)
            elif (k.price < self.stop_loss_price) & (current_pos > 0) & (len(self._order_manager.standing_order_set) == 0):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = -1
                _logger.info(f'{self.name} long stop loss, current price {k.price}, current size {current_pos}, order size {o.order_size}, stop price {self.stop_loss_price}')
                self.place_order(o)
            elif (k.price < self.profit_taking_price) & (current_pos < 0) & (len(self._order_manager.standing_order_set) == 0):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = 1
                _logger.info(f'{self.name} short taking profit, current price {k.price}, current size {current_pos}, order size {o.order_size}, profit price {self.profit_taking_price}')
                self.place_order(o)
            elif (k.price > self.stop_loss_price) & (current_pos < 0) & (len(self._order_manager.standing_order_set) == 0):
                o = OrderEvent()
                o.full_symbol = self.symbols[0]
                o.order_type = OrderType.MARKET
                o.order_size = 1
                _logger.info(f'{self.name} short stop loss, current price {k.price}, current size {current_pos}, order size {o.order_size}, stop price {self.stop_loss_price}')
                self.place_order(o)
            else:
                # _logger.info(f'{self.name} no action, current price {k.price}, current size {current_pos}, standing orders {len(self._order_manager.standing_order_set)}')
                pass


    def on_fill(self, fill_event):
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

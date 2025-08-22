#!/usr/bin/env python3
"""
替代股票数据API
支持多个数据源：Alpha Vantage, Finnhub, Polygon等
"""

import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, Any, Tuple, Optional

class AlternativeStockAPI:
    """替代股票数据API类"""
    
    def __init__(self):
        # API密钥配置
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        self.finnhub_key = os.getenv("FINNHUB_API_KEY", "demo")
        self.polygon_key = os.getenv("POLYGON_API_KEY", "demo")
        
        # API端点
        self.alpha_vantage_base = "https://www.alphavantage.co/query"
        self.finnhub_base = "https://finnhub.io/api/v1"
        self.polygon_base = "https://api.polygon.io/v2"
        
        # 请求会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TradingAgents/1.0'
        })
        
        # 缓存
        self._cache = {}
        self._cache_timestamps = {}
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
        """
        获取股票数据的主入口
        
        Args:
            symbol: 股票代码
            period: 时间周期
            
        Returns:
            (历史数据DataFrame, 股票信息字典)
        """
        # 检查缓存
        cache_key = f"{symbol}_{period}"
        if self._is_cache_valid(cache_key):
            print(f"📋 使用缓存数据: {symbol}")
            return self._cache[cache_key]
        
        # 尝试不同的数据源
        data_sources = [
            self._get_alpha_vantage_data,
            self._get_finnhub_data,
            self._get_polygon_data,
            self._get_free_api_data
        ]
        
        for i, get_data_func in enumerate(data_sources):
            try:
                print(f"🔍 尝试数据源 {i+1}/4: {get_data_func.__name__}")
                hist_data, info_data = get_data_func(symbol, period)
                
                if hist_data is not None and not hist_data.empty:
                    # 缓存数据
                    result = (hist_data, info_data)
                    self._cache[cache_key] = result
                    self._cache_timestamps[cache_key] = datetime.now()
                    print(f"✅ 成功获取 {symbol} 数据，来源: {get_data_func.__name__}")
                    return result
                    
            except Exception as e:
                print(f"⚠️ 数据源 {get_data_func.__name__} 失败: {e}")
                continue
        
        print(f"❌ 所有数据源都失败，使用模拟数据: {symbol}")
        return self._generate_mock_data(symbol, period)
    
    def _is_cache_valid(self, cache_key: str, max_age_minutes: int = 5) -> bool:
        """检查缓存是否有效"""
        if cache_key not in self._cache_timestamps:
            return False
        
        cache_time = self._cache_timestamps[cache_key]
        return (datetime.now() - cache_time).total_seconds() < max_age_minutes * 60
    
    def _get_alpha_vantage_data(self, symbol: str, period: str) -> Tuple[pd.DataFrame, Dict]:
        """使用Alpha Vantage API获取数据"""
        if self.alpha_vantage_key == "demo":
            raise ValueError("需要设置 ALPHA_VANTAGE_API_KEY")
        
        # 获取日线数据
        params = {
            'function': 'TIME_SERIES_DAILY_ADJUSTED',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': self.alpha_vantage_key
        }
        
        response = self.session.get(self.alpha_vantage_base, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'Error Message' in data:
            raise ValueError(f"Alpha Vantage错误: {data['Error Message']}")
        
        if 'Note' in data:
            raise ValueError("Alpha Vantage API限流")
        
        time_series = data.get('Time Series (Daily)', {})
        if not time_series:
            raise ValueError("未获取到时间序列数据")
        
        # 转换为DataFrame
        df_data = []
        for date_str, values in time_series.items():
            df_data.append({
                'Date': pd.to_datetime(date_str),
                'Open': float(values['1. open']),
                'High': float(values['2. high']),
                'Low': float(values['3. low']),
                'Close': float(values['4. close']),
                'Volume': int(values['6. volume'])
            })
        
        df = pd.DataFrame(df_data)
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        # 根据period筛选数据
        if period == "1mo":
            df = df.tail(30)
        elif period == "3mo":
            df = df.tail(90)
        elif period == "6mo":
            df = df.tail(180)
        elif period == "1y":
            df = df.tail(365)
        
        # 获取公司信息
        info = self._get_alpha_vantage_info(symbol)
        
        return df, info
    
    def _get_alpha_vantage_info(self, symbol: str) -> Dict:
        """获取Alpha Vantage公司信息"""
        try:
            params = {
                'function': 'OVERVIEW',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = self.session.get(self.alpha_vantage_base, params=params, timeout=10)
            data = response.json()
            
            return {
                'shortName': data.get('Name', symbol),
                'longName': data.get('Name', f"{symbol} Inc."),
                'currentPrice': float(data.get('50DayMovingAverage', 0)) if data.get('50DayMovingAverage') else None,
                'marketCap': int(float(data.get('MarketCapitalization', 0))) if data.get('MarketCapitalization') else None,
                'trailingPE': float(data.get('PERatio', 0)) if data.get('PERatio') else None,
                'beta': float(data.get('Beta', 1.0)) if data.get('Beta') else 1.0,
                'sector': data.get('Sector', 'Unknown'),
                'industry': data.get('Industry', 'Unknown')
            }
        except:
            return self._generate_mock_info(symbol)
    
    def _get_finnhub_data(self, symbol: str, period: str) -> Tuple[pd.DataFrame, Dict]:
        """使用Finnhub API获取数据"""
        if self.finnhub_key == "demo":
            raise ValueError("需要设置 FINNHUB_API_KEY")
        
        # 计算时间范围
        end_time = int(datetime.now().timestamp())
        if period == "1mo":
            start_time = int((datetime.now() - timedelta(days=30)).timestamp())
        elif period == "3mo":
            start_time = int((datetime.now() - timedelta(days=90)).timestamp())
        elif period == "6mo":
            start_time = int((datetime.now() - timedelta(days=180)).timestamp())
        else:  # 1y
            start_time = int((datetime.now() - timedelta(days=365)).timestamp())
        
        # 获取K线数据
        url = f"{self.finnhub_base}/stock/candle"
        params = {
            'symbol': symbol,
            'resolution': 'D',
            'from': start_time,
            'to': end_time,
            'token': self.finnhub_key
        }
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('s') != 'ok':
            raise ValueError(f"Finnhub错误: {data}")
        
        # 转换为DataFrame
        df = pd.DataFrame({
            'Open': data['o'],
            'High': data['h'],
            'Low': data['l'],
            'Close': data['c'],
            'Volume': data['v']
        })
        
        # 添加日期索引
        dates = [datetime.fromtimestamp(ts) for ts in data['t']]
        df.index = pd.DatetimeIndex(dates)
        
        # 获取公司信息
        info = self._get_finnhub_info(symbol)
        
        return df, info
    
    def _get_finnhub_info(self, symbol: str) -> Dict:
        """获取Finnhub公司信息"""
        try:
            # 获取公司基本信息
            url = f"{self.finnhub_base}/stock/profile2"
            params = {'symbol': symbol, 'token': self.finnhub_key}
            
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            # 获取实时报价
            quote_url = f"{self.finnhub_base}/quote"
            quote_response = self.session.get(quote_url, params=params, timeout=10)
            quote_data = quote_response.json()
            
            return {
                'shortName': data.get('name', symbol),
                'longName': data.get('name', f"{symbol} Inc."),
                'currentPrice': quote_data.get('c'),
                'regularMarketChangePercent': quote_data.get('dp'),
                'marketCap': data.get('marketCapitalization', 0) * 1000000 if data.get('marketCapitalization') else None,
                'sector': data.get('finnhubIndustry', 'Unknown'),
                'country': data.get('country', 'Unknown'),
                'currency': data.get('currency', 'USD'),
                'exchange': data.get('exchange', 'Unknown')
            }
        except:
            return self._generate_mock_info(symbol)
    
    def _get_polygon_data(self, symbol: str, period: str) -> Tuple[pd.DataFrame, Dict]:
        """使用Polygon API获取数据（免费版本有限制）"""
        raise ValueError("Polygon API需要付费订阅")
    
    def _get_free_api_data(self, symbol: str, period: str) -> Tuple[pd.DataFrame, Dict]:
        """使用免费API获取数据"""
        # 这里可以添加其他免费API，如Yahoo Finance的非官方API
        try:
            # 使用Yahoo Finance的非官方端点
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'period1': int((datetime.now() - timedelta(days=365)).timestamp()),
                'period2': int(datetime.now().timestamp()),
                'interval': '1d'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            result = data['chart']['result'][0]
            timestamps = result['timestamp']
            quotes = result['indicators']['quote'][0]
            
            df = pd.DataFrame({
                'Open': quotes['open'],
                'High': quotes['high'],
                'Low': quotes['low'],
                'Close': quotes['close'],
                'Volume': quotes['volume']
            })
            
            dates = [datetime.fromtimestamp(ts) for ts in timestamps]
            df.index = pd.DatetimeIndex(dates)
            
            # 移除NaN值
            df.dropna(inplace=True)
            
            # 根据period筛选
            if period == "1mo":
                df = df.tail(30)
            elif period == "3mo":
                df = df.tail(90)
            elif period == "6mo":
                df = df.tail(180)
            
            # 生成基本信息
            info = {
                'shortName': symbol,
                'longName': f"{symbol} Inc.",
                'currentPrice': df['Close'].iloc[-1] if not df.empty else None,
                'regularMarketChangePercent': ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100) if len(df) > 1 else 0
            }
            
            return df, info
            
        except Exception as e:
            raise ValueError(f"免费API失败: {e}")
    
    def _generate_mock_data(self, symbol: str, period: str) -> Tuple[pd.DataFrame, Dict]:
        """生成模拟数据"""
        print(f"📊 生成 {symbol} 的模拟数据")
        
        # 根据period确定天数
        if period == "1mo":
            days = 30
        elif period == "3mo":
            days = 90
        elif period == "6mo":
            days = 180
        else:
            days = 365
        
        # 生成日期范围
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # 使用种子确保一致性
        np.random.seed(hash(symbol) % 2**32)
        
        # 生成价格数据
        base_price = np.random.uniform(20, 200)
        returns = np.random.normal(0.001, 0.02, days)  # 日收益率
        prices = [base_price]
        
        for ret in returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 1.0))
        
        # 创建OHLC数据
        data = []
        for i, (date, close) in enumerate(zip(dates, prices)):
            open_price = close * np.random.uniform(0.99, 1.01)
            high = max(open_price, close) * np.random.uniform(1.0, 1.03)
            low = min(open_price, close) * np.random.uniform(0.97, 1.0)
            volume = int(np.random.uniform(1000000, 10000000))
            
            data.append({
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(close, 2),
                'Volume': volume
            })
        
        df = pd.DataFrame(data, index=dates)
        info = self._generate_mock_info(symbol)
        
        return df, info
    
    def _generate_mock_info(self, symbol: str) -> Dict:
        """生成模拟股票信息"""
        np.random.seed(hash(symbol) % 2**32)
        
        current_price = np.random.uniform(50, 300)
        
        return {
            'shortName': f"模拟股票 {symbol}",
            'longName': f"Mock Company {symbol} Inc.",
            'currentPrice': round(current_price, 2),
            'regularMarketPrice': round(current_price, 2),
            'regularMarketChangePercent': round(np.random.uniform(-5, 5), 2),
            'marketCap': int(np.random.uniform(1e9, 1e12)),
            'trailingPE': round(np.random.uniform(10, 50), 1),
            'regularMarketVolume': int(np.random.uniform(1e6, 1e8)),
            'beta': round(np.random.uniform(0.5, 2.0), 2),
            'sector': 'Technology',
            'industry': 'Software'
        }

# 全局实例
alternative_api = AlternativeStockAPI()

def get_alternative_stock_data(symbol: str, period: str = "1y") -> Tuple[Optional[pd.DataFrame], Optional[Dict]]:
    """
    获取替代股票数据的便捷函数
    
    Args:
        symbol: 股票代码
        period: 时间周期
        
    Returns:
        (历史数据DataFrame, 股票信息字典)
    """
    return alternative_api.get_stock_data(symbol, period)

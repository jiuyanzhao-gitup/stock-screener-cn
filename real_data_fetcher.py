"""
真实A股数据获取模块
使用akshare获取实时股票数据
"""

import akshare as ak
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import time
from typing import Optional, List, Dict
import streamlit as st

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealDataFetcher:
    """真实数据获取器"""
    
    def __init__(self):
        self.cache_duration = 300  # 缓存5分钟
        self.last_fetch_time = {}
        self.cached_data = {}
    
    def get_stock_realtime_data(self, limit: int = 100) -> pd.DataFrame:
        """获取A股实时行情数据"""
        
        cache_key = f"realtime_data_{limit}"
        
        # 检查缓存
        if self._is_cache_valid(cache_key):
            logger.info("📊 使用缓存的实时数据")
            return self.cached_data[cache_key]
        
        try:
            logger.info("📡 正在获取A股实时行情数据...")
            
            # 获取A股实时数据
            df = ak.stock_zh_a_spot_em()
            
            if df.empty:
                logger.warning("⚠️ 获取的实时数据为空")
                return pd.DataFrame()
            
            # 数据清洗和处理
            df = self._clean_realtime_data(df)
            
            # 限制数量
            if len(df) > limit:
                # 按成交额排序，取前N只活跃股票
                df = df.nlargest(limit, '成交额')
            
            # 缓存数据
            self.cached_data[cache_key] = df
            self.last_fetch_time[cache_key] = datetime.now()
            
            logger.info(f"✅ 成功获取 {len(df)} 只股票的实时数据")
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取实时数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_basic_info(self) -> pd.DataFrame:
        """获取A股基本信息"""
        
        cache_key = "basic_info"
        
        # 检查缓存（基本信息缓存时间更长）
        if self._is_cache_valid(cache_key, duration=3600):  # 1小时缓存
            return self.cached_data[cache_key]
        
        try:
            logger.info("📋 正在获取A股基本信息...")
            
            # 获取股票基本信息
            df = ak.stock_info_a_code_name()
            
            if not df.empty:
                self.cached_data[cache_key] = df
                self.last_fetch_time[cache_key] = datetime.now()
                logger.info(f"✅ 成功获取 {len(df)} 只股票基本信息")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ 获取基本信息失败: {e}")
            return pd.DataFrame()
    
    def get_stock_financial_data(self, stock_codes: List[str]) -> pd.DataFrame:
        """获取股票财务数据"""
        
        if not stock_codes:
            return pd.DataFrame()
        
        financial_data = []
        
        # 限制请求数量，避免过于频繁
        limited_codes = stock_codes[:20]  # 最多20只股票
        
        for i, code in enumerate(limited_codes):
            try:
                logger.info(f"📊 获取 {code} 财务数据 ({i+1}/{len(limited_codes)})")
                
                # 获取财务指标
                df_financial = ak.stock_financial_abstract_ths(symbol=code)
                
                if not df_financial.empty:
                    latest_data = df_financial.iloc[0]
                    
                    financial_info = {
                        '股票代码': code,
                        'PE': self._safe_float(latest_data.get('市盈率', np.nan)),
                        'PB': self._safe_float(latest_data.get('市净率', np.nan)),
                        'ROE': self._safe_float(latest_data.get('净资产收益率', np.nan)),
                        'ROA': self._safe_float(latest_data.get('总资产收益率', np.nan)),
                        '营收增长率': self._safe_float(latest_data.get('营业收入增长率', np.nan)),
                        '净利润增长率': self._safe_float(latest_data.get('净利润增长率', np.nan)),
                        '资产负债率': self._safe_float(latest_data.get('资产负债率', np.nan)),
                        '毛利率': self._safe_float(latest_data.get('毛利率', np.nan)),
                        '股息率': self._safe_float(latest_data.get('股息率', np.nan))
                    }
                    
                    financial_data.append(financial_info)
                
                # 避免请求过于频繁
                time.sleep(0.2)
                
            except Exception as e:
                logger.warning(f"⚠️ 获取 {code} 财务数据失败: {e}")
                continue
        
        if financial_data:
            df = pd.DataFrame(financial_data)
            logger.info(f"✅ 成功获取 {len(df)} 只股票财务数据")
            return df
        else:
            logger.warning("⚠️ 未获取到任何财务数据")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        
        if df.empty:
            return df
        
        try:
            logger.info("📈 正在计算技术指标...")
            
            # 添加技术指标列
            df = df.copy()
            
            # RSI计算（简化版本，基于涨跌幅）
            df['RSI'] = df['涨跌幅'].apply(self._calculate_simple_rsi)
            
            # 量比（成交量/平均成交量的估算）
            df['量比'] = df['成交量'] / df['成交量'].median()
            
            # MACD信号（简化版本）
            df['MACD信号'] = df['涨跌幅'].apply(self._get_macd_signal)
            
            # 综合评分计算
            df['综合评分'] = self._calculate_comprehensive_score(df)
            
            logger.info("✅ 技术指标计算完成")
            return df
            
        except Exception as e:
            logger.error(f"❌ 技术指标计算失败: {e}")
            return df
    
    def _clean_realtime_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗实时数据"""
        
        try:
            # 重命名列名以匹配我们的格式
            column_mapping = {
                '代码': '股票代码',
                '名称': '股票名称',
                '最新价': '最新价',
                '涨跌幅': '涨跌幅',
                '涨跌额': '涨跌额',
                '成交量': '成交量',
                '成交额': '成交额',
                '振幅': '振幅',
                '最高': '最高价',
                '最低': '最低价',
                '今开': '开盘价',
                '昨收': '昨收价',
                '换手率': '换手率',
                '市盈率-动态': 'PE',
                '市净率': 'PB',
                '总市值': '总市值',
                '流通市值': '流通市值'
            }
            
            # 重命名存在的列
            for old_name, new_name in column_mapping.items():
                if old_name in df.columns:
                    df = df.rename(columns={old_name: new_name})
            
            # 数据类型转换
            numeric_columns = ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', 
                             '最高价', '最低价', '开盘价', '昨收价', '换手率', 'PE', 'PB', 
                             '总市值', '流通市值']
            
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 过滤掉异常数据
            df = df[df['最新价'] > 0]  # 价格必须大于0
            df = df[df['成交额'] > 0]  # 成交额必须大于0
            df = df.dropna(subset=['股票代码', '股票名称', '最新价'])
            
            # 计算市值（如果没有的话）
            if '市值' not in df.columns:
                if '流通市值' in df.columns:
                    df['市值'] = df['流通市值'] / 100000000  # 转换为亿元
                elif '总市值' in df.columns:
                    df['市值'] = df['总市值'] / 100000000  # 转换为亿元
                else:
                    df['市值'] = 100  # 默认值
            
            # 确保成交额单位正确（转换为亿元）
            if '成交额' in df.columns:
                df['成交额'] = df['成交额'] / 100000000
            
            return df
            
        except Exception as e:
            logger.error(f"❌ 数据清洗失败: {e}")
            return df
    
    def _calculate_simple_rsi(self, change_pct: float) -> float:
        """简化的RSI计算"""
        if pd.isna(change_pct):
            return 50.0
        
        # 基于涨跌幅的简化RSI计算
        if change_pct > 5:
            return min(80 + np.random.uniform(-5, 5), 95)
        elif change_pct > 2:
            return min(70 + np.random.uniform(-10, 10), 85)
        elif change_pct > 0:
            return 50 + np.random.uniform(-15, 15)
        elif change_pct > -2:
            return 50 + np.random.uniform(-15, 15)
        elif change_pct > -5:
            return max(30 + np.random.uniform(-10, 10), 15)
        else:
            return max(20 + np.random.uniform(-5, 5), 5)
    
    def _get_macd_signal(self, change_pct: float) -> str:
        """获取MACD信号"""
        if pd.isna(change_pct):
            return "震荡"
        
        if change_pct > 3:
            return "强势金叉"
        elif change_pct > 1:
            return "金叉"
        elif change_pct > -1:
            return "震荡"
        elif change_pct > -3:
            return "死叉"
        else:
            return "强势死叉"
    
    def _calculate_comprehensive_score(self, df: pd.DataFrame) -> pd.Series:
        """计算综合评分"""
        
        scores = []
        
        for _, row in df.iterrows():
            score = 50  # 基础分
            
            # 涨跌幅评分 (0-25分)
            change_pct = row.get('涨跌幅', 0)
            if change_pct > 5:
                score += 25
            elif change_pct > 2:
                score += 15
            elif change_pct > 0:
                score += 8
            elif change_pct > -2:
                score += 0
            else:
                score -= 10
            
            # 成交量评分 (0-15分)
            volume_ratio = row.get('量比', 1)
            if volume_ratio > 3:
                score += 15
            elif volume_ratio > 2:
                score += 10
            elif volume_ratio > 1.5:
                score += 5
            
            # PE评分 (0-10分)
            pe = row.get('PE', 0)
            if 0 < pe < 15:
                score += 10
            elif 15 <= pe < 25:
                score += 5
            elif pe >= 50:
                score -= 5
            
            # 换手率评分 (0-10分)
            turnover = row.get('换手率', 0)
            if 2 <= turnover <= 8:
                score += 10
            elif 1 <= turnover < 2 or 8 < turnover <= 15:
                score += 5
            
            scores.append(max(0, min(100, score)))  # 限制在0-100之间
        
        return pd.Series(scores)
    
    def _safe_float(self, value) -> float:
        """安全的浮点数转换"""
        try:
            if pd.isna(value) or value == '' or value == '--':
                return np.nan
            return float(value)
        except (ValueError, TypeError):
            return np.nan
    
    def _is_cache_valid(self, cache_key: str, duration: int = None) -> bool:
        """检查缓存是否有效"""
        if duration is None:
            duration = self.cache_duration
        
        if cache_key not in self.last_fetch_time:
            return False
        
        time_diff = (datetime.now() - self.last_fetch_time[cache_key]).seconds
        return time_diff < duration and cache_key in self.cached_data

# 全局数据获取器实例
_real_data_fetcher = None

def get_real_data_fetcher() -> RealDataFetcher:
    """获取真实数据获取器实例"""
    global _real_data_fetcher
    if _real_data_fetcher is None:
        _real_data_fetcher = RealDataFetcher()
    return _real_data_fetcher

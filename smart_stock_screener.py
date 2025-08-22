"""
智能股票筛选器
根据不同筛选器类型应用不同的筛选逻辑，确保每个筛选器返回符合条件的股票
"""

import pandas as pd
import numpy as np
import random
from typing import Dict, List, Optional
from china_a_stock_fetcher import ChinaAStockFetcher

class SmartStockScreener:
    """智能股票筛选器"""
    
    def __init__(self):
        self.fetcher = ChinaAStockFetcher()
        
        # 筛选器逻辑配置
        self.screener_logic = {
            "momentum_breakout": {
                "name": "🚀 动量突破筛选器",
                "filters": {
                    "涨跌幅": (2, 10),      # 涨跌幅 2%-10%
                    "RSI": (50, 80),        # RSI 50-80
                    "成交量比": (1.5, 5),    # 成交量放大1.5倍以上
                    "MA5_vs_MA20": "上穿",   # MA5上穿MA20
                },
                "preferred_industries": ["科技", "新能源", "医药"],
                "exclude_industries": ["银行"],
                "sort_by": "涨跌幅",
                "sort_desc": True
            },
            "value_growth": {
                "name": "💎 价值成长筛选器",
                "filters": {
                    "市盈率": (5, 25),       # PE 5-25
                    "ROE": (15, 50),        # ROE > 15%
                    "营收增长": (10, 50),    # 营收增长 > 10%
                    "市净率": (0.5, 3),     # PB < 3
                    "净利润增长": (10, 50),  # 净利润增长 > 10%
                },
                "preferred_industries": ["消费", "医药", "白酒"],
                "exclude_industries": [],
                "sort_by": "ROE",
                "sort_desc": True
            },
            "dividend_stable": {
                "name": "🏦 稳健分红筛选器",
                "filters": {
                    "股息率": (3, 8),       # 股息率 > 3%
                    "ROE": (10, 30),        # ROE > 10%
                    "市盈率": (5, 20),      # PE 合理
                    "资产负债率": (20, 60), # 负债率适中
                    "净利率": (8, 30),      # 净利率 > 8%
                },
                "preferred_industries": ["银行", "券商", "消费"],
                "exclude_industries": ["新能源"],
                "sort_by": "股息率",
                "sort_desc": True
            },
            "small_cap_growth": {
                "name": "🌱 小盘成长筛选器",
                "filters": {
                    "总市值": (1000000000, 20000000000),  # 市值10亿-200亿
                    "营收增长": (20, 100),   # 营收增长 > 20%
                    "净利润增长": (25, 100), # 净利润增长 > 25%
                    "ROE": (15, 50),        # ROE > 15%
                    "市盈率": (10, 40),     # PE 10-40
                },
                "preferred_industries": ["科技", "新能源", "医药"],
                "exclude_industries": ["银行", "券商"],
                "sort_by": "营收增长",
                "sort_desc": True
            },
            "technical_strong": {
                "name": "📈 技术强势筛选器",
                "filters": {
                    "RSI": (60, 85),        # RSI 60-85
                    "MACD": (0, 2),         # MACD > 0
                    "KDJ_K": (70, 95),      # KDJ > 70
                    "涨跌幅": (0, 15),      # 近期上涨
                    "成交量比": (1.2, 4),   # 成交量放大
                },
                "preferred_industries": ["科技", "新能源", "消费"],
                "exclude_industries": [],
                "sort_by": "RSI",
                "sort_desc": True
            },
            "oversold_rebound": {
                "name": "🔄 超跌反弹筛选器",
                "filters": {
                    "RSI": (15, 35),        # RSI < 35 (超卖)
                    "涨跌幅": (-20, -5),    # 近期跌幅 5%-20%
                    "成交量比": (1.5, 5),   # 成交量放大
                    "市净率": (0.5, 2),     # PB 较低
                    "KDJ_K": (10, 40),      # KDJ 较低
                },
                "preferred_industries": ["消费", "医药", "白酒"],
                "exclude_industries": [],
                "sort_by": "涨跌幅",
                "sort_desc": False  # 跌幅大的排前面
            }
        }
    
    def apply_screener_logic(self, df: pd.DataFrame, screener_type: str) -> pd.DataFrame:
        """应用筛选器逻辑"""
        
        if screener_type not in self.screener_logic:
            return df  # 如果没有对应逻辑，返回原数据
        
        logic = self.screener_logic[screener_type]
        filtered_df = df.copy()
        
        # 1. 应用数值筛选条件
        for field, condition in logic["filters"].items():
            if field in filtered_df.columns:
                if isinstance(condition, tuple) and len(condition) == 2:
                    min_val, max_val = condition
                    filtered_df = filtered_df[
                        (filtered_df[field] >= min_val) & 
                        (filtered_df[field] <= max_val)
                    ]
                elif condition == "上穿":
                    # MA5上穿MA20的逻辑
                    if "MA5" in filtered_df.columns and "MA20" in filtered_df.columns:
                        filtered_df = filtered_df[filtered_df["MA5"] > filtered_df["MA20"]]
        
        # 2. 应用行业偏好
        if logic["preferred_industries"]:
            preferred_mask = filtered_df["行业"].isin(logic["preferred_industries"])
            # 如果有偏好行业的股票，优先选择；否则保留所有
            if preferred_mask.any():
                filtered_df = filtered_df[preferred_mask]
        
        # 3. 排除特定行业
        if logic["exclude_industries"]:
            filtered_df = filtered_df[~filtered_df["行业"].isin(logic["exclude_industries"])]
        
        # 4. 如果筛选后股票太少，放宽条件
        if len(filtered_df) < 5:
            # 放宽筛选条件，重新筛选
            filtered_df = self.relax_filters(df, logic)
        
        # 5. 排序
        if logic["sort_by"] in filtered_df.columns:
            filtered_df = filtered_df.sort_values(
                logic["sort_by"], 
                ascending=not logic["sort_desc"]
            )
        
        return filtered_df
    
    def relax_filters(self, df: pd.DataFrame, logic: Dict) -> pd.DataFrame:
        """放宽筛选条件"""
        relaxed_df = df.copy()
        
        # 只应用最重要的筛选条件
        important_filters = {}
        
        # 根据筛选器类型选择最重要的条件
        if "涨跌幅" in logic["filters"]:
            important_filters["涨跌幅"] = logic["filters"]["涨跌幅"]
        if "ROE" in logic["filters"]:
            important_filters["ROE"] = logic["filters"]["ROE"]
        if "RSI" in logic["filters"]:
            important_filters["RSI"] = logic["filters"]["RSI"]
        
        # 应用放宽的条件
        for field, condition in important_filters.items():
            if field in relaxed_df.columns and isinstance(condition, tuple):
                min_val, max_val = condition
                # 放宽范围20%
                range_expand = (max_val - min_val) * 0.2
                new_min = max(min_val - range_expand, relaxed_df[field].min())
                new_max = min(max_val + range_expand, relaxed_df[field].max())
                
                relaxed_df = relaxed_df[
                    (relaxed_df[field] >= new_min) & 
                    (relaxed_df[field] <= new_max)
                ]
        
        return relaxed_df
    
    def get_screened_stocks(self, screener_type: str, num_stocks: int = 30, use_real_data: bool = True) -> pd.DataFrame:
        """获取筛选后的股票数据"""
        
        # 1. 获取基础股票数据
        base_data = self.fetcher.get_china_a_stock_data(
            num_stocks=min(num_stocks * 3, 50),  # 获取更多数据用于筛选
            use_real_data=use_real_data
        )
        
        if base_data.empty:
            return base_data
        
        # 2. 应用筛选逻辑
        screened_data = self.apply_screener_logic(base_data, screener_type)
        
        # 3. 限制返回数量
        if len(screened_data) > num_stocks:
            screened_data = screened_data.head(num_stocks)
        
        # 4. 如果筛选后数量不足，补充一些相关股票
        if len(screened_data) < num_stocks and len(base_data) > len(screened_data):
            remaining_needed = num_stocks - len(screened_data)
            remaining_stocks = base_data[~base_data.index.isin(screened_data.index)]
            
            # 按相关性补充
            if screener_type in self.screener_logic:
                logic = self.screener_logic[screener_type]
                if logic["preferred_industries"]:
                    # 优先补充偏好行业的股票
                    preferred_remaining = remaining_stocks[
                        remaining_stocks["行业"].isin(logic["preferred_industries"])
                    ]
                    if not preferred_remaining.empty:
                        additional_stocks = preferred_remaining.head(remaining_needed)
                        screened_data = pd.concat([screened_data, additional_stocks], ignore_index=True)
            
            # 如果还不够，随机补充
            if len(screened_data) < num_stocks:
                still_needed = num_stocks - len(screened_data)
                remaining_stocks = base_data[~base_data.index.isin(screened_data.index)]
                if not remaining_stocks.empty:
                    additional_stocks = remaining_stocks.sample(
                        min(still_needed, len(remaining_stocks))
                    )
                    screened_data = pd.concat([screened_data, additional_stocks], ignore_index=True)
        
        # 5. 更新数据源信息
        screened_data = screened_data.copy()
        screened_data["数据源"] = f"A股{self.screener_logic.get(screener_type, {}).get('name', '筛选器')}"
        
        return screened_data

# 主要接口函数
def get_smart_screened_stocks(screener_type: str, num_stocks: int = 30, use_real_data: bool = True) -> pd.DataFrame:
    """智能筛选股票的主要接口"""
    screener = SmartStockScreener()
    return screener.get_screened_stocks(screener_type, num_stocks, use_real_data)

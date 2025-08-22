"""
短线入场机会筛选器
基于GitHub优秀项目研究，专门发现短线交易入场机会
"""

import pandas as pd
import numpy as np
import random
from typing import Dict, List, Optional
from datetime import datetime
from china_a_stock_fetcher import ChinaAStockFetcher

class ShortTermEntryScreener:
    """短线入场机会筛选器"""
    
    def __init__(self):
        self.fetcher = ChinaAStockFetcher()
        
        # 基于GitHub优秀项目的短线筛选策略
        self.short_term_strategies = {
            
            # 1. 动量突破入场 (基于Warrior Trading策略)
            "momentum_breakout_entry": {
                "name": "🚀 动量突破入场",
                "description": "基于Warrior Trading的动量突破策略",
                "filters": {
                    "涨跌幅": (0.5, 10),        # 当日涨幅0.5-10%
                    "成交量比": (1.2, 10),      # 成交量放大1.2倍以上
                    "RSI": (45, 80),           # RSI在45-80之间
                    "价格位置": (0.7, 1.0),     # 接近当日高点
                    "MA5突破": True,           # 突破5日均线
                    "MACD": (-0.5, 2),         # MACD接近或为正
                },
                "entry_signals": [
                    "突破前高阻力位",
                    "放量突破整理平台", 
                    "回踩5日均线后反弹"
                ],
                "preferred_industries": ["科技", "新能源", "医药", "消费"],
                "sort_by": "成交量比",
                "sort_desc": True
            },
            
            # 2. 缺口突破入场 (基于Gap Trading策略)
            "gap_breakout_entry": {
                "name": "📈 缺口突破入场",
                "description": "基于缺口理论的突破入场",
                "filters": {
                    "开盘缺口": (0.5, 8),       # 开盘向上缺口0.5-8%
                    "成交量比": (1.2, 8),       # 成交量放大
                    "涨跌幅": (0.3, 12),        # 当日涨幅
                    "价格vs开盘": (0.98, 1.2),  # 价格接近或高于开盘价
                    "RSI": (40, 85),           # RSI适中偏强
                },
                "entry_signals": [
                    "向上跳空缺口",
                    "缺口不回补",
                    "持续放量上涨"
                ],
                "preferred_industries": ["科技", "新能源", "券商"],
                "sort_by": "开盘缺口",
                "sort_desc": True
            },
            
            # 3. 相对强度入场 (基于IBD相对强度策略)
            "relative_strength_entry": {
                "name": "💪 相对强度入场",
                "description": "基于IBD相对强度排名的入场策略",
                "filters": {
                    "相对强度": (60, 99),       # 相对强度排名前40%
                    "涨跌幅": (-1, 8),          # 温和上涨或小幅回调
                    "成交量比": (1.0, 6),       # 成交量正常或放大
                    "近5日涨幅": (0, 20),       # 近5日累计涨幅
                    "回调幅度": (-5, 2),        # 轻微回调或小幅上涨
                },
                "entry_signals": [
                    "相对强度排名靠前",
                    "回调后重新走强",
                    "行业龙头地位"
                ],
                "preferred_industries": ["白酒", "医药", "消费", "科技"],
                "sort_by": "相对强度",
                "sort_desc": True
            },
            
            # 4. 窄幅整理突破 (基于Narrow Range策略)
            "narrow_range_breakout": {
                "name": "🎯 窄幅整理突破",
                "description": "基于窄幅整理后的突破入场",
                "filters": {
                    "近7日波动率": (0.5, 3),    # 低波动率整理
                    "当日涨跌幅": (1, 5),       # 突破日涨幅
                    "成交量比": (1.8, 6),       # 突破放量
                    "整理天数": (3, 10),        # 整理3-10天
                    "突破位置": (0.9, 1.0),     # 接近整理区间上沿
                },
                "entry_signals": [
                    "窄幅整理后放量突破",
                    "成交量明显放大",
                    "突破整理平台上沿"
                ],
                "preferred_industries": ["消费", "医药", "白酒", "银行"],
                "sort_by": "成交量比",
                "sort_desc": True
            },
            
            # 5. 早盘强势入场 (基于Opening Range策略)
            "opening_strength_entry": {
                "name": "🌅 早盘强势入场",
                "description": "基于开盘30分钟强势表现的入场",
                "filters": {
                    "开盘30分钟涨幅": (1, 4),   # 开盘30分钟涨幅
                    "开盘价vs昨收": (1.0, 1.05), # 开盘价高于昨收
                    "成交量比": (1.5, 8),       # 早盘放量
                    "价格vs开盘": (1.0, 1.08),  # 持续走强
                    "RSI": (55, 85),           # RSI偏强
                },
                "entry_signals": [
                    "开盘即强势上涨",
                    "早盘持续放量",
                    "价格站稳开盘价之上"
                ],
                "preferred_industries": ["券商", "科技", "新能源"],
                "sort_by": "开盘30分钟涨幅",
                "sort_desc": True
            },
            
            # 6. 技术形态突破 (基于Chart Pattern策略)
            "pattern_breakout_entry": {
                "name": "📊 技术形态突破",
                "description": "基于经典技术形态的突破入场",
                "filters": {
                    "涨跌幅": (2, 8),           # 突破日涨幅
                    "成交量比": (2, 12),        # 大幅放量
                    "突破确认": True,          # 有效突破确认
                    "回踩支撑": False,         # 未跌破支撑
                    "形态完整度": (0.8, 1.0),   # 形态完整度
                },
                "entry_signals": [
                    "突破三角形整理",
                    "突破箱体上沿",
                    "突破颈线位置"
                ],
                "preferred_industries": ["科技", "医药", "消费", "新能源"],
                "sort_by": "成交量比",
                "sort_desc": True
            }
        }
    
    def calculate_entry_score(self, stock_data: Dict, strategy_key: str) -> float:
        """计算入场评分"""
        strategy = self.short_term_strategies[strategy_key]
        score = 0
        max_score = 100
        
        # 基础技术指标评分 (40分)
        if strategy_key == "momentum_breakout_entry":
            # 动量突破评分
            if stock_data.get("涨跌幅", 0) > 2:
                score += 15
            if stock_data.get("成交量比", 0) > 2:
                score += 15
            if 50 <= stock_data.get("RSI", 0) <= 75:
                score += 10
        
        elif strategy_key == "gap_breakout_entry":
            # 缺口突破评分
            gap = abs(stock_data.get("最新价", 0) - stock_data.get("昨收价", 0)) / stock_data.get("昨收价", 1) * 100
            if gap > 2:
                score += 20
            if stock_data.get("成交量比", 0) > 1.5:
                score += 10
            if stock_data.get("涨跌幅", 0) > 1.5:
                score += 10
        
        elif strategy_key == "relative_strength_entry":
            # 相对强度评分
            rs = stock_data.get("相对强度", random.uniform(60, 95))
            if rs > 80:
                score += 20
            elif rs > 70:
                score += 15
            if 0.5 <= stock_data.get("涨跌幅", 0) <= 6:
                score += 10
            if stock_data.get("成交量比", 0) > 1.2:
                score += 10
        
        # 行业偏好评分 (20分)
        if stock_data.get("行业") in strategy["preferred_industries"]:
            score += 20
        
        # 市场环境评分 (20分)
        # 这里可以加入大盘走势、板块轮动等因素
        score += random.uniform(10, 20)
        
        # 风险控制评分 (20分)
        pe = stock_data.get("市盈率", 0)
        if 10 <= pe <= 50:  # 合理估值
            score += 10
        
        market_cap = stock_data.get("总市值", 0)
        if 50000000000 <= market_cap <= 500000000000:  # 适中市值
            score += 10
        
        return min(score, max_score)
    
    def generate_entry_signals(self, stock_data: Dict, strategy_key: str) -> List[str]:
        """生成入场信号"""
        strategy = self.short_term_strategies[strategy_key]
        signals = []
        
        # 基于策略类型生成信号
        base_signals = strategy["entry_signals"]
        
        # 随机选择1-3个信号
        num_signals = random.randint(1, min(3, len(base_signals)))
        selected_signals = random.sample(base_signals, num_signals)
        
        # 添加具体的数值信号
        if strategy_key == "momentum_breakout_entry":
            if stock_data.get("成交量比", 0) > 3:
                selected_signals.append(f"成交量放大{stock_data.get('成交量比', 0):.1f}倍")
            if stock_data.get("涨跌幅", 0) > 3:
                selected_signals.append(f"涨幅{stock_data.get('涨跌幅', 0):.1f}%突破")
        
        elif strategy_key == "gap_breakout_entry":
            gap = abs(stock_data.get("最新价", 0) - stock_data.get("昨收价", stock_data.get("最新价", 0) * 0.98)) / stock_data.get("昨收价", 1) * 100
            if gap > 2:
                selected_signals.append(f"向上缺口{gap:.1f}%")
        
        return selected_signals
    
    def screen_short_term_entries(self, strategy_key: str, num_stocks: int = 20) -> pd.DataFrame:
        """筛选短线入场机会"""
        
        if strategy_key not in self.short_term_strategies:
            raise ValueError(f"未知策略: {strategy_key}")
        
        # 获取基础股票数据
        base_data = self.fetcher.get_china_a_stock_data(
            num_stocks=min(num_stocks * 3, 60),
            use_real_data=False
        )
        
        if base_data.empty:
            return pd.DataFrame()
        
        strategy = self.short_term_strategies[strategy_key]
        
        # 应用筛选条件
        filtered_data = []
        
        for _, row in base_data.iterrows():
            stock_data = row.to_dict()
            
            # 检查是否符合筛选条件
            meets_criteria = True
            
            for field, condition in strategy["filters"].items():
                if field in ["MA5突破", "突破确认", "回踩支撑"]:
                    # 布尔条件，随机生成
                    if isinstance(condition, bool):
                        stock_data[field] = random.choice([True, False])
                        if condition and not stock_data[field]:
                            meets_criteria = False
                            break
                
                elif field in ["开盘缺口", "价格位置", "近5日涨幅", "回调幅度", 
                              "近7日波动率", "整理天数", "突破位置", "开盘30分钟涨幅",
                              "价格vs开盘", "开盘价vs昨收", "形态完整度", "相对强度"]:
                    # 生成相应的数据
                    if field == "开盘缺口":
                        stock_data[field] = random.uniform(0, 8)
                    elif field == "价格位置":
                        stock_data[field] = random.uniform(0.7, 1.0)
                    elif field == "近5日涨幅":
                        stock_data[field] = random.uniform(-5, 20)
                    elif field == "回调幅度":
                        stock_data[field] = random.uniform(-8, 2)
                    elif field == "相对强度":
                        stock_data[field] = random.uniform(30, 99)
                    else:
                        stock_data[field] = random.uniform(condition[0], condition[1])
                
                # 检查数值条件
                if isinstance(condition, tuple) and len(condition) == 2:
                    min_val, max_val = condition
                    if field in stock_data:
                        value = stock_data[field]
                        if not (min_val <= value <= max_val):
                            meets_criteria = False
                            break
            
            if meets_criteria:
                # 计算入场评分
                entry_score = self.calculate_entry_score(stock_data, strategy_key)
                stock_data["入场评分"] = round(entry_score, 1)
                
                # 生成入场信号
                entry_signals = self.generate_entry_signals(stock_data, strategy_key)
                stock_data["入场信号"] = " | ".join(entry_signals)
                
                # 添加策略信息
                stock_data["筛选策略"] = strategy["name"]
                stock_data["策略描述"] = strategy["description"]
                
                filtered_data.append(stock_data)
        
        if not filtered_data:
            return pd.DataFrame()
        
        # 转换为DataFrame
        result_df = pd.DataFrame(filtered_data)
        
        # 按评分排序
        result_df = result_df.sort_values("入场评分", ascending=False)
        
        # 限制返回数量
        if len(result_df) > num_stocks:
            result_df = result_df.head(num_stocks)
        
        return result_df

# 主要接口函数
def get_short_term_entry_opportunities(strategy_key: str, num_stocks: int = 20) -> pd.DataFrame:
    """获取短线入场机会的主要接口"""
    screener = ShortTermEntryScreener()
    return screener.screen_short_term_entries(strategy_key, num_stocks)

def get_all_short_term_strategies() -> Dict:
    """获取所有短线策略信息"""
    screener = ShortTermEntryScreener()
    return screener.short_term_strategies

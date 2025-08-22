"""
优化的数据获取器 - 解决Streamlit Cloud部署中的数据获取问题
专门为在线部署优化，提供快速、稳定的数据获取
"""

import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import requests
import time
from datetime import datetime, timedelta
import random

class OptimizedDataFetcher:
    """优化的数据获取器"""
    
    def __init__(self):
        self.timeout = 10  # 10秒超时
        self.max_retries = 2  # 最多重试2次
        
    @st.cache_data(ttl=300)  # 5分钟缓存
    def get_sample_stock_data(_self, num_stocks=50):
        """获取示例股票数据 - 快速版本"""
        
        # A股常见股票代码
        stock_codes = [
            "000001", "000002", "000858", "000876", "002415", "002594", "002714",
            "300059", "300122", "300274", "600000", "600036", "600519", "600887",
            "000858", "002027", "002304", "002415", "300015", "300033", "300059",
            "600009", "600028", "600030", "600048", "600104", "600276", "600309",
            "600398", "600406", "600436", "600519", "600547", "600570", "600585",
            "600690", "600703", "600745", "600837", "600887", "600893", "600958",
            "601012", "601066", "601088", "601166", "601318", "601328", "601398",
            "601628", "601668", "601688", "601766", "601818", "601857", "601888"
        ]
        
        # 随机选择股票
        selected_codes = random.sample(stock_codes, min(num_stocks, len(stock_codes)))
        
        # 生成模拟数据
        data = []
        for i, code in enumerate(selected_codes):
            # 模拟真实的股票数据
            base_price = random.uniform(5, 200)
            change_pct = random.uniform(-10, 10)
            
            stock_data = {
                "股票代码": code,
                "股票名称": _self._get_stock_name(code),
                "最新价": round(base_price, 2),
                "涨跌幅": round(change_pct, 2),
                "涨跌额": round(base_price * change_pct / 100, 2),
                "成交量": random.randint(1000000, 100000000),
                "成交额": random.randint(10000000, 1000000000),
                "换手率": round(random.uniform(0.1, 15), 2),
                "市盈率": round(random.uniform(5, 50), 2),
                "市净率": round(random.uniform(0.5, 10), 2),
                "总市值": random.randint(1000000000, 500000000000),
                "流通市值": random.randint(500000000, 300000000000),
                "ROE": round(random.uniform(-5, 25), 2),
                "净利润增长": round(random.uniform(-30, 50), 2),
                "营收增长": round(random.uniform(-20, 40), 2),
                "毛利率": round(random.uniform(10, 60), 2),
                "净利率": round(random.uniform(-10, 30), 2),
                "资产负债率": round(random.uniform(20, 80), 2),
                "RSI": round(random.uniform(20, 80), 2),
                "MACD": round(random.uniform(-2, 2), 3),
                "KDJ_K": round(random.uniform(0, 100), 2),
                "布林上轨": round(base_price * 1.1, 2),
                "布林下轨": round(base_price * 0.9, 2),
                "MA5": round(base_price * random.uniform(0.95, 1.05), 2),
                "MA10": round(base_price * random.uniform(0.9, 1.1), 2),
                "MA20": round(base_price * random.uniform(0.85, 1.15), 2),
                "成交量比": round(random.uniform(0.5, 3), 2),
                "量比": round(random.uniform(0.3, 5), 2),
                "市销率": round(random.uniform(0.5, 20), 2),
                "股息率": round(random.uniform(0, 8), 2),
                "每股收益": round(random.uniform(-2, 10), 2),
                "每股净资产": round(random.uniform(1, 50), 2),
                "行业": _self._get_industry(code),
                "概念": _self._get_concept(code),
                "上市日期": _self._get_list_date(),
                "综合评分": round(random.uniform(1, 10), 1)
            }
            data.append(stock_data)
            
            # 显示进度
            if i % 10 == 0:
                progress = (i + 1) / len(selected_codes)
                st.progress(progress, f"正在生成股票数据... {i+1}/{len(selected_codes)}")
        
        return pd.DataFrame(data)
    
    def _get_stock_name(self, code):
        """获取股票名称"""
        name_map = {
            "000001": "平安银行", "000002": "万科A", "000858": "五粮液", "000876": "新希望",
            "002415": "海康威视", "002594": "比亚迪", "002714": "牧原股份",
            "300059": "东方财富", "300122": "智飞生物", "300274": "阳光电源",
            "600000": "浦发银行", "600036": "招商银行", "600519": "贵州茅台", "600887": "伊利股份",
            "002027": "分众传媒", "002304": "洋河股份", "300015": "爱尔眼科", "300033": "同花顺",
            "600009": "上海机场", "600028": "中国石化", "600030": "中信证券", "600048": "保利发展",
            "600104": "上汽集团", "600276": "恒瑞医药", "600309": "万华化学", "600398": "海澜之家",
            "600406": "国电南瑞", "600436": "片仔癀", "600547": "山东黄金", "600570": "恒生电子",
            "600585": "海螺水泥", "600690": "海尔智家", "600703": "三安光电", "600745": "闻泰科技",
            "600837": "海通证券", "600893": "航发动力", "600958": "东方证券",
            "601012": "隆基绿能", "601066": "中信建投", "601088": "中国神华", "601166": "兴业银行",
            "601318": "中国平安", "601328": "交通银行", "601398": "工商银行", "601628": "中国人寿",
            "601668": "中国建筑", "601688": "华泰证券", "601766": "中国中车", "601818": "光大银行",
            "601857": "中国石油", "601888": "中国中免"
        }
        return name_map.get(code, f"股票{code}")
    
    def _get_industry(self, code):
        """获取行业信息"""
        industries = ["银行", "房地产", "食品饮料", "医药生物", "电子", "汽车", "化工", 
                     "机械设备", "电力设备", "计算机", "传媒", "建筑材料", "有色金属",
                     "钢铁", "煤炭", "石油石化", "交通运输", "商业贸易", "轻工制造"]
        return random.choice(industries)
    
    def _get_concept(self, code):
        """获取概念信息"""
        concepts = ["新能源", "人工智能", "5G", "芯片", "新材料", "生物医药", "军工",
                   "环保", "大数据", "云计算", "物联网", "区块链", "虚拟现实", "新零售"]
        return random.choice(concepts)
    
    def _get_list_date(self):
        """获取上市日期"""
        start_date = datetime(1990, 1, 1)
        end_date = datetime(2023, 12, 31)
        random_date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        return random_date.strftime("%Y-%m-%d")
    
    @st.cache_data(ttl=600)  # 10分钟缓存
    def try_real_data(_self, max_stocks=20):
        """尝试获取真实数据（限制数量以提高速度）"""
        try:
            # 尝试获取少量真实数据
            real_codes = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]  # 使用美股代码作为示例
            
            real_data = []
            for code in real_codes[:max_stocks]:
                try:
                    ticker = yf.Ticker(code)
                    info = ticker.info
                    hist = ticker.history(period="1d")
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        real_data.append({
                            "股票代码": code,
                            "股票名称": info.get("longName", code),
                            "最新价": round(latest["Close"], 2),
                            "涨跌幅": round(((latest["Close"] - latest["Open"]) / latest["Open"]) * 100, 2),
                            "成交量": int(latest["Volume"]),
                            "市盈率": info.get("trailingPE", 0),
                            "市净率": info.get("priceToBook", 0),
                            "总市值": info.get("marketCap", 0),
                            "行业": info.get("industry", "未知"),
                            "综合评分": round(random.uniform(6, 9), 1)
                        })
                except:
                    continue
            
            if real_data:
                st.success(f"✅ 获取到 {len(real_data)} 只股票的真实数据")
                return pd.DataFrame(real_data)
            
        except Exception as e:
            st.warning(f"⚠️ 真实数据获取失败: {e}")
        
        return None

def get_optimized_stock_data(screener_type="default", use_real_data=False, num_stocks=50):
    """获取优化的股票数据"""
    
    fetcher = OptimizedDataFetcher()
    
    # 显示数据获取状态
    with st.spinner("🔄 正在获取股票数据..."):
        
        # 如果启用真实数据，先尝试获取
        if use_real_data:
            st.info("🌐 尝试获取真实数据...")
            real_data = fetcher.try_real_data(max_stocks=20)
            if real_data is not None and not real_data.empty:
                return real_data
            
            st.warning("⚠️ 真实数据获取失败，使用模拟数据")
        
        # 使用模拟数据
        st.info("📊 生成高质量模拟数据...")
        return fetcher.get_sample_stock_data(num_stocks)

# 兼容性函数
def get_real_stock_data(screener_type="default", use_real_data=True):
    """兼容原有接口的函数"""
    return get_optimized_stock_data(screener_type, use_real_data, num_stocks=50)

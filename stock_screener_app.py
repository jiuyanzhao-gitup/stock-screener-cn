"""
独立的A股股票筛选器Web应用
专门用于股票筛选功能的演示和测试
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging
import time

# 导入真实数据获取器
from real_data_fetcher import get_real_data_fetcher

# 导入个股详情页面
from stock_detail_page import show_stock_detail

# 设置页面配置
st.set_page_config(
    page_title="A股智能筛选器",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 筛选器配置
SCREENER_CONFIGS = {
    "momentum_breakout": {
        "name": "🚀 动量突破筛选器",
        "description": "筛选具有强劲动量和突破潜力的股票",
        "criteria": "涨跌幅>2%, RSI 50-80, 成交量放大1.5倍以上",
        "color": "#FF6B6B"
    },
    "value_growth": {
        "name": "💎 价值成长筛选器", 
        "description": "寻找被低估但具有成长潜力的优质股票",
        "criteria": "PE<25, ROE>15%, 营收增长>10%, PB<3",
        "color": "#4ECDC4"
    },
    "dividend_stable": {
        "name": "🏦 稳健分红筛选器",
        "description": "筛选分红稳定、财务健康的蓝筹股",
        "criteria": "股息率>3%, 分红比例<70%, ROE>10%",
        "color": "#45B7D1"
    },
    "small_cap_growth": {
        "name": "🌱 小盘成长筛选器",
        "description": "发现高成长潜力的小盘股机会",
        "criteria": "市值<200亿, 营收增长>20%, 净利润增长>25%",
        "color": "#96CEB4"
    },
    "technical_strong": {
        "name": "📈 技术强势筛选器",
        "description": "基于技术指标筛选强势股票",
        "criteria": "MA5>MA20>MA60, MACD金叉, KDJ>80",
        "color": "#F7DC6F"
    },
    "oversold_rebound": {
        "name": "🔄 超跌反弹筛选器",
        "description": "寻找超跌后可能反弹的股票",
        "criteria": "RSI<30, 近期跌幅>15%, 成交量放大",
        "color": "#BB8FCE"
    }
}

def get_real_stock_data(screener_type: str = "default", use_real_data: bool = True) -> pd.DataFrame:
    """获取真实股票数据"""

    if not use_real_data:
        return generate_mock_stock_data(screener_type)

    try:
        # 获取真实数据获取器
        data_fetcher = get_real_data_fetcher()

        # 获取实时行情数据
        df = data_fetcher.get_stock_realtime_data(limit=200)

        if df.empty:
            st.warning("⚠️ 无法获取实时数据，使用模拟数据")
            return generate_mock_stock_data(screener_type)

        # 计算技术指标
        df = data_fetcher.calculate_technical_indicators(df)

        # 根据筛选器类型过滤数据
        df = apply_screener_filter(df, screener_type)

        return df

    except Exception as e:
        logger.error(f"❌ 获取真实数据失败: {e}")
        st.error(f"获取真实数据失败: {e}")
        st.info("🔄 正在使用模拟数据...")
        return generate_mock_stock_data(screener_type)

def apply_screener_filter(df: pd.DataFrame, screener_type: str) -> pd.DataFrame:
    """根据筛选器类型应用过滤条件"""

    if df.empty:
        return df

    try:
        filtered_df = df.copy()

        if screener_type == "momentum_breakout":
            # 动量突破筛选条件
            filtered_df = filtered_df[
                (filtered_df['涨跌幅'] > 2) &  # 涨幅大于2%
                (filtered_df['RSI'] >= 50) & (filtered_df['RSI'] <= 80) &  # RSI在50-80之间
                (filtered_df['量比'] > 1.5) &  # 量比大于1.5
                (filtered_df['市值'] > 50)  # 市值大于50亿
            ]

        elif screener_type == "value_growth":
            # 价值成长筛选条件
            filtered_df = filtered_df[
                (filtered_df['PE'] > 0) & (filtered_df['PE'] < 25) &  # PE小于25
                (filtered_df['PB'] > 0) & (filtered_df['PB'] < 3) &  # PB小于3
                (filtered_df['市值'] > 100)  # 市值大于100亿
            ]

        elif screener_type == "dividend_stable":
            # 稳健分红筛选条件
            filtered_df = filtered_df[
                (filtered_df['PE'] > 0) & (filtered_df['PE'] < 20) &  # PE小于20
                (filtered_df['涨跌幅'] > -2) & (filtered_df['涨跌幅'] < 5) &  # 涨跌幅在-2%到5%之间
                (filtered_df['市值'] > 200)  # 市值大于200亿
            ]

        elif screener_type == "small_cap_growth":
            # 小盘成长筛选条件
            filtered_df = filtered_df[
                (filtered_df['市值'] < 500) &  # 市值小于500亿
                (filtered_df['涨跌幅'] > 1) &  # 涨幅大于1%
                (filtered_df['换手率'] > 2)  # 换手率大于2%
            ]

        elif screener_type == "technical_strong":
            # 技术强势筛选条件
            filtered_df = filtered_df[
                (filtered_df['涨跌幅'] > 1) &  # 涨幅大于1%
                (filtered_df['RSI'] > 60) &  # RSI大于60
                (filtered_df['量比'] > 1.2)  # 量比大于1.2
            ]

        elif screener_type == "oversold_rebound":
            # 超跌反弹筛选条件
            filtered_df = filtered_df[
                (filtered_df['涨跌幅'] < -3) &  # 跌幅大于3%
                (filtered_df['RSI'] < 40) &  # RSI小于40
                (filtered_df['量比'] > 1.5)  # 量比大于1.5
            ]

        # 按综合评分排序
        if '综合评分' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('综合评分', ascending=False)

        # 限制结果数量
        return filtered_df.head(30)

    except Exception as e:
        logger.error(f"❌ 应用筛选条件失败: {e}")
        return df.head(20)

def generate_mock_stock_data(screener_type: str = "default") -> pd.DataFrame:
    """生成模拟股票数据（备用方案）"""

    np.random.seed(42)  # 确保结果可重现

    # A股股票池
    stock_pool = [
        ("000001", "平安银行"), ("000002", "万科A"), ("000858", "五粮液"),
        ("000876", "新希望"), ("002415", "海康威视"), ("002594", "比亚迪"),
        ("600036", "招商银行"), ("600519", "贵州茅台"), ("600887", "伊利股份"),
        ("601318", "中国平安"), ("601398", "工商银行"), ("601857", "中国石油"),
        ("000063", "中兴通讯"), ("000725", "京东方A"), ("002230", "科大讯飞"),
        ("300059", "东方财富"), ("300750", "宁德时代"), ("688981", "中芯国际")
    ]

    # 根据筛选器类型调整参数
    if screener_type == "momentum_breakout":
        n_stocks = np.random.randint(8, 15)
        price_change_range = (2, 15)
        rsi_range = (50, 80)
    elif screener_type == "value_growth":
        n_stocks = np.random.randint(6, 12)
        price_change_range = (-2, 8)
        rsi_range = (40, 70)
    elif screener_type == "dividend_stable":
        n_stocks = np.random.randint(5, 10)
        price_change_range = (-1, 5)
        rsi_range = (45, 65)
    else:
        n_stocks = np.random.randint(8, 16)
        price_change_range = (-5, 12)
        rsi_range = (25, 75)

    # 随机选择股票
    selected_stocks = np.random.choice(len(stock_pool), n_stocks, replace=False)

    results = []
    for i in selected_stocks:
        code, name = stock_pool[i]

        stock_data = {
            "股票代码": code,
            "股票名称": name,
            "最新价": round(np.random.uniform(15, 200), 2),
            "涨跌幅": round(np.random.uniform(price_change_range[0], price_change_range[1]), 2),
            "成交量": int(np.random.uniform(1000000, 50000000)),
            "成交额": round(np.random.uniform(5, 500), 2),
            "市值": round(np.random.uniform(100, 8000), 2),
            "PE": round(np.random.uniform(8, 45), 2),
            "PB": round(np.random.uniform(0.8, 6), 2),
            "ROE": round(np.random.uniform(5, 30), 2),
            "ROA": round(np.random.uniform(2, 15), 2),
            "RSI": round(np.random.uniform(rsi_range[0], rsi_range[1]), 1),
            "MACD": round(np.random.uniform(-2, 3), 3),
            "KDJ_K": round(np.random.uniform(20, 90), 1),
            "换手率": round(np.random.uniform(0.5, 15), 2),
            "量比": round(np.random.uniform(0.5, 5), 2),
            "综合评分": round(np.random.uniform(60, 95), 1)
        }
        results.append(stock_data)

    df = pd.DataFrame(results)
    return df.sort_values("综合评分", ascending=False)

def render_header():
    """渲染页面头部"""

    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #2E86AB; margin-bottom: 10px;">🔍 A股智能筛选器</h1>
        <p style="color: #666; font-size: 18px; margin: 0;">
            专业的中国A股股票筛选工具 | 实时数据分析 | 快速发现投资机会
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 显示数据状态
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if 'data_source' in st.session_state and 'update_time' in st.session_state:
            data_source = st.session_state['data_source']
            update_time = st.session_state['update_time']

            # 根据数据源显示不同颜色
            if data_source == "实时数据":
                st.success(f"📡 {data_source} | 更新时间: {update_time}")
            else:
                st.info(f"🔄 {data_source} | 更新时间: {update_time}")
        else:
            st.info("💡 选择筛选策略开始分析")

    st.markdown("---")

def render_preset_screeners():
    """渲染预设筛选器"""
    
    st.header("🎯 预设筛选策略")
    st.markdown("选择适合您投资风格的预设筛选器，一键筛选优质股票")
    
    # 创建两列布局
    col1, col2 = st.columns(2)
    
    screener_items = list(SCREENER_CONFIGS.items())
    
    for i, (key, config) in enumerate(screener_items):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            with st.container():
                # 筛选器卡片
                st.markdown(f"""
                <div style="
                    border: 2px solid {config['color']};
                    border-radius: 15px;
                    padding: 20px;
                    margin: 15px 0;
                    background: linear-gradient(135deg, {config['color']}15, transparent);
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                ">
                    <h4 style="color: {config['color']}; margin: 0 0 10px 0;">{config['name']}</h4>
                    <p style="margin: 10px 0; color: #555; line-height: 1.4;">{config['description']}</p>
                    <p style="margin: 10px 0; color: #777; font-size: 14px; font-style: italic;">
                        筛选条件: {config['criteria']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🚀 启动筛选", key=f"btn_{key}", use_container_width=True):
                    run_screener(key, config)

def render_custom_screener():
    """渲染自定义筛选器"""
    
    st.header("⚙️ 自定义筛选条件")
    st.markdown("根据您的具体需求设置个性化筛选条件")
    
    with st.form("custom_screener_form"):
        # 基本面指标
        st.subheader("📊 基本面指标")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            market_cap_range = st.slider("市值范围 (亿元)", 0, 10000, (50, 2000), 50)
            pe_range = st.slider("PE比率范围", 0.0, 100.0, (5.0, 30.0), 0.5)
        
        with col2:
            pb_range = st.slider("PB比率范围", 0.0, 10.0, (0.5, 5.0), 0.1)
            roe_min = st.number_input("ROE最低要求 (%)", 0.0, 50.0, 10.0, 0.5)
        
        with col3:
            revenue_growth_min = st.number_input("营收增长率最低 (%)", -50.0, 100.0, 5.0, 1.0)
            profit_growth_min = st.number_input("净利润增长率最低 (%)", -50.0, 100.0, 10.0, 1.0)
        
        # 技术面指标
        st.subheader("📈 技术面指标")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rsi_range = st.slider("RSI范围", 0, 100, (30, 70), 1)
            price_change_range = st.slider("近期涨跌幅范围 (%)", -50, 50, (-10, 20), 1)
        
        with col2:
            volume_ratio_min = st.number_input("量比最低要求", 0.1, 10.0, 1.0, 0.1)
            turnover_range = st.slider("换手率范围 (%)", 0.0, 20.0, (1.0, 10.0), 0.1)
        
        with col3:
            ma_trend = st.selectbox("均线趋势", ["不限", "多头排列", "空头排列", "震荡"], 0)
            macd_signal = st.selectbox("MACD信号", ["不限", "金叉", "死叉", "零轴上方", "零轴下方"], 0)
        
        # 行业和概念
        st.subheader("🏭 行业筛选")
        industries = st.multiselect(
            "选择行业 (可多选)",
            ["银行", "保险", "证券", "房地产", "医药生物", "食品饮料", "电子", "计算机", 
             "通信", "汽车", "化工", "机械设备", "电力设备", "有色金属", "钢铁"],
            default=[]
        )
        
        # 提交按钮
        submitted = st.form_submit_button("🔍 开始自定义筛选", use_container_width=True)

    # 在表单外处理提交
    if submitted:
        custom_criteria = {
            "market_cap_range": market_cap_range,
            "pe_range": pe_range,
            "pb_range": pb_range,
            "roe_min": roe_min,
            "revenue_growth_min": revenue_growth_min,
            "profit_growth_min": profit_growth_min,
            "rsi_range": rsi_range,
            "price_change_range": price_change_range,
            "volume_ratio_min": volume_ratio_min,
            "turnover_range": turnover_range,
            "ma_trend": ma_trend,
            "macd_signal": macd_signal,
            "industries": industries
        }
        run_custom_screener(custom_criteria)

def run_screener(screener_key: str, config: dict):
    """运行预设筛选器"""

    with st.spinner(f"正在运行 {config['name']}..."):
        # 显示进度
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 步骤1: 获取实时股票数据
        status_text.text("📡 获取A股实时行情数据...")
        progress_bar.progress(20)

        # 获取真实数据
        results = get_real_stock_data(screener_key, use_real_data=True)

        if results.empty:
            status_text.text("⚠️ 实时数据获取失败，使用模拟数据...")
            progress_bar.progress(40)
            results = get_real_stock_data(screener_key, use_real_data=False)
        else:
            progress_bar.progress(60)

        # 步骤2: 应用筛选条件
        status_text.text("🔍 应用筛选条件...")
        progress_bar.progress(80)
        time.sleep(0.5)

        # 步骤3: 完成筛选
        status_text.text("✅ 筛选完成...")
        progress_bar.progress(100)
        time.sleep(0.3)

        # 保存到session state
        st.session_state.screening_results = results
        st.session_state.last_screener = config['name']
        st.session_state.screener_type = screener_key
        st.session_state.data_source = "实时数据" if not results.empty else "模拟数据"
        st.session_state.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 清除进度显示
        progress_bar.empty()
        status_text.empty()

        if not results.empty:
            st.success(f"✅ {config['name']} 筛选完成！找到 {len(results)} 只符合条件的股票")

            # 显示数据来源信息
            data_source = st.session_state.get('data_source', '未知')
            update_time = st.session_state.get('update_time', '未知')
            st.info(f"📊 数据来源: {data_source} | 更新时间: {update_time}")

            # 显示结果预览
            display_results_preview(results)
        else:
            st.warning("😔 未找到符合条件的股票，请尝试其他筛选策略")

def run_custom_screener(criteria: dict):
    """运行自定义筛选器"""

    with st.spinner("正在执行自定义筛选..."):
        # 显示筛选条件
        conditions_text = format_criteria(criteria)
        st.info(f"📋 筛选条件: {conditions_text}")

        # 显示进度
        progress_bar = st.progress(0)
        status_text = st.empty()

        # 步骤1: 获取实时数据
        status_text.text("📡 获取A股实时数据...")
        progress_bar.progress(30)

        try:
            # 获取真实数据
            data_fetcher = get_real_data_fetcher()
            df = data_fetcher.get_stock_realtime_data(limit=300)

            if df.empty:
                status_text.text("⚠️ 使用模拟数据...")
                df = generate_mock_stock_data("custom")
                data_source = "模拟数据"
            else:
                df = data_fetcher.calculate_technical_indicators(df)
                data_source = "实时数据"

            progress_bar.progress(60)

            # 步骤2: 应用自定义筛选条件
            status_text.text("🔍 应用自定义筛选条件...")
            results = apply_custom_criteria(df, criteria)
            progress_bar.progress(90)

            # 步骤3: 完成
            status_text.text("✅ 筛选完成...")
            progress_bar.progress(100)
            time.sleep(0.3)

        except Exception as e:
            logger.error(f"❌ 自定义筛选失败: {e}")
            results = generate_mock_stock_data("custom")
            data_source = "模拟数据"

        # 保存结果
        st.session_state.screening_results = results
        st.session_state.last_screener = "自定义筛选器"
        st.session_state.screener_type = "custom"
        st.session_state.data_source = data_source
        st.session_state.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 清除进度显示
        progress_bar.empty()
        status_text.empty()

        if not results.empty:
            st.success(f"✅ 自定义筛选完成！找到 {len(results)} 只符合条件的股票")

            # 显示数据来源
            update_time = st.session_state.get('update_time', '未知')
            st.info(f"📊 数据来源: {data_source} | 更新时间: {update_time}")

            # 显示结果预览
            display_results_preview(results)
        else:
            st.warning("😔 未找到符合条件的股票，请尝试调整筛选条件")

def apply_custom_criteria(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """应用自定义筛选条件"""

    if df.empty:
        return df

    try:
        filtered_df = df.copy()

        # 市值范围筛选
        if criteria.get("market_cap_range"):
            min_cap, max_cap = criteria["market_cap_range"]
            if '市值' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['市值'] >= min_cap) &
                    (filtered_df['市值'] <= max_cap)
                ]

        # PE范围筛选
        if criteria.get("pe_range"):
            min_pe, max_pe = criteria["pe_range"]
            if 'PE' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['PE'] >= min_pe) &
                    (filtered_df['PE'] <= max_pe) &
                    (filtered_df['PE'] > 0)
                ]

        # PB范围筛选
        if criteria.get("pb_range"):
            min_pb, max_pb = criteria["pb_range"]
            if 'PB' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['PB'] >= min_pb) &
                    (filtered_df['PB'] <= max_pb) &
                    (filtered_df['PB'] > 0)
                ]

        # RSI范围筛选
        if criteria.get("rsi_range"):
            min_rsi, max_rsi = criteria["rsi_range"]
            if 'RSI' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['RSI'] >= min_rsi) &
                    (filtered_df['RSI'] <= max_rsi)
                ]

        # 涨跌幅范围筛选
        if criteria.get("price_change_range"):
            min_change, max_change = criteria["price_change_range"]
            if '涨跌幅' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['涨跌幅'] >= min_change) &
                    (filtered_df['涨跌幅'] <= max_change)
                ]

        # 量比筛选
        if criteria.get("volume_ratio_min"):
            min_ratio = criteria["volume_ratio_min"]
            if '量比' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['量比'] >= min_ratio]

        # 换手率范围筛选
        if criteria.get("turnover_range"):
            min_turnover, max_turnover = criteria["turnover_range"]
            if '换手率' in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df['换手率'] >= min_turnover) &
                    (filtered_df['换手率'] <= max_turnover)
                ]

        # 按综合评分排序
        if '综合评分' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('综合评分', ascending=False)

        return filtered_df.head(30)  # 限制结果数量

    except Exception as e:
        logger.error(f"❌ 应用自定义条件失败: {e}")
        return df.head(20)

def display_results_preview(results: pd.DataFrame):
    """显示结果预览"""

    if results.empty:
        st.warning("未找到符合条件的股票")
        return

    st.subheader("📊 筛选结果预览")

    # 统计信息
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("筛选出股票数", len(results))

    with col2:
        if '综合评分' in results.columns:
            avg_score = results['综合评分'].mean()
            st.metric("平均综合评分", f"{avg_score:.1f}")
        else:
            st.metric("平均综合评分", "N/A")

    with col3:
        if '涨跌幅' in results.columns:
            avg_change = results['涨跌幅'].mean()
            st.metric("平均涨跌幅", f"{avg_change:+.2f}%")
        else:
            st.metric("平均涨跌幅", "N/A")

    with col4:
        if 'PE' in results.columns:
            avg_pe = results['PE'].mean()
            st.metric("平均PE", f"{avg_pe:.1f}")
        else:
            st.metric("平均PE", "N/A")

    # 显示前10只股票
    st.markdown("**TOP 10 股票:**")

    # 动态选择可用的列
    base_cols = ['股票代码', '股票名称']
    optional_cols = ['最新价', '涨跌幅', '市值', 'PE', 'PB', 'ROE', '换手率', '量比', 'RSI', '综合评分']

    # 只选择存在的列
    display_cols = []
    for col in base_cols + optional_cols:
        if col in results.columns:
            display_cols.append(col)

    # 确保至少有基础列
    if not display_cols:
        display_cols = list(results.columns[:6])  # 取前6列作为默认显示

    # 格式化显示
    preview_data = results.head(10)[display_cols].copy()

    # 安全的格式化函数
    def safe_format_percent(x):
        try:
            return f"{float(x):+.2f}%" if pd.notna(x) else "N/A"
        except:
            return "N/A"

    def safe_format_number(x, suffix=""):
        try:
            return f"{float(x):.0f}{suffix}" if pd.notna(x) else "N/A"
        except:
            return "N/A"

    # 格式化各列
    if '涨跌幅' in preview_data.columns:
        preview_data['涨跌幅'] = preview_data['涨跌幅'].apply(safe_format_percent)

    if '市值' in preview_data.columns:
        preview_data['市值'] = preview_data['市值'].apply(lambda x: safe_format_number(x, "亿"))

    if '换手率' in preview_data.columns:
        preview_data['换手率'] = preview_data['换手率'].apply(lambda x: safe_format_number(x, "%"))

    # 添加点击功能的表格
    st.markdown("**点击股票名称查看详细分析:**")

    # 创建可点击的股票列表
    for idx, row in preview_data.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1.5, 1.5, 1, 1, 1, 1.5])

        with col1:
            # 股票代码和名称按钮
            if st.button(f"{row['股票代码']}", key=f"stock_{idx}", use_container_width=True):
                st.session_state.show_stock_detail = True
                st.session_state.current_stock = {
                    'code': row['股票代码'],
                    'name': row['股票名称']
                }
                st.rerun()

        with col2:
            st.write(row['股票名称'])

        with col3:
            if '最新价' in row:
                st.write(f"¥{row['最新价']}")

        with col4:
            if '涨跌幅' in row:
                st.write(row['涨跌幅'])

        with col5:
            if '综合评分' in row:
                st.write(f"{row['综合评分']}")

        with col6:
            # AI分析按钮
            if st.button("🤖 AI分析", key=f"ai_analysis_{idx}", use_container_width=True):
                # 设置选中的股票进行AI分析
                st.session_state.analysis_stock_code = row['股票代码']
                st.session_state.analysis_stock_name = row['股票名称']
                st.session_state.analysis_stock_data = row.to_dict()

                # 显示分析启动信息
                st.success(f"🚀 正在为 {row['股票代码']} - {row['股票名称']} 启动AI分析...")

                # 创建分析预览
                with st.expander(f"📊 {row['股票代码']} AI分析预览", expanded=True):
                    analysis_col1, analysis_col2 = st.columns(2)

                    with analysis_col1:
                        st.write("**基本信息**")
                        st.write(f"股票代码: {row['股票代码']}")
                        st.write(f"股票名称: {row['股票名称']}")
                        if '最新价' in row:
                            st.write(f"最新价: {row['最新价']}")
                        if '涨跌幅' in row:
                            st.write(f"涨跌幅: {row['涨跌幅']}")

                    with analysis_col2:
                        st.write("**AI分析选项**")
                        analysis_options = st.multiselect(
                            "选择分析类型",
                            ["技术面分析", "基本面分析", "风险评估", "投资建议"],
                            default=["技术面分析", "投资建议"],
                            key=f"analysis_options_{idx}"
                        )

                    # 快速分析按钮
                    if st.button(f"🚀 开始完整AI分析", key=f"full_analysis_{idx}", use_container_width=True):
                        st.session_state.selected_analysis_options = analysis_options
                        st.session_state.show_ai_analysis = True
                        st.info("💡 AI分析功能已准备就绪！请在AI分析页面查看详细结果。")

                        # 这里可以添加跳转到分析页面的逻辑
                        # 或者直接在当前页面显示分析结果

    st.markdown("---")

    # 查看详细结果按钮
    if st.button("📈 查看详细分析结果", use_container_width=True):
        st.session_state.show_detailed_results = True
        st.rerun()

def format_criteria(criteria: dict) -> str:
    """格式化筛选条件"""
    
    conditions = []
    
    if criteria.get("market_cap_range"):
        min_cap, max_cap = criteria["market_cap_range"]
        conditions.append(f"市值{min_cap}-{max_cap}亿")
    
    if criteria.get("pe_range"):
        min_pe, max_pe = criteria["pe_range"]
        conditions.append(f"PE{min_pe}-{max_pe}")
    
    if criteria.get("roe_min"):
        conditions.append(f"ROE≥{criteria['roe_min']}%")
    
    if criteria.get("industries"):
        conditions.append(f"行业:{','.join(criteria['industries'])}")
    
    return " | ".join(conditions) if conditions else "无特殊限制"

def render_detailed_results():
    """渲染详细结果页面"""

    if 'screening_results' not in st.session_state:
        st.info("🔍 请先运行筛选器以查看结果")
        return

    results = st.session_state.screening_results
    screener_name = st.session_state.get('last_screener', '股票筛选器')

    st.header(f"📊 {screener_name} - 详细结果")

    if results.empty:
        st.warning("😔 未找到符合条件的股票")
        return

    # 结果统计
    render_results_statistics(results)

    # 结果表格
    render_results_table(results)

    # 可视化图表
    render_results_charts(results)

    # 操作按钮
    render_action_buttons(results)

def render_results_statistics(results: pd.DataFrame):
    """渲染结果统计信息"""

    st.subheader("📈 统计概览")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("筛选股票数", len(results))

    with col2:
        if '综合评分' in results.columns:
            avg_score = results['综合评分'].mean()
            st.metric("平均评分", f"{avg_score:.1f}")
        else:
            st.metric("平均评分", "N/A")

    with col3:
        if '涨跌幅' in results.columns:
            avg_change = results['涨跌幅'].mean()
            st.metric("平均涨跌幅", f"{avg_change:+.2f}%")
        else:
            st.metric("平均涨跌幅", "N/A")

    with col4:
        if 'PE' in results.columns:
            avg_pe = results['PE'].mean()
            st.metric("平均PE", f"{avg_pe:.1f}")
        else:
            st.metric("平均PE", "N/A")

    with col5:
        if 'ROE' in results.columns:
            avg_roe = results['ROE'].mean()
            st.metric("平均ROE", f"{avg_roe:.1f}%")
        else:
            st.metric("平均ROE", "N/A")

def render_results_table(results: pd.DataFrame):
    """渲染结果表格"""

    st.subheader("📋 详细列表")

    # 排序选项
    col1, col2 = st.columns([1, 3])

    # 获取可用的排序列
    available_sort_cols = []
    potential_cols = ["综合评分", "涨跌幅", "成交量", "市值", "PE", "ROE", "RSI", "换手率", "量比"]
    for col in potential_cols:
        if col in results.columns:
            available_sort_cols.append(col)

    if not available_sort_cols:
        available_sort_cols = ["股票名称"]  # 默认选项

    with col1:
        sort_by = st.selectbox(
            "排序方式",
            available_sort_cols,
            index=0
        )

    with col2:
        ascending = st.checkbox("升序排列", value=False)

    # 排序数据
    if sort_by in results.columns:
        sorted_results = results.sort_values(sort_by, ascending=ascending)
    else:
        # 如果选择的列不存在，使用第一个可用的数值列
        numeric_cols = results.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            sorted_results = results.sort_values(numeric_cols[0], ascending=ascending)
        else:
            sorted_results = results

    # 安全的格式化函数
    def safe_format(x, format_type="default"):
        try:
            if pd.isna(x):
                return "N/A"
            if format_type == "percent":
                return f"{float(x):+.2f}%"
            elif format_type == "money":
                return f"{float(x):.0f}亿"
            elif format_type == "money_decimal":
                return f"{float(x):.1f}亿"
            elif format_type == "volume":
                return f"{float(x)/10000:.0f}万手"
            elif format_type == "percent_simple":
                return f"{float(x):.2f}%"
            else:
                return str(x)
        except:
            return "N/A"

    # 格式化显示数据
    display_data = sorted_results.copy()

    # 安全地格式化各列
    if '涨跌幅' in display_data.columns:
        display_data['涨跌幅'] = display_data['涨跌幅'].apply(lambda x: safe_format(x, "percent"))

    if '市值' in display_data.columns:
        display_data['市值'] = display_data['市值'].apply(lambda x: safe_format(x, "money"))

    if '成交额' in display_data.columns:
        display_data['成交额'] = display_data['成交额'].apply(lambda x: safe_format(x, "money_decimal"))

    if '成交量' in display_data.columns:
        display_data['成交量'] = display_data['成交量'].apply(lambda x: safe_format(x, "volume"))

    if '换手率' in display_data.columns:
        display_data['换手率'] = display_data['换手率'].apply(lambda x: safe_format(x, "percent_simple"))

    # 显示表格
    st.dataframe(
        display_data,
        use_container_width=True,
        height=400,
        hide_index=True
    )

def render_results_charts(results: pd.DataFrame):
    """渲染可视化图表"""

    st.subheader("📊 可视化分析")

    # 创建图表标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📈 评分分布", "💰 估值分析", "📊 技术指标", "🎯 综合对比"])

    with tab1:
        render_score_distribution(results)

    with tab2:
        render_valuation_analysis(results)

    with tab3:
        render_technical_analysis(results)

    with tab4:
        render_comprehensive_comparison(results)

def render_score_distribution(results: pd.DataFrame):
    """渲染评分分布图"""

    col1, col2 = st.columns(2)

    with col1:
        # 综合评分分布直方图
        fig_hist = px.histogram(
            results,
            x="综合评分",
            nbins=15,
            title="综合评分分布",
            color_discrete_sequence=["#FF6B6B"]
        )
        fig_hist.update_layout(height=350)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        # TOP10股票评分条形图
        top10 = results.nlargest(10, "综合评分")
        fig_bar = px.bar(
            top10,
            x="综合评分",
            y="股票名称",
            orientation="h",
            title="TOP10 综合评分",
            color="综合评分",
            color_continuous_scale="RdYlGn"
        )
        fig_bar.update_layout(height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

def render_valuation_analysis(results: pd.DataFrame):
    """渲染估值分析图"""

    col1, col2 = st.columns(2)

    with col1:
        # PE vs PB散点图
        fig_scatter = px.scatter(
            results,
            x="PE",
            y="PB",
            size="市值",
            color="综合评分",
            hover_name="股票名称",
            title="PE vs PB 估值分析",
            color_continuous_scale="Viridis"
        )
        fig_scatter.update_layout(height=350)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        # ROE vs 涨跌幅关系
        fig_roe = px.scatter(
            results,
            x="ROE",
            y="涨跌幅",
            size="市值",
            color="PE",
            hover_name="股票名称",
            title="ROE vs 涨跌幅关系",
            color_continuous_scale="RdYlBu_r"
        )
        fig_roe.update_layout(height=350)
        st.plotly_chart(fig_roe, use_container_width=True)

def render_technical_analysis(results: pd.DataFrame):
    """渲染技术分析图"""

    col1, col2 = st.columns(2)

    with col1:
        # RSI分布
        fig_rsi = px.histogram(
            results,
            x="RSI",
            nbins=20,
            title="RSI指标分布",
            color_discrete_sequence=["#4ECDC4"]
        )
        fig_rsi.add_vline(x=30, line_dash="dash", line_color="red", annotation_text="超卖线")
        fig_rsi.add_vline(x=70, line_dash="dash", line_color="red", annotation_text="超买线")
        fig_rsi.update_layout(height=350)
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col2:
        # 量比 vs 涨跌幅
        fig_volume = px.scatter(
            results,
            x="量比",
            y="涨跌幅",
            size="换手率",
            color="RSI",
            hover_name="股票名称",
            title="量比 vs 涨跌幅关系",
            color_continuous_scale="Plasma"
        )
        fig_volume.update_layout(height=350)
        st.plotly_chart(fig_volume, use_container_width=True)

def render_comprehensive_comparison(results: pd.DataFrame):
    """渲染综合对比图"""

    # 选择对比股票
    selected_stocks = st.multiselect(
        "选择要对比的股票 (最多5只)",
        options=results['股票名称'].tolist(),
        default=results['股票名称'].head(3).tolist(),
        max_selections=5
    )

    if selected_stocks:
        comparison_data = results[results['股票名称'].isin(selected_stocks)]

        # 雷达图对比
        categories = ['综合评分', 'ROE', 'RSI', '量比', '换手率']

        fig_radar = go.Figure()

        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#F7DC6F']

        for i, (_, stock) in enumerate(comparison_data.iterrows()):
            values = []
            for cat in categories:
                if cat == '综合评分':
                    values.append(stock[cat])
                elif cat == 'ROE':
                    values.append(min(stock[cat] * 3, 100))  # 标准化到0-100
                elif cat == 'RSI':
                    values.append(stock[cat])
                elif cat == '量比':
                    values.append(min(stock[cat] * 20, 100))  # 标准化到0-100
                elif cat == '换手率':
                    values.append(min(stock[cat] * 10, 100))  # 标准化到0-100

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=stock['股票名称'],
                line_color=colors[i % len(colors)]
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="股票综合对比雷达图",
            height=500
        )

        st.plotly_chart(fig_radar, use_container_width=True)

def render_action_buttons(results: pd.DataFrame):
    """渲染操作按钮"""

    st.subheader("🎯 快速操作")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 重新筛选", use_container_width=True):
            st.session_state.show_detailed_results = False
            st.rerun()

    with col2:
        if st.button("📊 导出Excel", use_container_width=True):
            csv = results.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="下载CSV文件",
                data=csv,
                file_name=f"股票筛选结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col3:
        if st.button("📈 AI技术分析", use_container_width=True):
            # 跳转到AI分析页面
            if 'filtered_stocks' in st.session_state and not st.session_state.filtered_stocks.empty:
                # 选择第一只股票进行分析
                first_stock = st.session_state.filtered_stocks.iloc[0]
                stock_code = first_stock['股票代码']

                # 设置分析参数
                st.session_state.analysis_stock_code = stock_code
                st.session_state.analysis_stock_name = first_stock.get('股票名称', stock_code)
                st.session_state.analysis_type = 'technical'

                # 显示跳转信息
                st.success(f"正在为 {stock_code} 准备AI技术分析...")
                st.info("💡 提示：您可以在AI分析页面查看完整的技术分析报告")

                # 可以在这里添加跳转逻辑或者显示分析预览
                with st.expander("🔍 快速技术分析预览", expanded=True):
                    st.write(f"**股票代码**: {stock_code}")
                    st.write(f"**当前价格**: {first_stock.get('当前价格', 'N/A')}")
                    st.write(f"**涨跌幅**: {first_stock.get('涨跌幅', 'N/A')}")
                    st.write("**建议**: 请使用完整AI分析功能获取详细技术分析")

                    if st.button("🚀 进入完整AI分析", use_container_width=True):
                        st.session_state.show_ai_analysis = True
                        st.rerun()
            else:
                st.warning("请先筛选股票后再进行分析")

    with col4:
        if st.button("💰 AI基本面分析", use_container_width=True):
            # 跳转到AI基本面分析
            if 'filtered_stocks' in st.session_state and not st.session_state.filtered_stocks.empty:
                # 选择第一只股票进行分析
                first_stock = st.session_state.filtered_stocks.iloc[0]
                stock_code = first_stock['股票代码']

                # 设置分析参数
                st.session_state.analysis_stock_code = stock_code
                st.session_state.analysis_stock_name = first_stock.get('股票名称', stock_code)
                st.session_state.analysis_type = 'fundamental'

                # 显示跳转信息
                st.success(f"正在为 {stock_code} 准备AI基本面分析...")
                st.info("💡 提示：您可以在AI分析页面查看完整的基本面分析报告")

                # 基本面分析预览
                with st.expander("🔍 快速基本面分析预览", expanded=True):
                    st.write(f"**股票代码**: {stock_code}")
                    st.write(f"**PE比率**: {first_stock.get('PE比率', 'N/A')}")
                    st.write(f"**ROE**: {first_stock.get('ROE', 'N/A')}")
                    st.write(f"**营收增长**: {first_stock.get('营收增长', 'N/A')}")
                    st.write("**建议**: 请使用完整AI分析功能获取详细基本面分析")

                    if st.button("🚀 进入完整AI分析", use_container_width=True):
                        st.session_state.show_ai_analysis = True
                        st.rerun()
            else:
                st.warning("请先筛选股票后再进行分析")

def main():
    """主函数"""

    # 渲染页面头部
    render_header()

    # 检查是否要显示个股详情页面
    if st.session_state.get('show_stock_detail', False):
        current_stock = st.session_state.get('current_stock')
        if current_stock:
            show_stock_detail(current_stock['code'], current_stock['name'])
            return

    # 检查是否要显示详细结果
    if st.session_state.get('show_detailed_results', False):
        render_detailed_results()
        return

    # 创建主要标签页
    tab1, tab2 = st.tabs(["🎯 预设筛选器", "⚙️ 自定义筛选"])

    with tab1:
        render_preset_screeners()

    with tab2:
        render_custom_screener()

    # 侧边栏信息
    with st.sidebar:
        st.markdown("### 📊 筛选器说明")
        st.markdown("""
        **预设筛选器**：
        - 🚀 动量突破：适合短线交易
        - 💎 价值成长：适合中长线投资
        - 🏦 稳健分红：适合稳健投资者
        - 🌱 小盘成长：适合成长投资
        - 📈 技术强势：基于技术指标
        - 🔄 超跌反弹：寻找反弹机会

        **自定义筛选**：
        - 可根据个人需求设置条件
        - 支持基本面和技术面指标
        - 灵活的参数组合
        """)

        st.markdown("---")
        st.markdown("### 💡 使用提示")
        st.markdown("""
        1. 选择适合的筛选策略
        2. 查看筛选结果和评分
        3. **点击股票代码进入详细分析**
        4. 启动多AI协作分析
        5. 导出结果进行深入研究
        """)

        st.markdown("---")
        st.markdown("### 🚀 新功能")
        st.markdown("""
        **个股详细分析**：
        - 📊 基本信息和实时数据
        - 📈 价格走势和K线图
        - 💰 财务数据摘要
        - 🤖 多AI协作分析

        **多AI分析包括**：
        - 🔍 基本面分析AI
        - 📈 技术面分析AI
        - 📰 市场情绪分析AI
        - ⚠️ 风险评估AI
        """)

if __name__ == "__main__":
    main()

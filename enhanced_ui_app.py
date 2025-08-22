"""
增强版用户界面
左侧栏显示所有筛选器，右侧整页显示详细分析数据
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_stock_screener import get_smart_screened_stocks, SmartStockScreener

# 导入短线入场机会筛选器
try:
    from short_term_entry_screener import get_short_term_entry_opportunities, get_all_short_term_strategies
    USE_SHORT_TERM_SCREENER = True
except ImportError:
    USE_SHORT_TERM_SCREENER = False

# 页面配置
st.set_page_config(
    page_title="智能股票筛选器 - 专业版",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .screener-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .signal-badge {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def initialize_screener_options():
    """初始化筛选器选项"""
    # 常规筛选器
    regular_screeners = {
        "momentum_breakout": {
            "name": "🚀 动量突破筛选器",
            "category": "技术分析",
            "description": "寻找突破上涨的强势股票",
            "type": "regular"
        },
        "value_growth": {
            "name": "💎 价值成长筛选器", 
            "category": "基本面分析",
            "description": "寻找低估值高成长的价值股",
            "type": "regular"
        },
        "dividend_stable": {
            "name": "🏦 稳健分红筛选器",
            "category": "收益投资",
            "description": "寻找高股息率的稳健股票",
            "type": "regular"
        },
        "small_cap_growth": {
            "name": "🌱 小盘成长筛选器",
            "category": "成长投资",
            "description": "寻找高成长潜力的小盘股",
            "type": "regular"
        },
        "technical_strong": {
            "name": "📈 技术强势筛选器",
            "category": "技术分析",
            "description": "寻找技术指标强势的股票",
            "type": "regular"
        },
        "oversold_rebound": {
            "name": "🔄 超跌反弹筛选器",
            "category": "反转策略",
            "description": "寻找超跌后反弹的机会",
            "type": "regular"
        }
    }
    
    # 短线入场机会筛选器
    short_term_screeners = {}
    if USE_SHORT_TERM_SCREENER:
        strategies = get_all_short_term_strategies()
        for key, strategy in strategies.items():
            short_term_screeners[key] = {
                "name": strategy["name"],
                "category": "短线交易",
                "description": strategy["description"],
                "type": "short_term"
            }
    
    return regular_screeners, short_term_screeners

def render_sidebar():
    """渲染左侧栏"""
    st.sidebar.markdown("# 📊 智能股票筛选器")
    st.sidebar.markdown("---")
    
    regular_screeners, short_term_screeners = initialize_screener_options()
    
    # 常规筛选器
    st.sidebar.markdown("## 🔍 常规筛选器")
    selected_regular = None
    
    for key, info in regular_screeners.items():
        if st.sidebar.button(
            f"{info['name']}", 
            key=f"regular_{key}",
            help=info['description'],
            use_container_width=True
        ):
            st.session_state['selected_screener'] = key
            st.session_state['screener_type'] = 'regular'
            selected_regular = key
    
    st.sidebar.markdown("---")
    
    # 短线入场机会筛选器
    if USE_SHORT_TERM_SCREENER:
        st.sidebar.markdown("## ⚡ 短线入场机会")
        selected_short_term = None
        
        for key, info in short_term_screeners.items():
            if st.sidebar.button(
                f"{info['name']}", 
                key=f"short_term_{key}",
                help=info['description'],
                use_container_width=True
            ):
                st.session_state['selected_screener'] = key
                st.session_state['screener_type'] = 'short_term'
                selected_short_term = key
    
    st.sidebar.markdown("---")
    
    # 参数设置
    st.sidebar.markdown("## ⚙️ 参数设置")
    num_stocks = st.sidebar.slider("股票数量", 5, 50, 20)
    use_real_data = st.sidebar.checkbox("使用实时数据", value=False)
    
    # 自动刷新
    auto_refresh = st.sidebar.checkbox("自动刷新 (30秒)", value=False)
    if auto_refresh:
        st.rerun()
    
    return num_stocks, use_real_data

def render_screener_details(screener_key, screener_type):
    """渲染筛选器详细信息"""
    regular_screeners, short_term_screeners = initialize_screener_options()
    
    if screener_type == 'regular':
        screener_info = regular_screeners.get(screener_key, {})
        screener = SmartStockScreener()
        if screener_key in screener.screener_logic:
            logic = screener.screener_logic[screener_key]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### {screener_info['name']}")
                st.markdown(f"**类别**: {screener_info['category']}")
                st.markdown(f"**描述**: {screener_info['description']}")
            
            with col2:
                st.markdown("#### 📋 筛选条件")
                for field, condition in logic["filters"].items():
                    if isinstance(condition, tuple):
                        st.write(f"• {field}: {condition[0]} ~ {condition[1]}")
                    else:
                        st.write(f"• {field}: {condition}")
                
                if logic["preferred_industries"]:
                    st.write(f"• 偏好行业: {', '.join(logic['preferred_industries'])}")
    
    elif screener_type == 'short_term':
        screener_info = short_term_screeners.get(screener_key, {})
        if USE_SHORT_TERM_SCREENER:
            strategies = get_all_short_term_strategies()
            if screener_key in strategies:
                strategy = strategies[screener_key]
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"### {screener_info['name']}")
                    st.markdown(f"**类别**: {screener_info['category']}")
                    st.markdown(f"**策略描述**: {screener_info['description']}")
                
                with col2:
                    st.markdown("#### 📋 入场条件")
                    for field, condition in strategy["filters"].items():
                        if isinstance(condition, tuple):
                            st.write(f"• {field}: {condition[0]} ~ {condition[1]}")
                        else:
                            st.write(f"• {field}: {condition}")
                    
                    st.markdown("#### 🎯 入场信号")
                    for signal in strategy["entry_signals"]:
                        st.write(f"• {signal}")

def render_analysis_results(df, screener_type, screener_key):
    """渲染详细分析结果"""
    if df.empty:
        st.warning("⚠️ 没有找到符合条件的股票")
        return
    
    # 关键指标概览
    st.markdown("## 📊 关键指标概览")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("股票数量", len(df))
    
    with col2:
        avg_change = df["涨跌幅"].mean()
        st.metric("平均涨跌幅", f"{avg_change:+.2f}%")
    
    with col3:
        positive_count = (df["涨跌幅"] > 0).sum()
        st.metric("上涨股票", f"{positive_count}/{len(df)}")
    
    with col4:
        if "市盈率" in df.columns:
            avg_pe = df["市盈率"].mean()
            st.metric("平均市盈率", f"{avg_pe:.1f}")
        elif "入场评分" in df.columns:
            avg_score = df["入场评分"].mean()
            st.metric("平均入场评分", f"{avg_score:.1f}")
    
    with col5:
        if not df["行业"].empty:
            top_industry = df["行业"].value_counts().index[0]
            industry_count = df["行业"].value_counts().iloc[0]
            st.metric("主要行业", f"{top_industry}")
            st.caption(f"{industry_count}只股票")
    
    # 详细数据表格
    st.markdown("## 📋 详细筛选结果")
    
    # 根据筛选器类型选择显示列
    if screener_type == 'short_term' and "入场评分" in df.columns:
        display_columns = [
            "股票代码", "股票名称", "最新价", "涨跌幅", "入场评分", 
            "入场信号", "行业", "成交量", "市盈率"
        ]
    else:
        display_columns = [
            "股票代码", "股票名称", "最新价", "涨跌幅", "涨跌额", 
            "成交量", "市盈率", "市净率", "ROE", "行业"
        ]
    
    # 确保列存在
    available_columns = [col for col in display_columns if col in df.columns]
    display_df = df[available_columns].copy()
    
    # 格式化显示
    if "最新价" in display_df.columns:
        display_df["最新价"] = display_df["最新价"].apply(lambda x: f"¥{x:.2f}")
    if "涨跌幅" in display_df.columns:
        display_df["涨跌幅"] = display_df["涨跌幅"].apply(lambda x: f"{x:+.2f}%")
    if "涨跌额" in display_df.columns:
        display_df["涨跌额"] = display_df["涨跌额"].apply(lambda x: f"{x:+.2f}")
    
    st.dataframe(
        display_df,
        use_container_width=True,
        height=400
    )
    
    # 可视化分析
    st.markdown("## 📈 可视化分析")
    
    # 创建图表
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # 涨跌幅分布
        fig_hist = px.histogram(
            df, 
            x="涨跌幅", 
            title="涨跌幅分布",
            nbins=15,
            color_discrete_sequence=["#1f77b4"]
        )
        fig_hist.update_layout(height=350)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with chart_col2:
        # 行业分布
        industry_counts = df["行业"].value_counts().head(8)
        fig_pie = px.pie(
            values=industry_counts.values,
            names=industry_counts.index,
            title="行业分布"
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # 散点图分析
    if len(df) > 1:
        st.markdown("### 📊 多维度分析")
        
        scatter_col1, scatter_col2 = st.columns(2)
        
        with scatter_col1:
            # 涨跌幅 vs 成交量比
            if "成交量比" in df.columns:
                fig_scatter1 = px.scatter(
                    df, 
                    x="成交量比", 
                    y="涨跌幅",
                    color="行业",
                    size="市盈率" if "市盈率" in df.columns else None,
                    hover_data=["股票代码", "股票名称"],
                    title="涨跌幅 vs 成交量比"
                )
                fig_scatter1.update_layout(height=350)
                st.plotly_chart(fig_scatter1, use_container_width=True)
        
        with scatter_col2:
            # 市盈率 vs ROE
            if "市盈率" in df.columns and "ROE" in df.columns:
                fig_scatter2 = px.scatter(
                    df, 
                    x="市盈率", 
                    y="ROE",
                    color="涨跌幅",
                    size="成交量",
                    hover_data=["股票代码", "股票名称"],
                    title="市盈率 vs ROE",
                    color_continuous_scale="RdYlGn"
                )
                fig_scatter2.update_layout(height=350)
                st.plotly_chart(fig_scatter2, use_container_width=True)
    
    # 短线入场机会特殊分析
    if screener_type == 'short_term' and "入场评分" in df.columns:
        st.markdown("### ⚡ 短线入场机会分析")
        
        entry_col1, entry_col2 = st.columns(2)
        
        with entry_col1:
            # 入场评分分布
            fig_score = px.histogram(
                df, 
                x="入场评分", 
                title="入场评分分布",
                nbins=10,
                color_discrete_sequence=["#ff7f0e"]
            )
            fig_score.update_layout(height=300)
            st.plotly_chart(fig_score, use_container_width=True)
        
        with entry_col2:
            # 评分 vs 涨跌幅
            fig_score_change = px.scatter(
                df, 
                x="入场评分", 
                y="涨跌幅",
                color="行业",
                hover_data=["股票代码", "股票名称"],
                title="入场评分 vs 涨跌幅"
            )
            fig_score_change.update_layout(height=300)
            st.plotly_chart(fig_score_change, use_container_width=True)
        
        # 入场信号分析
        if "入场信号" in df.columns:
            st.markdown("#### 🎯 入场信号统计")
            
            # 统计所有入场信号
            all_signals = []
            for signals in df["入场信号"]:
                if pd.notna(signals):
                    all_signals.extend(signals.split(" | "))
            
            if all_signals:
                signal_counts = pd.Series(all_signals).value_counts().head(10)
                
                fig_signals = px.bar(
                    x=signal_counts.values,
                    y=signal_counts.index,
                    orientation='h',
                    title="入场信号频次统计",
                    color_discrete_sequence=["#2ca02c"]
                )
                fig_signals.update_layout(height=400)
                st.plotly_chart(fig_signals, use_container_width=True)
    
    # 数据导出
    st.markdown("## 💾 数据导出")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载完整数据 (CSV)",
            data=csv,
            file_name=f"筛选结果_{screener_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with export_col2:
        # 生成分析报告
        report = generate_analysis_report(df, screener_type, screener_key)
        st.download_button(
            label="📄 下载分析报告 (TXT)",
            data=report,
            file_name=f"分析报告_{screener_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

def generate_analysis_report(df, screener_type, screener_key):
    """生成分析报告"""
    report = f"""
智能股票筛选器分析报告
========================

筛选器: {screener_key}
筛选类型: {screener_type}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

基本统计
--------
股票数量: {len(df)}
平均涨跌幅: {df['涨跌幅'].mean():+.2f}%
上涨股票: {(df['涨跌幅'] > 0).sum()}/{len(df)}
主要行业: {df['行业'].value_counts().index[0] if not df['行业'].empty else 'N/A'}

详细结果
--------
"""
    
    for _, row in df.head(10).iterrows():
        report += f"{row['股票代码']} {row['股票名称']}: ¥{row['最新价']:.2f} ({row['涨跌幅']:+.2f}%) [{row['行业']}]\n"
    
    if screener_type == 'short_term' and "入场评分" in df.columns:
        report += f"\n入场机会分析\n"
        report += f"平均入场评分: {df['入场评分'].mean():.1f}/100\n"
        report += f"高评分股票(>80分): {len(df[df['入场评分'] > 80])}/{len(df)}\n"
    
    report += f"\n报告结束\n"
    
    return report

def main():
    """主应用"""
    
    # 渲染左侧栏
    num_stocks, use_real_data = render_sidebar()
    
    # 主内容区域
    st.markdown('<div class="main-header">🧠 智能股票筛选器 - 专业版</div>', unsafe_allow_html=True)
    
    # 检查是否选择了筛选器
    if 'selected_screener' not in st.session_state:
        st.markdown("## 👈 请从左侧选择一个筛选器开始分析")
        
        # 显示功能介绍
        st.markdown("### 🎯 功能特色")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("""
            **🔍 常规筛选器**
            - 动量突破筛选器
            - 价值成长筛选器  
            - 稳健分红筛选器
            - 小盘成长筛选器
            - 技术强势筛选器
            - 超跌反弹筛选器
            """)
        
        with feature_col2:
            st.markdown("""
            **⚡ 短线入场机会**
            - 动量突破入场
            - 缺口突破入场
            - 相对强度入场
            - 窄幅整理突破
            - 早盘强势入场
            - 技术形态突破
            """)
        
        return
    
    # 获取选择的筛选器信息
    selected_screener = st.session_state['selected_screener']
    screener_type = st.session_state.get('screener_type', 'regular')
    
    # 显示筛选器详细信息
    render_screener_details(selected_screener, screener_type)
    
    st.markdown("---")
    
    # 执行筛选按钮
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔍 开始筛选", type="primary", use_container_width=True):
            st.session_state['run_screening'] = True
    
    with col2:
        if st.button("🔄 重新筛选", use_container_width=True):
            st.session_state['run_screening'] = True
            st.rerun()
    
    # 执行筛选
    if st.session_state.get('run_screening', False):
        
        with st.spinner(f"🧠 正在执行智能筛选..."):
            try:
                # 根据筛选器类型获取结果
                if screener_type == 'short_term' and USE_SHORT_TERM_SCREENER:
                    df = get_short_term_entry_opportunities(
                        selected_screener,
                        num_stocks=num_stocks
                    )
                else:
                    df = get_smart_screened_stocks(
                        selected_screener, 
                        num_stocks=num_stocks, 
                        use_real_data=use_real_data
                    )
                
                if not df.empty:
                    st.success(f"✅ 筛选完成！找到 {len(df)} 只符合条件的股票")
                    
                    # 渲染详细分析结果
                    render_analysis_results(df, screener_type, selected_screener)
                    
                else:
                    st.warning("⚠️ 没有找到符合条件的股票，请尝试调整筛选参数")
                    
            except Exception as e:
                st.error(f"❌ 筛选过程中出现错误: {e}")
                st.exception(e)
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    **📞 联系方式:** 微信: jyzhao77 | Email: 577745211@qq.com
    
    **🔧 技术说明:** 基于GitHub优秀项目研究，结合中国A股市场特点开发的智能股票筛选系统
    """)

if __name__ == "__main__":
    main()

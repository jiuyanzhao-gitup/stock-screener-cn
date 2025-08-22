"""
本地测试应用
用于测试智能股票筛选器的本地Streamlit应用
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_stock_screener import get_smart_screened_stocks, SmartStockScreener

# 页面配置
st.set_page_config(
    page_title="智能股票筛选器 - 本地测试",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """主应用"""
    
    st.title("🧠 智能股票筛选器 - 本地测试")
    st.markdown("---")
    
    # 主界面筛选器选择（更明显）
    st.header("📊 选择筛选器")

    # 筛选器选择
    screener_options = {
        "momentum_breakout": "🚀 动量突破筛选器",
        "value_growth": "💎 价值成长筛选器",
        "dividend_stable": "🏦 稳健分红筛选器",
        "small_cap_growth": "🌱 小盘成长筛选器",
        "technical_strong": "📈 技术强势筛选器",
        "oversold_rebound": "🔄 超跌反弹筛选器"
    }

    # 使用列布局显示筛选器选择
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_screener = st.selectbox(
            "请选择要测试的筛选器:",
            options=list(screener_options.keys()),
            format_func=lambda x: screener_options[x],
            index=0
        )

    with col2:
        st.write("") # 空行
        st.write("") # 空行
        if st.button("🔍 开始筛选", type="primary"):
            st.session_state['run_screening'] = True

    # 侧边栏配置
    st.sidebar.header("⚙️ 筛选参数")
    
    # 股票数量
    num_stocks = st.sidebar.slider("股票数量", 5, 50, 20)

    # 数据源选择
    use_real_data = st.sidebar.checkbox("使用实时数据", value=False, help="勾选使用实时数据，不勾选使用模拟数据")
    
    # 显示筛选器详情
    screener = SmartStockScreener()
    if selected_screener in screener.screener_logic:
        logic = screener.screener_logic[selected_screener]
        
        st.sidebar.markdown("### 📋 筛选标准")
        st.sidebar.markdown(f"**{logic['name']}**")
        
        # 显示筛选条件
        for field, condition in logic["filters"].items():
            if isinstance(condition, tuple):
                st.sidebar.write(f"• {field}: {condition[0]} - {condition[1]}")
            else:
                st.sidebar.write(f"• {field}: {condition}")
        
        # 显示行业偏好
        if logic["preferred_industries"]:
            st.sidebar.write(f"• 偏好行业: {', '.join(logic['preferred_industries'])}")
        
        if logic["exclude_industries"]:
            st.sidebar.write(f"• 排除行业: {', '.join(logic['exclude_industries'])}")
    
    # 显示当前选择的筛选器
    st.markdown(f"### 当前选择: {screener_options[selected_screener]}")
    st.markdown("---")
    
    # 执行筛选
    if st.session_state.get('run_screening', False):
        
        with st.spinner("🧠 正在执行智能筛选..."):
            try:
                # 获取筛选结果
                df = get_smart_screened_stocks(
                    selected_screener, 
                    num_stocks=num_stocks, 
                    use_real_data=use_real_data
                )
                
                if not df.empty:
                    st.success(f"✅ 筛选完成！找到 {len(df)} 只符合条件的股票")
                    
                    # 显示筛选结果统计
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_change = df["涨跌幅"].mean()
                        st.metric("平均涨跌幅", f"{avg_change:+.2f}%")
                    
                    with col2:
                        positive_count = (df["涨跌幅"] > 0).sum()
                        st.metric("上涨股票", f"{positive_count}/{len(df)}")
                    
                    with col3:
                        top_industry = df["行业"].value_counts().index[0]
                        industry_count = df["行业"].value_counts().iloc[0]
                        st.metric("主要行业", f"{top_industry} ({industry_count}只)")
                    
                    with col4:
                        avg_pe = df["市盈率"].mean()
                        st.metric("平均市盈率", f"{avg_pe:.1f}")
                    
                    # 筛选条件验证
                    st.markdown("### 🔍 筛选条件验证")
                    
                    if selected_screener in screener.screener_logic:
                        logic = screener.screener_logic[selected_screener]
                        
                        verification_cols = st.columns(3)
                        
                        with verification_cols[0]:
                            st.markdown("**数值条件验证:**")
                            for field, condition in logic["filters"].items():
                                if isinstance(condition, tuple) and field in df.columns:
                                    min_val, max_val = condition
                                    valid_count = df[(df[field] >= min_val) & (df[field] <= max_val)].shape[0]
                                    total_count = len(df)
                                    compliance_rate = valid_count / total_count * 100
                                    
                                    status = "✅" if compliance_rate >= 90 else "⚠️" if compliance_rate >= 70 else "❌"
                                    st.write(f"{status} {field}: {valid_count}/{total_count} ({compliance_rate:.1f}%)")
                        
                        with verification_cols[1]:
                            st.markdown("**行业分布:**")
                            industry_dist = df["行业"].value_counts()
                            for industry, count in industry_dist.head(5).items():
                                percentage = count / len(df) * 100
                                st.write(f"• {industry}: {count}只 ({percentage:.1f}%)")
                        
                        with verification_cols[2]:
                            st.markdown("**关键指标范围:**")
                            key_fields = ["涨跌幅", "市盈率", "RSI", "成交量比"]
                            for field in key_fields:
                                if field in df.columns:
                                    min_val = df[field].min()
                                    max_val = df[field].max()
                                    st.write(f"• {field}: {min_val:.2f} ~ {max_val:.2f}")
                    
                    # 详细结果表格
                    st.markdown("### 📊 筛选结果详情")
                    
                    # 选择要显示的列
                    display_columns = [
                        "股票代码", "股票名称", "最新价", "涨跌幅", "涨跌额", 
                        "成交量", "市盈率", "市净率", "ROE", "行业", "数据源"
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
                    
                    # 可视化图表
                    st.markdown("### 📈 数据可视化")
                    
                    chart_col1, chart_col2 = st.columns(2)
                    
                    with chart_col1:
                        # 涨跌幅分布
                        fig_change = px.histogram(
                            df, 
                            x="涨跌幅", 
                            title="涨跌幅分布",
                            nbins=10,
                            color_discrete_sequence=["#1f77b4"]
                        )
                        fig_change.update_layout(height=300)
                        st.plotly_chart(fig_change, use_container_width=True)
                    
                    with chart_col2:
                        # 行业分布
                        industry_counts = df["行业"].value_counts().head(8)
                        fig_industry = px.pie(
                            values=industry_counts.values,
                            names=industry_counts.index,
                            title="行业分布"
                        )
                        fig_industry.update_layout(height=300)
                        st.plotly_chart(fig_industry, use_container_width=True)
                    
                    # 下载数据
                    st.markdown("### 💾 导出数据")
                    csv = df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 下载筛选结果 (CSV)",
                        data=csv,
                        file_name=f"{screener_options[selected_screener]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                else:
                    st.warning("⚠️ 没有找到符合条件的股票，请尝试调整筛选条件")
                    
            except Exception as e:
                st.error(f"❌ 筛选过程中出现错误: {e}")
                st.exception(e)
    
    # 页脚信息
    st.markdown("---")
    st.markdown("""
    **📞 联系方式:**
    - 微信: jyzhao77
    - Email: 577745211@qq.com
    
    **🔧 技术说明:**
    - 本应用使用智能筛选算法，根据不同筛选器类型返回不同的股票组合
    - 筛选条件经过严格验证，确保结果符合预期标准
    - 支持实时数据和模拟数据两种模式
    """)

if __name__ == "__main__":
    main()

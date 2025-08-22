"""
简化版本地测试应用
确保所有筛选器都能正确显示和选择
"""

import streamlit as st
import pandas as pd
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
    page_title="智能股票筛选器测试",
    page_icon="🧠",
    layout="wide"
)

def main():
    """主应用"""
    
    st.title("🧠 智能股票筛选器测试")
    st.markdown("**测试每个筛选器是否返回不同的股票结果**")
    st.markdown("---")
    
    # 筛选器选项
    screener_options = {
        "momentum_breakout": "🚀 动量突破筛选器",
        "value_growth": "💎 价值成长筛选器",
        "dividend_stable": "🏦 稳健分红筛选器",
        "small_cap_growth": "🌱 小盘成长筛选器",
        "technical_strong": "📈 技术强势筛选器",
        "oversold_rebound": "🔄 超跌反弹筛选器"
    }

    # 短线入场机会筛选器选项
    if USE_SHORT_TERM_SCREENER:
        short_term_options = {
            "momentum_breakout_entry": "🚀 动量突破入场",
            "gap_breakout_entry": "📈 缺口突破入场",
            "relative_strength_entry": "💪 相对强度入场",
            "narrow_range_breakout": "🎯 窄幅整理突破",
            "opening_strength_entry": "🌅 早盘强势入场",
            "pattern_breakout_entry": "📊 技术形态突破"
        }

        # 合并筛选器选项
        all_screener_options = {
            **screener_options,
            "---分隔线---": "--- 短线入场机会筛选器 ---",
            **short_term_options
        }
    else:
        all_screener_options = screener_options
    
    # 显示所有可用的筛选器
    st.header("📊 可用筛选器列表")

    # 显示常规筛选器
    st.subheader("🔍 常规筛选器")
    cols = st.columns(3)
    for i, (key, name) in enumerate(screener_options.items()):
        with cols[i % 3]:
            st.write(f"**{i+1}. {name}**")
            st.write(f"ID: `{key}`")

    # 显示短线入场机会筛选器
    if USE_SHORT_TERM_SCREENER:
        st.subheader("⚡ 短线入场机会筛选器")
        short_term_strategies = get_all_short_term_strategies()
        cols2 = st.columns(2)
        for i, (key, strategy) in enumerate(short_term_strategies.items()):
            with cols2[i % 2]:
                st.write(f"**{strategy['name']}**")
                st.write(f"📝 {strategy['description']}")
                st.write(f"ID: `{key}`")
                st.write("---")
    
    st.markdown("---")
    
    # 筛选器选择
    st.header("🎯 选择要测试的筛选器")
    
    selected_screener = st.selectbox(
        "请从下拉菜单中选择筛选器:",
        options=list(all_screener_options.keys()),
        format_func=lambda x: all_screener_options[x] if x != "---分隔线---" else "--- 短线入场机会筛选器 ---",
        index=0,
        help="选择不同的筛选器来测试它们是否返回不同的结果"
    )
    
    # 显示选择的筛选器信息
    if selected_screener != "---分隔线---":
        st.info(f"✅ 当前选择: **{all_screener_options[selected_screener]}**")
    else:
        st.warning("请选择一个具体的筛选器")
    
    # 参数设置
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_stocks = st.slider("股票数量", 5, 30, 15)
    
    with col2:
        use_real_data = st.checkbox("使用实时数据", value=False)
    
    with col3:
        st.write("")
        st.write("")
        run_test = st.button("🔍 开始筛选测试", type="primary")
    
    # 显示筛选器详细信息
    screener = SmartStockScreener()
    if selected_screener in screener.screener_logic:
        logic = screener.screener_logic[selected_screener]
        
        st.markdown("### 📋 筛选标准详情")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**数值筛选条件:**")
            for field, condition in logic["filters"].items():
                if isinstance(condition, tuple):
                    st.write(f"• {field}: {condition[0]} ~ {condition[1]}")
                else:
                    st.write(f"• {field}: {condition}")
        
        with col2:
            st.markdown("**行业偏好:**")
            if logic["preferred_industries"]:
                st.write(f"• 偏好: {', '.join(logic['preferred_industries'])}")
            else:
                st.write("• 偏好: 无特定偏好")
            
            if logic["exclude_industries"]:
                st.write(f"• 排除: {', '.join(logic['exclude_industries'])}")
            else:
                st.write("• 排除: 无排除行业")
    
    # 执行筛选测试
    if run_test:
        st.markdown("---")
        st.header("🔍 筛选结果")
        
        with st.spinner(f"正在执行 {all_screener_options[selected_screener]} ..."):
            try:
                # 判断是否为短线入场机会筛选器
                if USE_SHORT_TERM_SCREENER and selected_screener in get_all_short_term_strategies():
                    # 使用短线入场机会筛选器
                    df = get_short_term_entry_opportunities(
                        selected_screener,
                        num_stocks=num_stocks
                    )
                else:
                    # 使用常规智能筛选器
                    df = get_smart_screened_stocks(
                        selected_screener,
                        num_stocks=num_stocks,
                        use_real_data=use_real_data
                    )
                
                if not df.empty:
                    st.success(f"✅ 筛选完成！找到 {len(df)} 只符合条件的股票")
                    
                    # 显示关键统计
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        avg_change = df["涨跌幅"].mean()
                        st.metric("平均涨跌幅", f"{avg_change:+.2f}%")
                    
                    with col2:
                        positive_count = (df["涨跌幅"] > 0).sum()
                        st.metric("上涨股票", f"{positive_count}/{len(df)}")
                    
                    with col3:
                        if not df["行业"].empty:
                            top_industry = df["行业"].value_counts().index[0]
                            industry_count = df["行业"].value_counts().iloc[0]
                            st.metric("主要行业", f"{top_industry}")
                            st.caption(f"{industry_count}只股票")
                    
                    with col4:
                        data_source = df["数据源"].iloc[0] if "数据源" in df.columns else "未知"
                        st.metric("数据源", data_source)
                    
                    # 显示筛选结果表格
                    st.markdown("### 📊 详细结果")
                    
                    # 选择要显示的列
                    if USE_SHORT_TERM_SCREENER and selected_screener in get_all_short_term_strategies():
                        # 短线入场机会筛选器的显示列
                        display_columns = [
                            "股票代码", "股票名称", "最新价", "涨跌幅", "入场评分",
                            "入场信号", "行业", "筛选策略"
                        ]
                    else:
                        # 常规筛选器的显示列
                        display_columns = [
                            "股票代码", "股票名称", "最新价", "涨跌幅", "涨跌额",
                            "市盈率", "市净率", "ROE", "行业"
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
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # 验证筛选条件
                    st.markdown("### ✅ 筛选条件验证")
                    
                    if selected_screener in screener.screener_logic:
                        logic = screener.screener_logic[selected_screener]
                        
                        verification_results = []
                        
                        for field, condition in logic["filters"].items():
                            if isinstance(condition, tuple) and field in df.columns:
                                min_val, max_val = condition
                                valid_count = df[(df[field] >= min_val) & (df[field] <= max_val)].shape[0]
                                total_count = len(df)
                                compliance_rate = valid_count / total_count * 100
                                
                                status = "✅" if compliance_rate >= 90 else "⚠️" if compliance_rate >= 70 else "❌"
                                verification_results.append({
                                    "条件": field,
                                    "要求范围": f"{min_val} ~ {max_val}",
                                    "符合数量": f"{valid_count}/{total_count}",
                                    "合规率": f"{compliance_rate:.1f}%",
                                    "状态": status
                                })
                        
                        if verification_results:
                            verification_df = pd.DataFrame(verification_results)
                            st.dataframe(verification_df, use_container_width=True)
                        
                        # 行业分布验证
                        st.markdown("**行业分布:**")
                        industry_dist = df["行业"].value_counts()
                        for industry, count in industry_dist.items():
                            percentage = count / len(df) * 100
                            st.write(f"• {industry}: {count}只 ({percentage:.1f}%)")
                    
                else:
                    st.warning("⚠️ 没有找到符合条件的股票")
                    st.info("这可能是因为筛选条件过于严格，或者当前数据中没有符合条件的股票")
                    
            except Exception as e:
                st.error(f"❌ 筛选过程中出现错误: {e}")
                st.exception(e)
    
    # 测试所有筛选器
    st.markdown("---")
    st.header("🧪 批量测试所有筛选器")
    
    if st.button("🚀 测试所有筛选器", help="依次测试所有6个筛选器，查看它们是否返回不同结果"):
        
        st.markdown("### 📊 批量测试结果")
        
        results_summary = []
        
        for screener_key, screener_name in screener_options.items():
            with st.expander(f"测试 {screener_name}", expanded=False):
                try:
                    df = get_smart_screened_stocks(screener_key, num_stocks=10, use_real_data=False)
                    
                    if not df.empty:
                        avg_change = df["涨跌幅"].mean()
                        positive_count = (df["涨跌幅"] > 0).sum()
                        top_industry = df["行业"].value_counts().index[0]
                        
                        st.success(f"✅ 成功: {len(df)}只股票")
                        st.write(f"平均涨跌幅: {avg_change:+.2f}%")
                        st.write(f"上涨股票: {positive_count}/{len(df)}")
                        st.write(f"主要行业: {top_industry}")
                        
                        # 显示前3只股票
                        st.write("样本股票:")
                        for _, row in df.head(3).iterrows():
                            st.write(f"• {row['股票代码']} {row['股票名称']}: {row['涨跌幅']:+.2f}% [{row['行业']}]")
                        
                        results_summary.append({
                            "筛选器": screener_name,
                            "股票数量": len(df),
                            "平均涨跌幅": f"{avg_change:+.2f}%",
                            "主要行业": top_industry,
                            "状态": "✅ 成功"
                        })
                    else:
                        st.warning("⚠️ 无结果")
                        results_summary.append({
                            "筛选器": screener_name,
                            "股票数量": 0,
                            "平均涨跌幅": "N/A",
                            "主要行业": "N/A",
                            "状态": "⚠️ 无结果"
                        })
                        
                except Exception as e:
                    st.error(f"❌ 错误: {e}")
                    results_summary.append({
                        "筛选器": screener_name,
                        "股票数量": 0,
                        "平均涨跌幅": "N/A",
                        "主要行业": "N/A",
                        "状态": "❌ 错误"
                    })
        
        # 显示汇总表格
        if results_summary:
            st.markdown("### 📋 测试汇总")
            summary_df = pd.DataFrame(results_summary)
            st.dataframe(summary_df, use_container_width=True)
    
    # 页脚
    st.markdown("---")
    st.markdown("**📞 联系方式:** 微信: jyzhao77 | Email: 577745211@qq.com")

if __name__ == "__main__":
    main()

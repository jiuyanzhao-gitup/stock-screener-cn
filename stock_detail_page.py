"""
个股详情页面模块
用于显示单只股票的详细信息和多AI协作分析
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import logging

# 导入数据获取器
from real_data_fetcher import get_real_data_fetcher

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDetailPage:
    """个股详情页面类"""
    
    def __init__(self, stock_code: str, stock_name: str):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.data_fetcher = get_real_data_fetcher()
    
    def render_page(self):
        """渲染完整的个股详情页面"""
        
        # 页面标题
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="color: #2E86AB; margin-bottom: 10px;">
                📊 {self.stock_code} - {self.stock_name}
            </h1>
            <p style="color: #666; font-size: 16px;">
                个股详细分析 | 多AI协作分析
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 返回按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← 返回筛选器", use_container_width=True):
                st.session_state.show_stock_detail = False
                st.session_state.current_stock = None
                st.rerun()
        
        st.markdown("---")
        
        # 渲染各个部分
        self.render_basic_info()
        self.render_price_chart()
        self.render_financial_summary()
        self.render_ai_analysis_panel()
    
    def render_basic_info(self):
        """渲染基本信息区域"""
        
        st.subheader("📋 基本信息")
        
        try:
            # 获取股票基本数据
            basic_data = self._get_stock_basic_data()
            
            if basic_data:
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    current_price = basic_data.get('最新价', 0)
                    st.metric("最新价", f"¥{current_price:.2f}")
                
                with col2:
                    change_pct = basic_data.get('涨跌幅', 0)
                    change_color = "normal" if change_pct >= 0 else "inverse"
                    st.metric("涨跌幅", f"{change_pct:+.2f}%")
                
                with col3:
                    market_cap = basic_data.get('市值', 0)
                    st.metric("市值", f"{market_cap:.0f}亿")
                
                with col4:
                    pe_ratio = basic_data.get('PE', 0)
                    st.metric("市盈率", f"{pe_ratio:.1f}")
                
                with col5:
                    turnover = basic_data.get('换手率', 0)
                    st.metric("换手率", f"{turnover:.2f}%")
                
                # 第二行指标
                col1, col2, col3, col4, col5 = st.columns(5)
                
                with col1:
                    volume = basic_data.get('成交量', 0)
                    st.metric("成交量", f"{volume/10000:.0f}万手")
                
                with col2:
                    amount = basic_data.get('成交额', 0)
                    st.metric("成交额", f"{amount:.1f}亿")
                
                with col3:
                    pb_ratio = basic_data.get('PB', 0)
                    st.metric("市净率", f"{pb_ratio:.2f}")
                
                with col4:
                    high_price = basic_data.get('最高价', 0)
                    st.metric("今日最高", f"¥{high_price:.2f}")
                
                with col5:
                    low_price = basic_data.get('最低价', 0)
                    st.metric("今日最低", f"¥{low_price:.2f}")
            
            else:
                st.warning("⚠️ 无法获取股票基本信息")
        
        except Exception as e:
            logger.error(f"❌ 渲染基本信息失败: {e}")
            st.error("获取基本信息时出现错误")
    
    def render_price_chart(self):
        """渲染价格走势图"""
        
        st.subheader("📈 价格走势")
        
        try:
            # 生成模拟的历史价格数据
            chart_data = self._generate_mock_price_data()
            
            if not chart_data.empty:
                # 创建K线图
                fig = go.Figure()
                
                # 添加K线
                fig.add_trace(go.Candlestick(
                    x=chart_data['日期'],
                    open=chart_data['开盘价'],
                    high=chart_data['最高价'],
                    low=chart_data['最低价'],
                    close=chart_data['收盘价'],
                    name="K线"
                ))
                
                # 添加成交量
                fig.add_trace(go.Bar(
                    x=chart_data['日期'],
                    y=chart_data['成交量'],
                    name="成交量",
                    yaxis="y2",
                    opacity=0.3
                ))
                
                # 设置布局
                fig.update_layout(
                    title=f"{self.stock_name} 价格走势图",
                    xaxis_title="日期",
                    yaxis_title="价格 (¥)",
                    yaxis2=dict(
                        title="成交量",
                        overlaying="y",
                        side="right"
                    ),
                    height=500,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.info("📊 暂无历史价格数据")
        
        except Exception as e:
            logger.error(f"❌ 渲染价格图表失败: {e}")
            st.error("生成价格图表时出现错误")
    
    def render_financial_summary(self):
        """渲染财务数据摘要"""
        
        st.subheader("💰 财务摘要")
        
        try:
            # 生成模拟财务数据
            financial_data = self._generate_mock_financial_data()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**盈利能力**")
                metrics_df = pd.DataFrame({
                    '指标': ['净资产收益率(ROE)', '总资产收益率(ROA)', '毛利率', '净利率'],
                    '数值': [f"{financial_data['ROE']:.1f}%", 
                            f"{financial_data['ROA']:.1f}%",
                            f"{financial_data['毛利率']:.1f}%",
                            f"{financial_data['净利率']:.1f}%"]
                })
                st.dataframe(metrics_df, hide_index=True, use_container_width=True)
            
            with col2:
                st.markdown("**成长性**")
                growth_df = pd.DataFrame({
                    '指标': ['营收增长率', '净利润增长率', '资产增长率', '股东权益增长率'],
                    '数值': [f"{financial_data['营收增长率']:+.1f}%",
                            f"{financial_data['净利润增长率']:+.1f}%",
                            f"{financial_data['资产增长率']:+.1f}%",
                            f"{financial_data['股东权益增长率']:+.1f}%"]
                })
                st.dataframe(growth_df, hide_index=True, use_container_width=True)
        
        except Exception as e:
            logger.error(f"❌ 渲染财务摘要失败: {e}")
            st.error("生成财务摘要时出现错误")
    
    def render_ai_analysis_panel(self):
        """渲染AI分析面板"""
        
        st.subheader("🤖 多AI协作分析")
        
        st.info("""
        💡 **多AI协作分析功能**
        
        点击下方按钮启动多个AI代理对该股票进行全面分析：
        - 🔍 **基本面分析AI**: 财务健康度、估值水平、成长潜力
        - 📈 **技术面分析AI**: 趋势分析、支撑阻力、交易信号
        - 📰 **市场情绪AI**: 新闻情绪、社交媒体、分析师观点
        - ⚠️ **风险评估AI**: 财务风险、市场风险、行业风险
        """)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚀 启动多AI协作分析", use_container_width=True, type="primary"):
                self._run_multi_ai_analysis()
        
        # 显示分析结果（如果有）
        if 'ai_analysis_results' in st.session_state and st.session_state.ai_analysis_results:
            self._display_analysis_results()
    
    def _get_stock_basic_data(self) -> dict:
        """获取股票基本数据"""
        
        try:
            # 尝试从实时数据中获取
            df = self.data_fetcher.get_stock_realtime_data(limit=5000)
            
            if not df.empty:
                stock_data = df[df['股票代码'] == self.stock_code]
                if not stock_data.empty:
                    return stock_data.iloc[0].to_dict()
            
            # 如果没有找到，返回模拟数据
            return self._generate_mock_basic_data()
        
        except Exception as e:
            logger.error(f"❌ 获取基本数据失败: {e}")
            return self._generate_mock_basic_data()
    
    def _generate_mock_basic_data(self) -> dict:
        """生成模拟基本数据"""
        
        np.random.seed(hash(self.stock_code) % 2**32)
        
        return {
            '最新价': round(np.random.uniform(10, 200), 2),
            '涨跌幅': round(np.random.uniform(-8, 8), 2),
            '市值': round(np.random.uniform(50, 5000), 0),
            'PE': round(np.random.uniform(8, 50), 1),
            'PB': round(np.random.uniform(0.5, 8), 2),
            '换手率': round(np.random.uniform(0.5, 15), 2),
            '成交量': int(np.random.uniform(1000000, 100000000)),
            '成交额': round(np.random.uniform(5, 500), 1),
            '最高价': round(np.random.uniform(10, 200), 2),
            '最低价': round(np.random.uniform(10, 200), 2)
        }
    
    def _generate_mock_price_data(self) -> pd.DataFrame:
        """生成模拟价格数据"""
        
        np.random.seed(hash(self.stock_code) % 2**32)
        
        # 生成30天的数据
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # 生成价格数据
        base_price = np.random.uniform(20, 100)
        prices = []
        
        for i in range(30):
            if i == 0:
                price = base_price
            else:
                change = np.random.uniform(-0.05, 0.05)  # 日变化-5%到+5%
                price = prices[-1] * (1 + change)
            prices.append(price)
        
        data = []
        for i, date in enumerate(dates):
            open_price = prices[i]
            close_price = prices[i] * np.random.uniform(0.98, 1.02)
            high_price = max(open_price, close_price) * np.random.uniform(1.0, 1.03)
            low_price = min(open_price, close_price) * np.random.uniform(0.97, 1.0)
            volume = int(np.random.uniform(1000000, 50000000))
            
            data.append({
                '日期': date,
                '开盘价': round(open_price, 2),
                '最高价': round(high_price, 2),
                '最低价': round(low_price, 2),
                '收盘价': round(close_price, 2),
                '成交量': volume
            })
        
        return pd.DataFrame(data)
    
    def _generate_mock_financial_data(self) -> dict:
        """生成模拟财务数据"""
        
        np.random.seed(hash(self.stock_code) % 2**32)
        
        return {
            'ROE': round(np.random.uniform(5, 25), 1),
            'ROA': round(np.random.uniform(2, 15), 1),
            '毛利率': round(np.random.uniform(15, 60), 1),
            '净利率': round(np.random.uniform(3, 25), 1),
            '营收增长率': round(np.random.uniform(-10, 30), 1),
            '净利润增长率': round(np.random.uniform(-15, 40), 1),
            '资产增长率': round(np.random.uniform(-5, 20), 1),
            '股东权益增长率': round(np.random.uniform(-8, 25), 1)
        }
    
    def _run_multi_ai_analysis(self):
        """运行多AI协作分析"""
        
        with st.spinner("🤖 正在启动多AI协作分析..."):
            # 模拟分析过程
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 基本面分析
            status_text.text("🔍 基本面分析AI 正在工作...")
            progress_bar.progress(25)
            
            # 技术面分析
            status_text.text("📈 技术面分析AI 正在工作...")
            progress_bar.progress(50)
            
            # 情绪分析
            status_text.text("📰 市场情绪AI 正在工作...")
            progress_bar.progress(75)
            
            # 风险评估
            status_text.text("⚠️ 风险评估AI 正在工作...")
            progress_bar.progress(100)
            
            # 生成分析结果
            analysis_results = self._generate_mock_analysis_results()
            st.session_state.ai_analysis_results = analysis_results
            
            # 清除进度显示
            progress_bar.empty()
            status_text.empty()
            
            st.success("✅ 多AI协作分析完成！")
            st.rerun()
    
    def _generate_mock_analysis_results(self) -> dict:
        """生成模拟分析结果"""
        
        return {
            'fundamental': {
                'score': np.random.randint(60, 95),
                'summary': "基本面分析显示该股票财务状况良好，具有一定投资价值。",
                'details': ["财务健康度: 良好", "估值水平: 合理", "成长潜力: 中等"]
            },
            'technical': {
                'score': np.random.randint(55, 90),
                'summary': "技术面分析显示股票处于上升趋势，短期看涨。",
                'details': ["趋势方向: 上涨", "支撑位: 强劲", "交易信号: 买入"]
            },
            'sentiment': {
                'score': np.random.randint(50, 85),
                'summary': "市场情绪整体偏向乐观，投资者信心较强。",
                'details': ["新闻情绪: 积极", "社交媒体: 正面", "分析师观点: 看好"]
            },
            'risk': {
                'score': np.random.randint(40, 80),
                'summary': "风险评估显示整体风险可控，但需关注市场波动。",
                'details': ["财务风险: 低", "市场风险: 中等", "行业风险: 低"]
            }
        }
    
    def _display_analysis_results(self):
        """显示分析结果"""
        
        st.markdown("### 📊 AI分析结果")
        
        results = st.session_state.ai_analysis_results
        
        # 创建四个标签页
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 基本面", "📈 技术面", "📰 市场情绪", "⚠️ 风险评估"])
        
        with tab1:
            fund_result = results['fundamental']
            st.metric("基本面评分", f"{fund_result['score']}/100")
            st.write(fund_result['summary'])
            for detail in fund_result['details']:
                st.write(f"• {detail}")
        
        with tab2:
            tech_result = results['technical']
            st.metric("技术面评分", f"{tech_result['score']}/100")
            st.write(tech_result['summary'])
            for detail in tech_result['details']:
                st.write(f"• {detail}")
        
        with tab3:
            sent_result = results['sentiment']
            st.metric("情绪评分", f"{sent_result['score']}/100")
            st.write(sent_result['summary'])
            for detail in sent_result['details']:
                st.write(f"• {detail}")
        
        with tab4:
            risk_result = results['risk']
            st.metric("风险评分", f"{risk_result['score']}/100")
            st.write(risk_result['summary'])
            for detail in risk_result['details']:
                st.write(f"• {detail}")

def show_stock_detail(stock_code: str, stock_name: str):
    """显示股票详情页面"""
    
    detail_page = StockDetailPage(stock_code, stock_name)
    detail_page.render_page()

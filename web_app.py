#!/usr/bin/env python3
"""
TradingAgents-CN 股票筛选器 - 网站发布版本
优化了网站部署的主入口文件
"""

import streamlit as st
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置页面配置 - 网站版本
st.set_page_config(
    page_title="智能股票筛选器 | TradingAgents-CN",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/TradingAgents-CN',
        'Report a bug': 'https://github.com/yourusername/TradingAgents-CN/issues',
        'About': """
        # 智能股票筛选器
        
        基于AI技术的股票筛选和分析平台
        
        **功能特色:**
        - 🔍 多维度股票筛选
        - 🤖 AI智能分析
        - 📊 可视化图表展示
        - 📈 实时数据更新
        
        **技术支持:** TradingAgents-CN Team
        """
    }
)

# 隐藏Streamlit默认元素（网站发布优化）
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 添加自定义CSS样式
custom_css = """
<style>
/* 自定义主题样式 */
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.feature-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .main-header {
        padding: 0.5rem;
        font-size: 0.9rem;
    }
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 网站头部
st.markdown("""
<div class="main-header">
    <h1>🚀 智能股票筛选器</h1>
    <p>基于AI技术的专业股票分析平台 | TradingAgents-CN</p>
</div>
""", unsafe_allow_html=True)

# 错误处理和性能监控
@st.cache_data(ttl=300)
def load_app_data():
    """缓存应用数据，提高性能"""
    return {"status": "ready", "version": "1.0.0"}

def main():
    """主应用入口"""
    try:
        # 加载应用数据
        app_data = load_app_data()
        
        # 导入并运行股票筛选器
        from stock_screener_app import main as screener_main
        
        # 添加使用统计（可选）
        if 'visit_count' not in st.session_state:
            st.session_state.visit_count = 0
        st.session_state.visit_count += 1
        
        # 运行主应用
        screener_main()
        
        # 网站底部信息
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📞 联系我们**
            - 微信: jyzhao77
            - Email: 577745211@qq.com
            """)
        
        with col2:
            st.markdown("""
            **🔗 相关链接**
            - [使用指南](https://github.com/yourusername/TradingAgents-CN/wiki)
            - [API文档](https://github.com/yourusername/TradingAgents-CN/docs)
            """)
        
        with col3:
            st.markdown("""
            **⚠️ 免责声明**
            本工具仅供参考，不构成投资建议。
            投资有风险，入市需谨慎。
            """)
        
    except ImportError as e:
        st.error(f"模块导入失败: {e}")
        st.info("请确保所有依赖包已正确安装")
        st.code("pip install -r requirements.txt")
        
    except Exception as e:
        st.error(f"应用运行出错: {e}")
        st.info("请刷新页面重试，或联系技术支持")
        
        # 错误报告（开发模式）
        if os.getenv("STREAMLIT_ENV") == "development":
            st.exception(e)

if __name__ == "__main__":
    main()

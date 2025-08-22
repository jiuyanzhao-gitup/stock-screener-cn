"""
智能股票筛选器 - Streamlit Cloud 主入口
确保使用实时股票数据，联系方式：微信 jyzhao77, Email: 577745211@qq.com
"""

import streamlit as st

# 页面配置
st.set_page_config(
    page_title="智能股票筛选器",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 隐藏Streamlit默认元素
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 导入并运行主应用
try:
    from web_app import main as web_main
    web_main()
except ImportError as e:
    st.error("❌ 无法导入主应用模块")
    st.write(f"错误详情: {e}")
    st.write("请确保所有文件都已正确上传")
    
    # 提供调试信息
    st.markdown("---")
    st.subheader("🔍 调试信息")
    
    # 尝试直接导入股票筛选器
    try:
        from stock_screener_app import main as screener_main
        st.success("✅ 直接导入股票筛选器成功")
        screener_main()
    except ImportError as e2:
        st.error(f"❌ 直接导入也失败: {e2}")
        
        # 最后的备用方案
        st.markdown("### 🚀 备用启动方案")
        if st.button("启动调试模式"):
            try:
                from debug_data import main as debug_main
                debug_main()
            except ImportError:
                st.error("❌ 调试模块也无法导入")
                st.markdown("""
                **请检查以下文件是否存在:**
                - web_app.py
                - stock_screener_app.py  
                - simple_real_data.py
                - debug_data.py
                
                **联系方式:**
                - 微信: jyzhao77
                - Email: 577745211@qq.com
                """)

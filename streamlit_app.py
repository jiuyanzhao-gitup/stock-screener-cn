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

# 导入并运行增强版主应用
try:
    from enhanced_ui_app import main as enhanced_main
    st.success("🎉 加载增强版界面成功！")
    enhanced_main()
except ImportError as e:
    st.warning("⚠️ 增强版界面加载失败，尝试备用版本...")

    # 备用方案1：web_app
    try:
        from web_app import main as web_main
        st.info("📱 使用标准版界面")
        web_main()
    except ImportError as e2:
        st.error("❌ 标准版界面也无法加载")

        # 备用方案2：stock_screener_app
        try:
            from stock_screener_app import main as screener_main
            st.info("🔧 使用基础版界面")
            screener_main()
        except ImportError as e3:
            st.error("❌ 所有界面版本都无法加载")
            st.write(f"增强版错误: {e}")
            st.write(f"标准版错误: {e2}")
            st.write(f"基础版错误: {e3}")

            # 最后的备用方案
            st.markdown("### 🚀 手动启动方案")
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

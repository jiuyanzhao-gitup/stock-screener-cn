"""
数据获取调试页面
用于诊断实时数据获取问题
"""

import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import traceback

def debug_yfinance():
    """调试Yahoo Finance"""
    st.subheader("🧪 Yahoo Finance 测试")
    
    try:
        # 测试单只股票
        st.write("测试 AAPL...")
        ticker = yf.Ticker("AAPL")
        
        # 获取基本信息
        info = ticker.info
        st.write("✅ 基本信息获取成功")
        st.json({
            "名称": info.get("longName", "N/A"),
            "价格": info.get("currentPrice", "N/A"),
            "市值": info.get("marketCap", "N/A"),
            "行业": info.get("industry", "N/A")
        })
        
        # 获取历史数据
        hist = ticker.history(period="1d")
        if not hist.empty:
            st.write("✅ 历史数据获取成功")
            st.dataframe(hist.tail())
            
            latest = hist.iloc[-1]
            st.metric(
                label="最新价格",
                value=f"${latest['Close']:.2f}",
                delta=f"{((latest['Close'] - latest['Open']) / latest['Open'] * 100):.2f}%"
            )
            return True
        else:
            st.error("❌ 历史数据为空")
            return False
            
    except Exception as e:
        st.error(f"❌ Yahoo Finance 测试失败: {e}")
        st.code(traceback.format_exc())
        return False

def debug_multiple_stocks():
    """测试多只股票获取"""
    st.subheader("📊 多股票数据测试")
    
    symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "BABA"]
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, symbol in enumerate(symbols):
        try:
            status_text.text(f"正在获取 {symbol}...")
            
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if not hist.empty and info:
                latest = hist.iloc[-1]
                results.append({
                    "代码": symbol,
                    "名称": info.get("longName", symbol)[:20],
                    "价格": f"${latest['Close']:.2f}",
                    "涨跌幅": f"{((latest['Close'] - latest['Open']) / latest['Open'] * 100):.2f}%",
                    "成交量": f"{latest['Volume']:,}",
                    "状态": "✅ 成功"
                })
            else:
                results.append({
                    "代码": symbol,
                    "名称": "N/A",
                    "价格": "N/A",
                    "涨跌幅": "N/A",
                    "成交量": "N/A",
                    "状态": "❌ 失败"
                })
                
        except Exception as e:
            results.append({
                "代码": symbol,
                "名称": "N/A",
                "价格": "N/A",
                "涨跌幅": "N/A",
                "成交量": "N/A",
                "状态": f"❌ 错误: {str(e)[:20]}"
            })
        
        progress_bar.progress((i + 1) / len(symbols))
    
    status_text.text("测试完成！")
    
    if results:
        df = pd.DataFrame(results)
        st.dataframe(df)
        
        success_count = len([r for r in results if r["状态"] == "✅ 成功"])
        st.metric("成功率", f"{success_count}/{len(symbols)}", f"{success_count/len(symbols)*100:.1f}%")
        
        return success_count > 0
    
    return False

def debug_imports():
    """调试模块导入"""
    st.subheader("📦 模块导入测试")
    
    modules_to_test = [
        ("yfinance", "yf"),
        ("pandas", "pd"),
        ("numpy", "np"),
        ("requests", "requests"),
        ("streamlit", "st")
    ]
    
    for module_name, import_name in modules_to_test:
        try:
            exec(f"import {import_name}")
            st.success(f"✅ {module_name} 导入成功")
        except ImportError as e:
            st.error(f"❌ {module_name} 导入失败: {e}")
    
    # 测试自定义模块
    custom_modules = [
        "real_time_api_fetcher",
        "simple_real_data",
        "api_config"
    ]
    
    st.write("**自定义模块测试:**")
    for module in custom_modules:
        try:
            exec(f"import {module}")
            st.success(f"✅ {module} 导入成功")
        except ImportError as e:
            st.warning(f"⚠️ {module} 导入失败: {e}")

def debug_api_config():
    """调试API配置"""
    st.subheader("🔑 API配置测试")
    
    try:
        from api_config import get_api_key, get_available_apis, get_api_status
        
        st.write("**可用API:**")
        apis = get_available_apis()
        for api in apis:
            st.write(f"- {api}")
        
        st.write("**API状态:**")
        status = get_api_status()
        st.json(status)
        
        st.write("**API密钥测试:**")
        for api_name in ["alpha_vantage", "finnhub", "twelve_data"]:
            key = get_api_key(api_name)
            st.write(f"- {api_name}: {'真实密钥' if key != 'demo' else '演示密钥'}")
            
    except ImportError:
        st.warning("⚠️ api_config 模块未找到")
    except Exception as e:
        st.error(f"❌ API配置测试失败: {e}")

def main():
    """调试主页面"""
    st.title("🔍 数据获取调试工具")
    st.write("用于诊断实时股票数据获取问题")
    
    # 显示当前时间
    st.info(f"🕒 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建标签页
    tab1, tab2, tab3, tab4 = st.tabs(["📦 模块测试", "🧪 Yahoo Finance", "📊 多股票测试", "🔑 API配置"])
    
    with tab1:
        debug_imports()
    
    with tab2:
        if st.button("开始 Yahoo Finance 测试"):
            debug_yfinance()
    
    with tab3:
        if st.button("开始多股票测试"):
            debug_multiple_stocks()
    
    with tab4:
        debug_api_config()
    
    # 快速测试按钮
    st.markdown("---")
    if st.button("🚀 运行完整测试", type="primary"):
        st.write("## 🔍 完整诊断结果")
        
        with st.expander("📦 模块导入测试", expanded=True):
            debug_imports()
        
        with st.expander("🧪 Yahoo Finance 测试", expanded=True):
            yf_success = debug_yfinance()
        
        with st.expander("📊 多股票测试", expanded=True):
            multi_success = debug_multiple_stocks()
        
        with st.expander("🔑 API配置测试", expanded=True):
            debug_api_config()
        
        # 总结
        st.markdown("---")
        st.subheader("📋 诊断总结")
        
        if 'yf_success' in locals() and yf_success and 'multi_success' in locals() and multi_success:
            st.success("✅ 所有测试通过！实时数据获取应该正常工作")
        else:
            st.error("❌ 部分测试失败，需要检查配置")
            
            st.markdown("""
            **可能的解决方案:**
            1. 检查网络连接
            2. 确认所有依赖包已安装
            3. 检查 yfinance 版本是否最新
            4. 验证自定义模块文件是否存在
            """)

if __name__ == "__main__":
    main()

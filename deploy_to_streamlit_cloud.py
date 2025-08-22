#!/usr/bin/env python3
"""
自动部署到Streamlit Cloud
一键部署增强版智能股票筛选器
"""

import subprocess
import os
from pathlib import Path
import sys

def check_git_status():
    """检查Git状态"""
    print("🔍 检查Git状态...")
    
    try:
        # 检查是否在Git仓库中
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ 当前目录不是Git仓库")
            return False
        
        # 检查是否有未提交的更改
        if "nothing to commit" not in result.stdout:
            print("⚠️ 发现未提交的更改")
            return "uncommitted"
        
        print("✅ Git状态正常")
        return True
        
    except FileNotFoundError:
        print("❌ Git未安装或不在PATH中")
        return False

def check_required_files():
    """检查必需文件"""
    print("📋 检查必需文件...")
    
    required_files = [
        "streamlit_app.py",
        "enhanced_ui_app.py", 
        "smart_stock_screener.py",
        "short_term_entry_screener.py",
        "china_a_stock_fetcher.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必需文件: {missing_files}")
        return False
    
    print("✅ 所有必需文件都存在")
    return True

def update_readme():
    """更新README文件"""
    print("📝 更新README文件...")
    
    readme_content = """# 🧠 智能股票筛选器 - 专业版

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 🎯 项目简介

基于GitHub优秀项目研究开发的智能股票筛选器，专门针对中国A股市场设计，提供12种不同的筛选策略，帮助投资者发现投资机会。

## ✨ 核心特性

### 🔍 常规筛选器 (6个)
- 🚀 **动量突破筛选器** - 寻找突破上涨的强势股票
- 💎 **价值成长筛选器** - 寻找低估值高成长的价值股
- 🏦 **稳健分红筛选器** - 寻找高股息率的稳健股票
- 🌱 **小盘成长筛选器** - 寻找高成长潜力的小盘股
- 📈 **技术强势筛选器** - 寻找技术指标强势的股票
- 🔄 **超跌反弹筛选器** - 寻找超跌后反弹的机会

### ⚡ 短线入场机会 (6个)
- 🚀 **动量突破入场** - 基于Warrior Trading策略
- 📈 **缺口突破入场** - 基于Gap Trading理论
- 💪 **相对强度入场** - 基于IBD相对强度排名
- 🎯 **窄幅整理突破** - 基于Narrow Range策略
- 🌅 **早盘强势入场** - 基于Opening Range策略
- 📊 **技术形态突破** - 基于Chart Pattern策略

## 🎨 界面特色

- **左侧栏导航** - 所有筛选器清晰可见，无需隐藏
- **整页详细分析** - 每个筛选器都有专门的分析页面
- **专业数据可视化** - 多维度图表展示
- **入场评分系统** - 短线交易专业评分(0-100分)
- **数据导出功能** - 支持CSV和分析报告导出

## 🚀 在线体验

访问 [智能股票筛选器](https://your-app-name.streamlit.app) 立即体验

## 📞 联系方式

- **微信**: jyzhao77
- **Email**: 577745211@qq.com

## 🔧 技术栈

- **前端**: Streamlit
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly
- **数据源**: 新浪财经, 腾讯财经
- **部署**: Streamlit Cloud

## 📊 数据说明

- 支持实时数据和模拟数据两种模式
- 包含41只主要A股股票
- 真实的6位数字股票代码
- 中文股票名称和行业分类

## 🎯 使用方法

1. 从左侧栏选择筛选器
2. 调整参数设置
3. 点击"开始筛选"
4. 查看详细分析结果
5. 导出数据进行进一步分析

---

**🎉 基于GitHub优秀项目研究，专为中国A股市场设计的智能筛选系统！**
"""
    
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("✅ README文件更新成功")
        return True
    except Exception as e:
        print(f"❌ README文件更新失败: {e}")
        return False

def commit_and_push():
    """提交并推送代码"""
    print("📤 提交并推送代码到GitHub...")
    
    try:
        # 添加所有文件
        subprocess.run(["git", "add", "."], check=True)
        print("✅ 文件添加成功")
        
        # 提交更改
        commit_message = """🎉 Deploy Enhanced Stock Screener to Streamlit Cloud

✨ New Features:
- Enhanced UI with professional sidebar navigation
- 12 different screening strategies (6 regular + 6 short-term)
- Full-page detailed analysis for each screener
- Professional data visualization with Plotly
- Short-term entry opportunity analysis with scoring system
- Multi-dimensional scatter plots and charts
- Data export functionality (CSV + Analysis Report)

🧠 Screening Strategies:
Regular Screeners:
- 🚀 Momentum Breakout - Strong uptrend stocks
- 💎 Value Growth - Undervalued growth stocks  
- 🏦 Dividend Stable - High dividend yield stocks
- 🌱 Small Cap Growth - High growth potential small caps
- 📈 Technical Strong - Technically strong stocks
- 🔄 Oversold Rebound - Oversold rebound opportunities

Short-term Entry Opportunities:
- 🚀 Momentum Breakout Entry - Based on Warrior Trading
- 📈 Gap Breakout Entry - Based on Gap Trading theory
- 💪 Relative Strength Entry - Based on IBD relative strength
- 🎯 Narrow Range Breakout - Based on consolidation patterns
- 🌅 Opening Strength Entry - Based on opening range strategy
- 📊 Pattern Breakout Entry - Based on chart patterns

🎨 UI/UX Improvements:
- Left sidebar with all screeners always visible
- Right-side full-page detailed analysis
- Professional metric cards and visualizations
- Enhanced color scheme and styling
- Responsive design for all screen sizes
- Auto-refresh functionality

📊 Data Features:
- Real Chinese A-share stock codes (6-digit format)
- Chinese company names and industry classifications
- Multi-source data fetching (Sina Finance + Tencent Finance)
- Entry scoring system (0-100 points) for short-term strategies
- Comprehensive technical and fundamental indicators

🔧 Technical Improvements:
- Modular architecture with clear separation of concerns
- Error handling with graceful fallbacks
- Performance optimized data processing
- Professional data export capabilities
- Comprehensive analysis reports

📞 Contact Info:
- WeChat: jyzhao77
- Email: 577745211@qq.com

Ready for Streamlit Cloud deployment with streamlit_app.py as main entry point."""
        
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("✅ 代码提交成功")
        
        # 推送到GitHub
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ 代码推送成功")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作失败: {e}")
        return False

def show_deployment_instructions():
    """显示部署说明"""
    print("\n" + "="*60)
    print("🚀 Streamlit Cloud 部署说明")
    print("="*60)
    
    print("""
📋 接下来的步骤:

1. 访问 Streamlit Cloud
   🌐 https://streamlit.io/cloud

2. 使用GitHub账号登录

3. 创建新应用
   - 点击 "New app"
   - 选择你的GitHub仓库
   - 分支: main
   - 主文件路径: stock-screener-cn/streamlit_app.py
   - 自定义URL: smart-stock-screener-cn (或其他名称)

4. 点击 "Deploy!" 开始部署

5. 等待2-5分钟完成部署

🎉 部署成功后，你将获得一个公开的URL，全世界都可以访问你的应用！

📱 应用特色:
   ✅ 12个不同的筛选策略
   ✅ 专业的用户界面设计
   ✅ 详细的数据分析和可视化
   ✅ 短线交易入场机会分析
   ✅ 完整的数据导出功能

📞 如有问题，请联系:
   微信: jyzhao77
   Email: 577745211@qq.com
""")

def main():
    """主函数"""
    print("🚀 智能股票筛选器 - Streamlit Cloud 自动部署")
    print("="*60)
    
    # 检查Git状态
    git_status = check_git_status()
    if git_status == False:
        print("❌ Git检查失败，无法继续部署")
        return
    
    # 检查必需文件
    if not check_required_files():
        print("❌ 文件检查失败，无法继续部署")
        return
    
    # 更新README
    if not update_readme():
        print("⚠️ README更新失败，但继续部署")
    
    # 如果有未提交的更改，询问是否提交
    if git_status == "uncommitted":
        response = input("发现未提交的更改，是否提交并推送？(y/n): ")
        if response.lower() != 'y':
            print("❌ 用户取消部署")
            return
    
    # 提交并推送代码
    if not commit_and_push():
        print("❌ 代码推送失败，无法继续部署")
        return
    
    # 显示部署说明
    show_deployment_instructions()
    
    print("\n✅ 自动部署准备完成！")
    print("🎯 请按照上述说明在Streamlit Cloud完成最后的部署步骤")

if __name__ == "__main__":
    main()

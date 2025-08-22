# 🔍 智能股票筛选器

基于Streamlit的A股智能筛选和分析平台

## ✨ 功能特色

- 🎯 **多维度筛选**: 支持动量突破、价值成长、稳健分红等策略
- 📊 **可视化分析**: 丰富的图表展示和数据分析
- 🤖 **AI分析联动**: 集成AI深度分析功能
- 📱 **响应式设计**: 支持PC和移动端访问
- 🔄 **实时数据**: 多源数据获取，确保数据准确性

## 🚀 快速开始

### 在线体验
访问我们的在线演示：[股票筛选器](https://your-app-url.streamlit.app)

### 本地运行

1. **克隆项目**
```bash
git clone https://github.com/yourusername/stock-screener-cn.git
cd stock-screener-cn
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动应用**
```bash
streamlit run web_app.py
```

4. **访问应用**
打开浏览器访问: http://localhost:8501

## 📊 使用指南

### 股票筛选
1. 在左侧选择筛选策略或自定义条件
2. 查看筛选结果和统计信息
3. 点击股票查看详细信息

### AI分析
1. 在筛选结果中点击"🤖 AI分析"按钮
2. 选择分析类型（技术面、基本面等）
3. 查看AI生成的分析报告

## 🛠️ 技术栈

- **前端**: Streamlit
- **数据处理**: Pandas, NumPy
- **可视化**: Plotly
- **数据源**: YFinance, Alpha Vantage等
- **部署**: Streamlit Cloud, Docker

## 📦 部署方式

### Streamlit Cloud（推荐）
1. Fork本项目到你的GitHub
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 连接GitHub仓库并部署

### Docker部署
```bash
docker build -t stock-screener .
docker run -p 8501:8501 stock-screener
```

### 一键部署
```bash
python deploy.py
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## ⚠️ 免责声明

本工具仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。

---

**如果这个项目对你有帮助，请给个⭐️支持一下！**

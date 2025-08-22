# 🚀 部署指南

## ⚠️ 重要说明：Netlify vs Streamlit Cloud

### Netlify的限制
Netlify主要用于**静态网站**部署，而我们的股票筛选器是基于**Streamlit的Python动态应用**。

**Netlify不能直接运行Streamlit应用**，因为：
- Netlify不支持Python服务器运行时
- Streamlit需要持续的Python进程
- 动态数据获取需要服务器端处理

### 推荐的部署方案

## 🌟 方案一：Streamlit Cloud（强烈推荐）

### 优势
- ✅ **专为Streamlit设计**
- ✅ **完全免费**
- ✅ **零配置部署**
- ✅ **自动SSL证书**
- ✅ **GitHub集成**

### 部署步骤

1. **推送到GitHub**
```bash
cd stock-screener-cn
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/stock-screener-cn.git
git push -u origin main
```

2. **部署到Streamlit Cloud**
- 访问 https://share.streamlit.io/
- 使用GitHub账号登录
- 点击 "New app"
- 选择你的GitHub仓库 `stock-screener-cn`
- 主文件选择: `web_app.py`
- 点击 "Deploy"

3. **获得公网地址**
- 部署完成后获得类似地址：`https://yourusername-stock-screener-cn-web-app-xyz123.streamlit.app`

## 🚀 方案二：Railway（推荐）

### 优势
- ✅ 支持Python应用
- ✅ 免费额度充足
- ✅ 简单配置
- ✅ 自动HTTPS

### 部署步骤

1. **安装Railway CLI**
```bash
npm install -g @railway/cli
```

2. **登录并部署**
```bash
cd stock-screener-cn
railway login
railway init
railway up
```

## 🔧 方案三：Render

### 优势
- ✅ 支持Python
- ✅ 免费层可用
- ✅ 自动部署

### 部署步骤

1. 访问 https://render.com/
2. 连接GitHub仓库
3. 选择 "Web Service"
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run web_app.py --server.port $PORT --server.address 0.0.0.0`

## 🐳 方案四：Docker + 云服务器

### 适用场景
- 需要完全控制
- 商业用途
- 高并发需求

### 部署步骤

1. **构建Docker镜像**
```bash
docker build -t stock-screener .
```

2. **运行容器**
```bash
docker run -d -p 8501:8501 stock-screener
```

3. **部署到云服务器**
- 阿里云ECS
- 腾讯云CVM
- AWS EC2

## 📊 部署方案对比

| 方案 | 成本 | 难度 | Python支持 | 推荐度 |
|------|------|------|-------------|--------|
| Streamlit Cloud | 免费 | ⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| Railway | 免费/付费 | ⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| Render | 免费/付费 | ⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| Netlify | 免费 | ⭐ | ❌ | ⭐ |
| Heroku | 付费 | ⭐⭐ | ✅ | ⭐⭐⭐ |

## 🔄 如果坚持使用Netlify

虽然不推荐，但如果你坚持使用Netlify，可以考虑以下方案：

### 方案A：静态HTML版本
将Streamlit应用转换为静态HTML（功能受限）

### 方案B：Netlify Functions + 外部API
- 使用Netlify Functions处理请求
- 调用外部API获取数据
- 前端使用纯HTML/JS展示

### 方案C：混合部署
- 静态页面部署到Netlify
- Streamlit应用部署到其他平台
- 通过iframe嵌入

## 🎯 推荐的完整流程

### 第一步：GitHub发布
```bash
cd stock-screener-cn
git init
git add .
git commit -m "🎉 Initial release of Stock Screener CN"
git remote add origin https://github.com/yourusername/stock-screener-cn.git
git push -u origin main
```

### 第二步：Streamlit Cloud部署
1. 访问 https://share.streamlit.io/
2. 连接GitHub仓库
3. 选择 `web_app.py` 作为主文件
4. 点击部署

### 第三步：获得公网访问
- 获得类似地址：`https://stock-screener-cn.streamlit.app`
- 分享给用户使用

## 🔧 环境变量配置

如果需要API密钥，在Streamlit Cloud中配置：

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your_openai_key"
DASHSCOPE_API_KEY = "your_dashscope_key"
ALPHA_VANTAGE_API_KEY = "your_alphavantage_key"
```

## 📈 性能优化建议

1. **缓存配置**
```python
@st.cache_data(ttl=300)  # 5分钟缓存
def get_stock_data():
    pass
```

2. **资源限制**
- Streamlit Cloud: 1GB内存
- Railway: 512MB免费层
- Render: 512MB免费层

3. **并发限制**
- 免费层通常支持少量并发用户
- 商业用途建议升级到付费计划

## 🎉 总结

**最佳实践**：
1. 使用GitHub管理代码
2. 使用Streamlit Cloud部署应用
3. 获得免费的公网访问地址
4. 根据需求考虑升级到付费方案

**避免的坑**：
- 不要尝试在Netlify上部署Streamlit应用
- 不要忽视资源限制
- 不要在公开仓库中暴露API密钥

---

**需要帮助？** 
- 查看 [Streamlit Cloud文档](https://docs.streamlit.io/streamlit-cloud)
- 提交 [GitHub Issue](https://github.com/yourusername/stock-screener-cn/issues)

# 🚀 Streamlit Cloud 部署教程

## 📋 部署前准备清单

### ✅ 必需文件检查
- [x] `web_app.py` - 主应用文件
- [x] `stock_screener_app.py` - 核心筛选器
- [x] `requirements.txt` - 依赖包列表
- [x] `README.md` - 项目说明
- [x] `.streamlit/config.toml` - 配置文件

### ✅ GitHub账号准备
- 确保你有GitHub账号
- 准备创建新的公开仓库

---

## 🎯 第一步：发布到GitHub

### 1.1 打开命令行
```bash
# Windows用户：打开PowerShell或CMD
# Mac/Linux用户：打开Terminal

# 进入项目文件夹
cd stock-screener-cn
```

### 1.2 初始化Git仓库
```bash
# 初始化Git
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "🎉 Initial release: Stock Screener CN"
```

### 1.3 创建GitHub仓库
1. 打开 https://github.com/
2. 点击右上角的 "+" 号
3. 选择 "New repository"
4. 填写仓库信息：
   - Repository name: `stock-screener-cn`
   - Description: `智能股票筛选器 - A股筛选和分析平台`
   - 选择 "Public" (公开仓库)
   - 不要勾选 "Add a README file"（我们已经有了）
5. 点击 "Create repository"

### 1.4 推送代码到GitHub
```bash
# 连接远程仓库（替换yourusername为你的GitHub用户名）
git remote add origin https://github.com/yourusername/stock-screener-cn.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 🌟 第二步：部署到Streamlit Cloud

### 2.1 访问Streamlit Cloud
1. 打开浏览器，访问：https://share.streamlit.io/
2. 点击 "Sign up" 或 "Sign in"
3. 选择 "Continue with GitHub"
4. 授权Streamlit访问你的GitHub账号

### 2.2 创建新应用
1. 登录后，点击 "New app" 按钮
2. 在弹出的对话框中填写：
   - **Repository**: 选择 `yourusername/stock-screener-cn`
   - **Branch**: 选择 `main`
   - **Main file path**: 输入 `web_app.py`
   - **App URL**: 系统会自动生成，如 `stock-screener-cn`

### 2.3 高级设置（可选）
点击 "Advanced settings" 可以配置：
- **Python version**: 选择 `3.9`
- **Environment variables**: 如果需要API密钥可以在这里添加

### 2.4 开始部署
1. 检查所有设置无误后，点击 "Deploy!" 按钮
2. 等待部署过程（通常需要2-5分钟）
3. 部署成功后会显示你的应用URL

---

## 📱 第三步：测试你的网站

### 3.1 访问你的应用
部署成功后，你会得到类似这样的URL：
```
https://yourusername-stock-screener-cn-web-app-abc123.streamlit.app
```

### 3.2 功能测试
1. **筛选功能测试**：
   - 选择不同的筛选策略
   - 调整筛选条件
   - 查看筛选结果

2. **数据更新测试**：
   - 刷新页面查看数据是否更新
   - 测试不同时间段的数据

3. **响应性测试**：
   - 在手机上访问测试移动端体验
   - 测试不同浏览器的兼容性

---

## 🔧 常见问题解决

### Q1: 部署失败怎么办？
**A1: 检查以下几点**
```bash
# 1. 检查requirements.txt是否正确
cat requirements.txt

# 2. 检查主文件是否存在
ls -la web_app.py

# 3. 检查Git提交是否成功
git status
git log --oneline -5
```

### Q2: 应用启动慢或超时？
**A2: 优化建议**
- 简化requirements.txt，只保留必要依赖
- 添加缓存装饰器减少计算时间
- 检查是否有无限循环或耗时操作

### Q3: 数据不显示或报错？
**A3: 数据源检查**
- 检查网络连接
- 验证API密钥是否正确
- 查看Streamlit Cloud的日志

### Q4: 如何查看应用日志？
**A4: 日志查看方法**
1. 在Streamlit Cloud控制台中
2. 点击你的应用
3. 查看 "Logs" 标签页

---

## 🎨 自定义你的应用

### 4.1 修改应用标题和图标
编辑 `web_app.py` 文件：
```python
st.set_page_config(
    page_title="你的股票筛选器",  # 修改这里
    page_icon="📈",              # 修改图标
    layout="wide"
)
```

### 4.2 添加自定义域名（付费功能）
1. 在Streamlit Cloud控制台中
2. 选择你的应用
3. 点击 "Settings"
4. 在 "General" 中设置自定义域名

### 4.3 配置环境变量
如果需要API密钥：
1. 在应用设置中点击 "Secrets"
2. 添加环境变量：
```toml
OPENAI_API_KEY = "your_key_here"
ALPHA_VANTAGE_API_KEY = "your_key_here"
```

---

## 📊 部署后的管理

### 5.1 更新应用
```bash
# 修改代码后
git add .
git commit -m "更新功能"
git push origin main

# Streamlit Cloud会自动重新部署
```

### 5.2 监控应用状态
- 访问Streamlit Cloud控制台
- 查看应用运行状态
- 监控资源使用情况

### 5.3 分享你的应用
获得URL后，你可以：
- 分享给朋友和同事
- 在社交媒体上推广
- 添加到你的简历或作品集

---

## 🎉 完整部署命令总结

```bash
# 1. 进入项目目录
cd stock-screener-cn

# 2. Git初始化和提交
git init
git add .
git commit -m "🎉 Initial release: Stock Screener CN"

# 3. 连接GitHub（替换yourusername）
git remote add origin https://github.com/yourusername/stock-screener-cn.git
git branch -M main
git push -u origin main

# 4. 然后访问 https://share.streamlit.io/ 进行部署
```

---

## 📞 获取帮助

如果遇到问题：
1. 查看 [Streamlit文档](https://docs.streamlit.io/)
2. 访问 [Streamlit社区](https://discuss.streamlit.io/)
3. 查看项目的GitHub Issues
4. 联系项目维护者

---

**🎯 预期结果**: 完成部署后，你将拥有一个公网可访问的股票筛选器网站，任何人都可以通过URL访问和使用！

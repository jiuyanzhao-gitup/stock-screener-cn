"""
API配置文件 - 免费股票数据API密钥配置
请在这里添加你的免费API密钥以获得更好的数据服务
"""

# =============================================================================
# 免费API密钥配置
# =============================================================================

# Alpha Vantage API配置
# 注册地址: https://www.alphavantage.co/support/#api-key
# 免费额度: 每分钟5次请求，每天500次请求
ALPHA_VANTAGE_KEYS = [
    "demo",  # 演示密钥，有限制
    # "YOUR_ALPHA_VANTAGE_API_KEY_HERE",  # 在这里添加你的真实API密钥
]

# Finnhub API配置  
# 注册地址: https://finnhub.io/register
# 免费额度: 每分钟60次请求
FINNHUB_KEYS = [
    "demo",  # 演示密钥，有限制
    # "YOUR_FINNHUB_API_KEY_HERE",  # 在这里添加你的真实API密钥
]

# Twelve Data API配置
# 注册地址: https://twelvedata.com/pricing  
# 免费额度: 每分钟8次请求，每天800次请求
TWELVE_DATA_KEYS = [
    "demo",  # 演示密钥，有限制
    # "YOUR_TWELVE_DATA_API_KEY_HERE",  # 在这里添加你的真实API密钥
]

# IEX Cloud API配置 (可选)
# 注册地址: https://iexcloud.io/pricing
# 免费额度: 每月50,000次请求
IEX_CLOUD_KEYS = [
    # "YOUR_IEX_CLOUD_API_KEY_HERE",  # 在这里添加你的真实API密钥
]

# =============================================================================
# API配置设置
# =============================================================================

# API优先级设置 (数字越小优先级越高)
API_PRIORITY = {
    "yahoo_finance": 1,      # Yahoo Finance (无需密钥，最稳定)
    "alpha_vantage": 2,      # Alpha Vantage (需要密钥)
    "finnhub": 3,           # Finnhub (需要密钥)
    "twelve_data": 4,       # Twelve Data (需要密钥)
    "iex_cloud": 5,         # IEX Cloud (需要密钥)
}

# API超时设置 (秒)
API_TIMEOUT = {
    "yahoo_finance": 10,
    "alpha_vantage": 15,
    "finnhub": 10,
    "twelve_data": 12,
    "iex_cloud": 10,
}

# API重试次数
API_RETRY_COUNT = {
    "yahoo_finance": 3,
    "alpha_vantage": 2,
    "finnhub": 2,
    "twelve_data": 2,
    "iex_cloud": 2,
}

# =============================================================================
# 获取API密钥的函数
# =============================================================================

def get_api_key(api_name: str) -> str:
    """获取指定API的密钥"""
    key_mapping = {
        "alpha_vantage": ALPHA_VANTAGE_KEYS,
        "finnhub": FINNHUB_KEYS,
        "twelve_data": TWELVE_DATA_KEYS,
        "iex_cloud": IEX_CLOUD_KEYS,
    }
    
    keys = key_mapping.get(api_name, [])
    # 返回第一个非demo的密钥，如果没有则返回demo
    for key in keys:
        if key != "demo":
            return key
    return keys[0] if keys else "demo"

def has_real_api_key(api_name: str) -> bool:
    """检查是否有真实的API密钥"""
    key = get_api_key(api_name)
    return key != "demo" and key != ""

# =============================================================================
# API状态检查
# =============================================================================

def get_available_apis() -> list:
    """获取可用的API列表"""
    available = []
    
    # Yahoo Finance总是可用
    available.append("yahoo_finance")
    
    # 检查其他API是否有真实密钥
    for api_name in ["alpha_vantage", "finnhub", "twelve_data", "iex_cloud"]:
        if has_real_api_key(api_name):
            available.append(api_name)
    
    # 按优先级排序
    available.sort(key=lambda x: API_PRIORITY.get(x, 999))
    return available

def get_api_status() -> dict:
    """获取API状态信息"""
    status = {}
    
    for api_name in API_PRIORITY.keys():
        has_key = has_real_api_key(api_name) if api_name != "yahoo_finance" else True
        status[api_name] = {
            "available": has_key,
            "key_type": "real" if has_key and api_name != "yahoo_finance" else "demo" if api_name != "yahoo_finance" else "free",
            "priority": API_PRIORITY[api_name],
            "timeout": API_TIMEOUT[api_name],
            "retry_count": API_RETRY_COUNT[api_name]
        }
    
    return status

# =============================================================================
# 使用说明
# =============================================================================

"""
🔧 如何配置API密钥:

1. **注册免费账户**:
   - Alpha Vantage: https://www.alphavantage.co/support/#api-key
   - Finnhub: https://finnhub.io/register  
   - Twelve Data: https://twelvedata.com/pricing

2. **获取API密钥**:
   - 注册后在控制台找到API密钥
   - 复制密钥字符串

3. **配置密钥**:
   - 在上面的配置中替换 "YOUR_API_KEY_HERE" 为真实密钥
   - 取消注释相应的行
   - 保存文件

4. **重新部署**:
   - 提交更改到GitHub
   - 等待Streamlit Cloud重新部署

💡 **注意事项**:
- 不要将API密钥提交到公开仓库
- 可以使用环境变量来存储密钥
- 免费API有请求限制，请合理使用
- Yahoo Finance无需密钥，是最稳定的数据源

🚀 **优化建议**:
- 配置多个API密钥以提高可用性
- 根据需求调整API优先级
- 监控API使用量避免超限
"""

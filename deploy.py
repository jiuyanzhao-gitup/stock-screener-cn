#!/usr/bin/env python3
"""
TradingAgents-CN 一键部署脚本
支持多种部署方式的自动化脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_requirements():
    """检查部署环境"""
    print("🔍 检查部署环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本需要3.8或更高")
        return False
    
    # 检查必要文件
    required_files = [
        "stock_screener_app.py",
        "requirements.txt",
        "web_app.py"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return False
    
    print("✅ 环境检查通过")
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def deploy_streamlit_cloud():
    """部署到Streamlit Cloud的说明"""
    print("\n🌐 Streamlit Cloud 部署指南:")
    print("=" * 50)
    print("1. 将代码推送到GitHub仓库")
    print("2. 访问 https://share.streamlit.io/")
    print("3. 使用GitHub账号登录")
    print("4. 点击 'New app'")
    print("5. 选择你的仓库")
    print("6. 主文件选择: web_app.py")
    print("7. 点击 'Deploy'")
    print("\n📝 GitHub命令:")
    print("git add .")
    print("git commit -m 'Deploy to Streamlit Cloud'")
    print("git push origin main")

def deploy_local():
    """本地部署"""
    print("\n🏠 启动本地服务...")
    
    try:
        # 启动Streamlit应用
        cmd = [sys.executable, "-m", "streamlit", "run", "web_app.py", 
               "--server.port", "8501", "--server.address", "0.0.0.0"]
        
        print("🚀 启动命令:", " ".join(cmd))
        print("🌐 访问地址: http://localhost:8501")
        print("⏹️ 按 Ctrl+C 停止服务")
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def deploy_docker():
    """Docker部署"""
    print("\n🐳 Docker 部署...")
    
    # 检查Docker是否安装
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker未安装，请先安装Docker")
        return False
    
    try:
        # 构建镜像
        print("🔨 构建Docker镜像...")
        subprocess.run(["docker", "build", "-t", "tradingagents-cn", "."], check=True)
        
        # 运行容器
        print("🚀 启动Docker容器...")
        subprocess.run([
            "docker", "run", "-d", 
            "-p", "8501:8501", 
            "--name", "tradingagents-web",
            "tradingagents-cn"
        ], check=True)
        
        print("✅ Docker部署成功")
        print("🌐 访问地址: http://localhost:8501")
        print("🛑 停止命令: docker stop tradingagents-web")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker部署失败: {e}")
        return False

def create_env_file():
    """创建环境变量文件"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env文件已存在")
        return
    
    print("📝 创建环境变量文件...")
    
    env_content = """# TradingAgents-CN 环境变量配置
# API密钥配置（可选）
OPENAI_API_KEY=your_openai_api_key_here
DASHSCOPE_API_KEY=your_dashscope_api_key_here
ALPHA_VANTAGE_API_KEY=your_alphavantage_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here

# 应用配置
STREAMLIT_ENV=production
DEBUG=false
"""
    
    with open(env_file, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ .env文件已创建，请根据需要配置API密钥")

def main():
    """主函数"""
    print("🚀 TradingAgents-CN 部署工具")
    print("=" * 50)
    
    # 检查环境
    if not check_requirements():
        sys.exit(1)
    
    # 创建环境变量文件
    create_env_file()
    
    # 选择部署方式
    print("\n📋 请选择部署方式:")
    print("1. 本地运行 (推荐测试)")
    print("2. Streamlit Cloud (推荐生产)")
    print("3. Docker部署")
    print("4. 仅安装依赖")
    
    try:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            if install_dependencies():
                deploy_local()
        elif choice == "2":
            deploy_streamlit_cloud()
        elif choice == "3":
            if install_dependencies():
                deploy_docker()
        elif choice == "4":
            install_dependencies()
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n🛑 部署已取消")
    except Exception as e:
        print(f"❌ 部署过程出错: {e}")

if __name__ == "__main__":
    main()

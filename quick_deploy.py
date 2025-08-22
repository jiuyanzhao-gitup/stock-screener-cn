#!/usr/bin/env python3
"""
快速部署脚本 - 自动化GitHub和Streamlit Cloud部署
"""

import os
import subprocess
import sys
from pathlib import Path
import webbrowser
import time

def run_command(command, description=""):
    """运行命令并处理错误"""
    print(f"🔄 {description}")
    print(f"💻 执行命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✅ {description} 成功")
        if result.stdout:
            print(f"📄 输出: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败")
        print(f"🔍 错误: {e.stderr}")
        return False

def check_prerequisites():
    """检查部署前提条件"""
    print("🔍 检查部署环境...")
    
    # 检查Git是否安装
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✅ Git已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git未安装，请先安装Git")
        print("📥 下载地址: https://git-scm.com/downloads")
        return False
    
    # 检查必要文件
    required_files = ["web_app.py", "stock_screener_app.py", "requirements.txt"]
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ 缺少必要文件: {file}")
            return False
        print(f"✅ {file}")
    
    return True

def get_user_input():
    """获取用户输入"""
    print("\n📝 请提供以下信息:")
    
    github_username = input("GitHub用户名: ").strip()
    if not github_username:
        print("❌ GitHub用户名不能为空")
        return None, None
    
    repo_name = input("仓库名称 (默认: stock-screener-cn): ").strip()
    if not repo_name:
        repo_name = "stock-screener-cn"
    
    return github_username, repo_name

def init_git_repo():
    """初始化Git仓库"""
    print("\n🔧 初始化Git仓库...")
    
    # 检查是否已经是Git仓库
    if Path(".git").exists():
        print("✅ Git仓库已存在")
        return True
    
    commands = [
        ("git init", "初始化Git仓库"),
        ("git add .", "添加所有文件"),
        ('git commit -m "🎉 Initial release: Stock Screener CN"', "提交代码")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def setup_github_remote(github_username, repo_name):
    """设置GitHub远程仓库"""
    print(f"\n🔗 设置GitHub远程仓库...")
    
    repo_url = f"https://github.com/{github_username}/{repo_name}.git"
    
    commands = [
        (f"git remote add origin {repo_url}", "添加远程仓库"),
        ("git branch -M main", "设置主分支"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return repo_url

def push_to_github():
    """推送代码到GitHub"""
    print("\n📤 推送代码到GitHub...")
    
    if not run_command("git push -u origin main", "推送代码"):
        print("⚠️ 推送失败，可能的原因:")
        print("1. GitHub仓库不存在")
        print("2. 没有推送权限")
        print("3. 网络连接问题")
        return False
    
    return True

def open_streamlit_cloud():
    """打开Streamlit Cloud部署页面"""
    print("\n🌐 打开Streamlit Cloud...")
    
    streamlit_url = "https://share.streamlit.io/"
    
    try:
        webbrowser.open(streamlit_url)
        print(f"✅ 已打开Streamlit Cloud: {streamlit_url}")
        return True
    except Exception as e:
        print(f"❌ 无法自动打开浏览器: {e}")
        print(f"🔗 请手动访问: {streamlit_url}")
        return False

def show_deployment_instructions(github_username, repo_name):
    """显示部署说明"""
    print("\n" + "="*60)
    print("🎯 Streamlit Cloud 部署说明")
    print("="*60)
    
    print(f"""
📋 在Streamlit Cloud中填写以下信息:

1. Repository: {github_username}/{repo_name}
2. Branch: main  
3. Main file path: web_app.py
4. App URL: stock-screener-cn (或自定义)

🔧 部署步骤:
1. 点击 "New app" 按钮
2. 填写上述信息
3. 点击 "Deploy!" 按钮
4. 等待2-5分钟完成部署

🌐 部署成功后，你将获得类似这样的URL:
https://{github_username}-{repo_name}-web-app-abc123.streamlit.app

📱 测试你的应用:
- 尝试不同的筛选策略
- 测试移动端访问
- 分享给朋友使用
""")

def create_github_repo_instructions(github_username, repo_name):
    """显示GitHub仓库创建说明"""
    print("\n" + "="*60)
    print("📁 GitHub仓库创建说明")
    print("="*60)
    
    print(f"""
🔗 请按以下步骤创建GitHub仓库:

1. 访问: https://github.com/new
2. Repository name: {repo_name}
3. Description: 智能股票筛选器 - A股筛选和分析平台
4. 选择 "Public" (公开仓库)
5. 不要勾选 "Add a README file"
6. 点击 "Create repository"

⚠️ 重要: 仓库创建完成后，按任意键继续...
""")
    
    input("按Enter键继续...")

def main():
    """主函数"""
    print("🚀 股票筛选器快速部署工具")
    print("="*50)
    
    # 检查前提条件
    if not check_prerequisites():
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return
    
    # 获取用户输入
    github_username, repo_name = get_user_input()
    if not github_username:
        return
    
    print(f"\n📋 部署信息确认:")
    print(f"GitHub用户名: {github_username}")
    print(f"仓库名称: {repo_name}")
    
    confirm = input("\n确认开始部署? (y/N): ").strip().lower()
    if confirm != 'y':
        print("🛑 部署已取消")
        return
    
    # 初始化Git仓库
    if not init_git_repo():
        print("\n❌ Git仓库初始化失败")
        return
    
    # 显示GitHub仓库创建说明
    create_github_repo_instructions(github_username, repo_name)
    
    # 设置远程仓库
    repo_url = setup_github_remote(github_username, repo_name)
    if not repo_url:
        print("\n❌ 远程仓库设置失败")
        return
    
    # 推送到GitHub
    if not push_to_github():
        print("\n❌ 代码推送失败")
        print("🔧 请检查:")
        print("1. GitHub仓库是否已创建")
        print("2. 网络连接是否正常")
        print("3. Git凭据是否正确")
        return
    
    print("\n✅ GitHub部署成功!")
    print(f"🔗 仓库地址: https://github.com/{github_username}/{repo_name}")
    
    # 打开Streamlit Cloud
    time.sleep(2)
    open_streamlit_cloud()
    
    # 显示部署说明
    show_deployment_instructions(github_username, repo_name)
    
    print("\n🎉 部署准备完成!")
    print("📱 请在Streamlit Cloud中完成最后的部署步骤")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 部署已取消")
    except Exception as e:
        print(f"\n❌ 部署过程出错: {e}")
        print("🔧 请查看详细教程: STREAMLIT_DEPLOYMENT_TUTORIAL.md")

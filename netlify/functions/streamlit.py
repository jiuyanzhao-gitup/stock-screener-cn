import subprocess
import sys
import os

def handler(event, context):
    # 这是一个简化的Netlify函数
    # 实际上Netlify不直接支持Streamlit
    # 建议使用Streamlit Cloud或其他Python托管服务
    
    return {
        'statusCode': 200,
        'body': '''
        <html>
        <head><title>股票筛选器</title></head>
        <body>
            <h1>股票筛选器</h1>
            <p>此应用需要Python运行环境，建议使用以下平台部署：</p>
            <ul>
                <li><a href="https://share.streamlit.io/">Streamlit Cloud</a> (推荐)</li>
                <li><a href="https://railway.app/">Railway</a></li>
                <li><a href="https://render.com/">Render</a></li>
            </ul>
        </body>
        </html>
        '''
    }

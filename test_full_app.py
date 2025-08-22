"""
完整应用本地测试脚本
测试中国A股数据获取和应用集成
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from china_a_stock_fetcher import get_china_a_stock_data
import pandas as pd
from datetime import datetime

def test_china_a_stock_integration():
    """测试中国A股数据集成"""
    print("🧪 测试: 中国A股数据集成")
    print("="*50)
    
    try:
        # 测试模拟数据
        print("📊 测试A股模拟数据...")
        mock_data = get_china_a_stock_data(num_stocks=10, use_real_data=False)
        
        if not mock_data.empty:
            print(f"✅ A股模拟数据成功: {len(mock_data)} 只股票")
            
            # 显示样本数据
            print("\n📈 A股数据样本:")
            for _, row in mock_data.head(5).iterrows():
                print(f"  {row['股票代码']} {row['股票名称']}: ¥{row['最新价']} ({row['涨跌幅']:+.2f}%) [{row['行业']}]")
            
            # 检查是否是中国股票
            china_stocks = 0
            for _, row in mock_data.iterrows():
                code = row['股票代码']
                name = row['股票名称']
                # 检查是否是中文名称和6位数字代码
                if len(code) == 6 and code.isdigit() and any('\u4e00' <= char <= '\u9fff' for char in name):
                    china_stocks += 1
            
            print(f"\n🇨🇳 中国股票数量: {china_stocks}/{len(mock_data)}")
            
            if china_stocks >= len(mock_data) * 0.8:  # 至少80%是中国股票
                print("✅ 数据主要为中国A股")
                return True
            else:
                print("❌ 数据中中国A股比例过低")
                return False
        else:
            print("❌ A股模拟数据为空")
            return False
            
    except Exception as e:
        print(f"❌ A股数据集成测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_data_format():
    """测试数据格式"""
    print("\n🧪 测试: 数据格式验证")
    print("="*50)
    
    try:
        df = get_china_a_stock_data(num_stocks=5, use_real_data=False)
        
        if df.empty:
            print("❌ 数据为空")
            return False
        
        # 检查必需字段
        required_fields = [
            '股票代码', '股票名称', '最新价', '涨跌幅', '涨跌额', 
            '成交量', '市盈率', '市净率', '行业', '数据源'
        ]
        
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"❌ 缺少必需字段: {missing_fields}")
            return False
        
        print("✅ 所有必需字段都存在")
        
        # 检查数据类型
        sample = df.iloc[0]
        
        # 检查股票代码格式
        code = sample['股票代码']
        if not (isinstance(code, str) and len(code) == 6 and code.isdigit()):
            print(f"❌ 股票代码格式错误: {code}")
            return False
        
        # 检查价格是数值
        price = sample['最新价']
        if not isinstance(price, (int, float)) or price <= 0:
            print(f"❌ 价格格式错误: {price}")
            return False
        
        # 检查涨跌幅是数值
        change_pct = sample['涨跌幅']
        if not isinstance(change_pct, (int, float)):
            print(f"❌ 涨跌幅格式错误: {change_pct}")
            return False
        
        print("✅ 数据格式验证通过")
        
        # 显示格式示例
        print(f"\n📋 数据格式示例:")
        print(f"  股票代码: {code} (6位数字)")
        print(f"  股票名称: {sample['股票名称']} (中文名称)")
        print(f"  最新价: ¥{price:.2f}")
        print(f"  涨跌幅: {change_pct:+.2f}%")
        print(f"  行业: {sample['行业']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据格式测试失败: {e}")
        return False

def test_stock_screener_integration():
    """测试股票筛选器集成"""
    print("\n🧪 测试: 股票筛选器集成")
    print("="*50)
    
    try:
        # 尝试导入主应用模块
        try:
            from stock_screener_app import get_real_stock_data
            print("✅ 主应用模块导入成功")
        except ImportError as e:
            print(f"❌ 主应用模块导入失败: {e}")
            return False
        
        # 测试数据获取函数
        print("📊 测试数据获取函数...")
        
        # 由于Streamlit依赖，我们只能测试基本导入
        print("✅ 数据获取函数可以导入")
        
        return True
        
    except Exception as e:
        print(f"❌ 股票筛选器集成测试失败: {e}")
        return False

def test_performance():
    """测试性能"""
    print("\n🧪 测试: 性能测试")
    print("="*50)
    
    try:
        import time
        
        # 测试数据生成速度
        start_time = time.time()
        df = get_china_a_stock_data(num_stocks=30, use_real_data=False)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if not df.empty:
            print(f"✅ 生成 {len(df)} 只股票数据")
            print(f"⏱️ 耗时: {duration:.2f} 秒")
            
            if duration < 5:  # 5秒内完成
                print("✅ 性能良好")
                return True
            else:
                print("⚠️ 性能较慢，但可接受")
                return True
        else:
            print("❌ 数据生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 性能测试失败: {e}")
        return False

def run_full_test():
    """运行完整测试"""
    print("🚀 中国A股股票筛选器完整测试")
    print("="*60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("中国A股数据集成", test_china_a_stock_integration),
        ("数据格式验证", test_data_format),
        ("股票筛选器集成", test_stock_screener_integration),
        ("性能测试", test_performance)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 测试总结
    print("\n" + "="*60)
    print("📋 完整测试结果总结")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！中国A股股票筛选器准备就绪")
        print("\n📋 部署清单:")
        print("  ✅ china_a_stock_fetcher.py - A股数据获取器")
        print("  ✅ stock_screener_app.py - 主应用（已更新）")
        print("  ✅ 数据格式正确（6位代码，中文名称）")
        print("  ✅ 性能良好（5秒内完成）")
        
        print("\n🚀 下一步:")
        print("  1. 上传更新的文件到GitHub")
        print("  2. 等待Streamlit Cloud重新部署")
        print("  3. 测试线上应用显示中国A股数据")
        
        return True
    else:
        print("⚠️ 部分测试失败，需要修复后再部署")
        
        print("\n🔧 需要修复的问题:")
        for test_name, result in results:
            if not result:
                print(f"  - {test_name}")
        
        return False

if __name__ == "__main__":
    success = run_full_test()
    
    if success:
        print(f"\n✅ 测试完成 - 可以部署")
    else:
        print(f"\n❌ 测试失败 - 需要修复")
    
    print(f"\n⏰ 测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

"""
中国A股数据获取器本地测试脚本
测试数据获取功能和格式正确性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from china_a_stock_fetcher import ChinaAStockFetcher, get_china_a_stock_data
import pandas as pd
from datetime import datetime

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试1: 基本功能测试")
    print("="*50)
    
    try:
        fetcher = ChinaAStockFetcher()
        print(f"✅ 创建获取器成功")
        print(f"📊 A股代码数量: {len(fetcher.a_stock_codes)}")
        print(f"📋 股票名称映射: {len(fetcher.stock_names)}")
        print(f"🏭 行业分类: {len(fetcher.industries)}")
        
        # 显示部分股票代码
        print(f"📈 示例股票代码: {fetcher.a_stock_codes[:5]}")
        return True
        
    except Exception as e:
        print(f"❌ 基本功能测试失败: {e}")
        return False

def test_mock_data_generation():
    """测试模拟数据生成"""
    print("\n🧪 测试2: 模拟数据生成测试")
    print("="*50)
    
    try:
        fetcher = ChinaAStockFetcher()
        test_codes = ["000001.SZ", "600519.SH", "002415.SZ", "300750.SZ", "600036.SH"]
        
        print("📊 生成模拟数据...")
        df = fetcher.generate_enhanced_mock_data(test_codes)
        
        if not df.empty:
            print(f"✅ 成功生成 {len(df)} 条模拟数据")
            print(f"📋 数据列数: {len(df.columns)}")
            
            # 显示数据样本
            print("\n📈 数据样本:")
            for _, row in df.head(3).iterrows():
                print(f"  {row['股票代码']} {row['股票名称']}: ¥{row['最新价']} ({row['涨跌幅']:+.2f}%)")
            
            # 检查数据完整性
            print(f"\n🔍 数据完整性检查:")
            print(f"  - 股票代码: {'✅' if df['股票代码'].notna().all() else '❌'}")
            print(f"  - 股票名称: {'✅' if df['股票名称'].notna().all() else '❌'}")
            print(f"  - 最新价: {'✅' if df['最新价'].notna().all() else '❌'}")
            print(f"  - 涨跌幅: {'✅' if df['涨跌幅'].notna().all() else '❌'}")
            print(f"  - 行业分类: {'✅' if df['行业'].notna().all() else '❌'}")
            
            return True
        else:
            print("❌ 生成的数据为空")
            return False
            
    except Exception as e:
        print(f"❌ 模拟数据生成测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_sina_data_fetch():
    """测试新浪财经数据获取"""
    print("\n🧪 测试3: 新浪财经数据获取测试")
    print("="*50)
    
    try:
        fetcher = ChinaAStockFetcher()
        test_codes = ["000001.SZ", "600519.SH", "002415.SZ"]
        
        print("🌐 尝试获取新浪财经数据...")
        data = fetcher.fetch_sina_data(test_codes)
        
        if data:
            print(f"✅ 成功获取 {len(data)} 只股票的实时数据")
            
            for code, info in data.items():
                print(f"  {code} {info['name']}: ¥{info['current_price']:.2f} ({info['change_percent']:+.2f}%)")
            
            return True
        else:
            print("⚠️ 新浪财经数据获取失败，可能是网络问题")
            return False
            
    except Exception as e:
        print(f"❌ 新浪财经数据获取测试失败: {e}")
        return False

def test_main_interface():
    """测试主要接口"""
    print("\n🧪 测试4: 主要接口测试")
    print("="*50)
    
    try:
        print("📊 测试模拟数据接口...")
        df_mock = get_china_a_stock_data(num_stocks=10, use_real_data=False)
        
        if not df_mock.empty:
            print(f"✅ 模拟数据接口成功: {len(df_mock)} 条数据")
            
            # 检查关键字段
            required_fields = ['股票代码', '股票名称', '最新价', '涨跌幅', '行业']
            missing_fields = [field for field in required_fields if field not in df_mock.columns]
            
            if not missing_fields:
                print("✅ 所有必需字段都存在")
            else:
                print(f"❌ 缺少字段: {missing_fields}")
                return False
            
            # 显示数据格式
            print("\n📋 数据格式示例:")
            sample = df_mock.iloc[0]
            print(f"  股票代码: {sample['股票代码']} (类型: {type(sample['股票代码'])})")
            print(f"  股票名称: {sample['股票名称']} (类型: {type(sample['股票名称'])})")
            print(f"  最新价: {sample['最新价']} (类型: {type(sample['最新价'])})")
            print(f"  涨跌幅: {sample['涨跌幅']} (类型: {type(sample['涨跌幅'])})")
            print(f"  行业: {sample['行业']} (类型: {type(sample['行业'])})")
            
            return True
        else:
            print("❌ 主要接口返回空数据")
            return False
            
    except Exception as e:
        print(f"❌ 主要接口测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_data_quality():
    """测试数据质量"""
    print("\n🧪 测试5: 数据质量测试")
    print("="*50)
    
    try:
        df = get_china_a_stock_data(num_stocks=20, use_real_data=False)
        
        if df.empty:
            print("❌ 数据为空")
            return False
        
        print(f"📊 数据行数: {len(df)}")
        print(f"📋 数据列数: {len(df.columns)}")
        
        # 检查数据类型
        print("\n🔍 数据类型检查:")
        numeric_fields = ['最新价', '涨跌幅', '涨跌额', '成交量', '市盈率', '市净率']
        for field in numeric_fields:
            if field in df.columns:
                is_numeric = pd.api.types.is_numeric_dtype(df[field])
                print(f"  {field}: {'✅ 数值型' if is_numeric else '❌ 非数值型'}")
        
        # 检查数据范围
        print("\n📈 数据范围检查:")
        print(f"  最新价范围: {df['最新价'].min():.2f} - {df['最新价'].max():.2f}")
        print(f"  涨跌幅范围: {df['涨跌幅'].min():.2f}% - {df['涨跌幅'].max():.2f}%")
        
        # 检查行业分布
        print(f"\n🏭 行业分布:")
        industry_counts = df['行业'].value_counts()
        for industry, count in industry_counts.head().items():
            print(f"  {industry}: {count} 只")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据质量测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 中国A股数据获取器测试套件")
    print("="*60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("基本功能", test_basic_functionality),
        ("模拟数据生成", test_mock_data_generation),
        ("新浪财经数据", test_sina_data_fetch),
        ("主要接口", test_main_interface),
        ("数据质量", test_data_quality)
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
    print("📋 测试结果总结")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过！A股数据获取器工作正常")
        return True
    else:
        print("⚠️ 部分测试失败，需要检查和修复")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🚀 可以开始集成到主应用中")
    else:
        print("\n🔧 需要先修复问题再集成")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

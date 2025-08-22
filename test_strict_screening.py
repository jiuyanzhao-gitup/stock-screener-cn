"""
严格筛选器测试
验证每个筛选器的结果是否严格符合筛选标准
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_stock_screener import get_smart_screened_stocks, SmartStockScreener
import pandas as pd
from datetime import datetime

def test_momentum_breakout_strict():
    """严格测试动量突破筛选器"""
    print("🧪 严格测试: 🚀 动量突破筛选器")
    print("="*50)
    print("筛选标准: 涨跌幅>2%, RSI 50-80, 成交量比>1.5, 排除银行股")
    
    try:
        df = get_smart_screened_stocks("momentum_breakout", num_stocks=20, use_real_data=False)
        
        if df.empty:
            print("❌ 筛选结果为空")
            return False
        
        print(f"📊 筛选结果: {len(df)} 只股票")
        
        # 严格验证每个条件
        violations = []
        
        # 1. 检查涨跌幅 > 2%
        low_change = df[df["涨跌幅"] < 2]
        if not low_change.empty:
            violations.append(f"涨跌幅<2%: {len(low_change)}只")
            print("❌ 涨跌幅违规股票:")
            for _, row in low_change.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: {row['涨跌幅']:+.2f}%")
        
        # 2. 检查RSI 50-80
        bad_rsi = df[(df["RSI"] < 50) | (df["RSI"] > 80)]
        if not bad_rsi.empty:
            violations.append(f"RSI不在50-80: {len(bad_rsi)}只")
            print("❌ RSI违规股票:")
            for _, row in bad_rsi.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: RSI {row['RSI']:.1f}")
        
        # 3. 检查成交量比 > 1.5
        low_volume = df[df["成交量比"] < 1.5]
        if not low_volume.empty:
            violations.append(f"成交量比<1.5: {len(low_volume)}只")
            print("❌ 成交量比违规股票:")
            for _, row in low_volume.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: 成交量比 {row['成交量比']:.2f}")
        
        # 4. 检查是否排除银行股
        bank_stocks = df[df["行业"] == "银行"]
        if not bank_stocks.empty:
            violations.append(f"包含银行股: {len(bank_stocks)}只")
            print("❌ 银行股违规:")
            for _, row in bank_stocks.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: {row['行业']}")
        
        # 总结
        if not violations:
            print("✅ 所有股票都符合筛选标准")
            print("📈 符合标准的股票样本:")
            for _, row in df.head(3).iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: {row['涨跌幅']:+.2f}%, RSI {row['RSI']:.1f}, 成交量比 {row['成交量比']:.2f}")
            return True
        else:
            print(f"❌ 发现 {len(violations)} 类违规:")
            for v in violations:
                print(f"   - {v}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_oversold_rebound_strict():
    """严格测试超跌反弹筛选器"""
    print("\n🧪 严格测试: 🔄 超跌反弹筛选器")
    print("="*50)
    print("筛选标准: RSI 20-45, 涨跌幅 -15%到0%, 成交量比>1.2")
    
    try:
        df = get_smart_screened_stocks("oversold_rebound", num_stocks=20, use_real_data=False)
        
        if df.empty:
            print("❌ 筛选结果为空")
            return False
        
        print(f"📊 筛选结果: {len(df)} 只股票")
        
        violations = []
        
        # 1. 检查RSI 20-45
        bad_rsi = df[(df["RSI"] < 20) | (df["RSI"] > 45)]
        if not bad_rsi.empty:
            violations.append(f"RSI不在20-45: {len(bad_rsi)}只")
            print("❌ RSI违规股票:")
            for _, row in bad_rsi.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: RSI {row['RSI']:.1f}")

        # 2. 检查涨跌幅 -15%到0%
        bad_change = df[(df["涨跌幅"] > 0) | (df["涨跌幅"] < -15)]
        if not bad_change.empty:
            violations.append(f"涨跌幅不在-15%到0%: {len(bad_change)}只")
            print("❌ 涨跌幅违规股票:")
            for _, row in bad_change.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: {row['涨跌幅']:+.2f}%")

        # 3. 检查成交量比 > 1.2
        low_volume = df[df["成交量比"] < 1.2]
        if not low_volume.empty:
            violations.append(f"成交量比<1.2: {len(low_volume)}只")
        
        if not violations:
            print("✅ 所有股票都符合筛选标准")
            return True
        else:
            print(f"❌ 发现 {len(violations)} 类违规:")
            for v in violations:
                print(f"   - {v}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_dividend_stable_strict():
    """严格测试稳健分红筛选器"""
    print("\n🧪 严格测试: 🏦 稳健分红筛选器")
    print("="*50)
    print("筛选标准: 股息率>2%, ROE 8-35%, 市盈率 3-25%, 资产负债率 15-70%")
    
    try:
        df = get_smart_screened_stocks("dividend_stable", num_stocks=20, use_real_data=False)
        
        if df.empty:
            print("❌ 筛选结果为空")
            return False
        
        print(f"📊 筛选结果: {len(df)} 只股票")
        
        violations = []
        
        # 1. 检查股息率 > 2%
        low_dividend = df[df["股息率"] < 2]
        if not low_dividend.empty:
            violations.append(f"股息率<2%: {len(low_dividend)}只")
            print("❌ 股息率违规股票:")
            for _, row in low_dividend.iterrows():
                print(f"   {row['股票代码']} {row['股票名称']}: 股息率 {row['股息率']:.2f}%")

        # 2. 检查ROE 8-35%
        bad_roe = df[(df["ROE"] < 8) | (df["ROE"] > 35)]
        if not bad_roe.empty:
            violations.append(f"ROE不在8-35%: {len(bad_roe)}只")

        # 3. 检查市盈率 3-25
        bad_pe = df[(df["市盈率"] < 3) | (df["市盈率"] > 25)]
        if not bad_pe.empty:
            violations.append(f"市盈率不在3-25: {len(bad_pe)}只")
        
        if not violations:
            print("✅ 所有股票都符合筛选标准")
            return True
        else:
            print(f"❌ 发现 {len(violations)} 类违规:")
            for v in violations:
                print(f"   - {v}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_all_screeners_strict():
    """严格测试所有筛选器"""
    print("🔍 严格筛选器标准验证")
    print("="*60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("动量突破筛选器", test_momentum_breakout_strict),
        ("超跌反弹筛选器", test_oversold_rebound_strict),
        ("稳健分红筛选器", test_dividend_stable_strict),
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
    print("📋 严格筛选器测试总结")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 筛选器通过严格测试")
    
    if passed == len(results):
        print("🎉 所有筛选器都严格符合标准！")
        return True
    else:
        print("⚠️ 部分筛选器不符合标准，需要修复")
        return False

if __name__ == "__main__":
    success = test_all_screeners_strict()
    
    if success:
        print(f"\n✅ 严格测试通过 - 筛选器符合标准")
    else:
        print(f"\n❌ 严格测试失败 - 需要修复筛选逻辑")
    
    print(f"\n⏰ 测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

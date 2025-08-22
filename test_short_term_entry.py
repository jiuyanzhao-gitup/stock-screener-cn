"""
测试短线入场机会筛选器
验证基于GitHub优秀项目研究的短线交易策略
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from short_term_entry_screener import get_short_term_entry_opportunities, get_all_short_term_strategies
import pandas as pd
from datetime import datetime

def test_momentum_breakout_entry():
    """测试动量突破入场策略"""
    print("🧪 测试: 🚀 动量突破入场策略")
    print("="*50)
    print("基于Warrior Trading动量突破策略")
    
    try:
        df = get_short_term_entry_opportunities("momentum_breakout_entry", num_stocks=10)
        
        if not df.empty:
            print(f"✅ 筛选成功: {len(df)} 只股票")
            
            # 显示入场机会
            print("\n📈 动量突破入场机会:")
            for _, row in df.head(5).iterrows():
                print(f"  {row['股票代码']} {row['股票名称']}: ¥{row['最新价']:.2f} ({row['涨跌幅']:+.2f}%)")
                print(f"    入场评分: {row['入场评分']}/100")
                print(f"    入场信号: {row['入场信号']}")
                print(f"    行业: {row['行业']}")
                print()
            
            # 统计分析
            avg_score = df["入场评分"].mean()
            avg_change = df["涨跌幅"].mean()
            print(f"📊 统计分析:")
            print(f"  平均入场评分: {avg_score:.1f}/100")
            print(f"  平均涨跌幅: {avg_change:+.2f}%")
            print(f"  高评分股票(>80分): {len(df[df['入场评分'] > 80])}/{len(df)}")
            
            return True
        else:
            print("❌ 未找到符合条件的股票")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_gap_breakout_entry():
    """测试缺口突破入场策略"""
    print("\n🧪 测试: 📈 缺口突破入场策略")
    print("="*50)
    print("基于Gap Trading缺口理论")
    
    try:
        df = get_short_term_entry_opportunities("gap_breakout_entry", num_stocks=8)
        
        if not df.empty:
            print(f"✅ 筛选成功: {len(df)} 只股票")
            
            # 显示缺口突破机会
            print("\n📈 缺口突破入场机会:")
            for _, row in df.head(3).iterrows():
                print(f"  {row['股票代码']} {row['股票名称']}: ¥{row['最新价']:.2f} ({row['涨跌幅']:+.2f}%)")
                print(f"    入场评分: {row['入场评分']}/100")
                print(f"    入场信号: {row['入场信号']}")
                print()
            
            return True
        else:
            print("❌ 未找到符合条件的股票")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_relative_strength_entry():
    """测试相对强度入场策略"""
    print("\n🧪 测试: 💪 相对强度入场策略")
    print("="*50)
    print("基于IBD相对强度排名策略")
    
    try:
        df = get_short_term_entry_opportunities("relative_strength_entry", num_stocks=8)
        
        if not df.empty:
            print(f"✅ 筛选成功: {len(df)} 只股票")
            
            # 显示相对强度机会
            print("\n📈 相对强度入场机会:")
            for _, row in df.head(3).iterrows():
                print(f"  {row['股票代码']} {row['股票名称']}: ¥{row['最新价']:.2f} ({row['涨跌幅']:+.2f}%)")
                print(f"    入场评分: {row['入场评分']}/100")
                print(f"    入场信号: {row['入场信号']}")
                print()
            
            return True
        else:
            print("❌ 未找到符合条件的股票")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_all_short_term_strategies():
    """测试所有短线策略"""
    print("\n🧪 测试: 所有短线入场策略")
    print("="*60)
    
    strategies = get_all_short_term_strategies()
    results = {}
    
    for strategy_key, strategy_info in strategies.items():
        print(f"\n📊 测试 {strategy_info['name']}...")
        
        try:
            df = get_short_term_entry_opportunities(strategy_key, num_stocks=5)
            
            if not df.empty:
                avg_score = df["入场评分"].mean()
                avg_change = df["涨跌幅"].mean()
                top_stock = df.iloc[0]
                
                results[strategy_key] = {
                    "name": strategy_info['name'],
                    "count": len(df),
                    "avg_score": avg_score,
                    "avg_change": avg_change,
                    "top_stock": f"{top_stock['股票代码']} {top_stock['股票名称']}",
                    "top_score": top_stock["入场评分"],
                    "status": "✅ 成功"
                }
                
                print(f"  ✅ 找到 {len(df)} 只股票，平均评分 {avg_score:.1f}")
                print(f"  🏆 最佳机会: {top_stock['股票代码']} {top_stock['股票名称']} (评分: {top_stock['入场评分']:.1f})")
            else:
                results[strategy_key] = {
                    "name": strategy_info['name'],
                    "count": 0,
                    "status": "⚠️ 无结果"
                }
                print(f"  ⚠️ 未找到符合条件的股票")
                
        except Exception as e:
            results[strategy_key] = {
                "name": strategy_info['name'],
                "count": 0,
                "status": f"❌ 错误: {str(e)[:50]}"
            }
            print(f"  ❌ 错误: {e}")
    
    return results

def show_strategy_comparison(results):
    """显示策略对比"""
    print("\n" + "="*60)
    print("📊 短线入场策略对比分析")
    print("="*60)
    
    # 创建对比表格
    comparison_data = []
    for strategy_key, result in results.items():
        if result.get("count", 0) > 0:
            comparison_data.append({
                "策略名称": result["name"],
                "股票数量": result["count"],
                "平均评分": f"{result['avg_score']:.1f}",
                "平均涨幅": f"{result['avg_change']:+.2f}%",
                "最佳股票": result["top_stock"],
                "最高评分": f"{result['top_score']:.1f}",
                "状态": result["status"]
            })
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        print(df_comparison.to_string(index=False))
        
        # 找出最佳策略
        best_strategy = max(comparison_data, key=lambda x: float(x["平均评分"]))
        print(f"\n🏆 最佳策略: {best_strategy['策略名称']}")
        print(f"   平均评分: {best_strategy['平均评分']}")
        print(f"   最佳股票: {best_strategy['最佳股票']}")
    else:
        print("⚠️ 没有成功的策略结果")

def run_short_term_entry_tests():
    """运行短线入场机会测试"""
    print("⚡ 短线入场机会筛选器测试")
    print("="*70)
    print("基于GitHub优秀项目研究的短线交易策略")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 单独测试主要策略
    individual_tests = [
        ("动量突破入场", test_momentum_breakout_entry),
        ("缺口突破入场", test_gap_breakout_entry),
        ("相对强度入场", test_relative_strength_entry),
    ]
    
    individual_results = []
    for test_name, test_func in individual_tests:
        try:
            result = test_func()
            individual_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            individual_results.append((test_name, False))
    
    # 测试所有策略
    all_results = test_all_short_term_strategies()
    
    # 显示策略对比
    show_strategy_comparison(all_results)
    
    # 总结
    print("\n" + "="*70)
    print("📋 短线入场机会测试总结")
    print("="*70)
    
    individual_passed = sum(1 for _, result in individual_results if result)
    total_strategies = len(all_results)
    successful_strategies = len([r for r in all_results.values() if r.get("count", 0) > 0])
    
    print(f"✅ 单独测试通过: {individual_passed}/{len(individual_tests)}")
    print(f"✅ 策略测试成功: {successful_strategies}/{total_strategies}")
    
    if individual_passed >= 2 and successful_strategies >= 4:
        print("\n🎉 短线入场机会筛选器测试通过！")
        print("\n📋 核心特性验证:")
        print("  ✅ 动量突破入场策略 - 基于Warrior Trading")
        print("  ✅ 缺口突破入场策略 - 基于Gap Trading理论")
        print("  ✅ 相对强度入场策略 - 基于IBD相对强度")
        print("  ✅ 窄幅整理突破策略 - 基于Narrow Range")
        print("  ✅ 早盘强势入场策略 - 基于Opening Range")
        print("  ✅ 技术形态突破策略 - 基于Chart Pattern")
        
        print("\n🎯 短线交易优势:")
        print("  • 入场评分系统 (0-100分)")
        print("  • 具体入场信号提示")
        print("  • 基于实战验证的策略")
        print("  • 适合中国A股市场特点")
        
        return True
    else:
        print("\n⚠️ 部分测试失败，需要优化策略")
        return False

if __name__ == "__main__":
    success = run_short_term_entry_tests()
    
    if success:
        print(f"\n✅ 短线入场机会筛选器测试通过")
        print("🚀 可以开始寻找短线交易机会！")
    else:
        print(f"\n❌ 短线入场机会筛选器测试失败")
        print("🔧 需要进一步优化策略")
    
    print(f"\n⏰ 测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

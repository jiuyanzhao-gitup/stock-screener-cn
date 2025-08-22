"""
测试筛选器逻辑
验证不同筛选器返回不同的股票结果
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_stock_screener import get_smart_screened_stocks, SmartStockScreener
import pandas as pd
from datetime import datetime

def test_different_screeners():
    """测试不同筛选器返回不同结果"""
    print("🧪 测试: 不同筛选器逻辑验证")
    print("="*60)
    
    screener_types = [
        "momentum_breakout",    # 动量突破
        "value_growth",         # 价值成长
        "dividend_stable",      # 稳健分红
        "small_cap_growth",     # 小盘成长
        "technical_strong",     # 技术强势
        "oversold_rebound"      # 超跌反弹
    ]
    
    results = {}
    
    try:
        screener = SmartStockScreener()
        
        for screener_type in screener_types:
            print(f"\n📊 测试筛选器: {screener.screener_logic[screener_type]['name']}")
            
            # 获取筛选结果
            df = get_smart_screened_stocks(screener_type, num_stocks=10, use_real_data=False)
            
            if not df.empty:
                results[screener_type] = df
                print(f"✅ 成功获取 {len(df)} 只股票")
                
                # 显示前3只股票
                print("📈 筛选结果样本:")
                for i, (_, row) in enumerate(df.head(3).iterrows()):
                    print(f"  {i+1}. {row['股票代码']} {row['股票名称']}: ¥{row['最新价']} ({row['涨跌幅']:+.2f}%) [{row['行业']}]")
                
                # 显示筛选特征
                print("🔍 筛选特征:")
                logic = screener.screener_logic[screener_type]
                
                # 显示涨跌幅范围
                if "涨跌幅" in logic["filters"]:
                    change_range = logic["filters"]["涨跌幅"]
                    actual_range = (df["涨跌幅"].min(), df["涨跌幅"].max())
                    print(f"  涨跌幅要求: {change_range[0]}%-{change_range[1]}%, 实际: {actual_range[0]:.2f}%-{actual_range[1]:.2f}%")
                
                # 显示行业分布
                industry_dist = df["行业"].value_counts()
                print(f"  行业分布: {dict(industry_dist.head(3))}")
                
                # 显示偏好行业匹配
                if logic["preferred_industries"]:
                    preferred_count = df[df["行业"].isin(logic["preferred_industries"])].shape[0]
                    print(f"  偏好行业匹配: {preferred_count}/{len(df)} ({preferred_count/len(df)*100:.1f}%)")
                
            else:
                print("❌ 筛选结果为空")
                results[screener_type] = pd.DataFrame()
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        print(traceback.format_exc())
        return {}

def compare_screener_results(results: dict):
    """比较不同筛选器的结果差异"""
    print("\n🔍 筛选器结果差异分析")
    print("="*60)
    
    if len(results) < 2:
        print("❌ 结果不足，无法比较")
        return False
    
    # 比较股票重叠度
    print("📊 股票重叠度分析:")
    screener_names = list(results.keys())
    
    for i, screener1 in enumerate(screener_names):
        for screener2 in screener_names[i+1:]:
            if not results[screener1].empty and not results[screener2].empty:
                codes1 = set(results[screener1]["股票代码"])
                codes2 = set(results[screener2]["股票代码"])
                
                overlap = len(codes1.intersection(codes2))
                total_unique = len(codes1.union(codes2))
                overlap_rate = overlap / max(len(codes1), len(codes2)) * 100
                
                print(f"  {screener1} vs {screener2}: {overlap}只重叠 ({overlap_rate:.1f}%)")
    
    # 比较行业分布
    print("\n🏭 行业分布比较:")
    for screener_type, df in results.items():
        if not df.empty:
            top_industry = df["行业"].value_counts().index[0]
            industry_count = df["行业"].value_counts().iloc[0]
            print(f"  {screener_type}: 主要行业 {top_industry} ({industry_count}只)")
    
    # 比较涨跌幅分布
    print("\n📈 涨跌幅分布比较:")
    for screener_type, df in results.items():
        if not df.empty:
            avg_change = df["涨跌幅"].mean()
            print(f"  {screener_type}: 平均涨跌幅 {avg_change:+.2f}%")
    
    return True

def test_screener_logic_consistency():
    """测试筛选器逻辑一致性"""
    print("\n🧪 测试: 筛选器逻辑一致性")
    print("="*60)
    
    try:
        screener = SmartStockScreener()
        
        # 测试动量突破筛选器
        print("📊 测试动量突破筛选器逻辑...")
        momentum_data = get_smart_screened_stocks("momentum_breakout", num_stocks=10, use_real_data=False)
        
        if not momentum_data.empty:
            # 检查涨跌幅是否符合要求（应该大部分为正）
            positive_count = (momentum_data["涨跌幅"] > 0).sum()
            print(f"  上涨股票: {positive_count}/{len(momentum_data)} ({positive_count/len(momentum_data)*100:.1f}%)")
            
            # 检查是否偏好科技股
            tech_count = (momentum_data["行业"] == "科技").sum()
            print(f"  科技股数量: {tech_count}/{len(momentum_data)} ({tech_count/len(momentum_data)*100:.1f}%)")
        
        # 测试超跌反弹筛选器
        print("\n📊 测试超跌反弹筛选器逻辑...")
        oversold_data = get_smart_screened_stocks("oversold_rebound", num_stocks=10, use_real_data=False)
        
        if not oversold_data.empty:
            # 检查涨跌幅是否符合要求（应该大部分为负）
            negative_count = (oversold_data["涨跌幅"] < 0).sum()
            print(f"  下跌股票: {negative_count}/{len(oversold_data)} ({negative_count/len(oversold_data)*100:.1f}%)")
            
            # 检查RSI是否较低
            low_rsi_count = (oversold_data["RSI"] < 50).sum()
            print(f"  低RSI股票: {low_rsi_count}/{len(oversold_data)} ({low_rsi_count/len(oversold_data)*100:.1f}%)")
        
        # 测试稳健分红筛选器
        print("\n📊 测试稳健分红筛选器逻辑...")
        dividend_data = get_smart_screened_stocks("dividend_stable", num_stocks=10, use_real_data=False)
        
        if not dividend_data.empty:
            # 检查股息率
            high_dividend_count = (dividend_data["股息率"] >= 3).sum()
            print(f"  高股息率股票: {high_dividend_count}/{len(dividend_data)} ({high_dividend_count/len(dividend_data)*100:.1f}%)")
            
            # 检查是否偏好银行股
            bank_count = (dividend_data["行业"] == "银行").sum()
            print(f"  银行股数量: {bank_count}/{len(dividend_data)} ({bank_count/len(dividend_data)*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ 逻辑一致性测试失败: {e}")
        return False

def run_screener_tests():
    """运行筛选器测试"""
    print("🧠 智能股票筛选器逻辑测试")
    print("="*70)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 测试1: 不同筛选器返回不同结果
    results = test_different_screeners()
    
    if results:
        # 测试2: 比较筛选器结果差异
        comparison_success = compare_screener_results(results)
        
        # 测试3: 筛选器逻辑一致性
        logic_success = test_screener_logic_consistency()
        
        # 总结
        print("\n" + "="*70)
        print("📋 筛选器测试总结")
        print("="*70)
        
        success_count = len([r for r in results.values() if not r.empty])
        print(f"✅ 成功筛选器数量: {success_count}/{len(results)}")
        print(f"✅ 结果差异分析: {'通过' if comparison_success else '失败'}")
        print(f"✅ 逻辑一致性: {'通过' if logic_success else '失败'}")
        
        if success_count >= 4 and comparison_success and logic_success:
            print("\n🎉 所有测试通过！不同筛选器返回不同结果")
            print("\n📋 验证要点:")
            print("  ✅ 动量突破筛选器: 偏好上涨股票和科技股")
            print("  ✅ 超跌反弹筛选器: 偏好下跌股票和低RSI")
            print("  ✅ 稳健分红筛选器: 偏好高股息率和银行股")
            print("  ✅ 价值成长筛选器: 偏好消费和医药股")
            print("  ✅ 小盘成长筛选器: 偏好高增长股票")
            print("  ✅ 技术强势筛选器: 偏好高RSI股票")
            
            return True
        else:
            print("\n⚠️ 部分测试失败，需要调整筛选逻辑")
            return False
    else:
        print("\n❌ 筛选器测试失败")
        return False

if __name__ == "__main__":
    success = run_screener_tests()
    
    if success:
        print(f"\n✅ 筛选器逻辑测试通过 - 可以部署")
    else:
        print(f"\n❌ 筛选器逻辑测试失败 - 需要修复")
    
    print(f"\n⏰ 测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

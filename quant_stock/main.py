"""
A-Stock Quant System - Main Entry
"""

import argparse
import pandas as pd
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.data_fetcher import DataFetcher
from indicators.technical import TechnicalIndicators
from strategies.selector import get_selector


def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("        A-Stock Quant System v1.0")
    print("        Professional & Smart")
    print("=" * 60)
    print()


def analyze_single_stock(code: str, fetcher: DataFetcher):
    """Analyze single stock"""
    print(f"\n{'='*60}")
    print(f"Stock Analysis: {code}")
    print(f"{'='*60}")
    
    # Get data
    df = fetcher.get_daily_data(code)
    if len(df) == 0:
        print("Failed to fetch data")
        return
    
    # Calculate indicators
    df = TechnicalIndicators.calculate_all(df)
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # Basic info
    print(f"\n[Basic Data] (As of {df['date'].iloc[-1].strftime('%Y-%m-%d')})")
    print(f"   Close:    {latest['close']:.2f}")
    print(f"   Change:   {latest.get('pct_change', 0):.2f}%")
    print(f"   Volume:   {latest.get('volume', 0):,.0f}")
    
    # Moving averages
    print(f"\n[Moving Averages]")
    print(f"   MA5:  {latest.get('MA5', 0):.2f}")
    print(f"   MA10: {latest.get('MA10', 0):.2f}")
    print(f"   MA20: {latest.get('MA20', 0):.2f}")
    print(f"   MA60: {latest.get('MA60', 0):.2f}")
    
    # Trend judgment
    if (latest.get('MA5', 0) > latest.get('MA10', 0) > 
        latest.get('MA20', 0) > latest.get('MA60', 0)):
        print("   [OK] Bullish Alignment")
    elif (latest.get('MA5', 0) < latest.get('MA10', 0) < 
          latest.get('MA20', 0) < latest.get('MA60', 0)):
        print("   [X] Bearish Alignment")
    else:
        print("   [!] Mixed Alignment")
    
    # MACD
    print(f"\n[MACD Indicator]")
    print(f"   DIF:   {latest.get('DIF', 0):.4f}")
    print(f"   DEA:   {latest.get('DEA', 0):.4f}")
    print(f"   MACD:  {latest.get('MACD', 0):.4f}")
    
    if latest.get('DIF', 0) > latest.get('DEA', 0):
        if prev.get('DIF', 0) <= prev.get('DEA', 0):
            print("   [OK] Golden Cross (New)")
        else:
            print("   [OK] Golden Cross State")
    else:
        if prev.get('DIF', 0) >= prev.get('DEA', 0):
            print("   [X] Dead Cross (New)")
        else:
            print("   [X] Dead Cross State")
    
    # KDJ
    print(f"\n[KDJ Indicator]")
    print(f"   K: {latest.get('K', 0):.2f}")
    print(f"   D: {latest.get('D', 0):.2f}")
    print(f"   J: {latest.get('J', 0):.2f}")
    
    if latest.get('K', 0) > 80:
        print("   [!] Overbought Zone")
    elif latest.get('K', 0) < 20:
        print("   [OK] Oversold Zone")
    
    # RSI
    print(f"\n[RSI Indicator]")
    print(f"   RSI6:  {latest.get('RSI6', 0):.2f}")
    print(f"   RSI12: {latest.get('RSI12', 0):.2f}")
    print(f"   RSI24: {latest.get('RSI24', 0):.2f}")
    
    # Bollinger Bands
    print(f"\n[Bollinger Bands]")
    print(f"   Upper: {latest.get('BOLL_UPPER', 0):.2f}")
    print(f"   Mid:   {latest.get('BOLL_MID', 0):.2f}")
    print(f"   Lower: {latest.get('BOLL_LOWER', 0):.2f}")
    
    if latest['close'] > latest.get('BOLL_UPPER', 0):
        print("   [!] Above Upper Band (Possible Overbought)")
    elif latest['close'] < latest.get('BOLL_LOWER', 0):
        print("   [OK] Below Lower Band (Possible Oversold)")
    
    # Trading suggestions
    print(f"\n[Trading Suggestions]")
    
    # Support levels
    support_short = df['low'].iloc[-5:].min()
    support_mid = df['low'].iloc[-20:].min()
    print(f"   Support:  {support_short:.2f} (Short), {support_mid:.2f} (Mid)")
    
    # Resistance levels
    resistance_short = df['high'].iloc[-5:].max()
    resistance_mid = df['high'].iloc[-20:].max()
    print(f"   Resist:   {resistance_short:.2f} (Short), {resistance_mid:.2f} (Mid)")
    
    # Stop loss
    stop_loss = latest['close'] * 0.95
    print(f"   StopLoss: {stop_loss:.2f} (-5%)")
    
    # Overall score
    score = 0
    reasons = []
    
    if latest.get('MA5', 0) > latest.get('MA10', 0):
        score += 1
        reasons.append("MA5>MA10")
    if latest.get('DIF', 0) > latest.get('DEA', 0):
        score += 1
        reasons.append("MACD Golden")
    if latest.get('K', 0) > latest.get('D', 0):
        score += 1
        reasons.append("KDJ Golden")
    if latest['close'] > latest.get('MA20', 0):
        score += 1
        reasons.append("Above MA20")
    if latest.get('volume', 0) > df['volume'].iloc[-10:].mean():
        score += 1
        reasons.append("Volume Up")
    
    print(f"\n[Overall Score]: {score}/5")
    if reasons:
        print(f"   Reasons: {', '.join(reasons)}")
    
    if score >= 4:
        print(f"   [OK] Suggestion: Consider Entry")
    elif score >= 2:
        print(f"   [-] Suggestion: Wait & See")
    else:
        print(f"   [X] Suggestion: Avoid")


def run_screening(strategy: str, top_n: int, fetcher: DataFetcher):
    """Run stock screening"""
    print(f"\n[Running Strategy]: {strategy}")
    print(f"[Top N]: {top_n}")
    print()
    
    selector = get_selector(strategy)
    result = selector.select(top_n=top_n)
    
    if len(result) == 0:
        print("[X] No stocks match criteria")
        return
    
    print(f"[OK] Found {len(result)} matching stocks:\n")
    
    # Format output
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(result.to_string(index=False))
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "quant_stock/output"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/selection_{strategy}_{timestamp}.csv"
    result.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n[Saved] Results saved to: {filename}")


def interactive_mode(fetcher: DataFetcher):
    """Interactive mode"""
    print("\n[Interactive Mode]")
    print("Commands:")
    print("  analyze <code>  - Analyze single stock")
    print("  screen <strategy> - Screen stocks (breakout/trend)")
    print("  help            - Show help")
    print("  quit            - Exit")
    print()
    
    while True:
        try:
            cmd = input(">>> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split()
            action = parts[0].lower()
            
            if action == 'quit' or action == 'exit':
                print("[Bye]!")
                break
            
            elif action == 'analyze' and len(parts) >= 2:
                code = parts[1]
                analyze_single_stock(code, fetcher)
            
            elif action == 'screen' and len(parts) >= 2:
                strategy = parts[1]
                run_screening(strategy, 10, fetcher)
            
            elif action == 'help':
                print("\nAvailable strategies:")
                print("  breakout - Breakout strategy (Short-term)")
                print("  trend    - Trend strategy (Mid-term)")
                print("  value    - Value strategy (Long-term)")
                print()
            
            else:
                print("[X] Unknown command, type 'help' for help")
        
        except KeyboardInterrupt:
            print("\n[Bye]!")
            break
        except Exception as e:
            print(f"[X] Error: {e}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='A-Stock Quant System')
    parser.add_argument('--strategy', '-s', type=str, default='breakout',
                       choices=['breakout', 'trend', 'value'],
                       help='Screening strategy (default: breakout)')
    parser.add_argument('--top', '-t', type=int, default=10,
                       help='Number of stocks to return (default: 10)')
    parser.add_argument('--analyze', '-a', type=str,
                       help='Analyze single stock code')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Initialize data fetcher
    fetcher = DataFetcher()
    
    # Create output directory
    os.makedirs('quant_stock/output', exist_ok=True)
    
    if args.analyze:
        # Analyze single stock
        analyze_single_stock(args.analyze, fetcher)
    
    elif args.interactive:
        # Interactive mode
        interactive_mode(fetcher)
    
    else:
        # Run screening
        run_screening(args.strategy, args.top, fetcher)


if __name__ == "__main__":
    main()

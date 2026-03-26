"""
A-Stock Quant Analysis Web App
股票量化分析Web界面
使用 Streamlit + Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import baostock as bs
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="A-Stock Quant Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .positive {
        color: #ff4b4b;
    }
    .negative {
        color: #00cc00;
    }
</style>
""", unsafe_allow_html=True)


def get_stock_data(stock_code, days=120):
    """Get stock data from baostock"""
    lg = bs.login()
    if lg.error_code != '0':
        st.error(f"Login failed: {lg.error_msg}")
        return None
    
    # Format code
    if stock_code.startswith('6'):
        bs_code = f"{stock_code}.sh"
    else:
        bs_code = f"{stock_code}.sz"
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    rs = bs.query_history_k_data_plus(
        bs_code,
        "date,open,high,low,close,volume",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3"
    )
    
    data_list = []
    while (rs.error_code == '0') and rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if len(data_list) == 0:
        return None
    
    df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()
    
    return df.sort_values('date').reset_index(drop=True)


def calculate_indicators(df):
    """Calculate technical indicators"""
    # Moving averages
    for period in [5, 10, 20, 60]:
        df[f'MA{period}'] = df['close'].rolling(window=period).mean()
    
    # MACD
    ema_fast = df['close'].ewm(span=12, adjust=False).mean()
    ema_slow = df['close'].ewm(span=26, adjust=False).mean()
    df['DIF'] = ema_fast - ema_slow
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
    df['MACD'] = (df['DIF'] - df['DEA']) * 2
    
    # KDJ
    lowest_low = df['low'].rolling(window=9).min()
    highest_high = df['high'].rolling(window=9).max()
    df['RSV'] = (df['close'] - lowest_low) / (highest_high - lowest_low) * 100
    df['K'] = df['RSV'].ewm(com=2, adjust=False).mean()
    df['D'] = df['K'].ewm(com=2, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    # RSI
    for period in [6, 12, 24]:
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        df[f'RSI{period}'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BOLL_MID'] = df['close'].rolling(window=20).mean()
    std = df['close'].rolling(window=20).std()
    df['BOLL_UPPER'] = df['BOLL_MID'] + 2 * std
    df['BOLL_LOWER'] = df['BOLL_MID'] - 2 * std
    
    return df


def create_candlestick_chart(df):
    """Create candlestick chart with indicators"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=('Price & Moving Averages', 'MACD', 'Volume')
    )
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='K-Line'
        ),
        row=1, col=1
    )
    
    # Moving averages
    colors = {'MA5': '#FFA500', 'MA10': '#0000FF', 'MA20': '#800080', 'MA60': '#008000'}
    for ma in ['MA5', 'MA10', 'MA20', 'MA60']:
        fig.add_trace(
            go.Scatter(x=df['date'], y=df[ma], name=ma, line=dict(color=colors[ma], width=1)),
            row=1, col=1
        )
    
    # Bollinger Bands
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['BOLL_UPPER'], name='BOLL Upper', 
                   line=dict(color='gray', width=1, dash='dash')),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['BOLL_LOWER'], name='BOLL Lower',
                   line=dict(color='gray', width=1, dash='dash'),
                   fill='tonexty', fillcolor='rgba(128,128,128,0.1)'),
        row=1, col=1
    )
    
    # MACD
    fig.add_trace(go.Bar(x=df['date'], y=df['MACD'], name='MACD', marker_color='blue'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['DIF'], name='DIF', line=dict(color='orange')), row=2, col=1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['DEA'], name='DEA', line=dict(color='purple')), row=2, col=1)
    
    # Volume
    colors_vol = ['red' if df['close'].iloc[i] >= df['open'].iloc[i] else 'green' 
                  for i in range(len(df))]
    fig.add_trace(
        go.Bar(x=df['date'], y=df['volume'], name='Volume', marker_color=colors_vol),
        row=3, col=1
    )
    
    fig.update_layout(
        height=800,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        title_text="Technical Analysis Chart",
        title_x=0.5
    )
    
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="Volume", row=3, col=1)
    
    return fig


def calculate_score(df):
    """Calculate overall score"""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    score = 0
    reasons = []
    
    if latest['MA5'] > latest['MA10']:
        score += 1
        reasons.append("MA5>MA10")
    if latest['DIF'] > latest['DEA']:
        score += 1
        reasons.append("MACD Golden")
    if latest['K'] > latest['D']:
        score += 1
        reasons.append("KDJ Golden")
    if latest['close'] > latest['MA20']:
        score += 1
        reasons.append("Above MA20")
    if latest['volume'] > df['volume'].iloc[-10:].mean():
        score += 1
        reasons.append("Volume Up")
    
    return score, reasons


def main():
    # Header
    st.markdown('<h1 class="main-header">📈 A-Stock Quant Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional Technical Analysis for A-Share Stocks</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    stock_code = st.sidebar.text_input("Stock Code", value="002969", 
                                        help="Enter stock code (e.g., 000001 for Ping An Bank)")
    
    stock_name = st.sidebar.text_input("Stock Name (Optional)", value="JiaMei Packaging")
    
    days = st.sidebar.slider("Analysis Period (Days)", min_value=30, max_value=365, value=120)
    
    analyze_btn = st.sidebar.button("🔍 Analyze", type="primary")
    
    # About section
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **About:**
    This tool provides technical analysis for A-share stocks using:
    - Real data from Baostock
    - Moving Averages (MA5/10/20/60)
    - MACD, KDJ, RSI indicators
    - Bollinger Bands
    
    **Disclaimer:** For reference only, not investment advice!
    """)
    
    # Main content
    if analyze_btn or stock_code:
        with st.spinner("📊 Fetching data and calculating indicators..."):
            df = get_stock_data(stock_code, days)
            
            if df is None or len(df) == 0:
                st.error(f"❌ Failed to fetch data for {stock_code}. Please check the stock code.")
                return
            
            df = calculate_indicators(df)
        
        # Latest data
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        change = (latest['close'] - prev['close']) / prev['close'] * 100
        
        # Metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Close Price", f"{latest['close']:.2f}", f"{change:+.2f}%")
        
        with col2:
            st.metric("Volume", f"{latest['volume']/1e8:.2f}亿")
        
        with col3:
            st.metric("MA20", f"{latest['MA20']:.2f}")
        
        with col4:
            rsi_status = "Overbought" if latest['RSI6'] > 80 else "Oversold" if latest['RSI6'] < 20 else "Normal"
            st.metric("RSI(6)", f"{latest['RSI6']:.1f}", rsi_status)
        
        with col5:
            score, reasons = calculate_score(df)
            score_color = "normal" if score >= 3 else "off"
            st.metric("Score", f"{score}/5", 
                     "Bullish" if score >= 4 else "Neutral" if score >= 2 else "Bearish")
        
        # Chart
        st.plotly_chart(create_candlestick_chart(df), use_container_width=True)
        
        # Detailed analysis
        st.subheader("📋 Detailed Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Moving Averages")
            ma_data = {
                "Period": ["MA5", "MA10", "MA20", "MA60"],
                "Value": [f"{latest['MA5']:.2f}", f"{latest['MA10']:.2f}", 
                         f"{latest['MA20']:.2f}", f"{latest['MA60']:.2f}"],
                "Trend": [
                    "↑" if latest['MA5'] > latest['MA10'] else "↓",
                    "↑" if latest['MA10'] > latest['MA20'] else "↓",
                    "↑" if latest['MA20'] > latest['MA60'] else "↓",
                    "-"
                ]
            }
            st.dataframe(pd.DataFrame(ma_data), hide_index=True, use_container_width=True)
            
            st.markdown("#### MACD")
            macd_signal = "Golden Cross" if latest['DIF'] > latest['DEA'] and prev['DIF'] <= prev['DEA'] else \
                         "Dead Cross" if latest['DIF'] < latest['DEA'] and prev['DIF'] >= prev['DEA'] else \
                         "Golden State" if latest['DIF'] > latest['DEA'] else "Dead State"
            st.write(f"**DIF:** {latest['DIF']:.4f}")
            st.write(f"**DEA:** {latest['DEA']:.4f}")
            st.write(f"**MACD:** {latest['MACD']:.4f}")
            st.write(f"**Signal:** {macd_signal}")
        
        with col2:
            st.markdown("#### KDJ")
            kdj_signal = "Golden Cross" if latest['K'] > latest['D'] and prev['K'] <= prev['D'] else \
                        "Dead Cross" if latest['K'] < latest['D'] and prev['K'] >= prev['D'] else \
                        "Golden State" if latest['K'] > latest['D'] else "Dead State"
            st.write(f"**K:** {latest['K']:.2f}")
            st.write(f"**D:** {latest['D']:.2f}")
            st.write(f"**J:** {latest['J']:.2f}")
            st.write(f"**Signal:** {kdj_signal}")
            if latest['K'] > 80:
                st.warning("⚠️ Overbought Zone")
            elif latest['K'] < 20:
                st.success("✅ Oversold Zone")
            
            st.markdown("#### Bollinger Bands")
            st.write(f"**Upper:** {latest['BOLL_UPPER']:.2f}")
            st.write(f"**Middle:** {latest['BOLL_MID']:.2f}")
            st.write(f"**Lower:** {latest['BOLL_LOWER']:.2f}")
            if latest['close'] > latest['BOLL_UPPER']:
                st.warning("⚠️ Price above upper band")
            elif latest['close'] < latest['BOLL_LOWER']:
                st.success("✅ Price below lower band (possible rebound)")
        
        # Trading suggestions
        st.subheader("💡 Trading Suggestions")
        
        support_short = df['low'].iloc[-5:].min()
        support_mid = df['low'].iloc[-20:].min()
        resistance_short = df['high'].iloc[-5:].max()
        resistance_mid = df['high'].iloc[-20:].max()
        stop_loss = latest['close'] * 0.95
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Support Levels**\n\nShort-term: {support_short:.2f}\nMid-term: {support_mid:.2f}")
        with col2:
            st.warning(f"**Resistance Levels**\n\nShort-term: {resistance_short:.2f}\nMid-term: {resistance_mid:.2f}")
        with col3:
            st.error(f"**Stop Loss**\n\nSuggested: {stop_loss:.2f} (-5%)")
        
        # Overall assessment
        st.subheader("🎯 Overall Assessment")
        
        score, reasons = calculate_score(df)
        
        if score >= 4:
            st.success(f"""
            **Score: {score}/5** - **Bullish Signal** 🟢
            
            **Reasons:** {', '.join(reasons)}
            
            **Suggestion:** Consider entry with proper risk management. Set stop loss at {stop_loss:.2f}.
            """)
        elif score >= 2:
            st.warning(f"""
            **Score: {score}/5** - **Neutral Signal** 🟡
            
            **Reasons:** {', '.join(reasons)}
            
            **Suggestion:** Wait for clearer signals. Monitor key support/resistance levels.
            """)
        else:
            st.error(f"""
            **Score: {score}/5** - **Bearish Signal** 🔴
            
            **Reasons:** {', '.join(reasons) if reasons else 'Multiple bearish indicators'}
            
            **Suggestion:** Avoid entry. Wait for trend reversal signals.
            """)
        
        # Data table
        with st.expander("📊 View Raw Data"):
            st.dataframe(df.tail(20), use_container_width=True)


if __name__ == "__main__":
    main()

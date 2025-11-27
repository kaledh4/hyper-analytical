"""
Hyper-Analytical Market Intelligence Engine
============================================
Advanced crypto market analysis with AI-powered insights.

Features:
- Bull Market Support Band (BMSB) calculation
- Logarithmic Regression Risk Metric (0-1 scale)
- Federal Reserve macroeconomic data integration
- Heikin-Ashi trend analysis
- OpenRouter AI commentary generation
- Telegram notifications

Author: Hyper Analytical
"""

import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import requests
import os
import json
from datetime import datetime, timedelta

# ==========================================
# Configuration
# ==========================================
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SITE_URL = "https://kaledh4.github.io/hyper-analytical/"  # Update with your GitHub Pages URL

# ==========================================
# Data Fetching Functions
# ==========================================

def get_macro_data():
    """
    Fetches macroeconomic data from St. Louis Fed (FRED).
    Returns: DataFrame with Fed Funds Rate, Treasury Yields, and CPI
    """
    print("📊 Fetching macro data from FRED...")
    start = datetime.now() - timedelta(days=365*5)
    
    try:
        # DGS10 = 10-Year Treasury, DGS2 = 2-Year Treasury, 
        # FEDFUNDS = Fed Funds Rate, CPIAUCSL = CPI
        macro = web.DataReader(['DGS10', 'DGS2', 'FEDFUNDS', 'CPIAUCSL'], 
                              'fred', start, datetime.now())
        
        # Calculate Yield Curve (10Y - 2Y) - Recession Indicator
        macro['Yield_Curve'] = macro['DGS10'] - macro['DGS2']
        
        print("✅ Macro data retrieved successfully")
        return macro
    except Exception as e:
        print(f"⚠️ FRED Data Error (Using fallbacks): {e}")
        return pd.DataFrame()


def get_crypto_data(ticker):
    """
    Fetches crypto data and calculates technical indicators.
    Args:
        ticker: Yahoo Finance ticker symbol (e.g., 'BTC-USD')
    Returns: DataFrame with OHLCV + indicators
    """
    print(f"📈 Fetching {ticker} data...")
    df = yf.download(ticker, period="5y", interval="1wk", progress=False)
    
    # Handle MultiIndex columns (yfinance structure)
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs(ticker, axis=1, level=1)
    
    # Remove incomplete current week
    df = df[:-1]
    
    # 1. Bull Market Support Band (BMSB)
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
    
    # 2. Heikin-Ashi (Trend Smoothing)
    df['HA_Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4
    df['HA_Open'] = (df['Open'].shift(1) + df['Close'].shift(1)) / 2
    df['Trend'] = np.where(df['HA_Close'] > df['HA_Open'], "Bullish", "Bearish")
    
    print(f"✅ {ticker} data ready")
    return df


# ==========================================
# Risk Metric Calculator
# ==========================================

def calculate_risk_metric(df):
    """
    Advanced Risk Metric using Logarithmic Regression.
    
    Methodology:
    1. Fit log-log regression to price data
    2. Calculate deviation from "fair value" 
    3. Normalize to 0-1 scale using 4-year rolling window
    
    Returns: (current_risk, previous_risk)
    """
    print("🧮 Calculating Risk Metric...")
    
    data = df.copy().dropna()
    
    # Prepare logarithmic data
    data['log_price'] = np.log(data['Close'])
    data['time_idx'] = np.arange(1, len(data) + 1)
    data['log_time'] = np.log(data['time_idx'])
    
    # Fit Linear Regression on Log-Log data
    try:
        slope, intercept = np.polyfit(data['log_time'], data['log_price'], 1)
        data['fair_value'] = np.exp(intercept + slope * data['log_time'])
        
        # Calculate % Deviation from Fair Value
        data['deviation'] = (data['Close'] - data['fair_value']) / data['fair_value']
        
        # Normalize to 0-1 using rolling 200-week window (~4 years)
        roll_min = data['deviation'].rolling(window=200, min_periods=50).min()
        roll_max = data['deviation'].rolling(window=200, min_periods=50).max()
        
        data['risk'] = (data['deviation'] - roll_min) / (roll_max - roll_min)
        data['risk'] = data['risk'].clip(0, 1)  # Ensure 0-1 range
        
        # Get last 52 weeks of risk data for charting
        risk_history = data['risk'].tail(52).fillna(0.5).tolist()
        
        current_risk = float(data['risk'].iloc[-1])
        previous_risk = float(data['risk'].iloc[-2])
        
        print(f"✅ Risk Metric: {current_risk:.2f}")
        return current_risk, previous_risk, risk_history
        
    except Exception as e:
        print(f"⚠️ Risk calculation error: {e}")
        return 0.5, 0.5, [0.5] * 52  # Fallback values


# ==========================================
# AI Analysis Generator
# ==========================================

def generate_cowen_analysis(btc, eth, dxy, macro_data, risk_current, risk_prev):
    """
    Generates professional market commentary using OpenRouter AI.
    
    Tone: Data-driven, analytical, macro-focused, actionable
    Style: Clear, concise, informative with future projections
    """
    print("🤖 Generating AI commentary...")
    
    # Extract key metrics
    btc_price = float(btc['Close'].iloc[-1])
    sma_20 = float(btc['SMA_20'].iloc[-1])
    ema_21 = float(btc['EMA_21'].iloc[-1])
    eth_btc_ratio = float(eth['Close'].iloc[-1] / btc['Close'].iloc[-1])
    dxy_val = float(dxy['Close'].iloc[-1])
    
    # Macro data with fallbacks
    if not macro_data.empty:
        yield_curve = float(macro_data['Yield_Curve'].iloc[-1])
        fed_rate = float(macro_data['FEDFUNDS'].iloc[-1])
    else:
        yield_curve = -0.35
        fed_rate = 5.25
    
    # Construct the prompt
    prompt = f"""You are a professional crypto market analyst at Hyper Analytical. Provide a comprehensive, data-driven daily market update.

CORE PRINCIPLES:
1. **Data-First**: Base all analysis on actual numbers and technical indicators
2. **Clarity**: Explain complex concepts in accessible language
3. **Macro-Aware**: Always connect crypto markets to broader economic trends
4. **Actionable**: Provide clear guidance for risk management and positioning
5. **Balanced**: Present both bullish and bearish scenarios objectively

TODAY'S DATA:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Bitcoin Price**: ${btc_price:,.0f}
**Bull Market Support Band**: 
  - 20W SMA: ${sma_20:,.0f}
  - 21W EMA: ${ema_21:,.0f}
  - Status: {"Above (bullish structure)" if btc_price > max(sma_20, ema_21) else "Below (bearish structure)" if btc_price < min(sma_20, ema_21) else "Inside (choppy/neutral)"}

**Risk Metric (0.0-1.0)**: {risk_current:.2f} (Previous: {risk_prev:.2f})
  - 0.0-0.4 = Depression/Accumulation Zone
  - 0.4-0.7 = Neutral
  - 0.7-1.0 = Euphoria/Distribution Zone
  - Trend: {"Rising (increasing risk)" if risk_current > risk_prev else "Falling (decreasing risk)"}

**ETH/BTC Ratio**: {eth_btc_ratio:.5f}
  - Context: {"ETH losing ground to BTC" if eth_btc_ratio < 0.05 else "ETH showing relative strength"}

**Macro Environment**:
  - DXY (Dollar): {dxy_val:.2f}
  - Fed Funds Rate: {fed_rate:.2f}%
  - Yield Curve (10Y-2Y): {yield_curve:.2f}% {"⚠️ INVERTED (recession warning)" if yield_curve < 0 else "✅ Normal"}

STRUCTURE YOUR UPDATE:
1. **The Valuation** (2-3 sentences): Discuss Bitcoin's position relative to BMSB. Are we testing support? Far above it? Use both linear and logarithmic perspectives.

2. **The Risk Analysis** (2-3 sentences): Explain the Risk Metric reading. Is this a time for aggressive accumulation or defensive cash positioning? Reference historical cycles.

3. **The Macro Picture** (2-3 sentences): Analyze DXY strength and Fed policy impact on risk assets. Mention liquidity conditions and correlation to traditional markets.

4. **Altcoin Dynamics** (1-2 sentences): Assess ETH/BTC. Are alts bleeding to Bitcoin? Is this typical pre-halving behavior?

5. **What to Expect Next** (2-3 sentences): Based on current data, what scenarios are most likely in the coming weeks? Provide probability estimates if possible.

6. **Actionable Verdict** (1-2 sentences): Clear guidance - accumulate, hold, reduce exposure, or stay cash. Include a risk/reward assessment.

Conclude with a brief forward-looking statement.

**CRITICAL**: Be specific with numbers. Reference the actual data points. Avoid generic statements. Provide genuine value."""

    # Call OpenRouter API
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": SITE_URL,
            "X-Title": "Hyper Analytical"
        }
        
        payload = {
            "model": "openai/gpt-oss-20b:free",  # Free tier model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,  # Low for analytical consistency
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            analysis = response.json()['choices'][0]['message']['content']
            print("✅ AI analysis generated")
            return analysis
        else:
            print(f"⚠️ OpenRouter error: {response.status_code} - {response.text}")
            return generate_fallback_analysis(btc_price, sma_20, ema_21, risk_current)
            
    except Exception as e:
        print(f"⚠️ AI generation failed: {e}")
        return generate_fallback_analysis(btc_price, sma_20, ema_21, risk_current)


def generate_fallback_analysis(price, sma, ema, risk):
    """Fallback analysis if AI API fails"""
    band_status = "above" if price > max(sma, ema) else "below" if price < min(sma, ema) else "within"
    risk_zone = "accumulation" if risk < 0.4 else "distribution" if risk > 0.7 else "neutral"
    
    return f"""**Market Update**

Bitcoin is currently trading {band_status} the Bull Market Support Band (20W SMA: ${sma:,.0f}, 21W EMA: ${ema:,.0f}). 

The Risk Metric sits at {risk:.2f}, indicating a {risk_zone} zone. {"This suggests cautious accumulation may be favorable." if risk < 0.5 else "Higher risk levels warrant defensive positioning."}

Macro headwinds from the Federal Reserve's higher-for-longer policy continue to pressure risk assets. The DXY remains elevated, creating headwinds for crypto.

**Verdict**: {"Gradual accumulation with tight risk management" if risk < 0.5 else "Cash is a position - patience is key"}.

Analysis by Hyper Analytical."""


# ==========================================
# Telegram Notification
# ==========================================

def send_telegram_alert(data):
    """Sends notification to Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials not configured")
        return
    
    print("📱 Sending Telegram alert...")
    
    try:
        message = f"""**📊 Hyper Analytical Daily Update**

**Bitcoin**: ${data['btc_price']:,.0f}
**Risk**: {data['risk_metric']['current']:.2f}/1.0
**BMSB**: ${data['bmsb']['sma_20']:,.0f} - ${data['bmsb']['ema_21']:,.0f}

**Macro**:
• DXY: {data['macro']['dxy']:.2f}
• Fed Rate: {data['macro']['fed_rate']:.2f}%
• Yield Curve: {data['macro']['yield_inversion']:.2f}%

🔗 Full Analysis: {SITE_URL}

_Powered by Hyper Analytical_"""

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            },
            timeout=10
        )
        print("✅ Telegram alert sent")
    except Exception as e:
        print(f"⚠️ Telegram error: {e}")


# ==========================================
# Main Execution
# ==========================================

def main():
    """Main execution pipeline"""
    print("=" * 60)
    print("🚀 HYPER ANALYTICAL - Market Intelligence Engine")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    # 1. Fetch macro data
    macro = get_macro_data()
    
    # 2. Fetch crypto data
    btc = get_crypto_data("BTC-USD")
    eth = get_crypto_data("ETH-USD")
    dxy = get_crypto_data("DX-Y.NYB")
    
    # 3. Calculate risk metric
    risk_current, risk_prev, risk_history = calculate_risk_metric(btc)
    
    # 4. Generate AI analysis
    analysis = generate_cowen_analysis(btc, eth, dxy, macro, risk_current, risk_prev)
    
    # 5. Prepare dashboard data
    dashboard_data = {
        "date": datetime.now().strftime("%B %d, %Y"),
        "btc_price": float(btc['Close'].iloc[-1]),
        "eth_btc": float(eth['Close'].iloc[-1] / btc['Close'].iloc[-1]),
        "bmsb": {
            "sma_20": float(btc['SMA_20'].iloc[-1]),
            "ema_21": float(btc['EMA_21'].iloc[-1])
        },
        "risk_metric": {
            "current": risk_current,
            "previous": risk_prev,
            "history": risk_history
        },
        "macro": {
            "dxy": float(dxy['Close'].iloc[-1]),
            "yield_inversion": float(macro['Yield_Curve'].iloc[-1]) if not macro.empty else -0.35,
            "fed_rate": float(macro['FEDFUNDS'].iloc[-1]) if not macro.empty else 5.25
        },
        "commentary": analysis,
        "generated_at": datetime.now().isoformat()
    }
    
    # 6. Write to JSON file
    print("\n💾 Writing dashboard data...")
    with open("dashboard_data.json", "w") as f:
        json.dump(dashboard_data, f, indent=2)
    print("✅ Data saved to dashboard_data.json")
    
    # 7. Send Telegram notification
    send_telegram_alert(dashboard_data)
    
    print("\n" + "=" * 60)
    print("✅ EXECUTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

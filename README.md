# 📊 Hyper Analytical - Crypto Market Intelligence

![Banner](./icons/icon-512.png)

**Real-time crypto market intelligence powered by AI**. Professional analysis with actionable insights, updated daily via GitHub Actions.

🔗 **Live App**: [https://kaledh4.github.io/hyper-analytical/](https://kaledh4.github.io/hyper-analytical/)

---

## ✨ Features

- **📊 Real-time Market Intelligence** - Powered by OpenRouter AI (free tier)
- **🤖 Daily AI Digests** - Automated updates every 24 hours via GitHub Actions
- **📱 Progressive Web App** - Install on any device, works offline
- **🎨 Modern UI/UX** - Sleek dark theme with smooth animations
- **⚡ Lightning Fast** - Optimized performance with smart caching
- **🔒 Secure** - API keys stored in GitHub Secrets
- **🌐 GitHub Pages** - Free hosting, zero maintenance
- **🔍 Data Validation** - Automatic data consistency checks
- **🔧 Data Correction** - Live data correction for accuracy
- **🧮 Standardized Risk Metrics** - MVRV Z-Score, Puell Multiple, and proprietary metrics

---

## 🚀 Quick Start

### 1️⃣ Fork This Repository

Click the **Fork** button at the top right of this page.

### 2️⃣ Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Set **Source** to `main` branch
3. Click **Save**
4. Your site will be live at `https://<your-username>.github.io/hyper-analytical/`

### 3️⃣ Configure Secrets

Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add the following secrets:

| Secret Name | Description | How to Get It |
|------------|-------------|---------------|
| `OPENROUTER_API_KEY` | OpenRouter API Key (free) | Sign up at [openrouter.ai](https://openrouter.ai) |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token (optional) | Message [@BotFather](https://t.me/BotFather) on Telegram |
| `TELEGRAM_CHAT_ID` | Your Telegram Chat ID (optional) | Message your bot, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates` |

> 💡 **Telegram Bot Setup Tips**:
> - After creating your bot with BotFather, send `/start` to your bot
> - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` to find your chat ID
> - The bot will send daily market updates if properly configured

### 4️⃣ Update Configuration

Edit `macro_analysis.py` line 24:

```python
SITE_URL = "https://<YOUR-USERNAME>.github.io/hyper-analytical/"
```

### 5️⃣ Run First Analysis

1. Go to **Actions** tab
2. Click **Daily Market Analysis**
3. Click **Run workflow** → **Run workflow**
4. Wait ~2 minutes
5. Visit your GitHub Pages URL!

---

## 📱 Install as PWA

### Desktop (Chrome/Edge)
1. Visit your GitHub Pages URL
2. Look for the install icon (⊕) in the address bar
3. Click **Install**

### Mobile (iOS)
1. Open in Safari
2. Tap the Share button
3. Scroll down and tap **Add to Home Screen**

### Mobile (Android)
1. Open in Chrome
2. Tap the menu (⋮)
3. Tap **Install app** or **Add to Home Screen**

---

## 🧮 How It Works

### Architecture

```
┌─────────────────┐
│  GitHub Actions │ ← Runs daily at 9 AM UTC
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ macro_analysis  │ ← Fetches data & runs AI
│     .py         │
└────────┬────────┘
         │
         ├──► Yahoo Finance (yfinance) - BTC, ETH, DXY prices
         ├──► FRED API (pandas-datareader) - Fed Funds, Yields, CPI
         ├──► Data Validation & Correction Modules
         ├──► Standardized Risk Metrics Calculation
         └──► OpenRouter AI - Generates commentary
         │
         ▼
┌─────────────────┐
│dashboard_data   │ ← Committed to repo
│    .json        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  index.html     │ ← Loads on GitHub Pages
│  (PWA Frontend) │
└─────────────────┘
```

### Data Sources

1. **Yahoo Finance** (via `yfinance` library)
   - Bitcoin (BTC-USD) weekly OHLC data
   - Ethereum (ETH-USD) weekly OHLC data
   - US Dollar Index (DX-Y.NYB)

2. **Federal Reserve Economic Data** (FRED)
   - 10-Year Treasury Yield (DGS10)
   - 2-Year Treasury Yield (DGS2)
   - Federal Funds Rate (FEDFUNDS)
   - Consumer Price Index (CPIAUCSL)

3. **OpenRouter AI**
   - Model: `openai/gpt-oss-20b:free`
   - Generates Hyper Analytical-style commentary

### Indicators Calculated

#### 1. **Bull Market Support Band (BMSB)**
```
20-Week Simple Moving Average (SMA)
21-Week Exponential Moving Average (EMA)
```
- **Above Band** → Bullish structure (support)
- **Below Band** → Bearish structure (resistance)
- **Inside Band** → Choppy/neutral zone

#### 2. **Risk Metric (0.0 - 1.0)**
Logarithmic regression-based oscillator:

```python
# Fit: ln(P) = a + b * ln(time)
deviation = (price - fair_value) / fair_value
risk = normalize(deviation, 4-year rolling window)
```

- **0.0 - 0.4** → Accumulation zone (undervalued)
- **0.4 - 0.7** → Neutral zone
- **0.7 - 1.0** → Distribution zone (overvalued)

#### 3. **Standardized Risk Metrics**
- **MVRV Z-Score** - Market Value to Realized Value ratio standardized
- **Puell Multiple** - Daily issuance relative to annual average
- **Composite Risk Score** - Weighted combination of all metrics

#### 4. **Heikin-Ashi Trend**
Smoothed candlestick analysis for trend confirmation.

#### 5. **Macro Indicators**
- **Yield Curve** (10Y - 2Y): Negative = recession warning
- **DXY Index**: Higher = headwind for crypto
- **Fed Funds Rate**: Higher = tighter liquidity

---

## 🛠️ Development

### Local Testing

1. **Install Python dependencies**:
   ```bash
   pip install yfinance pandas pandas-datareader numpy requests
   ```

2. **Set environment variables**:
   ```bash
   export OPENROUTER_API_KEY="your-key-here"
   export TELEGRAM_BOT_TOKEN="your-token"  # Optional
   export TELEGRAM_CHAT_ID="your-id"       # Optional
   ```

3. **Run analysis**:
   ```bash
   python macro_analysis.py
   ```

4. **Serve locally**:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Or use any static server
   npx serve .
   ```

5. **Visit**: `http://localhost:8000`

### Project Structure

```
hyper-analytical/
├── .github/
│   └── workflows/
│       └── daily_analysis.yml    # GitHub Actions workflow
├── icons/
│   ├── icon-192.png              # PWA icon (192x192)
│   └── icon-512.png              # PWA icon (512x512)
├── index.html                    # Main PWA interface
├── styles.css                    # Mobile-first CSS
├── service-worker.js             # PWA service worker
├── manifest.json                 # PWA manifest
├── macro_analysis.py             # Python analysis engine
├── data_validator.py             # Data validation module
├── data_corrector.py             # Data correction module
├── risk_metrics.py               # Standardized risk metrics
├── dashboard_data.json           # Generated data (auto-updated)
├── HOW_TO.txt                    # Setup instructions
├── example_enhanced_analysis.py  # Example usage of enhanced features
└── README.md                     # This file
```

---

## ⚖️ Legal Disclaimer

### ⚠️ For Informational Purposes Only

The analysis and recommendations generated by this application are for **demonstration and educational purposes only**. They are generated by an AI model based on market data and **do not constitute financial advice**.

**Important:**
- ❌ **Do NOT trade based on these recommendations**
- 📚 **Always conduct your own due diligence**
- 🚫 **The developers assume NO liability** for financial decisions made based on this data
- 💼 **Consult a qualified financial advisor** before making investment decisions

This tool is for **educational and research purposes only**.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/kaledh4/hyper-analytical/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kaledh4/hyper-analytical/discussions)

---

<div align="center">

**Powered by Hyper Analytical**

_Real-time market intelligence at your fingertips_ 📊

[⭐ Star this repo](https://github.com/kaledh4/hyper-analytical) if you find it useful!

</div>
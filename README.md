# 🤖 Web3 AI Tracker

> AI-powered on-chain activity tracker with LLM analysis — built for airdrop hunters & DeFi researchers.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 🧠 What It Does

- 🔍 **On-chain surveillance** — monitors wallet activity via Etherscan/Alchemy API
- 🤖 **AI analysis** — feeds transaction data to Claude API for pattern detection
- 🐋 **Whale alerts** — detects large movements and unusual token flows
- 🪂 **Airdrop signals** — identifies early interaction patterns with new protocols
- 📲 **Telegram notifications** — real-time alerts to your phone

## 🛠 Stack

| Layer | Tech |
|-------|------|
| On-chain data | `web3.py` + Etherscan API |
| AI analysis | Anthropic Claude API |
| Notifications | Telegram Bot API |
| Scheduler | GitHub Actions (cron) |
| Config | `.env` + `config.yaml` |

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/web3-ai-tracker
cd web3-ai-tracker
pip install -r requirements.txt
cp config/.env.example config/.env
# Fill in your API keys, then:
python src/main.py
```

## 📁 Project Structure

```
web3-ai-tracker/
├── src/
│   ├── main.py           # Entry point
│   ├── tracker.py        # On-chain data fetching
│   ├── analyzer.py       # Claude AI analysis
│   └── notifier.py       # Telegram notifications
├── config/
│   ├── .env.example      # Environment variables template
│   └── config.yaml       # Wallets & settings
├── scripts/
│   └── run.sh            # Shell runner
├── requirements.txt
└── README.md
```

## 🔑 Required API Keys

- `ETHERSCAN_API_KEY` — [etherscan.io/apis](https://etherscan.io/apis)
- `ANTHROPIC_API_KEY` — [console.anthropic.com](https://console.anthropic.com)
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` — via [@BotFather](https://t.me/BotFather)

## 📲 Sample Alert

```
🚨 Whale Alert Detected

Wallet: 0xd8dA...6045
Action: Transferred 50,000 USDC → new contract
Contract Age: 2 days old
Risk Level: MEDIUM

🤖 AI Analysis:
"This wallet has interacted with 3 new DeFi protocols
in the past week. Pattern consistent with early
airdrop farming behavior. Protocol may be preparing
a token launch."

→ Contract: 0x1234...abcd
→ Tx: https://etherscan.io/tx/0x...
```

## ⚙️ GitHub Actions (Auto-run every hour)

The `.github/workflows/tracker.yml` runs the tracker on a cron schedule — zero server needed.

## 🪪 License

MIT — free to use, fork, and build on top of.

---

Built with ❤️ by a Bored Ape who learned to code 🐒
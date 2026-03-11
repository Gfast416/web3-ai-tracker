"""
web3-ai-tracker/src/notifier.py
Telegram bot notification system
"""
import os
import requests


TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram_alert(message: str, parse_mode: str = "Markdown") -> bool:
    """Send a message to Telegram chat."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️  Telegram credentials not set. Skipping notification.")
        return False

    url = TELEGRAM_API.format(token=token)
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"❌ Telegram error: {e}")
        return False


def format_whale_alert(wallet: str, tx: dict, ai_analysis: str) -> str:
    """Format a whale movement alert message."""
    short_wallet = f"{wallet[:6]}...{wallet[-4:]}"
    short_tx = f"{tx['hash'][:10]}..."

    return f"""🚨 *Whale Alert*

*Wallet:* `{short_wallet}`
*Value:* {tx.get('value_eth', 0):.2f} ETH
*Type:* {'Contract Interaction' if tx.get('is_contract') else 'Transfer'}

🤖 *AI Analysis:*
{ai_analysis}

🔗 [View on Etherscan](https://etherscan.io/tx/{tx['hash']})"""


def format_daily_summary(summary: str, alert_count: int) -> str:
    """Format the daily summary message."""
    return f"""📊 *Daily Web3 Intelligence Report*
━━━━━━━━━━━━━━━━━
Total Alerts: {alert_count}

{summary}

━━━━━━━━━━━━━━━━━
_Powered by Web3 AI Tracker 🤖_"""
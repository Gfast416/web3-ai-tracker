"""
web3-ai-tracker/src/main.py
Entry point — runs the full tracking pipeline
"""
import os
import yaml
from dotenv import load_dotenv

from tracker import get_wallet_transactions, get_token_transfers, is_whale_movement
from analyzer import analyze_wallet_activity, summarize_daily_report
from notifier import send_telegram_alert, format_whale_alert, format_daily_summary

load_dotenv("config/.env")


def load_config() -> dict:
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def run():
    config = load_config()
    wallets = config.get("wallets", [])
    whale_threshold = config.get("whale_threshold_eth", 10.0)
    alerts_today = []

    print(f"🚀 Starting Web3 AI Tracker — monitoring {len(wallets)} wallets\n")

    for wallet_entry in wallets:
        wallet = wallet_entry["address"]
        label = wallet_entry.get("label", "Unknown")
        print(f"🔍 Scanning: {label} ({wallet[:8]}...)")

        # Fetch data
        txs = get_wallet_transactions(wallet, limit=20)
        tokens = get_token_transfers(wallet, limit=20)

        if not txs:
            print(f"  ↳ No transactions found\n")
            continue

        # Convert to dicts for AI
        tx_dicts = [t.__dict__ for t in txs]

        # Check for whale movements
        whale_txs = [t for t in txs if is_whale_movement(t, whale_threshold)]

        if whale_txs:
            print(f"  🐋 {len(whale_txs)} whale transaction(s) detected!")

            # Get AI analysis
            analysis = analyze_wallet_activity(wallet, tx_dicts, tokens)

            # Send immediate alert
            whale_tx_dict = whale_txs[0].__dict__
            whale_tx_dict["is_contract"] = whale_txs[0].is_contract_interaction
            alert_msg = format_whale_alert(wallet, whale_tx_dict, analysis)
            send_telegram_alert(alert_msg)

            alerts_today.append({
                "wallet": wallet,
                "label": label,
                "whale_tx_count": len(whale_txs),
                "analysis": analysis,
            })
        else:
            print(f"  ↳ No whale activity. Routine scan complete.")

        print()

    # Send daily summary if there were alerts
    if alerts_today:
        summary_text = summarize_daily_report(alerts_today)
        summary_msg = format_daily_summary(summary_text, len(alerts_today))
        send_telegram_alert(summary_msg)
        print(f"\n📲 Daily summary sent to Telegram.")
    else:
        print("✅ All quiet. No significant activity today.")


if __name__ == "__main__":
    run()
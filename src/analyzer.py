"""
web3-ai-tracker/src/analyzer.py
Claude API integration for on-chain pattern analysis
"""
import os
import json
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def analyze_wallet_activity(wallet: str, transactions: list[dict], token_transfers: list[dict]) -> str:
    """
    Send wallet activity to Claude for AI analysis.
    Returns a human-readable analysis with risk level and signals.
    """
    prompt = f"""You are a Web3 intelligence analyst. Analyze the following on-chain activity for wallet {wallet}.

## Recent Transactions (last 20):
{json.dumps(transactions, indent=2)}

## Token Transfers (last 20):
{json.dumps(token_transfers, indent=2)}

Please provide:
1. **Behavior Pattern** - What type of wallet is this? (airdrop farmer, whale, bot, regular user, etc.)
2. **Airdrop Signals** - Any signs of early protocol interaction that could indicate airdrop farming?
3. **Risk Assessment** - LOW / MEDIUM / HIGH with reason
4. **Notable Activity** - Any unusual or interesting transactions worth flagging
5. **Recommendation** - Should we track this wallet more closely?

Be concise. Max 150 words. Use emojis sparingly."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def summarize_daily_report(alerts: list[dict]) -> str:
    """Generate a daily summary of all tracked wallets."""
    if not alerts:
        return "✅ No significant activity detected in the past 24 hours."

    prompt = f"""You are a DeFi market intelligence assistant.

Here are today's on-chain alerts from tracked wallets:
{json.dumps(alerts, indent=2)}

Write a concise daily summary (max 200 words) covering:
- Total alerts and significance
- Most important wallet movements
- Any coordinated activity patterns
- Market implications (if any)

Use a professional but approachable tone. Include relevant emojis."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
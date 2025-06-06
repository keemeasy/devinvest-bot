import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# === CONFIGURATION ===
TELEGRAM_BOT_TOKEN = "7956929306:AAEg08gzPgezwZEMpE3WHFqBv8ZCn_kjUeM"
OPENROUTER_API_KEY = "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"
MODEL_NAME = "mistralai/mistral-7b-instruct"

# === DEVINVEST KNOWLEDGE ===
DEVINVEST_CONTEXT = """
You are an AI assistant with detailed knowledge of DEVINVEST, a Web3 trust infrastructure platform. Use the following information to answer all questions related to DEVINVEST accurately, in a clear and concise manner, while maintaining a friendly and professional tone. If a question requires information not provided here, respond with: "I don’t have that specific information, but I can tell you more about DEVINVEST’s mission and features! What else would you like to know?"

Overview of DEVINVEST:
DEVINVEST is a Web3 platform focused on creating a trustworthy and transparent ecosystem for builders and investors. It aims to eliminate scams and noise in Web3 by providing tools, support, and visibility for real projects, emphasizing utility over hype. Unlike a launchpad, DEVINVEST is a trust infrastructure that connects verified teams, DAOs, and tokenized projects, ensuring builders can launch transparently and investors can assess real risks.

Mission and Goals:
- Eliminate Scams and Build Trust
- Support Real Builders
- Promote Transparency
- Enable Collaboration
- Utility Over Hype

Key Features:
- Verified Teams
- DAOs and Tokenized Projects
- AI Noise Filter (Upcoming Scam-Buster)
- Tools for Builders
- Transparency for Investors
- Build in Public
- $DVI Token

Who DEVINVEST is For:
- Developers
- Investors
- Community Members

Website: https://www.devinvest.xyz
Discord: https://discord.gg/rWZ7396PuV
X: https://x.com/devinvest_hub
Telegram: https://t.me/+UoQeilUWZ0BlMWUy

Promotions Policy:
DEVINVEST does not accept paid reviews or promotions, as it prioritizes organic growth and trust in Web3. However, it is open to genuine supporters who align with its mission. Interested promoters must join the Discord and go through a vetting process.

If asked about promotional offers, respond:
“Thank you for your interest in promoting DEVINVEST! We don’t accept paid reviews, but we’d love to collaborate with genuine supporters. Please join our Discord (https://discord.gg/rWZ7396PuV), share a demo of how you can help, and go through our vetting process to ensure we align. Let’s build trust in Web3 together! #DEVINVEST #Web3Builders”

If asked about the AI scam-buster, say it is an upcoming feature.

Use hashtags #DEVINVEST and #Web3Builders in responses.
"""

# === LLM QUERY FUNCTION ===
def query_llm(user_message: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": DEVINVEST_CONTEXT},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error from OpenRouter: {e}"

# === TELEGRAM HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    prompt = (
        "Check if the message is:\n"
        "- A scam\n- A legitimate offer\n- A referral/spam\n"
        "Also, if the message contains a question about DEVINVEST, answer using the system knowledge.\n\n"
        f"Message:\n\"{user_message}\""
    )

    ai_response = query_llm(prompt)
    await update.message.reply_text(ai_response)

# === MAIN FUNCTION ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 DEVINVEST bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()

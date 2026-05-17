import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = """You are Hamzeh AI Tutor — an English conversation coach assistant created by Hamzeh, a professional English trainer.

Your personality:
- Friendly, funny, and encouraging — you joke around but stay focused
- You never make students feel bad about mistakes
- You always use this exact correction format: "Instead of saying [wrong] → You gotta say [correct]"
- You celebrate small wins enthusiastically
- You mix Arabic and English naturally (Arabic for comfort, English for teaching)

Your job:
1. Welcome new students warmly in Arabic then English
2. Correct grammar mistakes using Hamzeh's style
3. Give daily speaking challenges
4. Encourage students to keep practicing
5. Answer questions about English in a simple fun way

Rules:
- NEVER just say "wrong" — always give the correct version
- Keep responses SHORT and punchy (max 4-5 lines)
- Always end with a question or challenge to keep the conversation going
- If student writes in Arabic only, encourage them to try in English too"""

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
user_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome = f"""يا هلا {user_name}! 👋

I'm Hamzeh AI Tutor — your English practice buddy, available 24/7! 🔥

I'm here to help you:
✅ Practice speaking English
✅ Fix your grammar (no judgment!)
✅ Give you daily challenges

Just write anything in English and let's go! Don't be scared — even if it's wrong, that's how we learn 💪

So tell me... what's your name and where are you from? 😄"""
    await update.message.reply_text(welcome)
    user_histories[update.effective_user.id] = []

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_text})

    if len(user_histories[user_id]) > 20:
        user_histories[user_id] = user_histories[user_id][-20:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=user_histories[user_id]
        )
        bot_reply = response.content[0].text
        user_histories[user_id].append({"role": "assistant", "content": bot_reply})
        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("Oops! Something went wrong. Try again in a second 😅")
        logging.error(f"Error: {e}")

async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    challenges = [
        "🎯 Today's challenge: Tell me about your morning in 3 sentences. GO! ⏱️",
        "🎯 Today's challenge: Describe your favorite food without saying its name. I'll guess! 😄",
        "🎯 Today's challenge: Tell me about a funny thing that happened to you. Full sentences only! 💪",
        "🎯 Today's challenge: What would you do if you had 1 million dollars? Tell me in English! 🤑",
        "🎯 Today's challenge: Describe your best friend without saying their name. 3 sentences minimum! 🧠"
    ]
    await update.message.reply_text(random.choice(challenges))

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """Here's what I can do for you! 🔥

/start — Start fresh
/challenge — Get a daily speaking challenge
/help — Show this menu

Or just... write anything in English and I'll help you improve it! 💪

Remember: mistakes are welcome here 😄"""
    await update.message.reply_text(help_text)

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Hamzeh AI Tutor is running!")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
========================================
 Hamzeh AI Tutor Bot - Setup Guide
========================================

STEP 1 - Install Python
------------------------
Download from: https://python.org
Make sure to check "Add Python to PATH" during install

STEP 2 - Install the bot requirements
--------------------------------------
Open Command Prompt (Windows) or Terminal (Mac)
Go to the bot folder, then run:
    pip install -r requirements.txt

STEP 3 - Add your keys to bot.py
----------------------------------
Open bot.py with any text editor (Notepad is fine)

Find this line:
    TELEGRAM_TOKEN = "YOUR_TOKEN_HERE"
Replace with your Telegram token:
    TELEGRAM_TOKEN = "8896433854:AAG8a-2gu_k4uvPoSgBK62cbD87x36BCYo0"

Find this line:
    ANTHROPIC_API_KEY = "YOUR_ANTHROPIC_KEY_HERE"
Replace with your Anthropic key (see below how to get it)

STEP 4 - Get Anthropic API Key
--------------------------------
1. Go to: https://console.anthropic.com
2. Sign up / Log in
3. Click "API Keys" 
4. Click "Create Key"
5. Copy the key and paste it in bot.py

STEP 5 - Run the bot!
----------------------
In Command Prompt / Terminal:
    python bot.py

You should see:
    Hamzeh AI Tutor is running!

STEP 6 - Test it
-----------------
Open Telegram, search for your bot name
Send /start and enjoy!

========================================
 To keep the bot running 24/7
========================================
Use a free cloud service like:
- Railway.app (free tier available)
- Render.com (free tier available)

Need help? The setup is simple — you only need to add 2 keys!

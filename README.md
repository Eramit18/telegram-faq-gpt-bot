# 🤖 Telegram Support Bot with GPT Fallback

This is a fully functional Telegram chatbot designed for customer support. It handles predefined FAQs and falls back to OpenAI's GPT for smart, human-like responses.

## 🚀 Features
- 📄 Answers FAQs instantly
- 🤖 Uses GPT if no FAQ match is found
- ✨ Markdown formatting with emojis and polite tone
- ⌛ Typing animation to simulate human response
- 💬 Inline buttons: View FAQs, Ask GPT, Contact Support
- 🧠 Logs all user messages in `user_queries.json`
- 🛠️ Easy to configure and deploy (polling mode — no Flask/Ngrok)

## 📁 File Structure

| File                                                                                                                                                                        Purpose                          
|------------------------------------------------------------------------------------------------------------------------------------------------
| main.py                                                                                                                                                           Main Telegram bot logic          
| faq.py                                                                                                                                                             Simple FAQ system                 
| faq_data.json                                                                                                                                                  Stores question-answer pairs   
| openai_fallback.py                                                                                                                                          GPT fallback logic                   
| user_queries.json                                                                                                                                             Logs user queries                    
| .env.example                                                                                                                                                   Template for environment config  
| requirements.txt                                                                                                                                               Python dependencies               

## 🧪 How to Run

1. **Clone this repo**
```bash
git clone https://github.com/yourusername/telegram-support-gpt-bot.git
cd telegram-support-gpt-bot


2.Install dependencies:
"pip install -r requirements.txt" run in cmd.

3. Configure environment
Rename .env.example to .env and add your keys:

BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key

4. Run the bot
python main.py

📄 License
This project is open source under the MIT license.

Created with ❤️ by [Amit Kumar]




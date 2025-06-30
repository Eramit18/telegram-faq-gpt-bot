-- 🤖 Telegram FAQ + GPT Bot

A smart Telegram chatbot that answers FAQs instantly, and uses OpenAI GPT as a fallback for unknown queries. Built with `python-telegram-bot` and OpenAI's `gpt-3.5`.


--✨ Features

- 📄 Answer pre-defined FAQs instantly
- 🧠 Fallback to OpenAI GPT for new questions
- ⌨️ Typing animation for real chat feel
- 📝 Logs all user queries to `user_queries.json`
- 📲 Inline button menu (FAQs / GPT / Contact Support)
- 🌐 Deployable anywhere (Render, Fly.io, Replit)


-- 📁 Project Structure

```bash
├── main.py                # Bot logic & message handlers
├── faq.py                 # Custom FAQ database
├── openai_fallback.py     # GPT fallback handler
├── user_queries.json      # Stores all user messages
├── .env.example           # Sample env config
├── requirements.txt       # Dependencies
└── README.md              # You are here!

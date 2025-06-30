<<<<<<< HEAD
faq_data = {
    "what is your name": "I'm your friendly assistant bot, here to help you!",
    "how are you": "I'm doing great, thank you! How can I assist you today?",
    "what can you do": "I can answer questions, assist with tasks, and chat with you!",
    "help": "Sure! You can ask me anything, or type /start to begin.",
}

def check_faq(message: str) -> str | None:
    message = message.lower().strip()
    for question, answer in faq_data.items():
        if question in message:
            return answer
    return None
=======
faq_data = {
    "what is your name": "I'm your friendly assistant bot, here to help you!",
    "how are you": "I'm doing great, thank you! How can I assist you today?",
    "what can you do": "I can answer questions, assist with tasks, and chat with you!",
    "help": "Sure! You can ask me anything, or type /start to begin.",
}

def check_faq(message: str) -> str | None:
    message = message.lower().strip()
    for question, answer in faq_data.items():
        if question in message:
            return answer
    return None
>>>>>>> 416e5f9d350cae4a75f9a8f7f324ae491ab36b5b

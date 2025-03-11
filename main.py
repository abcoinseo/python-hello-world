import os
import requests
import telebot
from flask import Flask, request

app = Flask(__name__)

# 🔹 Env Variables থেকে Token ও API Key নেওয়া
TELEGRAM_BOT_TOKEN = os.getenv("8174267515:AAElG9MkHRGIFmbf_4k_HektTAdNIXnPcfY")
GAMINI_API_KEY = os.getenv("AIzaSyBll0reKSpvfXzapeSqP7wE782qYOcVLP4")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_gamini_response(user_message):
    """Gamini AI API-তে পাঠিয়ে উত্তর পাওয়া"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"
    headers = {"Content-Type": "application/json"}
    params = {"key": GAMINI_API_KEY}
    data = {
        "prompt": {"text": user_message},
        "temperature": 0.7,
        "maxTokens": 200
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    result = response.json()
    
    try:
        return result["candidates"][0]["output"]
    except:
        return "দুঃখিত, আমি উত্তর দিতে পারছি না। 😢"

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    """Telegram Update প্রসেস করে"""
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "🤖 হ্যালো! আমি AI Chatbot। যেকোনো প্রশ্ন করুন।")

@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    """Telegram Chat এর রিপ্লাই দিবে"""
    user_text = message.text
    reply = get_gamini_response(user_text)
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

import telebot
import requests

# Замените 'TOKEN' на токен вашего Telegram-бота
TOKEN = 'TOKEN'
# Замените 'API' на ваш API ключ от OpenAI
API = 'API'

bot = telebot.TeleBot(TOKEN)


def get_gpt_response(prompt):
    headers = {
        'Authorization': f'Bearer {API}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-3.5-turbo',  # или другой доступный вам модель
        'messages': [{'role': 'user', 'content': prompt}],
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Ошибка: {response.status_code}, {response.text}"


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    bot.reply_to(message, "Обрабатываю ваш запрос...")

    gpt_response = get_gpt_response(user_input)
    bot.send_message(message.chat.id, gpt_response)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)

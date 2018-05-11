import telebot  # импортируем модуль pyTelegramBotAPI
import conf     # импортируем наш секретный токен

bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает длину вашего сообщения.")
    
@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на любое сообщение
def send_len(message):
	bot.send_message(message.chat.id, 'В вашем сообщении {} символов.'.format(len(message.text)))
    
if __name__ == '__main__':
    bot.polling(none_stop=True)
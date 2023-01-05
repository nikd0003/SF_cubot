import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет! Бот умеет конвертировать курсы валют.\n" \
           "Посмотреть доступные валюты - введите /values\n" \
           "Чтобы конвертировать одну валюту в другую\n" \
           "введите команду в формате:\n" \
           "[исходная валюта] [конечная валюта] [сумма]\n" \
           "Всего должно быть 3 разделеннsх пробелом параметра\n" \
           "без кавычек или скобок.\n" \
           "Например:\n" \
           "евро рубль 100"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '🔄 Валюты, доступные для конвертации и их ключи:\n' \
           '[Ключ]    ➡    [Валюта]'
    # for i in exchanges.keys():
    #    text = '\n'.join((text, i))
    for key, lst in exchanges.items():
        text += f'\n{key}    ➡    {lst[2]}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров или пропустили пробел!')
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


if __name__ == '__main__':
    bot.polling()

import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Я могу показать текущие курсы валют.\n' +
                     'Для отображения доступных валют нажмите /values.\n' +
                     'Для помощи по запросам нажмите /help.')


@bot.message_handler(commands=['help'])  # обработка команд /help
def help_command(message: telebot.types.Message):
    text = "Посмотреть доступные валюты - введите /values\n" \
           "Чтобы конвертировать одну валюту в другую\n" \
           "введите команду в формате:\n" \
           "[ключ исходной валюты] [ключ конечной валюты] [сумма]\n" \
           "Всего должно быть 3 разделенных пробелом параметра\n" \
           "без кавычек и скобок.\n" \
           "Например:\n" \
           "евро рубль 100"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])  # обработка команды /values
def values(message: telebot.types.Message):
    text = '🔄 Валюты, доступные для конвертации и их ключи:\n' \
           '[Валюта]    ➡    [Ключ]'
    for key, lst in exchanges.items():
        text += f'\n{lst}              ➡    {key}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])  # обработка конвертации валют
def converter(message: telebot.types.Message):  # принимаем и разбираем запрос на конвертацию, проверка ввода
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


if __name__ == '__main__':  # точка входа
    bot.infinity_polling()

import telebot
import atexit

bot = telebot.TeleBot('...')

from telebot import types
from threading import Thread

maxMessagesCount = 20

messages = []
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    infoButton = types.KeyboardButton("ℹ Информация о проекте️")
    sendMessageButton = types.KeyboardButton("🚬 Направить пример сообщения")

    markup.row(infoButton)
    markup.row(sendMessageButton)
    bot.send_message(
        message.from_user.id, 
        "Приветствую! Данный бот предназначен для сбора датасета для решения задачи распознавания суицидальных сообщений (и не только).",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def getTextMessages(message):
    messageType = None

    if (message.text == "⬅️ Вернуться на начальный экран"):
        start(message)
    elif (message.text == "ℹ Информация о проекте️"):
        bot.send_message(
            message.from_user.id, 
            "Если вкратце, то я простой магистрант ИУ7 из Бауманки, который пытается сделать не дипломную работу" +
            ", а что-то действительно нужное и важное. И вот мы тут пытаемся распознавать суицидальные сообщения.\n" + 
            "Так или иначе, одна из самых больших проблем -- отсутствие датасета суицидальных сообщений. " +
            "Тема эта достаточно закрытая, в интернете ее если и обсуждают, то в очень странных местах (не думайте, что я так называю мед. форумы с дизайном из 98-го года). "
            "Парсить странички интернета и сидеть их размечать, к сожалению, не представляется сейчас возможным, однако, почему бы не попросить помощи у окружающих меня людей" +
            "?\n\n" +
            "Вот поэтому мы сейчас тут. Хочу Вас поблагодарить за проявленный интерес и тот вклад, который Вы, возможно, внесете или уже внесли ❤️"
        )
    elif (message.text == "🚬 Направить пример сообщения" or message.text == "Понятненько!" or message.text == "" or message.text == "⬅️ Вернуться"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        suicidalButton = types.KeyboardButton("⛈ Суицидальное сообщение")
        suicidalTopic = types.KeyboardButton("🎃 Сообщение на суицидальную тематику (но не суицидальное)")
        infoButton = types.KeyboardButton("🤔 Чем они отличаются?")
        
        goBackButton = types.KeyboardButton("⬅️ Вернуться на начальный экран")
 
        markup.row(suicidalButton)
        markup.row(suicidalTopic)
        markup.row(infoButton)
        markup.row()
        markup.row(goBackButton)
        
        bot.send_message(message.from_user.id, "Какой тип сообщения будет направлен?", reply_markup=markup)
    elif (message.text == "🤔 Чем они отличаются?"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        gotItButton = types.KeyboardButton("Понятненько!")

        markup.add(gotItButton)

        bot.send_message(
            message.from_user.id, 
            "*Суицидальные* сообщения являются показателем глубокой депрессии. Человек, посылающий подобные письма может размышлять о суициде, как о методе решения своих проблем. Также к этой группе сообщений относятся и прямые слова о действиях, которые готов совершить человек.\n" +
            "\n*Сообщения на суицидальную тематику* заключаются в обычном разговоре (хотя для кого как) о стремлении человека умереть. Здесь могут оказаться и какие-то философские рассуждения, и просто шутки про суицид.\n" +
            "\nВаше видение может несколько отличаться от принятых в данной работе. Прошу принять это как условность, в дальнейшем мои друзья из сферы медицины помогут употребить в работе более точные определения.",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    elif (message.text == "⛈ Суицидальное сообщение"):
        bot.send_message(
            message.from_user.id,
            "Введите сообщение:",
            reply_markup=types.ReplyKeyboardRemove()
        )

        users[message.from_user.id] = 0
    elif (message.text == "🎃 Сообщение на суицидальную тематику (но не суицидальное)"):
        bot.send_message(
            message.from_user.id,
            "Введите сообщение:",
            reply_markup=types.ReplyKeyboardRemove(),
            
        )

        users[message.from_user.id] = 1
    elif (users.get(message.from_user.id, None) != None):
        print("saving message: " + message.text)
        messages.append([message.text, users.pop(message.from_user.id)])
        if (maxMessagesCount < len(messages)):
            Thread(target=saveCurrentMessages).start()
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        goBackButton = types.KeyboardButton("⬅️ Вернуться")

        markup.add(goBackButton)

        bot.send_message(message.from_user.id, "Сообщение сохранено!", reply_markup=markup)        

def saveCurrentMessages():
    file = open("./loldb.txt", "a+")
    text = ""
    for message in messages:
        text += message[0] + "; "
        text += str(message[1]) + "\n"
    file.write(text)
    file.close()

atexit.register(saveCurrentMessages)

bot.polling(none_stop=True, interval=0)
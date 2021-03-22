from telegram import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telebot import types
import json

NAME, ME = range(2)
MEETING, YES, NO, NOT = range(4)

button_1 = "yes"
button_2 = "no"


b_1 = types.KeyboardButton(text = button_1)
b_2 = types.KeyboardButton(text = button_2)
keyboard_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_1.add(b_2)
keyboard_1.add(b_1)

def start(update, context):
    update.message.reply_text(text = "Привет! Давай пройдем обучение и я расскажуб что я могу?")
    answer = update.message
    context.user_data["answer_1"] = answer
    if context.user_data["answer_1"] == "yes":
        return YES
    elif context.user_data["answer_1"] == "no":
        return NO

def meet(update, context):
    update.message.reply_text("Как тебя зовут?")
    return NAME

def name(update, context):
    name = update.message
    context.user_data["name"] = name
    update.message.reply_text("Привет! Я БОТИК и готов тебе помочь!")
    return ME

def me(update, context):
    pass

def yes_1(update, context):
    update.message.reply_text("Ура, давай тебе все расскажу. Пока я мало чего умею, но скоро буду крутым!")
    return ConversationHandler.END

def no_1(update, context):
    update.message.reply_text("Очень жалко, но ладно. До встречи!!!")
    return ConversationHandler.END

def back(update, context):
    update.message.reply_text("Я вас не понимаю, давай-те попробуем заново.")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Приятно было с вами  пообщаться!")
    return ConversationHandler.END

def main():
    updater = Updater(token = "1706546334:AAHFppxsSyjlkuVTw0g1R8fzAkt5D4M7kOA",
        use_context = True)

    dp = updater.dispatcher
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("meet", meet)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            ME: [MessageHandler(Filters.text & ~Filters.command, me)]
        },
        fallbacks=[CommandHandler("cancel", cancel)])
    )

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            YES: [MessageHandler(Filters.text & ~Filters.command, yes_1)],
            NO: [MessageHandler(Filters.text & ~Filters.command, no_1)],
            NOT: [MessageHandler(Filters.text & ~Filters.command, back)],

        },
        fallbacks=[CommandHandler("cancel", cancel)])
    )

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
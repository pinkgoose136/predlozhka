from ast import Call
import telegram
import os
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram import Update
from telegram.ext import (Updater,
                          PicklePersistence,
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
BOT_TOKEN = ""
da = range(1)

channel_id = ""
group_propose_id = ""
admin_id = ""
no = ['нет', 'отмена', 'отменить', 'не', 'не подтверждаю']

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Вас приветствует бот-предложка группы Bimba. Чтобы предложить новость для паблика отправьте сообщение и подтвердите его отправку")

def forward(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Подтвердите отправку сообщения\nДля подтверждения введите любой текст кроме \"нет\" либо \"отмена\"', reply_markup=ForceReply())
    return da

def check(update: Update, context: CallbackContext):
    d = update.message.text
    context.user_data['da'] = da

    if d.lower() in no:
        update.message.reply_text('Отменено')
        return ConversationHandler.END
    else:
        context.bot.send_message(update.message.chat.id, "Ваше сообщение успешно отправлено администрации паблика")
        context.bot.forward_message(admin_id, update.message.chat.id, update.message.message_id-2)
        return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    if (update.message.text).lower() in no:
        update.message.reply_text('Отменено')
        return ConversationHandler.END

if __name__ == "__main__":
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    _handlers = {}
    _handlers['start_handler'] = CommandHandler('start', start)
    _handlers['name_conversation_handler'] = ConversationHandler(
        entry_points=[MessageHandler(Filters._ChatType._Private, forward)],
        states={
            da: [MessageHandler(Filters.text, check)]
        },
        fallbacks=[MessageHandler(Filters.text, cancel)]
    )

    for name, _handler in _handlers.items():
        dispatcher.add_handler(_handler)

    updater.start_polling()
    updater.idle()
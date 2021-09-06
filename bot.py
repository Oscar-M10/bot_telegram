import os
import qrcode
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler,MessageHandler, Filters
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton

INPUT_TEXT = 0

def input_text(update, context):
    text = update.message.text
    print(text)

    filename = generate_qr(text)
    send_qr(filename)
    return ConversationHandler.END

def start(update, context):
   
    update.message.reply_text(
        text='Hola bienvenido, qué deseas hacer?',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Sobre el autor', url='https://www.google.com')],
            [InlineKeyboardButton(text='Generar qr', callback_data='qr')]
            
        ])
    )

def qr_command_handler(update, context):
    update.message.reply_text('Enviame el texto para generar un codigo QR')

    return INPUT_TEXT

def qr_callback_handler(update, context):

    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='enviame el texto para generar un código QR'
    )
    return INPUT_TEXT


def generate_qr(text):
    filename = text + '.jpg'

    img = qrcode.make(text)
    img.save(filename)
    return filename

def send_qr(filename, chat):
    
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(filename, 'rb')
    )
    
    os.unlink(filename)

def input_text(update,context):
    
    text = update.message.text

    filename = generate_qr(text)
    
    chat = update.message.chat

    send_qr(filename, chat)

    
   # print(filename)
    #send_qr(filename)
    
    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token='1782494160:AAF17SROOgRC3H9aFsAfT5UFF4KPthMcOKc', use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CallbackQueryHandler(pattern='qr',callback=qr_callback_handler)

        ],

        states={
            INPUT_TEXT:[MessageHandler(Filters.text, input_text)]
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()

import aiogram
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from flask import Flask,request
import os
api_token = '1125827816:AAHDSArWiPoqPV05M4RAUoqstj2BN-ZYLkk'
bot = Bot(token=api_token)
dp = Dispatcher(bot)
server = Flask(__name__)
inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка')
@dp.message_handler(commands=['start'])
async def echo_send(message : types.message):
     # await bot.promote_chat_member(message.from_user.id)
     await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)
@dp.message_handler()
async def echo_send(massege : types.message):
    await massege.answer(massege.text)
executor.start_polling(dp, skip_updates=False)
@server.route('/' + api_token, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = aiogram.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://blooming-temple-61669.herokuapp.com/' + api_token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


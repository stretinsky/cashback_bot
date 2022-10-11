from gettext import textdomain
import logging
import importlib
import keyboard

from os.path import dirname
from utils import TestStates
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters, FSMContext

def get_from_dotenv(key):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    return getenv(key)

messages = importlib.import_module(get_from_dotenv('MESSAGES_FILENAME'))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=get_from_dotenv('TELEGRAM_API_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()

    await message.answer(
        text=messages.start_message,
        reply_markup=keyboard.get_main_kb()
    )

@dp.callback_query_handler(lambda c: c.data == 'two')
async def handle_three(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        text=messages.two_message, 
        reply_markup=keyboard.get_back_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'three')
async def handle_three(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.GET_REQUEST)
    

    await callback_query.message.edit_text(
        text=messages.three_message, 
        reply_markup=keyboard.get_back_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def handle_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    state = dp.current_state(user=callback_query.from_user.id)
    await state.reset_state()

    await callback_query.message.edit_text(
        text=messages.start_message, 
        reply_markup=keyboard.get_main_kb()
    )

@dp.message_handler(state=TestStates.GET_REQUEST)
async def send_request(message: types.Message):
    await bot.forward_message(from_chat_id=message.chat.id, chat_id=get_from_dotenv('SUPPORT_CHAT_ID'), message_id=message.message_id)
    await message.answer(text='Ваше обращение будет рассмотрено в ближайшее время')

@dp.message_handler()
async def send_answer(message: types.Message):
    if 'reply_to_message' in message:
        if 'forward_from' in message.reply_to_message:
            await bot.send_message(chat_id=message.reply_to_message.forward_from.id, text=message.text)
            
@dp.callback_query_handler(lambda c: c.data == 'one')
async def handle_three(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(TestStates.GET_SCREENSHOT)
    
    await callback_query.message.edit_text(
        text=messages.one_message, 
        reply_markup=keyboard.get_back_keyboard()
    )

@dp.message_handler(state=TestStates.GET_SCREENSHOT, content_types=['photo', 'text'])
async def send_screenshot(pic: types.Message):
    await bot.copy_message(from_chat_id=pic.chat.id, chat_id=get_from_dotenv('READY_FOR_PAY_CHAT_ID'), message_id=pic.message_id, reply_markup=keyboard.get_apply_kb(pic.from_user.id, pic.from_user.username))
    await pic.answer(text='Ваше обращение будет рассмотрено в ближайшее время')

@dp.callback_query_handler(filters.Regexp(r"ok_.*"))
async def process_callback_ok(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)

    if callback_query.message.content_type == "photo":
        await callback_query.message.edit_caption(caption="обработано ✅")
    else: 
        await callback_query.message.edit_text(text=callback_query.message.text + " - обработано ✅")

    await bot.send_message(chat_id=user_id, text=messages.ok_message)
    state = await storage.set_state(user=user_id, state=TestStates.GET_NUMBER)

@dp.callback_query_handler(filters.Regexp(r"cancel_.*"))
async def process_callback_cancel(callback_query: types.CallbackQuery):
    user_id = callback_query.data.split('_')[1]
    await bot.answer_callback_query(callback_query.id)

    if callback_query.message.content_type == "photo":
        await callback_query.message.edit_caption(caption="обработано ❌")
    else: 
        await callback_query.message.edit_text(text=callback_query.message.text + " - обработано ❌")

    await bot.send_message(chat_id=user_id, text=messages.cancel_message)

@dp.callback_query_handler(lambda c: c.data == 'card')
async def handle_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        text=callback_query.message.text + " \nОплачено ✅", 
    )           


@dp.message_handler(state=TestStates.GET_NUMBER)
async def send_screenshot(message: types.Message):
    text = f"Оплатить: @{message.from_user.username}\n"
    text += f"Сообщение: {message.text}"
    await bot.send_message(chat_id=get_from_dotenv('READY_FOR_PAY_CHAT_ID'), text=text, reply_markup=keyboard.get_card_kb())
    await message.answer(text="Ожидайте поступления")
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
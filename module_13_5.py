from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = 'незабудьтеубратьключ'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup=kb)

@dp.message_handler(text=['Рассчитать'])
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['growth'] = int(message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = int(message.text)
        age = data['age']
        growth = data['growth']
        weight = data['weight']

    calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5

    await message.answer(f'Ваша норма калорий: {calories} ккал в день.')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
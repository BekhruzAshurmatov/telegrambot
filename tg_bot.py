from aiogram import Bot, Dispatcher, types
import asyncio
from tg_database import save_data, check_user_exists

Token = '7567562269:AAHu6cMJGhDgeLAZKh8qb05tsQD1X8lXT_o'
channel_name = '@zayavkid'

bot = Bot(token=Token)
dp = Dispatcher()

user_data = {}

@dp.message()
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    if message.text == '/start' or message.text == 'Оставить заявку еще раз':
        await welcome(message)
    elif user_id not in user_data:
        await welcome(message)
    elif 'name' not in user_data[user_id]:
        await ask_phone(message)
    elif 'phone' not in user_data[user_id]:
        await ask_age(message)
    elif 'age' not in user_data[user_id]:
        await total_message(message)
    elif message.text == 'да' and user_id in user_data:
        await update_confirmation(message)
    elif message.text == 'нет' and user_id in user_data:
        await cancel_update(message)


# @dp.message(Command('start'))
async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    await message.answer(f"Добро пожаловать! \n"
                         f"Пожалуйста введите ваше имя:")
    print(user_data)


async def ask_phone(message: types.Message):
    user_id = message.from_user.id
    name = message.text
    user_data[user_id]['name'] = name
    button = [
        [types.KeyboardButton(text='Поделиться контактом', request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"Пожалуйста отправьте свой номер или "
                         f"нажмите 'Поделиться контактом'", reply_markup=keyboard)
    print(user_data)


async def ask_age(message: types.Message):
    user_id = message.from_user.id
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    user_data[user_id]['phone'] = phone
    await message.answer(f"Пожалуйста, введите ваш возраст:\n")
    print(user_data)


async def total_message(message: types.Message):
    user_id = message.from_user.id
    age = message.text
    user_data[user_id]['age'] = age
    print(user_data)
    name = user_data[user_id]['name']
    phone = user_data[user_id]['phone']
    message_text = (f"Ваше имя: {name}\n"
                    f"Ваш номер: {phone}\n"
                    f"Ваш возраст: {age}")
    button = [
        [types.KeyboardButton(text='Оставить заявку еще раз')]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)

    if len(check_user_exists(user_id)) > 0:
        await message.answer(f"Выши данные существует в базе.\n"
                             f"Хотите обновить ваши данные (да, нет):")
    else:
        save_data(user_id, name, phone, age)
        await message.answer(f"Ваша заявка принята!\n"
                             f"{message_text}", reply_markup=keyboard)
        await bot.send_message(channel_name, message_text)
        print(user_data)
        del user_data[user_id]
        print(user_data)


async def update_confirmation(message: types.Message):
    user_id = message.from_user.id
    name = user_data[user_id]['name']
    phone = user_data[user_id]['phone']
    age = user_data[user_id]['age']

    save_data(user_id, name, phone, age)
    await message.answer(f"Спасибо, ваши данные обновлены!")
    message_text = (f"Ваше имя: {name}\n"
                    f"Ваш номер: {phone}\n"
                    f"Ваш возраст: {age}")
    await bot.send_message(channel_name, message_text)
    del user_data[user_id]
    print(user_data)


async def cancel_update(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"Данные не были обновлены.")
    del user_data[user_id]
    print(user_data)


async def main():
    await dp.start_polling(bot)


print('The bot is running...')
asyncio.run(main())
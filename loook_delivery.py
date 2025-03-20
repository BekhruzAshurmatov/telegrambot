from aiogram import Bot, Dispatcher, types
import asyncio
from random import randint
import importlib
import os
import requests

Token = '7985683028:AAE-XvdLwhfNzU6U8wxQHxKnj2nD8_gL1iI'
channel = ''

bot = Bot(token=Token)
dp = Dispatcher()

user_data = {}
project_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(project_dir, 'images')


email = 'bekhruzashurmatov1@gmail.com'
password = 'ElwGZZg0d4ja2b6BDyuQQNs4bJeMn0calvdmGZtV'

async def eskiz_login(email, password):
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {'email': email,
               'password': password}
    files = []
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    token = response.json()['data']['token']
    return token


async def send_sms(token, phone, verification_code):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    payload = {'mobile_phone': phone,
               'message': 'This is test from Eskiz',
               'from': '4546',
               'callback_url': 'http://0000.uz/test.php'}
    files = []
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code != 200:
        raise 'Что-то пошло не так'


@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    if message.text == '/start':
        await welcome(message)
    elif 'language' not in user_data[user_id]:
        await check_language(message)
    elif 'phone' not in user_data[user_id]:
        await check_phone(message)
    elif message.text in [lang.phone_btn2_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await resend_phone(message)
    elif message.text in [lang.sms_btn_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await resend_code(message)
    elif 'status' not in user_data[user_id]:
        await check_code(message)
    elif message.text in [lang.deliv_btn_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_delivery(message)
    elif message.text in [lang.deliv_btn2_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_settings(message)
    elif message.text in [lang.deliv_btn3_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_about(message)
    elif message.text in [lang.deliv_btn4_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_main(message)
    elif message.text in [lang.deliv_btn5_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_feedback(message)
    elif message.text in [lang.pickup_text for lang in [importlib.import_module(f'lang.{user_data[user_id]["language"]}')]]:
        await submenu_branches(message)
    elif 'back' in user_data[user_id]['state']:
        await back_menu(message)
    elif 'categories' in user_data[user_id]['state']:
        await show_menu(message)
    elif 'items' in user_data[user_id]['state']:
        await show_items(message)
    elif 'item' in user_data[user_id]['state']:
        await preview_item(message)
    elif 'preview' in user_data[user_id]['state']:
        await basket_m(message)
    elif 'delivery' in user_data[user_id]['state']:
        await preview_submenu_delivery(message)
    # elif 'branches' in user_data[user_id]['state']:
    #     await preview_submenu_branches(message)


async def welcome(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    button = [
        [
            types.KeyboardButton(text='🇷🇺 Русский'),
            types.KeyboardButton(text='🇬🇧 English'),
            types.KeyboardButton(text="🇺🇿 O'zbekcha")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"Здравствуйте! Добро пожаловать в наш бот!\n"
                         f"Давайте для начала выберем язык обслуживания!", reply_markup=keyboard)


def select_language(lang):
    if lang == '🇷🇺 Русский':
        return 'ru'
    elif lang == '🇬🇧 English':
        return 'en'
    elif lang == "🇺🇿 O'zbekcha":
        return 'uz'
    else:
        return 'uz'


async def check_language(message: types.Message):
    user_id = message.from_user.id
    lang = message.text
    lang = select_language(lang)
    user_data[user_id]['language'] = lang
    lang = importlib.import_module(f'lang.{lang}')
    button = [
        [types.KeyboardButton(text=lang.phone_btn_text, request_contact=True)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.phone_text}", reply_markup=keyboard)


async def check_phone(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text

    if phone[:4] != "+998":
        button = [
            [types.KeyboardButton(text=lang.phone_btn_text, request_contact=True)],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(f"{lang.phone_text}", reply_markup=keyboard)
        return

    user_data[user_id]['phone'] = phone
    await resend_verification_code(message)


async def resend_phone(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.phone_btn2_text:
        button = [
            [types.KeyboardButton(text=lang.phone_btn_text, request_contact=True)]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(f"{lang.phone_text}", reply_markup=keyboard)

        if 'phone' in user_data[user_id]:
            del user_data[user_id]['phone']


async def resend_verification_code(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.contact is not None:
        phone = message.contact.phone_number
    else:
        phone = message.text
    verification_code = randint(100000, 999999)
    user_data[user_id]['verification_code'] = verification_code
    try:
        token = await eskiz_login(email, password)
        await send_sms(token, phone, verification_code)
        button = [
            [types.KeyboardButton(text=lang.sms_btn_text)],
            [types.KeyboardButton(text=lang.phone_btn2_text)]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
        await message.answer(f"{lang.verify_text}", reply_markup=keyboard)
        await message.answer(f"<#> LOOOK\n"
                             f"code: {verification_code} - Kod podtverjdeniya dlya avtorizaci dlya bota v sisteme\n"
                             f"Delever\n"
                             f"OdFpf+SFqk/")
    except Exception as ex:
        print(ex)


async def resend_code(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.sms_btn_text:
        await resend_verification_code(message)


async def check_code(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    code = message.text
    verification_code = user_data[user_id]['verification_code']
    if code == str(verification_code):
        user_data[user_id]['status'] = 'verified'
        await main_menu(message)
    else:
        await message.answer(f"{lang.sms_text}")


async def back_menu(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.back_text or message.text == lang.menu_btn_text:
        await main_menu(message)


async def main_menu(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'back'
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    button = [
        [types.KeyboardButton(text=lang.deliv_btn_text)],
        [types.KeyboardButton(text=lang.deliv_btn2_text),
         types.KeyboardButton(text=lang.deliv_btn3_text)],
        [types.KeyboardButton(text=lang.deliv_btn4_text),
         types.KeyboardButton(text=lang.deliv_btn5_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.deliv_text}", reply_markup=keyboard)


async def submenu_delivery(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    user_data[user_id]['state'] = 'delivery'
    button = [
        [types.KeyboardButton(text=lang.pickup_text),
         types.KeyboardButton(text=lang.deliv1_text, request_location=True)],
        [types.KeyboardButton(text=lang.back_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.deliv_type}", reply_markup=keyboard)


async def preview_submenu_delivery(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.back_text:
        await main_menu(message)


async def submenu_settings(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')

    button = [
        [types.KeyboardButton(text=lang.lang_text),
         types.KeyboardButton(text=lang.birth_text)],
        [types.KeyboardButton(text=lang.phone_change_text),
         types.KeyboardButton(text=lang.back_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.choose_settings_text}", reply_markup=keyboard)


async def submenu_about(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')

    button = [
        [types.KeyboardButton(text=lang.back_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"loook", reply_markup=keyboard)


async def submenu_main(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')

    button = [
        [types.KeyboardButton(text=lang.menu_btn_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.menu_text}", reply_markup=keyboard)


async def submenu_feedback(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    button = [
        [types.KeyboardButton(text=lang.back_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.feedback_text}", reply_markup=keyboard)


async def submenu_branches(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    user_data[user_id]['state'] = 'categories'
    button = [
        [types.KeyboardButton(text=lang.back_text),
         types.KeyboardButton(text=lang.location_text, request_location=True)],
        [types.KeyboardButton(text=lang.branch1_text),
         types.KeyboardButton(text=lang.branch2_text)],
        [types.KeyboardButton(text=lang.branch3_text),
         types.KeyboardButton(text=lang.branch4_text)],
        [types.KeyboardButton(text=lang.branch5_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.answer(f"{lang.choose_branch}", reply_markup=keyboard)


# async def preview_submenu_branches(message:types.Message):
#     user_id = message.from_user.id
#     lang = user_data[user_id]['language']
#     lang = importlib.import_module(f'lang.{lang}')
#     if message.text == lang.back_text:
#         await submenu_delivery(message)


async def show_menu(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    if message.text == lang.branch1_text or message.text == lang.branch2_text or message.text == lang.branch3_text or message.text == lang.branch4_text or message.text == lang.branch5_text:
        await show_categories(message)


async def show_categories(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id]['state'] = 'items'
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    buttons = []
    row = []
    count = 1
    button = [types.KeyboardButton(text=lang.back_text),
              types.KeyboardButton(text=lang.cor1_text)]
    buttons.append(button)
    for category in lang.menu:
        button = types.KeyboardButton(text=category)
        row.append(button)
        count += 1

        if count % 2 != 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await message.answer(f"{lang.cat_text}", reply_markup=keyboard)


async def show_items(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    category = message.text
    user_data[user_id]['state'] = 'item'
    if message.text == lang.back_text:
        await submenu_delivery(message)
    elif category in lang.menu:
        user_data[user_id]['category'] = category
        buttons = []
        row = []
        count = 1
        button = [types.KeyboardButton(text=lang.back_text),
                  types.KeyboardButton(text=lang.cor1_text)]
        buttons.append(button)
        for item in lang.menu[category]:
            button = types.KeyboardButton(text=item)
            row.append(button)
            count += 1
            if count % 2 != 0:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
        keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer(f"{lang.prod_text}", reply_markup=keyboard)


async def preview_item(message:types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    item = message.text
    category = user_data[user_id]['category']
    count = 1
    text = ''

    if message.text == lang.back_text:
        del user_data[user_id]['category']
        await show_categories(message)

    elif item in lang.menu[category]:
        user_data[user_id]['state'] = 'preview'
        price = lang.menu[category][item]['price']
        image_title = lang.menu[category][item]['image']
        image_path = os.path.join(images_dir, image_title)
        user_data[user_id]['item'] = item
        global basket
        basket = {'item': item, 'count': 1}
        caption_text = f'{item}\n {lang.total_text}: {price}'
        media = types.InputMediaPhoto(
            media=types.FSInputFile(image_path),
            caption=caption_text
        )
        buttons = [
            [types.InlineKeyboardButton(text=f'➖', callback_data=f'minus,{item}'),
             types.InlineKeyboardButton(text=f'1', callback_data=f'count,{item}'),
             types.InlineKeyboardButton(text=f'➕', callback_data=f'plus,{item}')],
            [types.InlineKeyboardButton(text=f'{lang.cor_text}', callback_data=f'add,{item}')]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer_photo(types.FSInputFile(image_path), caption_text, reply_markup=keyboard)

    elif message.text == lang.cor1_text:
        user_data[user_id]['state'] = 'cart'
        btn = [[types.KeyboardButton(text=lang.yes), types.KeyboardButton(text=lang.return_menu)]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=btn, resize_keyboard=True)
        for i in basket_list:
            for k in i:
                total_price = i[k]
                # count += total_price
                text += f'{k} x {count} = {total_price}\n'
        user_data[user_id]['order_t'] = f'{text}\n{lang.total_text}: {total_price}'
        buttons = [
            [types.InlineKeyboardButton(text=f'{lang.confirm_order}', callback_data=f'minus,{item}')],
            [types.InlineKeyboardButton(text=f'{lang.continue_order}', callback_data=f'count,{item}')],
            [types.InlineKeyboardButton(text=f'{lang.clean_order}', callback_data=f'plus,{item}')],

            [types.InlineKeyboardButton(text=f'➖', callback_data=f'minus,{item}'),
             types.InlineKeyboardButton(text=f'{k}', callback_data=f'count,{item}'),
             types.InlineKeyboardButton(text=f'➕', callback_data=f'plus,{item}')]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(f'{lang.cor2_text}')
        await message.answer(f'{text}\n{lang.total_text}: {total_price}', reply_markup=keyboard)


@dp.callback_query(lambda c: c.data.startswith(('minus', 'plus', 'add')))
async def item_calculator(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    category = user_data[user_id]['category']
    user_id = callback.from_user.id
    action, item = callback.data.split(',')
    count = basket['count']
    price = lang.menu[category][item]['price']
    total_price = price * count
    if action == 'plus':
        count += 1
    elif action == 'minus':
        if count > 1:
            count -= 1
    elif action == 'add':
        await basket_summary(callback, user_id, basket, total_price)
    basket['count'] = count

    image_title = lang.menu[category][item]['image']
    image_path = os.path.join(images_dir, image_title)
    user_data[user_id]['item'] = item
    total_price = price * count
    caption_text = f'{item}\n {lang.total_text}: {count}x{price}={total_price}'
    media = types.InputMediaPhoto(
        media=types.FSInputFile(image_path),
        caption=caption_text
    )
    buttons = [
        [types.InlineKeyboardButton(text=f'➖', callback_data=f'minus,{item}'),
         types.InlineKeyboardButton(text=f'{count}', callback_data=f'count,{item}'),
         types.InlineKeyboardButton(text=f'➕', callback_data=f'plus,{item}')],
        [types.InlineKeyboardButton(text=f'{lang.cor_text}', callback_data=f'add,{item}')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    try:
        await callback.message.edit_media(media, reply_markup=keyboard)
    except:
        pass


basket_list = []
async def basket_summary(c, user_id, basket, total_price):
    if 'basket' not in user_data[user_id]:
        global basket_list
        basket_list = [{basket['item']: total_price}]
        user_data[user_id]['basket'] = basket_list
    else:
        basket_list.append({basket['item']: total_price})
        user_data[user_id]['basket'] = basket_list

    user_id = c.from_user.id
    user_data[user_id]['state'] = 'items'
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')

    buttons = []
    for category in lang.menu:
        button = [types.KeyboardButton(text=category)]
        buttons.append(button)
    # button = [types.KeyboardButton(text=lang.back)]
    # buttons.append(button)
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    await c.message.answer(lang.cat_text, reply_markup=keyboard)


all_basket = {}

async def basket_m(message: types.Message):
    user_id = message.from_user.id
    lang = user_data[user_id]['language']
    lang = importlib.import_module(f'lang.{lang}')
    user_data[user_id]['state'] = 'cart'
    if message.text == lang.cor1_text:
        item, c = basket.items()

        for i in basket_list:
            for k in i.values():
                await message.answer(f'{item[1]} x {c[1]} = {k}')
                all_basket[item[1]] = {'quantity': c[1], 'total_price': k}






async def main():
    await dp.start_polling(bot)


print('The bot is running...')
asyncio.run(main())

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data import alchemy

async def admin_buttons():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text="Statistika", callback_data="stat")
    btn2 = InlineKeyboardButton(text="Xabar yuborish", callback_data="send")
    btn3 = InlineKeyboardButton(text="Kanallarni sozlash", callback_data="channels")
    x.add(btn1, btn2, btn3)
    return x

async def channel_control():
    x = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="➕Kanal qo'shish", callback_data="channel_add")
    btn2 = InlineKeyboardButton(text="➖Kanalni olib tashlash", callback_data="channel_del")
    x.add(btn1, btn2)
    return x

async def home_keys():
    x = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardMarkup(text="👨‍💻Muxandis dasturchi",callback_data="collect-coder")
    btn2 = InlineKeyboardMarkup(text="👨‍🏫Informatika fani o'qituvchisi",callback_data="collect-teacher")
    btn3 = InlineKeyboardMarkup(text="🤵‍♂️Metodis",callback_data="collect-methodic")
    x.add(btn1,btn2,btn3)
    return x
    
async def join_key():
    keyboard = InlineKeyboardMarkup(row_width=1)
    x = await alchemy.get_channel()  
    r = 1
    for i in x:
        keyboard.add(
            InlineKeyboardButton(f"〽️ {r}-kanal", url=f"https://t.me/{i}")
        )
        r += 1
    keyboard.add(InlineKeyboardButton('✅ Tasdiqlash', callback_data='/start'))
    return keyboard

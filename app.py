from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from data.alchemy import (
    create_user, get_step, put_step, user_count, get_all_user, get_channel,
    put_channel, get_channel_with_id, delete_channel, change_info,get_info
)
from uuid import uuid4

from helper.zip_maker import zip_files
from parts.buttons import admin_buttons, channel_control, join_key, home_keys
import conf
import os
import logging

API_TOKEN = conf.BOT_TOKEN
ADMIN_ID = conf.ADMIN_ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

async def join(user_id):
    try:
        channels = await get_channel()
        r = 0
        for channel in channels:
            try:
                chat_member = await bot.get_chat_member(f"@{channel}", user_id)
                if chat_member.status in ['member', 'creator', 'administrator']:
                    r += 1
            except Exception as e:
                await bot.send_message(ADMIN_ID, f"Error checking chat member status: {e}")
        if r != len(channels):
            await bot.send_message(user_id,
                                   "<b>👋 Assalomu alaykum Botni ishga tushurish uchun kanallarga a'zo bo'ling va a'zolikni tekshirish buyrug'ini bosing.</b>",
                                   reply_markup=join_key())
            return False
        else:
            return True
    except Exception as e:
        await bot.send_message(ADMIN_ID, f"Error in join function: {e}")
        return True

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.text == "/start":
        await bot.send_message(message.chat.id, "<b>Salom, siz qaysi yo'nalish uchun hujjat topshirmoqchisiz?</b>", reply_markup=await home_keys())
        try:
            await create_user(cid=message.chat.id, name=message.chat.first_name)
        except Exception as e:
            logging.error(f"Error creating user: {str(e)}")

@dp.message_handler(content_types=['text'])
async def more(message: types.Message):
    if message.text == "/break":
       exit()
    step = await get_step(message.chat.id)
    try:
        if message.text == "/admin" and message.chat.id == ADMIN_ID:
            await bot.send_message(ADMIN_ID, "Salom, Admin", reply_markup=admin_buttons())
            await put_step(cid=message.chat.id, step="!!!")

        elif step == "channel_del" and message.text != "/start" and message.text != "/admin":
            try:
                channel_id = int(message.text)
                if await delete_channel(ch_id=channel_id):
                    await bot.send_message(message.chat.id, "Kanal olib tashlandi")
                else:
                    await bot.send_message(message.chat.id, "Xatolik! IDni to'g'ri kiritdingizmi tekshiring!")
            except Exception as e:
                await bot.send_message(message.chat.id, f"Error deleting channel: {e}")
            await put_step(cid=message.chat.id, step="!!!")

        elif step == "add_channel" and message.text != "/start" and message.text != "/admin":
            if await put_channel(message.text):
                await bot.send_message(message.chat.id, f"{message.text} kanali qabul qilindi!")
            else:
                await bot.send_message(message.chat.id, "Xatolik! Bu kanal oldin qo'shilgan bo'lishi mumkin yoki boshqa xatolik, iltimos tekshiring")
            await put_step(cid=message.chat.id, step="!!!")

        elif step == 'send':
            text = message.text
            mid = message.message_id
            await bot.send_message(message.chat.id, "Xabar yuborish boshlandi")
            try:
                for user_id in await get_all_user():
                    try:
                        await bot.forward_message(chat_id=user_id, from_chat_id=ADMIN_ID, message_id=mid)
                    except Exception as e:
                        logging.error(f"Error sending message to user {user_id}: {str(e)}")
                await bot.send_message(message.chat.id, "Tarqatish yakunlandi")
            except Exception as e:
                await bot.send_message(message.chat.id, f"Xabar yuborishda muammo bo'ldi: {str(e)}")
            await put_step(cid=message.chat.id, step="!!!")

        elif step == "get-passport":
            if message.document and message.document.mime_type == 'application/pdf':
                file_info = await bot.get_file(message.document.file_id)
                file_name = message.document.file_name
                downloaded_file = await bot.download_file(file_info.file_path)
                file_path = os.path.join(conf.DOWNLOADS_DIR, file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                await bot.reply_to(message, "Passport ma'lumotingiz qabul qilindi endi, diplomingizni yuboring, ilovasi bilan:")
                await change_info(cid=message.chat.id, type_info="passport_file_id", value=file_path)
                await put_step(cid=message.chat.id, step="get-diplom")
            else:
                await bot.reply_to(message, "Iltimos, faqat PDF fayllarini yuboring.")

        elif step == "get-diplom":
            if message.document and message.document.mime_type == 'application/pdf':
                file_info = await bot.get_file(message.document.file_id)
                file_name = message.document.file_name
                downloaded_file = await bot.download_file(file_info.file_path)
                file_path = os.path.join(conf.DOWNLOADS_DIR, file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                await bot.reply_to(message, "Diplom ma'lumotingiz qabul qilindi endi, obyektivinginni yuboring!")
                await change_info(cid=message.chat.id, type_info="diplom_file_id", value=file_path)
                await put_step(cid=message.chat.id, step="get-obyektiv")
            else:
                await bot.reply_to(message, "Iltimos, faqat PDF fayllarini yuboring.")

        elif step == "get-obyektiv":
            if message.document and message.document.mime_type == 'application/pdf':
                file_info = await bot.get_file(message.document.file_id)
                file_name = message.document.file_name
                downloaded_file = await bot.download_file(file_info.file_path)
                file_path = os.path.join(conf.DOWNLOADS_DIR, file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                await bot.reply_to(message, "Obyektivingiz qabul qilindi endi, sudlanganingiz yoki sudlanmaganingiz haqida ma'lumotni yuboring.")
                await change_info(cid=message.chat.id, type_info="obyektiv_file_id", value=file_path)
                await put_step(cid=message.chat.id, step="get-lang")
            else:
                await bot.reply_to(message, "Iltimos, faqat PDF fayllarini yuboring.")

        elif step == "get-lang":
            if message.document and message.document.mime_type == 'application/pdf':
                file_info = await bot.get_file(message.document.file_id)
                file_name = message.document.file_name
                downloaded_file = await bot.download_file(file_info.file_path)
                file_path = os.path.join(conf.DOWNLOADS_DIR, file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                await bot.reply_to(message, "Ma'lumotlaringiz adminga yuborildi")
                await change_info(cid=message.chat.id, type_info="legal_id", value=file_path)
                await put_step(cid=message.chat.id, step="get-legal")
            else:
                await bot.reply_to(message, "Iltimos, faqat PDF fayllarini yuboring.")

        elif step == "get-legal":
            if message.document and message.document.mime_type == 'application/pdf':
                file_info = await bot.get_file(message.document.file_id)
                file_name = message.document.file_name
                downloaded_file = await bot.download_file(file_info.file_path)
                file_path = os.path.join(conf.DOWNLOADS_DIR, file_name)
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                await bot.reply_to(message, "Ma'lumotlaringiz adminga yuborildi")
                await change_info(cid=message.chat.id, type_info="legal_id", value=file_path)
                await put_step(cid=message.chat.id, step="!!!")
            else:
                await bot.reply_to(message, "Iltimos, faqat PDF fayllarini yuboring.")
            
            #for zip 
            main_info = get_info(int(message.chat.id))
            p_type = main_info["person_type"]
            p_passport = main_info["passport"]
            p_diplom = main_info["diplom"]
            p_obyektiv = main_info["obyektiv"]
            p_lang = main_info["lang"]
            p_legal = main_info["legal"]

            l = [p_passport,p_diplom,p_obyektiv]
            if p_lang == "None": l.append(p_lang)
            if p_legal == "None": l.append(p_legal)

            res = zip_files(l, uuid4)
            with open(res, 'rb') as file:
                await message.answer_document(InputFile(file, filename=file), caption=p_type)
    except Exception as e:
        await bot.send_message(ADMIN_ID, f"Error in message handler: {e}")

@dp.callback_query_handler(lambda call: True)
async def callback_query(call: types.CallbackQuery):
    try:
        if "collect" in call.data:
            person_type = call.data.split("-")[1]
            await bot.send_message(call.message.chat.id, "Pasport yoki (ID-kartani)ni yuboring")
            await put_step(cid=call.message.chat.id, step="get-passport")
            await change_info(cid=call.message.chat.id, type_info="person_type", value=person_type)
        
        elif call.data == "/start":
            if await join(call.message.chat.id):
                await bot.send_message(call.message.chat.id, "<b>Obuna tasdiqlandi✅</b>")
        
        elif call.data == "stat" and str(call.message.chat.id) == str(ADMIN_ID):
            await bot.send_message(call.message.chat.id, f"Foydalanuvchilar soni: {await user_count()}")
        
        elif call.data == "send" and str(call.message.chat.id) == str(ADMIN_ID):
            await put_step(cid=call.message.chat.id, step="send")
            await bot.send_message(call.message.chat.id, "Forward xabaringizni yuboring")
        
        elif call.data == "channels" and str(call.message.chat.id) == str(ADMIN_ID):
            channels = await get_channel_with_id()
            await bot.send_message(call.message.chat.id, f"Kanallar ro'yxati:{channels}", reply_markup=channel_control())
        
        elif call.data == "channel_add" and str(call.message.chat.id) == str(ADMIN_ID):
            await put_step(cid=call.message.chat.id, step="add_channel")
            await bot.send_message(call.message.chat.id, "Kanali linkini yuboring! bekor qilish uchun /start !")
        
        elif call.data == "channel_del" and str(call.message.chat.id) == str(ADMIN_ID):
            await put_step(cid=call.message.chat.id, step="channel_del")
            channels = await get_channel_with_id()
            await bot.send_message(call.message.chat.id,
                                   f"{channels}\n⚠️O'chirmoqchi bo'lgan kanalingiz IDsini bering, bekor qilish uchun /start yoki /admin deng!")
    except Exception as e:
        await bot.send_message(ADMIN_ID, f"Error in callback query handler: {e}")

async def on_startup(dp):
    logging.info("Bot is starting...")

async def on_shutdown(dp):
    logging.info("Bot is stopping...")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

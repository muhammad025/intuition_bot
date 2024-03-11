import logging
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from buttons import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from sqlalchemy import create_engine
from aiogram.types import Message, CallbackQuery

API_TOKEN = '6811011387:AAES6B9op43Vm-Z6MIrV32JuAYUcXjDTdUk'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


db_engine = create_engine('sqlite:///transfers.db')

class Student(StatesGroup):
    fullname = State()
    password = State()
    phone = State()
    end = State()
    check_saver = State()


class Otziv(StatesGroup):
    # fullname = State()
    WAITING_FOR_REVIEW = State('waiting_for_review')

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Здравствуйте вас приветствует InTuition",reply_markup=boss_menu)

conn = sqlite3.connect('transfers.db')
cursor = conn.cursor()

# Create transfers table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS transfers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL
                )''')
conn.commit()



# States
class TransferState(StatesGroup):
    waiting_for_transfer = State()
    waiting_for_image = State()



# class ImageState(StatesGroup):
#     waiting_for_image = State()

fake_data = {
    "user_id": ['ism','password','phone']
}
@dp.message_handler(text="🔠Регистрация🔠")  
async def send_welcome(message: types.Message):
    await message.answer(f"Ведите свой имя и фамилия :")
    connection = sqlite3.connect("students.db")
    db = connection.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS users(
               fullname TEXT,
               password TEXT,
               phone TEXT

)""")
    
    db.execute(f"""
INSERT INTO users
VALUES (?,?,?)""",(f'{message.from_user.full_name}','password','phone'))
    connection.commit()
    await Student.fullname.set()
    

@dp.message_handler(state=Student.fullname)
async def echo(message: types.Message,state: FSMContext):
    fullname = message.text
    fake_data[message.from_user.id] = [fullname]
    # await message.answer(message.text)

    # await Student.fullname.set()

    await message.answer(f" Введите свой пароль:")

    await Student.next()


@dp.message_handler(state=Student.password)
async def echo(message: types.Message,state: FSMContext):
    # await message.answer(message.text)
    pss = fake_data[message.from_user.id]
    pss.append(message.text)
    fake_data[message.from_user.id] = pss
    contact = message.contact
    # await bot.send_contact(message.chat.id, contact.phone_number)
    await message.answer(f"Введите свой номер:",reply_markup=number)


    await Student.phone.set()
    # await state.finish()


# @dp.message_handler(state=Student.password)

    


@dp.message_handler(state=Student.phone,content_types=types.ContentType.CONTACT)
async def echo(message: types.Message,state: FSMContext):
    # await message.answer(message.contact)
    phone = message.contact['phone_number']
    pss = fake_data[message.from_user.id]
    pss.append(phone)

    connection = sqlite3.connect("students.db")
    db = connection.cursor()
    db.execute("""CREATE TABLE IF NOT EXISTS users(
                   fullname TEXT,
                   password TEXT,
                   phone TEXT
             

    )""")
        
    db.execute(f"""
    INSERT INTO users
    VALUES (?,?,?)""",(fake_data[message.from_user.id][0],fake_data[message.from_user.id][1],fake_data[message.from_user.id][2])) #  ,chatid
    connection.commit()

    await message.answer (f"Вы зарегестрировались🎉",reply_markup=boss_menu)

    await state.finish()


# @dp.message_handler(state=Student.money)
# async def echo(message: types.Message,state: FSMContext):
#     chatid = message.from_user.id
#     pss = fake_data[message.from_user.id]
#     pss.append(message.text)
#     fake_data[message.from_user.id] = pss
#     await message.answer("Введите свой сумму:")

#     connection = sqlite3.connect("students.db")
#     db = connection.cursor()
#     db.execute("""CREATE TABLE IF NOT EXISTS users(
#                    fullname TEXT,
#                    password TEXT,
#                    phone TEXT
             

#     )""")
        
#     db.execute(f"""
#     INSERT INTO users
#     VALUES (?,?,?,?)""",(fake_data[message.from_user.id][0],fake_data[message.from_user.id][1],fake_data[message.from_user.id][2],fake_data[message.from_user.id][3])) #  ,chatid
#     connection.commit()

#     await message.answer (f"Вы зарегестрировались🎉",reply_markup=boss_menu)

#     await state.finish()

   #    chatid INT

@dp.message_handler(text="📞Администрация📞")
async def echo(message: types.Message):
    await message.answer("+998 97 403 30 41")

@dp.message_handler(text="💰оплата💰")
async def echo(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text="💳Сделать оплату💳", callback_data='send_link')
    keyboard.add(button)
    await message.answer("Нажмите на кнопку что-бы сделать оплату", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'send_link')
async def send_link(callback_query: CallbackQuery):
    link = "https://my.click.uz/clickp2p/8228B4446313A9AA243C56E027E21BE37BF2B00EC639B74966FC8F37B5A64A60"  # Change this to your actual transfer link
    await callback_query.message.answer(f"""Нажмите [сюда]({link}) сделать перевод
    После перевод денег отправте чек нам,""", parse_mode=types.ParseMode.MARKDOWN)
    await Student.check_saver.set()


import sqlite3
from aiogram import types  # Assuming you are using aiogram library

@dp.message_handler(content_types=types.ContentType.PHOTO, state=Student.check_saver)
async def saver(message: types.Message, state: FSMContext):
    # Get the photo file ID
    photo_file_id = message.photo[-1].file_id
    
    # Download the photo file
    photo_file = await bot.download_file_by_id(file_id=photo_file_id)
    
    # Read the content of the BytesIO object (Note: no 'await' is needed for the read method)
    photo_content = photo_file.read()

    # Save the photo content to a local file
    file_path = f'uploads/{photo_file_id}.jpg'  # You can customize the file name and extension
    with open(file_path, 'wb') as local_file:
        local_file.write(photo_content)

    # Optionally, you can save additional information or perform further actions with the photo

    await message.answer("🎉Ваш перевод денег прошла успешно🎉")

#@dp.message_handler(text="👨‍🎓Профиль👨‍🎓",state = '*')
#async def echo(message: types.Message):
#    print(True)
 #   connection = sqlite3.connect("students.db")
 #   cursor = connection.cursor()
 #   users_list = cursor.execute("SELECT fullname,password,phone FROM users").fetchall()
 #   for i in users_list:
 #       print(i)
 #       if i[0] == message.from_user.username:
 #           # cursor.execute("SELECT * FROM students.db").fetchall()
  #          await message.answer(f"Уважаемый ученик\nИмя - {i[0]}\nПароль - {i[1]}\nНомер - {i[2]}")
        # else:
  #      #     await message.answer("Такое акаунта не сушествует")
 #           await message.answer("Вот ваши данный")
    

@dp.message_handler(text="👨‍🎓Профиль👨‍🎓", state='*')
async def echo(message: types.Message):
    print(True)
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()
    users_list = cursor.execute("SELECT fullname, password, phone FROM users").fetchall()

    for i in users_list:
        print(i)
        if i[2] == message.from_user.username:
            await message.answer(f"Уважаемый ученик\nИмя - {i[0]}\nПароль - {i[1]}\nНомер - {i[2]}")
            user_found = True

    if not user_found:
        await message.answer("Такой аккаунт не существует")
    else:
        await message.answer("Вот ваши данные")



@dp.message_handler(text="✍️ Оставить отзыв")
async def cmd_leave_review(message: types.Message):
    # Вход в состояние ожидания отзыва
    await Otziv.WAITING_FOR_REVIEW.set()

    # Запрашиваем у пользователя отзыв
    await message.reply("Пожалуйста, напишите ваш отзыв:",reply_markup=boss_menu)


# Обработчик для получения отзыва в состоянии WAITING_FOR_REVIEW
@dp.message_handler(state=Otziv.WAITING_FOR_REVIEW)
async def process_review(message: types.Message, state: FSMContext):
    # Получаем отзыв от пользователя
    review_text = message.text

    await state.finish()

    await message.reply("Спасибо за ваш отзыв! Мы очень ценим ваше мнение.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

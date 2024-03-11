from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

boss_menu = ReplyKeyboardMarkup(
    keyboard=
    [
        [
            KeyboardButton(text="🔠Регистрация🔠"),
          
        ],
        [
            KeyboardButton(text="👨‍🎓Профиль👨‍🎓"),
            KeyboardButton(text="📞Администрация📞"),
        ],
        [
            KeyboardButton(text="✍️ Оставить отзыв"),
            KeyboardButton(text="💰оплата💰"),
        ],
],
resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱Отправить номер📱", request_contact=True)
        ]
    ],
 resize_keyboard=True
)

# money = InlineKeyboardMarkup(
#     keyboard=[
#         [
#             InlineKeyboardButton(text="💳Сделать оплату💳", callback_data='send_link')
#         ]
#     ]
# )
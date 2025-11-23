import sqlite3
import telebot
import random
from datetime import datetime
from telebot import types
from Levenshtein import ratio
import sys

bot = telebot.TeleBot("7751699195:AAF0AzfPFOupH1BU1BUC6ZO8kmGwvyUlPVQ")

birthday_cong = bool(0)
idt = ''
in_research = bool(0)
# для изменения шрифта в сообщении:

def test_send_message_with_markdown(self):
    markdown = """
    *bold text*
    _italic text_
    [text](URL)
    """
    ret_msg = tb.send_message(CHAT_ID, markdown, parse_mode="Markdown")
    assert ret_msg.message_id

# табличка с данными

def create_table():
    conn = sqlite3.connect('../.idea/meetme.sql')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS profiles ( user_id INTEGER PRIMARY KEY, name TEXT, age TEXT, photo TEXT, sex TEXT, hobby TEXT )''')
    conn.commit()
    conn.close()

create_table()


def calculate_age(birthdate_str):
    try:
        birthdate = datetime.strptime(birthdate_str, '%d.%m.%Y').date()
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    except ValueError:
        return -1
    else:
        return age

def birthday_check(idt):
    today = datetime.today()
    conn = sqlite3.connect('../.idea/meetme.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles WHERE user_id=?", (idt,))
    profile = cur.fetchone()
    conn.close()
    if profile != None:
        try:
            birthdate_str = str(profile[2])
            birthdate = datetime.strptime(birthdate_str, '%d.%m.%Y').date()
        except:
            return 0
        if today.day == birthdate.day and today.month == birthdate.month:
            return 1
        else:
            return 0

def sex_identity():
    conn = sqlite3.connect('../.idea/meetme.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles WHERE user_id=?", (idt,))
    profile = cur.fetchone()
    conn.close()
    return profile[4]

def zodiac_sign(date_string):
    try:
        day, month, year = map(int, date_string.split('.'))
    except ValueError:
        return '-'
    else:
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Водолей ♒"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Рыбы ♓"
        elif (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Овен ♈"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Телец ♉"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Близнецы ♊"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Рак ♋"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Лев ♌"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Дева ♍"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return "Весы ♎"
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return "Скорпион ♏"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Стрелец ♐"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Козерог ♑"

@bot.message_handler(commands=['return'])
def return_to_start(message):
    main(message)


@bot.message_handler(commands=['start'])
def main(message):
    global birthday_cong, idt
    idt = message.from_user.id
    if birthday_cong == 0 and birthday_check(idt) == 1:
        birthday_cong = 1
        bot.send_message(message.chat.id, "MeetMe бот поздравляет тебя с днём рождения! 🤩🥳")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("1 ✨")
    item2 = types.KeyboardButton("2 🔎")
    item3 = types.KeyboardButton("3 🛠")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}, Я твой виртуальный помощник в мире знакомств!'
                     f' 💖Готов найти интересных людей и новые знакомства? Давай начнём!'
                     f'\n{item1.text} Создать профиль\n{item2.text} Поиск Партнёров\n{item3.text} Мой профиль\n'
                     f'Выбери один из вариантов, чтобы сделать свой первый шаг к новым знакомствам!', reply_markup = markup)

# создание профиля

    @bot.message_handler(func=lambda message: message.text == "1 ✨")
    def create_profile(message):
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE user_id=?", (message.from_user.id,))
        profile = cur.fetchone()
        conn.close()
        if profile is None:
            bot.send_message(message.chat.id, "Отлично! Давайте создадим твою анкету. Напиши свое имя: ")
            bot.register_next_step_handler(message, get_name)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton("ДА")
            item3 = types.KeyboardButton("НЕТ")
            markup.add(item2, item3)
            bot.send_message(message.chat.id, "У тебя уже есть профиль! Может ты хочешь создать его заново?", reply_markup = markup)
            bot.register_next_step_handler(message, reset_profile)

    def reset_profile(message):
        if message.text == "ДА":
            bot.send_message(message.chat.id, "Отлично! Давайте создадим твою анкету. Напиши свое имя: ")
            bot.register_next_step_handler(message, get_name)
        if message.text == "НЕТ":
            main(message)

    def get_name(message):
        name = message.text
        bot.send_message(message.chat.id, f"Супер! {name}, теперь отправь свой возраст в формате: XX.XX.XXXX \n_например: 11.09.2001_",parse_mode="Markdown")
        bot.register_next_step_handler(message, get_age, name)

    def get_age(message, name):
        age = message.text
        if calculate_age(age) >= 0:
            bot.send_message(message.chat.id, "Замечательно! Теперь отправь мне свою фотографию. ")
            bot.register_next_step_handler(message, get_photo, name, age)
        else:
            bot.send_message(message.chat.id, "Вы ввели свой возраст неправильно!")
            bot.send_message(message.chat.id, "Попробуйте ещё раз")
            bot.register_next_step_handler(message, get_age, name)

    def get_photo(message, name, age):
        ifitsphoto = bool(1)
        try:
            photo_file_id = message.photo[-1].file_id
            photo = photo_file_id
        except Exception:
            e = sys.exc_info()[1]
            print(e.args[0])
            bot.send_message(message.chat.id, "Вы отправили не фото 😡")
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            bot.register_next_step_handler(message, get_photo, name, age)
            ifitsphoto = False
        if ifitsphoto == 1:
            file_info = bot.get_file(photo)
            bot.download_file(file_info.file_path)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("♂️🚹")
            item2 = types.KeyboardButton("♀️️🚺")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, "Наайс! Теперь выбери свой пол:", reply_markup = markup)
            bot.register_next_step_handler(message, get_sex, name, age, photo_file_id)

    def get_sex(message, name, age, photo_file_id):
        sex = message.text
        if sex == "♂️🚹" or sex == "♀️️🚺":
            bot.send_message(message.chat.id,"Ого! Теперь расскажи о своих увлечениях.")
            bot.register_next_step_handler(message, get_hobby, name, age, photo_file_id, sex)
        else:
            bot.send_message(message.chat.id, "Ты сделал что-то не так 🤡")
            bot.send_message(message.chat.id, "Попробуйте еще раз")
            bot.register_next_step_handler(message, get_sex, name, age, photo_file_id)

    def get_hobby(message, name, age, photo_file_id, sex):
        hobby = message.text
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute('''INSERT OR REPLACE INTO profiles VALUES (?, ?, ?, ?, ?, ?)''',(message.from_user.id, name, age, photo_file_id, sex, hobby))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id,"Отлично! Твой профиль создан! Теперь ты можешь искать людей с похожими интересами")
        main(message)
# просмотр и редактирование профлия

    @bot.message_handler(func=lambda message: message.text == "2 🔎")
    def research(message):
        global idt, in_research
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE user_id=?", (message.from_user.id,))
        profile = cur.fetchone()
        if profile is None:
            bot.send_message(message.chat.id, "Вы не можете искать людей без профиля. Пожалуйста, создайте профиль.")
            return
        else:
            if message.text == "🔙":
                main(message)
            else:
                if message.text == "👍":
                    bot.send_message(message.chat.id, "Ура, вы нашли лучшую пару для себя, наверно вы даже сможете пообщаться в будущем.")
                cur.execute("SELECT user_id FROM profiles")
                user_ids = cur.fetchall()
                if in_research == 0:
                    bot.send_message(message.chat.id, f"Вот что нам удалось найти для тебя:")
                    in_research = 1
                random_user_id = random.choice(user_ids)[0]  # Выбираем случайный user_id
                cur.execute("SELECT * FROM profiles WHERE user_id=?", (random_user_id,))
                profile = cur.fetchone()
                if random_user_id != idt: # profile[4] != sex_identity() and
                    #print(idt)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("👍")
                    item2 = types.KeyboardButton("👎")
                    item3 = types.KeyboardButton("🔙")
                    markup.add(item1, item2, item3)
                    bot.send_message(message.chat.id, f"{profile[1]}"
                                                           f"\n{calculate_age(profile[2])} лет"
                                                           f"\nЗнак Зодиака: {zodiac_sign(profile[2])}"
                                                           f"\nПол: {profile[4]}"
                                                           f"\nУвлечения: {profile[5]}"
                                                           f"\nФото:", reply_markup = markup)
                    photo = profile[3]
                    bot.send_photo(message.chat.id, photo, reply_markup = markup)
                    conn.close()
                    bot.register_next_step_handler(message, research)




    @bot.message_handler(func=lambda message: message.text == "3 🛠")
    def show_profile(message):
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM profiles WHERE user_id=?", (message.from_user.id,))
        profile = cur.fetchone()
        conn.close()

        if profile is None:
            bot.send_message(message.chat.id, "Профиль не найден. Пожалуйста, создайте профиль.")
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Изменить что-либо")
        item2 = types.KeyboardButton("Вернуться в меню")
        markup.add(item1, item2)
        bot.send_message(message.chat.id,f"Твой текущий профиль:\nИмя: {profile[1]}"
                                         f"\nВозраст: {calculate_age(profile[2])}"
                                         f"\nЗнак Зодиака: {zodiac_sign(profile[2])}"
                                         f"\nПол: {profile[4]}"
                                         f"\nУвлечения: {profile[5]}"
                                         f"\nФото:",reply_markup = markup)
        photo = profile[3]
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id,f"Что ты хочешь сделать?",reply_markup = markup)
        bot.register_next_step_handler(message, edit_profile_proceed)

    def edit_profile_proceed(message):
        if message.text == "Изменить что-либо":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Изменить имя")
            item2 = types.KeyboardButton("Изменить дату рождения")
            item3 = types.KeyboardButton("Изменить фото")
            item4 = types.KeyboardButton("Изменить увлечения")
            markup.add(item1, item2, item3, item4)
            bot.send_message(message.chat.id, f"Выбери что хочешь изменить:", reply_markup=markup)
            bot.register_next_step_handler(message, edit_profile_handler)
        elif message.text == "Вернуться в меню":
            main(message)

# обработка выбора изменения в профиле

    def edit_profile_handler(message):
        if message.text == "Изменить имя":
            bot.send_message(message.chat.id, "Напиши новое имя:")
            bot.register_next_step_handler(message, edit_name)
        elif message.text == "Изменить дату рождения":
            bot.send_message(message.chat.id, "Напиши новую дату рождения")
            bot.register_next_step_handler(message, edit_age)
        elif message.text == "Изменить фото":
            bot.send_message(message.chat.id, "Отправь новую фотографию:")
            bot.register_next_step_handler(message, edit_photo)
        elif  message.text == "Изменить увлечения":
            bot.send_message(message.chat.id, "Напиши новые увлечения:")
            bot.register_next_step_handler(message, edit_hobby)
        else:
            info(message)

# изменение имени

    def edit_name(message):
        name = message.text
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET name=? WHERE user_id=?", (name, message.from_user.id))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Имя успешно изменено!")
        show_profile(message)

    def edit_age(message):
        age = message.text
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET age=? WHERE user_id=?", (age, message.from_user.id))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Дата рождения успешно изменена!")
        show_profile(message)

# изменение фото

    def edit_photo(message):
        photo_file_id = message.photo[-1].file_id
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET photo=? WHERE user_id=?", (photo_file_id, message.from_user.id))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Фотография успешно изменена!")
        show_profile(message)

#Изменение увлечений

    def edit_hobby(message):
        hobby = message.text
        conn = sqlite3.connect('../.idea/meetme.sql')
        cur = conn.cursor()
        cur.execute("UPDATE profiles SET hobby=? WHERE user_id=?", (hobby, message.from_user.id))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, "Увлечения успешно изменены!")
        show_profile(message)

#Сброс настроек

    @bot.message_handler(commands=['reset'])
    def reset(message):
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Да')
        button2 = types.KeyboardButton('Отмена')
        markup2.add(button1, button2)
        bot.send_message(message.chat.id, f'Вы точно хотите сбросить все ваши настройки?', reply_markup=markup2)
        bot.register_next_step_handler(message, confirm_reset)

    def confirm_reset(message):
        if message.text == "Да":
            conn = sqlite3.connect('../.idea/meetme.sql')
            cur = conn.cursor()
            cur.execute("DELETE FROM profiles WHERE user_id=?", (message.from_user.id,))
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, f'Вы успешно сбросили все настройки.')
            main(message)
        else:
            main(message)


#Обработчик помощи

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, 'Пока мы вам ничем не поможем 😔, но вы можете ввести /return, чтобы вернуться в главное меню')

#Обработчик стандартных сообщений

    @bot.message_handler()
    def info(message):
        if message.text.lower() == 'привет':
            bot.send_message(message.chat.id,
                    f'Привет, {message.from_user.first_name}, у тебя есть какие-то пожелания?')
        elif message.text.lower() == 'id':
            bot.reply_to(message, f'ID: {message.from_user.id}')
        else:
            bot.send_message(message.chat.id, "Я тебя не понимаю 😔. Попробуй использовать команды /start, /help, /return или введи текст из меню!")


bot.infinity_polling(none_stop=True)

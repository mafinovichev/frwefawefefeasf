from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
from random import randint

conn = sqlite3.connect(r'data.db')
cur = conn.cursor()

bot = Bot(token="5712862945:AAF7p18HPvYWUGu-nFZeI8C_xBk7yJx5MC8")
dp= Dispatcher(bot)

a=None
words=None
current_word=0
start_check = False

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    cur.execute("SELECT idtg FROM users;")
    result = cur.fetchall()
    user_tgid = message.from_user.id
    print(type(user_tgid))
    if (str(user_tgid), ) in result:
        await message.reply('You are registered!')
    else:
        cur.execute(f"""
        INSERT INTO USERS(idtg) VALUES({user_tgid});
        """)

        cur.execute(f"""
                INSERT INTO STATUS(tgid) VALUES({user_tgid});
                """)

        cur.execute(f"""
                INSERT INTO WORD(tgid) VALUES({user_tgid});
        """)

        cur.execute(f"INSERT INTO STATUS(status) WHERE tgid='{user_tgid}' VALUES(None);")

        conn.commit()
        await message.reply('Welcome!')

    i = 0
    print(result)
    start_check = True

@dp.message_handler(commands=['fill'])
async def process_start_command(mesasge: types.Message):
    await mesasge.reply('Enter two words in "Word:Translate"')
    user_tgid = mesasge.from_user.id
    cur.execute(f"INSERT INTO STATUS(status) WHERE tgid='{user_tgid}' VALUES(fill);")
    text = mesasge.text


@dp.message_handler(commands=['interview'])
async def process_start_command(mesasge: types.Message):
    await mesasge.reply('Interview start')
    global a
    global words
    global current_word
    user_tgid = mesasge.from_user.id
    cur.execute(f"SELECT words FROM word WHERE tgid={user_tgid};")
    results = cur.fetchone()
    print(results)
    a = 'interview'
    word = results[0].split(",")
    words = word[current_word].split(":")
    print(word)
    print(words)
    await mesasge.reply(words[current_word])



@dp.message_handler()
async def echo_send(message: types.Message):
    if a==None:
        await bot.send_message(message.from_user.id, message.text)
    elif a == 'fill':
        user_tgid = message.from_user.id
        cur.execute(f"SELECT tgid FROM word")
        result = cur.fetchall()
        if (str(user_tgid),) in result:
            cur.execute(f"SELECT words FROM word WHERE tgid={user_tgid};")
            results = cur.fetchone()
            new_string = results[0]+","+message.text
            cur.execute(f"UPDATE word SET words='{new_string}' where tgid={user_tgid};")
            conn.commit()
            await bot.send_message(message.from_user.id, 'Add ' + message.text)
        else:
            cur.execute(f"INSERT INTO WORD(tgid,words)VALUES({user_tgid},'{message.text}')")
            conn.commit()
            await bot.send_message(message.from_user.id, 'Add ' + message.text)

    elif a =='interview':
        global current_word
        global words

        if current_word >= len(words):
            await bot.send_message(message.from_user.id,'Interview finished')
        else:
            if message.text==words[current_word+1]:
                await bot.send_message(message.from_user.id,'Good!')
                current_word+=1
                await bot.send_message(message.from_user.id, words[current_word][0])




executor.start_polling(dp, skip_updates=True)
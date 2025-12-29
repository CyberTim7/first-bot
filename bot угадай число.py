from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import asyncio
from random import randint
import dotenv
import os

dotenv.load_dotenv('C:\\Users\\Lena\\Desktop\\github proects\\бот угадай число\\.env.txt')
bot_token = os.getenv('bot_token')



bot = Bot(token=bot_token)
dp = Dispatcher()

users = {}


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Привет! Я бот угадай число.\nГотов начинать?')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
        'attempts': 10,}    
        

@dp.message(Command(commands='users'))
async def info(message:Message):
    await message.answer(str(users))
    

@dp.message(Command(commands='cancel'))
async def cancel_command(message:Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры.\nЧтобы начать заново скажите "играть"')
        users[message.from_user.id]['in_game'] = False
        users[message.from_user.id]['attempts'] = 10
    else:
        await message.answer('В данный момент вы не играете.\nЕсли хотите начать скажите "играть"')


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def start_game(message:Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        global number
        number = randint(1, 100)
        await message.answer('Отлично!\nЯ загадал число от 1 до 100, угадай его!')
    else:
        await message.answer('Во время игры могу понимать только число или команду "cancel"')

@dp.message(F.text.lower().in_(['нет', 'не хочу']))
async def no_game(message: Message):
    await message.answer('Хорошо.\nЕсли захочешь сыграть напиши "играть"')

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_game(message: Message):
    if users[message.from_user.id]['in_game']:

        if int(message.text) == number:
                await message.answer('Вы угадали!\nСыграем еще?')
                users[message.from_user.id]['in_game'] = False
                users[message.from_user.id]['attempts'] = 10
        
        elif int(message.text) < number:
                users[message.from_user.id]['attempts'] -= 1
                await message.answer(f'Загаданное число больше\nОсталось попыток {users[message.from_user.id]['attempts']}')                
        
        elif int(message.text) > number:
                users[message.from_user.id]['attempts'] -= 1
                await message.answer(f'Загаданное число меньше\nОсталось попыток {users[message.from_user.id]['attempts']}')
        
        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'У вас больше не осталось попыток.\nЗагаданное число: {number}')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['attempts'] = 10
    else:
        await message.answer('Если хотите поиграть, сообщите мне об этом. Скажите "играть"')

    


async def main():
    print('Начинаю опрос сервера')
    try:
        await asyncio.wait_for(dp.start_polling(bot), timeout=200)
    except TimeoutError:
        print('Опрос сервера завершен')


if __name__ == '__main__':
    asyncio.run(main())

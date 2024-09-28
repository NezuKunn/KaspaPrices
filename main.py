import requests
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = '7850905881:AAGTeB1efx-HaJNxFtRVNyT0qicP4yq6CWs'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def set_commands(bot):
    commands = [
        types.BotCommand(command="/start", description="Start a bot")
    ]
    await bot.set_my_commands(commands)

yes = types.InlineKeyboardMarkup(row_width=2)
row = types.InlineKeyboardButton(text="Yeah!", callback_data="set")
yes.add(row)

async def aloa(bot):
    price = 0
    channel_id = -1002473253895
    url = f"https://api.kaspa.org/info/price?stringOnly=false"
    index = 0

    while True:
        headers = {
            "accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers).json()

            if index == 1:
                ca = "🔴" if price > float(response['price']) else "🟢"
            else:
                ca = "🟢"
                index = 1

            message_text = f"{ca} <b>${round(float(response['price']), 6)}</b> USDT"

            price = float(response['price'])

            await bot.send_message(channel_id, message_text, "html")
        except Exception as e:
            print(e)
        await asyncio.sleep(60*1)

@dp.message_handler(commands=['alo'])
async def start(message: types.Message, state: FSMContext):
    if message.from_user.id == 1495371921:
        asyncio.gather(aloa(bot))

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    asyncio.gather(set_commands(bot))
    try:
        data = await state.get_data()
        star = data["start"]
        if star == 1:
            mess = await bot.send_message(
                chat_id=message.chat.id,
                text="Prices has been added to this chat."
            )
            await asyncio.sleep(2)
            await bot.delete_message(
                chat_id=message.chat.id,
                message_id=mess.message_id
            )
            return
    except:
        pass
    await state.update_data(start=0)

    mess = await bot.send_message(
        chat_id=message.chat.id,
        text="Send Prices?",
        reply_markup=yes
    )
    await state.update_data(mess=mess)

@dp.callback_query_handler(lambda c: c.data == 'set')
async def da(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(start=1)
    data = await state.get_data()
    mess = data["mess"]
    await bot.delete_message(
        chat_id=callback_query.message.chat.id,
        message_id=mess.message_id
    )
    
    channel_id = callback_query.message.chat.id
    url = f"https://api.kaspa.org/info/price?stringOnly=false"
    index = 0

    while True:
        headers = {
            "accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers).json()

            if index == 1:
                data = await state.get_data()
                price = data["price"]

                ca = "📉" if price > float(response['price']) else "📈"
            else:
                ca = "📈"
                index = 1

            message_text = f"{ca} <b>${round(float(response['price']), 6)}</b> USDT"

            await state.update_data(price=float(response['price']))

            await bot.send_message(channel_id, message_text, "html")
        except Exception as e:
            print(e)
        await asyncio.sleep(60*1)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers import other_handlers, user_handlers

async def main() -> None:
    load_dotenv('.env')
    bot: Bot = Bot(token=os.getenv("API_TOKEN"))
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'There is exception - {_ex}')

# Запускаем поллинг
if __name__ == '__main__':
    asyncio.run(main())
#executor.start_polling(dp, skip_updates=True)



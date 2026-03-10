import os, asyncio, datetime, asyncpg
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

load_dotenv()
router = Router()
services = ['💅 Маникюр', '✂️ Стрижка', '💆‍♀️ Массаж']
pool = None

class Book(StatesGroup): manual = State()

async def is_free(d: datetime.date):
    async with pool.acquire() as conn:
        return not await conn.fetchval("SELECT 1 FROM records WHERE date = $1", d)

def kb_services():
    kb = InlineKeyboardBuilder()
    for s in services: kb.button(text=s, callback_data=f"s_{s}")
    return kb.adjust(1).as_markup()

async def kb_dates():
    kb = InlineKeyboardBuilder()
    d, count = datetime.date.today(), 0
    async with pool.acquire() as conn:
        taken = {r['date'] for r in await conn.fetch("SELECT date FROM records WHERE date >= $1", d)}
    while count < 6:
        if d not in taken:
            d_str = d.strftime("%d.%m.%Y")
            kb.button(text=d_str, callback_data=f"d_{d_str}")
            count += 1
        d += datetime.timedelta(days=1)
    kb.button(text="✍️ Ввести вручную", callback_data="manual")
    kb.button(text="🔙 В меню", callback_data="start")
    return kb.adjust(2, 2, 2, 1, 1).as_markup()

@router.message(F.text == '/start')
async def start_msg(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("✨ <b>Новая запись</b>\nВыберите услугу:", reply_markup=kb_services())

@router.callback_query(F.data == 'start')
async def start_call(c: CallbackQuery, state: FSMContext):
    await state.clear()
    await c.message.edit_text("✨ <b>Новая запись</b>\nВыберите услугу:", reply_markup=kb_services())

@router.callback_query(F.data.startswith('s_'))
async def get_srv(c: CallbackQuery, state: FSMContext):
    await state.update_data(srv=c.data[2:])
    await c.message.edit_text(f"Услуга: <b>{c.data[2:]}</b>\n\n📅 Выберите дату:", reply_markup=await kb_dates())

@router.callback_query(F.data == 'manual')
async def ask_manual(c: CallbackQuery, state: FSMContext):
    await state.set_state(Book.manual)
    await c.message.edit_text("✍️ Введите дату (ДД.ММ.ГГГГ):")

@router.callback_query(F.data.startswith('d_'))
async def get_date_call(c: CallbackQuery, state: FSMContext):
    d_str = c.data[2:]
    d_obj = datetime.datetime.strptime(d_str, "%d.%m.%Y").date()
    if not await is_free(d_obj): return await c.message.edit_text("❌ Дата занята. Выберите другую:", reply_markup=await kb_dates())
    
    data = await state.get_data()
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO records VALUES ($1, $2)", d_obj, data['srv'])
        
    await c.message.edit_text(f"✅ <b>Записано!</b>\nУслуга: {data['srv']}\n📅 Дата: <b>{d_str}</b>")
    await c.message.answer("✨ Хотите записаться еще?", reply_markup=kb_services())
    await state.clear()

@router.message(Book.manual)
async def get_date_msg(m: Message, state: FSMContext):
    try:
        d = datetime.datetime.strptime(m.text, "%d.%m.%Y").date()
        if d < datetime.date.today(): return await m.answer("⚠️ Эта дата уже прошла. Введите другую:")
        if not await is_free(d): return await m.answer("❌ Эта дата занята. Введите другую:", reply_markup=await kb_dates())
        
        data = await state.get_data()
        async with pool.acquire() as conn:
            await conn.execute("INSERT INTO records VALUES ($1, $2)", d, data['srv'])
            
        await m.answer(f"✅ <b>Записано!</b>\nУслуга: {data['srv']}\n📅 Дата: <b>{m.text}</b>")
        await m.answer("✨ Хотите записаться еще?", reply_markup=kb_services())
        await state.clear()
    except ValueError: await m.answer("⚠️ Неверный формат. Используйте <b>ДД.ММ.ГГГГ</b>:")

async def main():
    global pool
    pool = await asyncpg.create_pool(os.getenv('DATABASE_URL'))
    async with pool.acquire() as conn:
        await conn.execute("CREATE TABLE IF NOT EXISTS records (date DATE PRIMARY KEY, srv TEXT)")
        
    bot = Bot(token=os.getenv('BOT_TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
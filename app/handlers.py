from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from aiogram.types.menu_button_commands import MenuButtonCommands

from aiogram import F, Router

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Добро пожаловать в магазин еды', reply_markup=kb.main)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара.', reply_markup=await kb.categories())


@router.message(F.text == 'О нас')
async def info(message: Message):
    await message.answer('Вкус деревни - наше небольшое семейное хозяйство, расположенное недалеко от г. Такого-то '
                         'Московской обл., где с 2012 года мы производим натуральные, полезные и вкусные продукты '
                         '🏡\n\nПредлагаем попробовать:\n\n🧀 Продукцию наших коров и коз - \nот молока до сыра\n\n🍗 Мясо '
                         'бройлеров и перепелов\n\n🥚 Яйца куриные и перепелиные\n\nБесплатная доставка по Москве \nи '
                         'области 📦', reply_markup=kb.main)


@router.message(F.text == 'Контакты')
async def info(message: Message):
    await message.answer('Наши контакты:', reply_markup=await kb.links())


@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории', reply_markup=await kb.items(callback.data.split('_')[1]))


@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\n\nОписание: {item_data.description}\n\nЦена: {item_data.price}руб.', reply_markup=await kb.update_case())


@router.callback_query(F.data.startswith('update_case'))
async def upd_case(callback: CallbackQuery):
    await callback.answer('Товар был добавлен в корзину')


@router.callback_query(F.data.startswith('to_main'))
async def to_main(callback: CallbackQuery):
    await callback.answer('Перешли к каталогу')
    await callback.message.answer('Выберите категорию товара.', reply_markup=await kb.categories())


@router.callback_query(F.data.startswith('link_'))
async def links_sm(callback: CallbackQuery):
    await callback.answer('Вы перешли по ссылке')

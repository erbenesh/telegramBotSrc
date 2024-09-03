from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_category_item, get_link

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Каталог')],
                                     [KeyboardButton(text='Корзина')],
                                     [KeyboardButton(text='Контакты'),
                                      KeyboardButton(text='О нас')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


async def links():
    all_links = await get_link()
    keyboard = InlineKeyboardBuilder()

    for link in all_links:
        keyboard.add(InlineKeyboardButton(text=link.name, callback_data=f"link_{link.id}", url=f'{link.link}'))
    keyboard.add(InlineKeyboardButton(text='К каталогу', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, callback_data=f"category_{category.id}"))
    keyboard.add(InlineKeyboardButton(text='К каталогу', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def items(category_id):
    all_items = await get_category_item(category_id)
    keyboard = InlineKeyboardBuilder()

    for item in all_items:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}"))
    keyboard.add(InlineKeyboardButton(text='К каталогу', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()


async def update_case():
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='В корзину', callback_data='update_case'))
    keyboard.add(InlineKeyboardButton(text='К каталогу', callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

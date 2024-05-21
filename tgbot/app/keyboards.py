from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from app.languages import Language

async def main(data: dict):
    language = Language(language=data['language'])
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=language.get_string('chat_btn'), callback_data='chat'))
    keyboard.add(InlineKeyboardButton(text=language.get_string('help_btn'), callback_data='help'))
    keyboard.add(InlineKeyboardButton(text=language.get_string('settings_btn'), callback_data='settings'))
    return keyboard.adjust(3).as_markup()

async def settings(data: dict):
    language = Language(language=data['language'])
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=language.get_string('change_lang'), callback_data="change_lang"))
    return keyboard.adjust(1).as_markup()

async def change_lang(data: dict):
    language = Language(language=data['language'])
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text=language.get_string('english'), callback_data="Eng"),
                 InlineKeyboardButton(text=language.get_string('russian'), callback_data="Ru"))
    return keyboard.adjust(2).as_markup()

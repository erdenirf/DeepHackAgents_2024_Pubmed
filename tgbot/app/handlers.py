import requests
import httpx
import asyncio
from aiohttp import ClientSession
from aiogram import F, Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from app.languages import Language
from app.config import URL
# from app.middlewares import WebHook
import os
from dotenv import load_dotenv

SERVE_URL = URL

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_state()
    if data is not None and data.get('is_chatting'):
        await message.answer(Language(language=data['language']).get_string('chat_mode_help'))
    else:
        data = {'language': 'Ru', 'is_chatting': False}
        await state.set_state(data)
        await message.reply(Language(language=data['language']).get_string('welcome'), reply_markup=await kb.main(data))


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    data = await state.get_state()
    is_chatting = data['is_chatting']
    if is_chatting:
        await message.answer(Language(language=data['language']).get_string('chat_mode_help'))
    else:
        await message.answer(Language(language=data['language']).get_string('welcome'), reply_markup=await kb.main(data))

@router.callback_query(F.data == "help")
async def cmd_help(callback: CallbackQuery, state: FSMContext):
    data = await state.get_state()
    is_chatting = data['is_chatting']
    if is_chatting:
        data = await state.get_state()
        await callback.message.answer(Language(language=data['language']).get_string('chat_mode_help'))
    else:
        data = await state.get_state()
        await callback.message.answer(Language(language=data['language']).get_string('help'))

@router.message(F.text == "ping")
async def cmd_ping(message: Message, state: FSMContext):
    data = await state.get_state()
    await message.answer(Language(language=data['language']).get_string('ping'))

@router.callback_query(F.data == "chat")
async def cb_chat(callback: CallbackQuery, state: FSMContext):
    data = await state.get_state()
    if data is None:
        data = {'language': 'Ru', 'is_chatting': False}
        await state.set_state(data)
    data['is_chatting'] = True
    await state.set_state(data)
    await callback.answer("")
    await callback.message.answer(Language(language=data['language']).get_string('chat'))

@router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    data = await state.get_state()
    if data is None:
        data = {'language': 'Ru', 'is_chatting': True}
        await state.set_state(data)
    data['is_chatting'] = False
    await state.set_state(data)
    await message.answer(Language(language=data['language']).get_string('stopped'))

@router.callback_query(F.data == "settings")
async def cb_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    data = await state.get_state()
    await callback.message.edit_text(Language(language=data['language']).get_string('settings'), reply_markup=await kb.settings(data))

@router.callback_query(F.data == "change_lang")
async def cb_change_lang(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    data = await state.get_state()
    await callback.message.edit_text(Language(language=data['language']).get_string('change_lang'), reply_markup=await kb.change_lang(data))

@router.callback_query(F.data.in_({"Eng", "Ru"}))
async def cb_select_lang(callback: CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    data = await state.get_state()
    await callback.answer(Language(language=data['language']).get_string('change_lang_success'))
    await callback.message.delete()
    await callback.message.answer(Language(language=data['language']).get_string('welcome'), reply_markup=await kb.main(data))

@router.message()
async def echo(message: Message, state: FSMContext):
    data = await state.get_state()
    if data is None:
        data = {'language': 'Ru', 'is_chatting': False}
        await state.set_state(data)
    is_chatting = data.get('is_chatting', False)
    if is_chatting:
        async with ClientSession() as session:
            user_message_data = {"question": message.text}
            async with session.post(f"{SERVE_URL}/ask/", json=user_message_data) as response:
                if response.status == 200:
                    completion_data = await response.json()
                    completion = completion_data.get("response", "error")
                    # split the completion string into chunks of 4096 characters or less
                    chunks = [completion[i:i+4096] for i in range(0, len(completion), 4096)]
                    # send each chunk as a separate message
                    for chunk in chunks:
                        data = await state.get_state()
                        await message.answer(Language(language=data['language']).get_string(chunk))
                else:
                    data = await state.get_state()
                    await message.answer(Language(language=data['language']).get_string('chat_error'))
    else:
        await message.answer(Language(language=data['language']).get_string('restart'))
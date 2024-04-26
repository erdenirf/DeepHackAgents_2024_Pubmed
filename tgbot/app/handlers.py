import requests
import asyncio
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

is_chatting = False

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    global is_chatting
    if is_chatting:
        await message.answer(Language(**await state.get_data()).get_string('chat_mode_help'))
    else:
        await state.update_data(language='Eng')
        await message.reply(Language(**await state.get_data()).get_string('welcome'), reply_markup=await kb.main(state))

@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    global is_chatting
    if is_chatting:
        await message.answer(Language(**await state.get_data()).get_string('chat_mode_help'))
    else:
        await message.answer(Language(**await state.get_data()).get_string('welcome'), reply_markup=await kb.main(state))

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    global is_chatting
    if is_chatting:
        await message.answer(Language(**await state.get_data()).get_string('chat_mode_help'))
    else:
        await message.answer(Language(**await state.get_data()).get_string('help'))

@router.message(F.text == "ping")
async def cmd_ping(message: Message, state: FSMContext):
    await message.answer(Language(**await state.get_data()).get_string('ping'))

@router.callback_query(F.data == "chat")
async def cb_chat(callback: CallbackQuery, state: FSMContext):
    global is_chatting
    is_chatting = True
    await callback.answer("")
    await callback.message.answer(Language(**await state.get_data()).get_string('chat'))

@router.message(Command("stop"))
async def cmd_stop(message: Message, state: FSMContext):
    global is_chatting
    is_chatting = False
    await message.answer(Language(**await state.get_data()).get_string('stopped'))

@router.callback_query(F.data == "settings")
async def cb_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.edit_text(Language(**await state.get_data()).get_string('settings'), reply_markup=await kb.settings(state))

@router.callback_query(F.data == "change_lang")
async def cb_change_lang(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.edit_text(Language(**await state.get_data()).get_string('change_lang'), reply_markup=await kb.change_lang(state))

@router.callback_query(F.data.in_({"Eng", "Ru"}))
async def cb_select_lang(callback: CallbackQuery, state: FSMContext):
    await state.update_data(language=callback.data)
    await callback.answer(Language(**await state.get_data()).get_string('change_lang_success'))
    await callback.message.delete()
    await callback.message.answer(Language(**await state.get_data()).get_string('welcome'), reply_markup=await kb.main(state))

@router.message()
async def echo(message: Message, state: FSMContext):
    global is_chatting
    # Check if the user is in chat mode
    if is_chatting:
        user_message_data = {"user_id": message.from_user.id, "message": message.text}
        response = requests.post(f"{SERVE_URL}/gigachat/invoke/", json=user_message_data)
        if response.status_code == 200:
            print("User message sent successfully")

            completion_data = response.json()
            completion = completion_data.get("output", "error")

            await message.answer(completion['content'])
        else:
            print("Error sending user message")
            await message.answer(Language(**await state.get_data()).get_string('chat_error'))
    else:
        # The user is not in chat mode, so do nothing
        pass
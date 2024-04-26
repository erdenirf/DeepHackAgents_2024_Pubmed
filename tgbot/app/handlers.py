
import asyncio
from aiogram import F, Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
from app.languages import Language

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.update_data(language='Eng')
    await message.reply(Language(**await state.get_data()).get_string('welcome'), reply_markup=await kb.main(state))

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(Language(**await state.get_data()).get_string('help'))

@router.callback_query(F.data == "help")
async def cb_help(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer(Language(**await state.get_data()).get_string('help'))

@router.message(F.text == "ping")
async def cmd_ping(message: Message, state: FSMContext):
    await message.answer(Language(**await state.get_data()).get_string('ping'))

@router.callback_query(F.data == "chat")
async def cb_chat(callback: CallbackQuery, state: FSMContext):
    await callback.answer("")
    await callback.message.answer(Language(**await state.get_data()).get_string('chat'))

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
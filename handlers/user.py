from aiogram import types, Dispatcher
from aiogram.types.message import ContentTypes
from keyboards import markups as nav
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import bot, db, dp
import logging

from config import BOT_NICKNAME, PAYMENT_TOKEN
from translations.translations import set_localization
from contracts.token_transactions import token_transaction, token_connection


class FSMUser(StatesGroup):
    general = State()
    profile = State()
    buy_token = State()
    check_task = State()
    # create_task = State()
    submit_task = State()
    input_task_answer = State()


# #@dp.message_handler(commands=None, state=None)
async def cm_start(message: types.Message, state: FSMContext):
    print("###DEBUG### USER START")
    logging.debug("###DEBUG### USER START")
    # await bot.send_message(message.from_user.id, "Welcome to Main Menu!", reply_markup=nav.mainMenu)
    await state.set_state(FSMUser.general)
    print("###DEBUG### CURRENT STATE: USER-GENERAL")
    logging.debug("###DEBUG### CURRENT STATE: USER-GENERAL")


# @dp.message_handler(state = '*', commands=['cancel'])
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    # Allow user to cancel any action
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    # await message.reply('Cancelled.', reply_markup=nav.mainMenu)
    # await state.set_state(None)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(Text(equals='Active Tasks', ignore_case=True), state=FSMUser.general)
@dp.callback_query_handler(text_contains="showprofile_user", state=FSMUser.general)
async def show_profile(message: types.Message, state: FSMContext):
    print("###DEBUG### IN SHOW_PROFILE")
    logging.debug("###DEBUG### IN SHOW_PROFILE")
    user_lang = db.get_user_language(message.from_user.id)
    user_points = db.get_user_points(message.from_user.id)
    referral_count = db.count_referrals(message.from_user.id)
    # user_information = "<b>User Information</b>\nNickname: <b>" + db.get_nickname(message.from_user.id)+ "</b>\nWallet: <b>" + db.get_wallet(message.from_user.id) + f"</b>\nYour referral link: https://t.me/{BOT_NICKNAME}?start={message.from_user.id}" + f"\nReferral numbers: {referral_count}" + f"\nUser points: {user_points}"
    # user_information = "Информация о пользователе:" + f"\nКоличество Баллов: <b>{user_points}"+"</b>\nКошелек: <b>" + db.get_wallet(message.from_user.id) + f"</b>\nYour referral link: https://t.me/{BOT_NICKNAME}?start={message.from_user.id}" + f"\nReferral numbers: <b>{referral_count}</b>"
    # await bot.send_message(message.from_user.id, user_information, parse_mode="html")
    await bot.send_message(message.from_user.id, set_localization("👤 Информация о пользователе", user_lang)
                           + set_localization("\n🏆 Количество Баллов: ", user_lang) + f"<b>{user_points}</b>"
                           + set_localization("\n💲 Кошелек: ",
                                              user_lang) + f"<b>{db.get_wallet(message.from_user.id)}</b>"
                           + set_localization("\n👉 Ваша реферальная ссылка: ",
                                              user_lang) + f"https://t.me/{BOT_NICKNAME}?start={message.from_user.id}"
                           + set_localization("\n👥 Кол-во рефералов: ", user_lang) + f"<b>{referral_count}</b>",
                           parse_mode="html", reply_markup=nav.mainMenu(user_lang))
    await state.set_state(FSMUser.general)


# @dp.message_handler(Text(equals='Buy Token', ignore_case=True), state=FSMUser.general)
@dp.callback_query_handler(text_contains="buytokens_user", state=FSMUser.general)
async def buy_tokens(message: types.Message, state: FSMContext):
    print("###DEBUG### IN BUY_TOKEN")
    logging.debug("###DEBUG### IN BUY_TOKEN")
    user_lang = db.get_user_language(message.from_user.id)
    # tup_test=([500,250],[1000,500],[2000,1000])
    bundles = db.get_bundles()
    for tup in bundles:
        await bot.send_message(message.from_user.id, set_localization(str(tup[2]) + "\n", user_lang)
                               + str(tup[0]) + " Токенов "
                               + set_localization("за ", user_lang)
                               + str(tup[1]) + "RUB",
                               reply_markup=nav.InlineKeyboardMarkup().add(nav.InlineKeyboardButton(
                                   set_localization("Купить", user_lang),
                                   callback_data=("cbd_buy_tokens " + str(tup[0]) + "|" + str(tup[1]) + "|" + str(
                                       message.from_user.id)))))
    await state.set_state(FSMUser.general)
    # await state.set_state(None)
    # await state.set_state(FSMUser.buy_token)
    print("###DEBUG### IN BUY_TOKEN END")
    logging.debug("###DEBUG### IN BUY_TOKEN END")


# create invoice
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('cbd_buy_tokens '), state=FSMUser.general)
async def buy_tokens_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    # Get data from inlinekeyboard
    user_id = str(callback_query.data.split('|')[2])
    price_value = str(callback_query.data.split('|')[1])
    tokens_value = str(callback_query.data.split('|')[0].replace('cbd_buy_tokens ', ''))
    # print("###DEBUG### buy_tokens data: user_id="+user_id+" price="+price_value+" tokens="+tokens_value)
    # Token prices
    prices = [
        types.LabeledPrice(label=f'{tokens_value} Tokens', amount=int(price_value) * 100),
    ]
    await bot.send_invoice(user_id, title=f'Купить {tokens_value} Токенов',
                           description=f'Вы получите {tokens_value} Токенов',
                           provider_token=PAYMENT_TOKEN,
                           currency='rub',
                           prices=prices,
                           payload=f'{user_id}_bought_{tokens_value}_for_{price_value}')
    await state.set_state(FSMUser.general)
    async with state.proxy() as data:
        data['user_id_invoice'] = user_id
        data['tokens_amount_invoice'] = tokens_value


@dp.pre_checkout_query_handler(lambda query: True, state=FSMUser.general)
async def checkout(pre_checkout_query: types.PreCheckoutQuery, state: FSMContext):
    print("###DEBUG### IN pre_checkout_query_handler")
    logging.debug("###DEBUG### IN pre_checkout_query_handler")
    token_connection_status = await token_connection()
    if (token_connection_status):
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                            error_message="Payment service currently unavailable!"
                                                          " Try to pay again in a few minutes, we need a small rest.")
        user_id = ''
        tokens_value = ''
        async with state.proxy() as data:
            user_id = data['user_id_invoice']
            tokens_value = data['tokens_amount_invoice']

        await state.set_state(FSMUser.buy_token)

        async with state.proxy() as data:
            data['user_id_buytoken'] = user_id
            data['tokens_amount_buytoken'] = tokens_value
    else:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=False,
                                            error_message="Token transactions are currently not available!"
                                                          " Try to pay again in a few hours, we need a small rest.")
        await state.set_state(FSMUser.general)
        print("###DEBUG### END pre_checkout_query_handler")
        logging.debug("###DEBUG### END pre_checkout_query_handler")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message, state: FSMContext):
    print("###DEBUG### IN got_payment")
    logging.debug("###DEBUG### IN got_payment")
    user_id = ''
    tokens_value = ''
    async with state.proxy() as data:
        user_id = data['user_id_buytoken']
        tokens_value = data['tokens_amount_buytoken']
    user_wallet = db.get_wallet(user_id)
    # Transfer tokens
    await token_transaction(user_wallet, int(tokens_value))
    # Log invoice
    db.log_payment(user_id, message.successful_payment.total_amount / 100, int(tokens_value))
    await bot.send_message(message.chat.id,
                           'Ура! Спасибо за покупку! Вы купили `{}` Токенов за: `{} {}`'
                           '\n\n'.format(
                               tokens_value, message.successful_payment.total_amount / 100,
                               message.successful_payment.currency),
                           parse_mode='Markdown')
    await state.set_state(FSMUser.general)


# @dp.message_handler(Text(equals='Active Tasks', ignore_case=True), state=FSMUser.general)
@dp.callback_query_handler(text_contains="activetasks_user", state=FSMUser.general)
async def show_active_tasks(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    active_tasks = db.get_active_tasks(message.from_user.id)
    if not active_tasks:
        # await bot.send_message(message.from_user.id, "You have <b>0</b> active tasks", parse_mode="html")
        await bot.send_message(message.from_user.id,
                               set_localization("У вас ", user_lang) + "<b>0</b>" + set_localization(" активных задач",
                                                                                                     user_lang),
                               parse_mode="html", reply_markup=nav.mainMenu(user_lang))
        await state.set_state(FSMUser.general)
    else:
        await bot.send_message(message.from_user.id, set_localization("У вас ", user_lang) + "<b>" + str(
            len(active_tasks)) + "</b>" + set_localization(" активных задач", user_lang), parse_mode="html",
                               reply_markup=nav.mainMenu(user_lang))
        # for task in active_tasks:
        #     #await bot.send_message(message.from_user.id, task)
        #     await bot.send_message(message.from_user.id, task, reply_markup=nav.InlineKeyboardMarkup().add(nav.InlineKeyboardButton("Submit task", callback_data=("cbd_submit_task "+str(task)+"|"+str(message.from_user.id)))))
        for tup in active_tasks:
            # for task in tup:
            await bot.send_message(message.from_user.id,
                                   set_localization("Задача: ", user_lang) + str(tup[0]) + "\n" + set_localization(
                                       "Награда: ", user_lang) + str(tup[1]),
                                   reply_markup=nav.InlineKeyboardMarkup().add(
                                       nav.InlineKeyboardButton(set_localization("Подтвердить", user_lang),
                                                                callback_data=("cbd_submit_task " + str(
                                                                    tup[0]) + "|" + str(message.from_user.id)))))
        await state.set_state(FSMUser.general)
        # await state.set_state(None)


# #Submit wo answer
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('cbd_submit_task '))
# async def submit_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
#     user_id = str(callback_query.data.split('|')[1])
#     task_name = str(callback_query.data.split('|')[0].replace('cbd_submit_task ',''))
#     #await state.set_state(FSMUser.submit_task)
#     #await bot.answer_callback_query("Input your link:")
#     #await message.reply("Input your link:")
#     #print("###DEBUG### submit_task data: User_id="+str(message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
#     #print("###DEBUG### submit_task data: User_id="+str(callback_query.message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
#     print("###DEBUG### submit_task data: task="+task_name+" user_id="+user_id)
#     db.submit_task(user_id, task_name)
#     await callback_query.answer(text=(task_name +" has been submitted!"), show_alert=True)
#     await state.set_state(FSMUser.general)

# Submit with answer
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('cbd_submit_task '), state=FSMUser.general)
async def submit_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = str(callback_query.data.split('|')[1])
    task_name = str(callback_query.data.split('|')[0].replace('cbd_submit_task ', ''))
    # print("###DEBUG### submit_task data: User_id="+str(message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    # print("###DEBUG### submit_task data: User_id="+str(callback_query.message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    # print("###DEBUG### submit_task data: task="+task_name+" user_id="+user_id)
    # db.submit_task(user_id, task_name)
    # await callback_query.answer(text=(task_name +" has been submitted!"), show_alert=True)
    await bot.send_message(user_id, set_localization("Пожалуйста, укажите ссылку для ",
                                                     db.get_user_language(user_id)) + f"\"{task_name}\":",
                           reply_markup=types.ReplyKeyboardRemove())
    # await bot.send_message(user_id, f"Please, input answer for \"{task_name}\":", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(FSMUser.input_task_answer)
    async with state.proxy() as data:
        data['task_name'] = task_name


# @dp.message_handler(content_types=['text'], state=FSMUser.submit_task)
async def get_user_task_answer(message: types.Message, state: FSMContext):
    user_answer = message.text
    user_lang = db.get_user_language(message.from_user.id)
    task_name = ''
    async with state.proxy() as data:
        task_name = data['task_name']
        print(data['task_name'])
        logging.debug(data['task_name'])
    print("###DEBUG### user_answer in get_user_task_answer: " + str(user_answer))
    logging.debug("###DEBUG### user_answer in get_user_task_answer: " + str(user_answer))
    db.submit_task(message.from_user.id, task_name, user_answer)
    await bot.send_message(message.from_user.id, set_localization("Ваш ответ был отправлен!", user_lang) + "\n\n"
                           + set_localization("Задача: ", user_lang) + f"{task_name}" + "\n"
                           + set_localization("Доказательство: ", user_lang) + f"{user_answer}",
                           reply_markup=nav.mainMenu(user_lang))
    # await bot.send_message(message.from_user.id, f"Ваш ответ был отправлен!\n\nЗадание: {task_name}\nВаш ответ: {user_answer}", reply_markup=nav.mainMenu)
    await state.set_state(FSMUser.general)


# #@dp.message_handler(Text(equals='Active Tasks', ignore_case=True), state=FSMUser.general)
# async def show_active_tasks_button_version(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     await bot.send_message(message.from_user.id,'■□■□■□■□■□ <b>TASKS</b> □■□■□■□■□■', reply_markup=db.tasks_markup(user_id, nav.page))
#     await state.set_state(None)

# ### FOR DEBUG
# #@dp.message_handler(Text(equals='Active Tasks', ignore_case=True), state=FSMUser.general)
# async def show_all_tasks(message: types.Message, state: FSMContext):
#     ## Just show all tasks from tasks_bot
#     # active_tasks = db.get_task(message.from_user.id)
#     # for task in active_tasks:
#     #     await bot.send_message(message.from_user.id, task)
#     user_status = db.get_users_status()
#     for tup in user_status:
#         await bot.send_message(message.from_user.id,"User status Info: Task_id=" + str(tup[0])+" | User_id="+str(tup[1])+" | Answer_field="+str(tup[2])+" | Completed="+str(tup[3]))
#     #print("###DEBUG### "+str(user_status))
#     #for task in user_status:
#     #    await bot.send_message(message.from_user.id, task)
#     await state.set_state(FSMUser.general)

# ### FOR DEBUG
# #@dp.message_handler(content_types=['text'], state=FSMUser.profile)
# async def create_task(message: types.Message, state: FSMContext):
#     await message.reply("Enter your task:", reply_markup=types.ReplyKeyboardRemove())
#     await FSMUser.create_task.set()

# ### FOR DEBUG
# #@dp.message_handler(content_types=['text'], state=FSMUser.profile)
# async def input_task(message: types.Message, state: FSMContext):
#     db.create_task(message.from_user.id, message.text)
#     await bot.send_message(message.from_user.id, 
#                                                 "Task Created!\n"
#                                                 "Task: " + message.text + 
#                                                 "\nTask author: " + str(message.from_user.id), 
#                                                 reply_markup=nav.mainMenu)
#     await state.set_state(FSMUser.general)


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=None, state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    # dp.register_message_handler(show_profile, Text(equals=['👤 Профиль','👤 Profile'], ignore_case=True), state=FSMUser.general)
    # dp.register_message_handler(show_profile, commands=['show_profile'], state=FSMUser.general)
    # dp.register_message_handler(show_active_tasks, Text(equals=['🛠 Активные задачи','🛠  Active tasks'], ignore_case=True), state=FSMUser.general)
    # dp.register_message_handler(buy_tokens, Text(equals=['Купить токены','Buy Tokens'], ignore_case=True), state=FSMUser.general)
    dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT, state=FSMUser.buy_token)
    # dp.register_message_handler(show_all_tasks, Text(equals='~DEBUG~ Show All Tasks', ignore_case=True), state=FSMUser.general)
    # dp.register_message_handler(create_task, Text(equals='~DEBUG~ Create Task', ignore_case=True), state=FSMUser.general)
    # dp.register_message_handler(input_task, content_types=['text'], state=FSMUser.create_task)
    dp.register_message_handler(get_user_task_answer, content_types=['text'], state=FSMUser.input_task_answer)

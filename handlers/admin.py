from aiogram import types, Dispatcher
from keyboards import markups as nav
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot, db

from handlers.user import FSMUser
from config import ADMIN

import logging

global ID
ID = [int(i) for i in ADMIN]


class FSMAdmin(StatesGroup):
    admin_general = State()
    check_tasks = State()
    create_task = State()
    input_task = State()
    input_task_counter = State()
    input_task_reward = State()
    edit_task = State()
    delete_task = State()


# Get ID of current admin
# @dp.message_handler(commands=['admin'], is_chat_admin=True)
async def admin_command(message: types.Message, state: FSMContext):
    if message.from_user.id in ID:
        print("###DEBUG### ADMIN COMMAND START")
        logging.debug("###DEBUG### ADMIN COMMAND START")
        print("###DEBUG### State before ADMIN COMMAND:")
        logging.debug("###DEBUG### State before ADMIN COMMAND:")
        async with state.proxy() as data:
            print(str(data))
            logging.debug(str(data))
        # global ID
        # ID = message.from_user.id
        await state.finish()
        await state.set_state(FSMAdmin.admin_general)
        await message.delete()
        async with state.proxy() as data:
            print(str(data))
            logging.debug(str(data))
        await bot.send_message(message.from_user.id, "<b>Добро Пожаловать в Админ-Панель!</b>",
                               reply_markup=nav.adminMenu, parse_mode="html")


# @dp.message_handler(commands='Check_Tasks', state=None)
async def cm_start(message: types.Message, state: FSMContext):
    print("###DEBUG### ADMIN START")
    logging.debug("###DEBUG### ADMIN START")
    if message.from_user.id in ID:
        await state.set_state(FSMAdmin.admin_general)
    print("###DEBUG### CURRENT STATE: ADMIN-GENERAL")
    logging.debug("###DEBUG### CURRENT STATE: ADMIN-GENERAL")


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
    # await message.reply('Cancelled.', reply_markup = nav.mainMenu)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


# @dp.message_handler(commands='Check_Tasks', state=FSMAdmin.admin_general)
# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('adm_show_tasks'))
async def show_tasks_admin(message: types.Message, state: FSMContext):
    print("###DEBUG### CURRENT STATE: ADMIN-GENERAL | show_tasks_admin")
    logging.debug("###DEBUG### CURRENT STATE: ADMIN-GENERAL | show_tasks_admin")
    if message.from_user.id in ID:
        user_status = db.get_users_status()
        if not user_status:
            await bot.send_message(message.from_user.id, "You have <b>0</b> assigned tasks", parse_mode="html")
            await state.set_state(FSMAdmin.admin_general)
        else:
            for tup in user_status:
                await bot.send_message(message.from_user.id,
                                       "<u>Статус задачи</u>\n<b>Задача</b>: " + str(
                                           tup[1]) + "\n<b>Пользователь</b>: " + str(
                                           tup[2]) + "\n<b>Доказательство</b>: " + str(
                                           tup[3]) + "\n<b>Статус выполнения</b>: " + str(
                                           tup[4]) + "\n<b>Статус подтверждения</b>: " + str(tup[5]),
                                       parse_mode="html")
                # await bot.send_message(message.from_user.id,"User status Info: Task_id=" + str(tup[0])+" | User_id="+str(tup[1])+" | Answer_field="+str(tup[2])+" | Completed="+str(tup[3]))
        await state.set_state(FSMAdmin.admin_general)


# @dp.message_handler(commands='To Verify', state=FSMAdmin.admin_general)
async def show_tasks_to_verify_admin(message: types.Message, state: FSMContext):
    print("###DEBUG### CURRENT STATE: ADMIN-GENERAL | show_tasks_to_verify_admin")
    logging.debug("###DEBUG### CURRENT STATE: ADMIN-GENERAL | show_tasks_to_verify_admin")
    if message.from_user.id in ID:
        user_status = db.get_users_status(to_verify=1)
        if not user_status:
            await bot.send_message(message.from_user.id, "У вас <b>0</b> задач для проверки", parse_mode="html")
            await state.set_state(FSMAdmin.admin_general)
        else:
            for tup in user_status:
                print("###DEBUG### testsss")
                logging.debug("###DEBUG### testsss")
                await bot.send_message(message.from_user.id,
                                       "<u>Статус задачи</u>\n<b>Задача</b>: " + str(
                                           tup[1]) + "\n<b>Пользователь</b>: " + str(
                                           tup[2]) + "\n<b>Доказательство</b>: " + str(
                                           tup[3]) + "\n<b>Статус выполнения</b>: " + str(
                                           tup[4]) + "\n<b>Статус подтверждения</b>: " + str(tup[5]),
                                       reply_markup=nav.InlineKeyboardMarkup().add(nav.InlineKeyboardButton("Одобрить",
                                                                                                            callback_data=(
                                                                                                                    "cbd_approve_task " + str(
                                                                                                                tup[
                                                                                                                    1]) + "|" + str(
                                                                                                                message.from_user.id))),
                                                                                   nav.InlineKeyboardButton("Отклонить",
                                                                                                            callback_data=(
                                                                                                                    "cbd_deny_task " + str(
                                                                                                                tup[
                                                                                                                    1]) + "|" + str(
                                                                                                                message.from_user.id))),
                                                                                   ),
                                       parse_mode="html")
            # await bot.send_message(message.from_user.id,"<u>User status:</u>\n <b>Task</b> = " + str(tup[1])+"\n <b>User</b> = "+str(tup[2])+"\n <b>Answer</b> = "+str(tup[3])+"\n <b>Task status</b> = "+str(tup[4]),parse_mode="html")
            # await bot.send_message(message.from_user.id,"User status Info: Task_id=" + str(tup[0])+" | User_id="+str(tup[1])+" | Answer_field="+str(tup[2])+" | Completed="+str(tup[3]))
            await state.set_state(None)


# Approve task
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("cbd_approve_task "))
async def approve_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    print("###DEBUG### callback_query_handler in approve_callback_run")
    logging.debug("###DEBUG### callback_query_handler in approve_callback_run")
    user_id = str(callback_query.data.split('|')[1])
    task_name = str(callback_query.data.split('|')[0].replace('cbd_approve_task ', ''))
    # print("###DEBUG### submit_task data: User_id="+str(message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    # print("###DEBUG### submit_task data: User_id="+str(callback_query.message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    print("###DEBUG### approve_task data: task=" + task_name + " user_id=" + user_id)
    logging.debug("###DEBUG### approve_task data: task=" + task_name + " user_id=" + user_id)
    db.verify_task(user_id, task_name, 1)
    await callback_query.answer(text=("Кто выполнял задачу: " + db.get_nickname(
        user_id) + "\nЗадача: " + task_name + "\nДанная задача была зачтена!"), show_alert=True)
    await state.set_state(FSMAdmin.admin_general)


# Deny task
@dp.callback_query_handler(lambda x: x.data and x.data.startswith("cbd_deny_task "))
async def deny_callback_run(callback_query: types.CallbackQuery, state: FSMContext):
    print("###DEBUG### callback_query_handler in deny_callback_run")
    logging.debug("###DEBUG### callback_query_handler in deny_callback_run")
    user_id = str(callback_query.data.split('|')[1])
    task_name = str(callback_query.data.split('|')[0].replace('cbd_deny_task ', ''))
    # print("###DEBUG### submit_task data: User_id="+str(message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    # print("###DEBUG### submit_task data: User_id="+str(callback_query.message.from_user.id)+" task_name="+str(callback_query.data)+" task_answer="+str(message.text))
    print("###DEBUG### deny_task data: task=" + task_name + " user_id=" + user_id)
    logging.debug("###DEBUG### deny_task data: task=" + task_name + " user_id=" + user_id)
    db.verify_task(user_id, task_name, 0)
    await callback_query.answer(text=("Кто выполнял задачу: " + db.get_nickname(
        user_id) + "\nЗадача: " + task_name + "\nДанная задача была не принята!"), show_alert=True)
    await state.set_state(FSMAdmin.admin_general)


# #@dp.message_handler(commands='Check_Tasks', state=FSMAdmin.check_tasks)
# async def create_task_admin(message: types.Message, state: FSMContext):
#     print("###DEBUG### CURRENT STATE: ADMIN-GENERAL | create_task_admin")
#     if message.from_user.id == ID:
#         await message.reply("Enter your task:", reply_markup=types.ReplyKeyboardRemove())
#         await FSMAdmin.create_task.set()

# #@dp.message_handler(content_types=['text'], state=FSMAdmin.create_task)
# async def input_task_admin(message: types.Message, state: FSMContext):
#     db.create_task(message.from_user.id, message.text)
#     await bot.send_message(message.from_user.id, 
#                                                 "Task Created!\n"
#                                                 "Task: " + message.text + 
#                                                 "\nTask author: " + str(message.from_user.id), 
#                                                 reply_markup=nav.adminMenu)
#     await state.set_state(FSMAdmin.admin_general)

# @dp.message_handler(Text(equals='Create Task', ignore_case=True), state=FSMAdmin.admin_general)
async def create_task_admin(message: types.Message, state: FSMContext):
    print("###DEBUG### CURRENT STATE: ADMIN-GENERAL | create_task_admin")
    logging.debug("###DEBUG### CURRENT STATE: ADMIN-GENERAL | create_task_admin")
    if message.from_user.id in ID:
        await message.reply("Укажите название задачи:", reply_markup=types.ReplyKeyboardRemove())
        await FSMAdmin.create_task.set()


# @dp.message_handler(content_types=['text'], state=FSMAdmin.create_task)
async def input_task_admin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['task_name'] = message.text
    await bot.send_message(message.from_user.id,
                           "Укажите сколько раз можно выполнить эту задачу цифрами.\nСтандартное значение 1",
                           reply_markup=types.ReplyKeyboardRemove())
    await FSMAdmin.input_task.set()


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FSMAdmin.input_task)
async def input_task_counter_admin_invalid(message: types.Message, state: FSMContext):
    return await message.reply(
        "Вы должны указать количество цифрой.\nУкажите снова сколько раз можно выполнить эту задачу.\nСтандартное значение 1")


# @dp.message_handler(lambda message: message.text.isdigit(), state=FSMAdmin.input_task)
async def input_task_counter_admin(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    #    data['task_counter'] = message.text
    if (message.text == None):
        await state.update_data(task_counter=1)
    else:
        await state.update_data(task_counter=int(message.text))

    await bot.send_message(message.from_user.id,
                           "Укажите значение награды за выполнение задания цифрами.\nСтандартное значение награды 0",
                           reply_markup=types.ReplyKeyboardRemove())
    await FSMAdmin.input_task_counter.set()


# @dp.message_handler(lambda message: not message.text.isdigit(), state=FSMAdmin.input_task_counter)
async def input_task_reward_admin_invalid(message: types.Message, state: FSMContext):
    return await message.reply(
        "Вы должны указать значение награды цифрой.\nУкажите снова значение награды за выполнение задачи.\nСтандартное значение 0")


# @dp.message_handler(lambda message: message.text.isdigit(), state=FSMAdmin.input_task_counter)
async def input_task_reward_admin(message: types.Message, state: FSMContext):
    task_reward = message.text
    task_name = ''
    task_counter = 1
    async with state.proxy() as data:
        task_name = data['task_name']
        task_counter = data['task_counter']
    db.create_task(message.from_user.id, task_name, task_counter, task_reward)
    await bot.send_message(message.from_user.id,
                           "Задача Создана!"
                           "\nЗадача: " + task_name +
                           "\nАвтор Задачи: " + str(message.from_user.id) +
                           "\nСколько раз можно выполнить: " + str(task_counter) +
                           "\nНаграда за выполнение: " + str(task_reward),
                           reply_markup=nav.adminMenu)
    await state.set_state(FSMAdmin.admin_general)


# @dp.message_handler(state=FSMAdmin.general)
async def back_to_mainmenu_admin(message: types.Message, state: FSMContext):
    print("###DEBUG### CURRENT STATE: ADMIN-GENERAL | back_to_mainmenu_admin")
    logging.debug("###DEBUG### CURRENT STATE: ADMIN-GENERAL | back_to_mainmenu_admin")
    if message.from_user.id in ID:
        await state.finish()
        await state.set_state(FSMUser.general)
        user_lang = db.get_user_language(message.from_user.id)
        await bot.send_message(message.from_user.id, "<b>Вы вернулись в Главное Меню</b>", parse_mode="html",
                               reply_markup=nav.mainMenu(user_lang))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=['admin'], state='*')
    # dp.register_message_handler(admin_command, commands=['admin'], state='*', is_chat_admin=True)
    # dp.register_message_handler(cm_start, commands=None, state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(show_tasks_admin, Text(equals='Показать Задачи', ignore_case=True),
                                state=FSMAdmin.admin_general)
    dp.register_message_handler(show_tasks_to_verify_admin, Text(equals='Верификация', ignore_case=True),
                                state=FSMAdmin.admin_general)
    dp.register_message_handler(create_task_admin, Text(equals='Создать Задачу', ignore_case=True),
                                state=FSMAdmin.admin_general)
    dp.register_message_handler(input_task_admin, content_types=['text'], state=FSMAdmin.create_task)
    dp.register_message_handler(input_task_counter_admin_invalid, lambda message: not message.text.isdigit(),
                                state=FSMAdmin.input_task)
    dp.register_message_handler(input_task_counter_admin, lambda message: message.text.isdigit(),
                                state=FSMAdmin.input_task)
    dp.register_message_handler(input_task_reward_admin_invalid, lambda message: not message.text.isdigit(),
                                state=FSMAdmin.input_task_counter)
    dp.register_message_handler(input_task_reward_admin, lambda message: message.text.isdigit(),
                                state=FSMAdmin.input_task_counter)
    dp.register_message_handler(back_to_mainmenu_admin, Text(equals='Вернуться в Главное Меню', ignore_case=True),
                                state=FSMAdmin.admin_general)

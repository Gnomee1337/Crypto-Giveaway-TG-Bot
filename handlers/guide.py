from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
import re, logging, random

# For captcha
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from keyboards import markups as nav
from create_bot import bot, db, scheduler, dp
from handlers.user import FSMUser
from config import BOT_NICKNAME, CHANNELS
from translations.translations import set_localization


# #Delete this part
# from captcha import Captcha

class FSMGuide(StatesGroup):
    registration = State()
    set_language = State()
    captcha = State()
    captcha_input = State()
    balance = State()
    reaction = State()
    invite_friend = State()
    wallet = State()


# @dp.message_handler(commands=['start'], state=None)
async def cm_start(message: types.Message, state: FSMContext):
    # If user already created and passed guide
    if (db.user_exists(message.from_user.id) and (db.get_signup(message.from_user.id, ) == "done")):
        print("###DEBUG### OTHER FINISHED cuz USER EXISTS")
        logging.debug("###DEBUG### OTHER FINISHED cuz USER EXISTS")
        # Get user language
        user_lang = db.get_user_language(message.from_user.id)
        await bot.send_message(message.from_user.id,
                               set_localization("Привет ", user_lang) + message.from_user.username + set_localization(
                                   ", я твой помощник в проекте🔋 \{ProjectName\}\n🏆 Продолжай выполнять задания, чтобы получить токены!",
                                   user_lang), reply_markup=nav.mainMenu(user_lang))
        print("###DEBUG### SET STATE FSMUser.general")
        logging.debug("###DEBUG### SET STATE FSMUser.general")
        await state.set_state(FSMUser.general)
        print("###DEBUG### OTHER.py FINISHED")
        logging.debug("###DEBUG### OTHER.py FINISHED")
    else:
        # Check for referral
        start_command = message.text
        referral_id_from_message = str(start_command[7:])
        # If "/start" command with referral ID
        if (str(referral_id_from_message) != ""):
            # Check if the referral ID equal to the same user
            if (str(referral_id_from_message) != str(message.from_user.id)):
                # If referral ID unique then
                # Add user to DB
                db.add_user(message.from_user.id, message.from_user.username, referral_id_from_message)
                # Set next stage "captcha" for user
                db.set_signup(message.from_user.id, "captcha")
                # await bot.send_message(message.from_user.id, "Привет " + message.from_user.username + ", я твой помощник в проекте (ProjectName)\nПожалуйста начни выполнять задания, чтобы получить свои первые токены!")
                # await bot.send_message(message.from_user.id, "Нажмите на кнопку Присоединиться!", parse_mode="html", reply_markup=nav.connectMenu_guide)
                # await FSMGuide.captcha.set()
                # Ask for primary language
                await bot.send_message(message.from_user.id,
                                       "👋 Привет " + message.from_user.username + ", выбери язык использования!\n\n" + "👋 Hi " + message.from_user.username + ", pick a language to use!",
                                       parse_mode="html", reply_markup=nav.langMenu)
                await state.set_state(None)
                try:
                    # Notify referral owner about new invited user
                    # await bot.send_message(referral_id_from_message, f"Поздравляем!\nВашу реферальную ссылку использовал: {message.from_user.username}\nВы получили 1000 Токенов за вашего друга!")
                    await bot.send_message(referral_id_from_message,
                                           set_localization("🏆 Поздравляем!\nВашу реферальную ссылку использовал: ",
                                                            db.get_user_language(
                                                                message.from_user.id)) + set_localization(
                                               "\n📣 Вы получили 1000 Токенов за вашего друга!"))
                    db.increase_user_points(referral_id_from_message, 1000)
                    pass
                except:
                    pass

            # If referral ID equal to the same user, notify about abuse
            else:
                await bot.send_message(message.from_user.id,
                                       set_localization("❌ Вы пытались использовать свою же <u>реферальную ссылку</u>!",
                                                        db.get_user_language(message.from_user.id)), parse_mode="html")
                # Get user stage
                user_current_stage = db.get_signup(message.from_user.id)
                # Return user on his last stage in guide.py
                await check_user_stage(user_current_stage, message)
                # print("###DEBUG### SET STATE FSMUser.general")
                # await state.set_state(FSMUser.general)
                print("###DEBUG### cm_start in GUIDE.py FINISHED")
                logging.debug("###DEBUG### cm_start in GUIDE.py FINISHED")
        # If "/start" command without referral ID
        else:
            # If user already exists
            # Check on with stage he finished
            # And return to that stage
            if (db.user_exists(message.from_user.id)):
                # Get user stage
                user_stage = db.get_signup(message.from_user.id)
                # Return to last stage
                await check_user_stage(user_stage, message)
            else:
                # #Otherwise set his stage to "captcha" which is first
                # #Add user to DB
                # db.add_user(message.from_user.id, message.from_user.username)
                # #Set next stage "captcha" for user
                # db.set_signup(message.from_user.id,"captcha")
                # await bot.send_message(message.from_user.id, "Привет " + message.from_user.username + ", я твой помощник в проекте (ProjectName)\nПожалуйста начни выполнять задания, чтобы получить свои первые токены!")
                # await bot.send_message(message.from_user.id, "Нажмите на кнопку Присоединиться!", parse_mode="html", reply_markup=nav.connectMenu_guide)
                # await FSMGuide.captcha.set()

                # Otherwise set his stage to "set_language" which is first
                # Add user to DB
                db.add_user(message.from_user.id, message.from_user.username)
                # Set next stage "captcha" for user
                db.set_signup(message.from_user.id, "captcha")
                # Ask for primary language
                await bot.send_message(message.from_user.id,
                                       "👋 Привет " + message.from_user.username + ", выбери язык использования!\n\n" + "👋 Hi " + message.from_user.username + ", pick a language to use!",
                                       parse_mode="html", reply_markup=nav.langMenu)
                await state.set_state(None)
        print("###DEBUG### GUIDE.py cm_start FINISHED")
        logging.debug("###DEBUG### GUIDE.py cm_start FINISHED")


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
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


async def check_user_stage(currentstage, message: types.Message):
    print("###DEBUG### check_user_stage started")
    logging.debug("###DEBUG### check_user_stage started")
    user_lang = db.get_user_language(message.from_user.id)
    if (currentstage == "captcha"):
        await message.reply(set_localization("⚠️ Вам нужно решить капчу!", user_lang),
                            parse_mode="html", reply_markup=nav.connectMenu(user_lang))
        await FSMGuide.captcha.set()
    elif (currentstage == "balance"):
        await message.reply(set_localization("👉 Нажмите на кнопку \"💰 Баланс\" для посмотра баланса", user_lang),
                            parse_mode="html", reply_markup=nav.balanceMenu(user_lang))
        await FSMGuide.balance.set()
    elif (currentstage == "reaction"):
        await message.reply(set_localization("✅ Подпишитесь на канал: ", user_lang) + CHANNELS[0][2]
                            + set_localization("\nПосле выполнения этих заданий нажмите на кнопку", user_lang),
                            parse_mode="html", reply_markup=nav.reactionMenu(user_lang))
        # Turn on reminder
        try:
            scheduler.add_job(reaction_reminder, trigger='interval', seconds=8,
                              kwargs={'user_id': message.from_user.id}, id='reaction_reminder', replace_existing=True)
            scheduler.start()
        except:
            pass
        await FSMGuide.reaction.set()
    elif (currentstage == "invite_friend"):
        await message.reply(set_localization("👉 Ваша реферальная ссылка: ",
                                             user_lang) + f"https://t.me/{BOT_NICKNAME}?start={message.from_user.id}"
                            + set_localization("\n📣 Тебе нужно пригласить как минимум 1 друга 👥", user_lang),
                            parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
        # Turn on reminder
        try:
            scheduler.add_job(invitefriend_reminder, trigger='interval', seconds=8,
                              kwargs={'user_id': message.from_user.id}, id='invitefriend_reminder',
                              replace_existing=True)
            scheduler.start()
        except:
            pass
        await FSMGuide.invite_friend.set()
    elif (currentstage == "wallet"):
        await message.reply(set_localization("⚠️ Укажите ваш кошелек: ", user_lang), parse_mode="html")
        await FSMGuide.wallet.set()
    # else:
    #     await state.set_state(None)
    print("###DEBUG### check_user_stage finished")
    logging.debug("###DEBUG### check_user_stage finished")
    return True


@dp.callback_query_handler(text_contains="lang_", state=None)
async def setLanguage(callback: types.CallbackQuery):
    print("###DEBUG### setLanguage started")
    logging.debug("###DEBUG### setLanguage started")
    lang = callback.data[5:]
    db.change_user_language(callback.from_user.id, lang)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    # await bot.send_message(callback.from_user.id, set_localization("Язык установлен!", lang))

    await bot.send_message(callback.from_user.id, callback.from_user.username + set_localization(
        ", я твой помощник в проекте🔋 \{ProjectName\}\n🏆 Начни выполнять задания, чтобы получить токены!", lang),
                           reply_markup=nav.connectMenu(lang))
    # await bot.send_message(callback.from_user.id, "Нажмите на кнопку Присоединиться!", parse_mode="html", reply_markup=nav.connectMenu(lang))
    await FSMGuide.captcha.set()
    print("###DEBUG### setLanguage finished")
    logging.debug("###DEBUG### setLanguage finished")
    return 0


async def generate_captcha(text):
    # Taken from https://github.com/finake0/Aiogram-Captcha-2.0/blob/main/main.py
    # some parts from https://dev.to/magesh236/captcha-image-generator-python-7ee
    # And little bit modified
    img_width, img_height = 300, 100
    captcha_image = Image.new('RGB', (img_width, img_height),
                              color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    captcha_draw = ImageDraw.Draw(captcha_image)
    captcha_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", size=random.randint(30, 60))
    captcha_draw.polygon(
        [(random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255)),
         (random.randint(0, 255), random.randint(0, 255)), (random.randint(0, 255), random.randint(0, 255))],
        fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), outline=None)
    getit = lambda: (random.randrange(5, 85), random.randrange(5, 255))
    for i in range(5, random.randrange(6, 10)):
        captcha_draw.line((getit(), getit()),
                          fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                          width=random.randrange(0, 20))
    captcha_draw.text((random.randint(10, 100), random.randint(10, 50)), text, font=captcha_font,
                      fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    captcha_bytes = BytesIO()
    captcha_image.save(captcha_bytes, format='PNG')
    captcha_bytes.seek(0)
    return captcha_bytes


async def generate_captcha_number():
    return str(random.randint(10000, 99999))


async def captcha_input(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    user_answer = message.text
    async with state.proxy() as data:
        captcha_number = data['captcha_number']
    if user_answer == str(captcha_number):
        user_lang = db.get_user_language(message.from_user.id)
        # Change status to next stage "balance"
        await bot.send_message(message.from_user.id, set_localization("🏆 Поздравляю, Вы прошли капчу!", user_lang),
                               parse_mode="html")
        db.set_signup(message.from_user.id, "balance")
        # Give points
        await bot.send_message(message.from_user.id,
                               set_localization("За прохождение капчи Вы получили 100 Токенов!", user_lang),
                               parse_mode="html")
        db.increase_user_points(message.from_user.id, 100)
        # Next stage "balance"
        await bot.send_message(message.from_user.id,
                               set_localization("👉 Теперь нажми на кнопку '💰 Баланс' для просмотра Ваших токенов",
                                                user_lang), parse_mode="html", reply_markup=nav.balanceMenu(user_lang))
        await FSMGuide.balance.set()
    else:
        await bot.send_message(message.from_user.id, set_localization(
            "❌ Вы ввели неправильное число!\n👉 Нажмите снова на кнопку \"✅ Присоединиться\", чтобы попробовать еще раз",
            user_lang), reply_markup=nav.connectMenu(user_lang))
        # Wait for new user input
        await FSMGuide.captcha.set()
    return


# @dp.message_handler(Text(equals='Присоединиться', ignore_case=True), state=FSMGuide.captcha)
@dp.callback_query_handler(text_contains="connect_guide", state=FSMGuide.captcha)
async def captcha_stage(message: types.Message, state: FSMContext):
    # async def captcha_stage(call: types.CallbackQuery, state: FSMContext):
    print("CHECK USER DATA in INLINe")
    print(message.from_user.id)
    # Solve captcha
    captcha_number = await generate_captcha_number()
    await FSMGuide.captcha_input.set()
    async with state.proxy() as data:
        data['captcha_number'] = captcha_number
    await bot.send_message(message.from_user.id, set_localization("⚙️ Введите цифры на картинке:",
                                                                  db.get_user_language(message.from_user.id)))
    captcha_image = await generate_captcha(captcha_number)
    await bot.send_photo(message.from_user.id, captcha_image)

    # if(captcha_pass == "passed"):
    # If user solve captcha, then set next stage
    # db.set_signup(message.from_user.id, "balance")
    # await bot.send_message(message.from_user.id, "Теперь нажми на кнопку \"Баланс\" для посмотра ваших баллов",parse_mode="html", reply_markup=nav.balanceMenu_guide)
    # await FSMGuide.balance.set()
    # else:
    #     await message.reply("Вам нужно решить капчу!",parse_mode="html", reply_markup=nav.connectMenu_guide)
    #     await FSMGuide.captcha.set()
    print("###DEBUG### captcha_stage FINISHED")
    logging.debug("###DEBUG### captcha_stage FINISHED")
    return None


# @dp.message_handler(Text(equals='Баланс', ignore_case=True), state=FSMGuide.balance)
@dp.callback_query_handler(text_contains="balance_guide", state=FSMGuide.balance)
async def balance_stage(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    await bot.send_message(message.from_user.id,
                           set_localization("Ваш баланс: ", user_lang) + str(db.get_user_points(message.from_user.id)),
                           parse_mode="html")
    # Give points
    await bot.send_message(message.from_user.id,
                           set_localization("За проверку кнопки \"💰 Баланс\" вы получили <b>100</b> Токенов!",
                                            user_lang), parse_mode="html")
    db.increase_user_points(message.from_user.id, 100)
    # If user press balance, then set next stage
    db.set_signup(message.from_user.id, "reaction")
    # await bot.send_message(message.from_user.id, "Прочитайте пост и поставьте на нем реакцию: (post_link)\nПосле выполнения этих заданий нажмите на кнопку",parse_mode="html", reply_markup=nav.reactionMenu_guide)
    await bot.send_message(message.from_user.id,
                           set_localization("Ура! Ты выполнил задание и можешь приступить к следующему!\n", user_lang)
                           + set_localization("1️⃣ Подписаться на канал ", user_lang) + CHANNELS[0][2]
                           + set_localization("\n2️⃣ Прочитайте информацию о проекте", user_lang)
                           + set_localization("\n3️⃣ Поставьте реакцию 👍 на пост: ",
                                              user_lang) + "https://TEST_post_link"
                           + set_localization(
                               "\n📣После выполнения этих заданий нажмите на кнопку и получите свои токены 🔋!",
                               user_lang),
                           parse_mode="html", reply_markup=nav.reactionMenu(user_lang))
    await FSMGuide.reaction.set()
    return None


async def check_sub_channels(channels, user_id):
    # Check if user follow tg channels
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


async def reaction_reminder(user_id):
    user_lang = db.get_user_language(user_id)
    if (await check_sub_channels(CHANNELS, user_id)):
        await bot.send_message(user_id, set_localization(
            "🏆 <b>Вы подписались и поставили реакцию!</b>\nЧтобы продолжить зарабатывать Токены нажмите на кнопку!",
            user_lang), parse_mode="html", reply_markup=nav.reactionMenu(user_lang))
        await FSMGuide.reaction.set()
    else:
        await bot.send_message(user_id, set_localization(
            "👋 Привет, это твой Бот-Помощник!\n⚠️ <b>Вы все ещё не подписались на канал или не поставили реакцию!</b>\nНапоминаю, чтобы заработать токены тебе нужно:",
            user_lang)
                               + set_localization("1️⃣ Подписаться на канал ", user_lang) + CHANNELS[0][2]
                               + set_localization("\n2️⃣ Прочитайте информацию о проекте", user_lang)
                               + set_localization("\n3️⃣ Поставьте реакцию 👍 на пост: ",
                                                  user_lang) + "https://TEST_post_link"
                               + set_localization(
            "\n📣После выполнения этих заданий нажмите на кнопку и получите свои токены 🔋!", user_lang),
                               parse_mode="html", reply_markup=nav.reactionMenu(user_lang))
        await FSMGuide.reaction.set()
    return


# @dp.message_handler(content_types=['text'], state=FSMGuide.reaction)
@dp.callback_query_handler(text_contains="reaction_guide", state=FSMGuide.reaction)
async def reaction_stage(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    # check if reaction added and follow tg channel
    if (await check_sub_channels(CHANNELS, message.from_user.id)):
        # If user follow and add reaction, then set next stage
        db.set_signup(message.from_user.id, "invite_friend")
        # Give points
        await bot.send_message(message.from_user.id,
                               set_localization("📣За подписку на канал вы получили <b>500</b> 🔋Токенов!", user_lang),
                               parse_mode="html")
        db.increase_user_points(message.from_user.id, 500)
        # Turn off reminder
        try:
            if (scheduler.state != 0):
                print("###DEBUG### scheduler.shutdown in reaction_stage")
                logging.debug("###DEBUG### scheduler.shutdown in reaction_stage")
                scheduler.shutdown(wait=False)
                # print("###DEBUG### scheduler.pause in reaction_stage")
                # scheduler.pause()
            # Remove jobs if scheduler not empty
            if (scheduler.get_job('reaction_reminder') != None):
                print("###DEBUG### scheduler.remove_job in reaction_stage")
                logging.debug("###DEBUG### scheduler.remove_job in reaction_stage")
                scheduler.remove_job(job_id='reaction_reminder')
        except:
            pass
        # Next stage "invite_friend"
        await bot.send_message(message.from_user.id, set_localization("👉 Ваша реферальная ссылка: ",
                                                                      user_lang) + f"https://t.me/{BOT_NICKNAME}?start={message.from_user.id}"
                               + set_localization("\n📣 Тебе нужно пригласить как минимум 1 друга 👥", user_lang),
                               parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
        await FSMGuide.invite_friend.set()
    else:
        # If not follow/reaction return to same stage
        await bot.send_message(message.from_user.id,
                               set_localization("⚠️ <b>Вы не подписались на канал или не поставили реакцию!</b>\n",
                                                user_lang)
                               + set_localization("1️⃣ Подписаться на канал ", user_lang) + CHANNELS[0][2]
                               + set_localization("\n2️⃣ Прочитайте информацию о проекте", user_lang)
                               + set_localization("\n3️⃣ Поставьте реакцию 👍 на пост: ",
                                                  user_lang) + "https://TEST_post_link"
                               + set_localization(
                                   "\n📣После выполнения этих заданий нажмите на кнопку и получите свои токены 🔋!",
                                   user_lang),
                               parse_mode="html", reply_markup=nav.reactionMenu(user_lang))
        # Turn on reminder
        try:
            scheduler.add_job(reaction_reminder, trigger='interval', seconds=8,
                              kwargs={'user_id': message.from_user.id}, id='reaction_reminder', replace_existing=True)
            scheduler.start()
        except:
            pass
        # print("###DEBUG### after scheduler start")
        await FSMGuide.reaction.set()
    return None


async def invitefriend_reminder(user_id):
    user_lang = db.get_user_language(user_id)
    # Get "invited_friends" value from DB by user_id
    invited_friends = db.count_referrals(user_id)
    # Check if 1 friend invited
    if (invited_friends >= 1):
        await bot.send_message(user_id, set_localization(
            "👥 Ура! Вы пригласили друга и выполнили задание!\n🏆 Поздравляем с получением 1000 🔋 Токенов!", user_lang),
                               parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
        await FSMGuide.invite_friend.set()
    else:
        # If not invited 1 friend
        # Get "invite_fails" value from DB by user_id
        invite_fails = db.get_invite_fails(user_id)
        # If "invite_fails" less than 3
        if (invite_fails < 3):
            db.increase_invite_fails(user_id)
            await bot.send_message(user_id, set_localization("👋 Привет, это твой Бот-Помощник!\n", user_lang)
                                   + set_localization("👉 Ваша реферальная ссылка: ",
                                                      user_lang) + f"https://t.me/{BOT_NICKNAME}?start={user_id}"
                                   + set_localization(
                "\nТебе нужно пригласить как минимум 1 друга 👥\n🏆 После выполнения этого заданий нажмите на кнопку и получите свои токены!",
                user_lang),
                                   parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
            await FSMGuide.invite_friend.set()
        else:
            try:
                # Turn off reminder
                if (scheduler.state != 0):
                    print("###DEBUG### scheduler.shutdown in invitefriend_reminder")
                    logging.debug("###DEBUG### scheduler.shutdown in invitefriend_reminder")
                    scheduler.shutdown()
                if (scheduler.get_job('invitefriend_reminder') != None):
                    print("###DEBUG### scheduler.remove_job in invitefriend_reminder")
                    logging.debug("###DEBUG### scheduler.remove_job in invitefriend_reminder")
                    scheduler.remove_job('invitefriend_reminder')
            except:
                pass
            # If "invite_fails" more than 5, proceed user to next "wallet" stage
            await bot.send_message(user_id, set_localization(
                "👋 Привет, это твой Бот-Помощник!\n❌ Вы не привели друга и упустили возможность получить 1000 Токенов!\n🏆 Чтобы продолжить зарабатывать 🔋 Токены нажмите на кнопку!",
                user_lang),
                                   parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
            await FSMGuide.invite_friend.set()
    return


# @dp.message_handler(content_types=['text'], state=FSMGuide.invite_friend)
@dp.callback_query_handler(text_contains="invitefriend_guide", state=FSMGuide.invite_friend)
async def invite_friend_stage(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    # Get "invited_friends" value from DB by user_id
    invited_friends = db.count_referrals(message.from_user.id)
    # Check if 1 friend invited
    if (invited_friends >= 1):
        # If user invited 1 friend, then set next "wallet" stage
        db.set_signup(message.from_user.id, "wallet")
        # Give Points
        await bot.send_message(message.from_user.id, set_localization(
            "👥 Ура! Вы пригласили друга и выполнили задание!\n🏆 Поздравляем с получением 1000 🔋 Токенов!", user_lang),
                               parse_mode="html")
        db.increase_user_points(message.from_user.id, 1000)
        # Turn off reminder
        try:
            if (scheduler.state != 0):
                print("###DEBUG### scheduler.shutdown in invite_friend_stage")
                logging.debug("###DEBUG### scheduler.shutdown in invite_friend_stage")
                scheduler.shutdown()
            if (scheduler.get_job('invitefriend_reminder') != None):
                print("###DEBUG### scheduler.remove_job in invite_friend_stage")
                logging.debug("###DEBUG### scheduler.remove_job in invite_friend_stage")
                scheduler.remove_job('invitefriend_reminder')
        except:
            pass
        # Procced to next stage "wallet"
        await bot.send_message(message.from_user.id, set_localization(
            "🏆 Поздравляем! Это последний этап обучения!\nТебе нужно указать свой кошелек\n👉 Введите ваш адрес кошелька:",
            user_lang),
                               parse_mode="html")
        await FSMGuide.wallet.set()
    else:
        # If not invited 1 friend
        # Get "invite_fails" value from DB by user_id
        invite_fails = db.get_invite_fails(message.from_user.id)
        # If "invite_fails" less than 5
        if (invite_fails < 3):
            await bot.send_message(message.from_user.id,
                                   set_localization("👋 Привет, это твой Бот-Помощник!\n", user_lang)
                                   + set_localization("👉 Ваша реферальная ссылка: ",
                                                      user_lang) + f"https://t.me/{BOT_NICKNAME}?start={message.from_user.id}\n"
                                   + set_localization(
                                       "\nТебе нужно пригласить как минимум 1 друга 👥\n🏆 После выполнения этого заданий нажмите на кнопку и получите свои токены!",
                                       user_lang),
                                   parse_mode="html", reply_markup=nav.inviteFriendMenu(user_lang))
            # Turn on reminder
            try:
                scheduler.add_job(invitefriend_reminder, trigger='interval', seconds=8,
                                  kwargs={'user_id': message.from_user.id}, id='invitefriend_reminder',
                                  replace_existing=True)
                scheduler.start()
            except:
                pass
            # Force user to invite_friend again
            # db.increase_invite_fails(message.from_user.id)
            await FSMGuide.invite_friend.set()
        else:
            # If "invite_fails" more than 5, proceed user to next "wallet" stage
            await bot.send_message(message.from_user.id, set_localization(
                "👋 Привет, это твой Бот-Помощник!\n❌ Вы не привели друга и упустили возможность получить 1000 Токенов!\n🏆 Чтобы продолжить зарабатывать 🔋 Токены нажмите на кнопку!",
                user_lang),
                                   parse_mode="html")
            # Turn off reminder
            try:
                if (scheduler.state != 0):
                    print("###DEBUG### scheduler.shutdown in invite_friend_stage")
                    logging.debug("###DEBUG### scheduler.shutdown in invite_friend_stage")
                    scheduler.shutdown()
                if (scheduler.get_job('invitefriend_reminder') != None):
                    print("###DEBUG### scheduler.remove_job in invite_friend_stage")
                    logging.debug("###DEBUG### scheduler.remove_job in invite_friend_stage")
                    scheduler.remove_job('invitefriend_reminder')
            except:
                pass
            # Next stage "wallet"
            db.set_signup(message.from_user.id, "wallet")
            await bot.send_message(message.from_user.id, set_localization(
                "🏆 Поздравляем! Это последний этап обучения!\nТебе нужно указать свой кошелек\n👉 Введите ваш адрес кошелька:",
                user_lang), parse_mode="html")
            await FSMGuide.wallet.set()
    return None


# @dp.message_handler(content_types=['text'], state=FSMGuide.wallet)
# @dp.callback_query_handler(state=FSMGuide.wallet)
async def wallet_stage(message: types.Message, state: FSMContext):
    user_lang = db.get_user_language(message.from_user.id)
    # Get user wallet input
    user_wallet = message.text
    # test_string = re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$", message.text)
    # print("###DEBUG### test_string in WALLET")
    # print("###DEBUG### " + str(test_string))
    # Check wallet on match by reg exp
    if (re.match("^0x[a-fA-F0-9]{40}$", user_wallet)):
        # If user correctly input wallet, then finish guide module
        db.set_wallet(message.from_user.id, user_wallet)
        db.set_signup(message.from_user.id, "done")
        # Give points
        await bot.send_message(message.from_user.id,
                               set_localization("🏆 Вы указали кошелек и получили 100 Токенов!", user_lang),
                               parse_mode="html")
        db.increase_user_points(message.from_user.id, 100)
        # Back to MainMenu
        await bot.send_message(message.from_user.id, set_localization("Твой профиль заполнен!", user_lang),
                               parse_mode="html", reply_markup=nav.mainMenu(user_lang))
        # Assign to all active tasks
        db.assign_new_user_to_all_tasks(message.from_user.id)
        await state.set_state(FSMUser.general)
    else:
        # If wallet is incorrect, then again "wallet" stage
        db.set_signup(message.from_user.id, "wallet")
        await bot.send_message(message.from_user.id, set_localization(
            "❌ Вы ввели не правильно ваш кошелек!\nКошелек должен быть в формате:\n<b>0x5Ba607DB861Aa14256bC6DC3aAA5fB2d51ADC7cD</b>\n👉 Введите ваш кошелек ещё раз: ",
            user_lang),
                               parse_mode="html")
        await FSMGuide.wallet.set()
    return None


def register_handlers_guide(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['start'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    # dp.register_message_handler(user_registration, content_types=['text'], state=FSMGuide.registration)
    # dp.register_message_handler(captcha_stage, callback=,state=FSMGuide.captcha)
    dp.register_message_handler(captcha_input, state=FSMGuide.captcha_input)
    # dp.register_message_handler(balance_stage, Text(equals=['💰 Баланс','💰 Balance'], ignore_case=True), state=FSMGuide.balance)
    # dp.register_message_handler(reaction_stage, Text(equals=['✅ Прочитал пост и поставил реакцию','✅ I have read post and react'], ignore_case=True), state=FSMGuide.reaction)
    # dp.register_message_handler(invite_friend_stage, Text(equals=['👥 Пригласил друга','👥 Invited a friend'], ignore_case=True), state=FSMGuide.invite_friend)
    dp.register_message_handler(wallet_stage, content_types=['text'], state=FSMGuide.wallet)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove

from translations.translations import set_localization

# # User buttons:
# btnProfile = KeyboardButton("Profile")
# btnActiveTasks = KeyboardButton("Active Tasks")
# btnCreateTasks = KeyboardButton("~DEBUG~ Create Task")
# btnShowAllTasks = KeyboardButton("~DEBUG~ Show All Tasks")

# Admin buttons:
btnBackToMM_adm = KeyboardButton("Вернуться в Главное Меню")
btnShowTasks_adm = KeyboardButton("Показать Задачи")
btnCreateTask_adm = KeyboardButton("Создать Задачу")
btnVerifyTasks_adm = KeyboardButton("Верификация")
btnDeleteTask_adm = InlineKeyboardButton('Delete Task', callback_data='delete')
btnEditTask_adm = InlineKeyboardButton('Change Task Description', callback_data='edit')
btnNext_adm = InlineKeyboardButton('»', callback_data='next_btn')
btnBack_adm = InlineKeyboardButton('«', callback_data='back_btn')


# # Guide buttons:
# btnConnect_guide = KeyboardButton("Присоединиться")
# btnBalance_guide = KeyboardButton("Баланс")
# btnReaction_guide = KeyboardButton("Прочитал пост и поставил реакцию")
# btnInviteFriend_guide = KeyboardButton("Пригласил друга")

def connectMenu(lang):
    btnConnect_guide = InlineKeyboardButton(set_localization("✅ Присоединиться", lang), callback_data='connect_guide')

    connectMenu_guide = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    connectMenu_guide.add(btnConnect_guide)

    return connectMenu_guide


def balanceMenu(lang):
    btnBalance_guide = InlineKeyboardButton(set_localization("💰 Баланс", lang), callback_data='balance_guide')

    balanceMenu_guide = InlineKeyboardMarkup(resize_keyboard=True)
    balanceMenu_guide.add(btnBalance_guide)

    return balanceMenu_guide


def reactionMenu(lang):
    btnReaction_guide = InlineKeyboardButton(set_localization("✅ Прочитал пост и поставил реакцию", lang),
                                             callback_data='reaction_guide')

    reactionMenu_guide = InlineKeyboardMarkup(resize_keyboard=True)
    reactionMenu_guide.add(btnReaction_guide)

    return reactionMenu_guide


def inviteFriendMenu(lang):
    btnInviteFriend_guide = InlineKeyboardButton(set_localization("👥 Пригласил друга", lang),
                                                 callback_data='invitefriend_guide')

    inviteFriendMenu_guide = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    inviteFriendMenu_guide.add(btnInviteFriend_guide)

    return inviteFriendMenu_guide


def mainMenu(lang):
    btnProfile = InlineKeyboardButton(set_localization("👤 Профиль", lang), callback_data='showprofile_user')
    btnActiveTasks = InlineKeyboardButton(set_localization("🛠 Активные задачи", lang), callback_data='activetasks_user')
    btnBuyToken = InlineKeyboardButton("~WIP~ " + set_localization("Купить токены", lang),
                                       callback_data='buytokens_user')

    mainMenu = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    mainMenu.add(btnProfile, btnActiveTasks, btnBuyToken)

    return mainMenu


# # Guide
# connectMenu_guide = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
# connectMenu_guide.add(btnConnect_guide)
# balanceMenu_guide = ReplyKeyboardMarkup(resize_keyboard = True)
# balanceMenu_guide.add(btnBalance_guide)
# reactionMenu_guide = ReplyKeyboardMarkup(resize_keyboard = True)
# reactionMenu_guide.add(btnReaction_guide)
# inviteFriendMenu_guide = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
# inviteFriendMenu_guide.add(btnInviteFriend_guide)

# Language
langRU = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru')
langEN = InlineKeyboardButton(text='🇺🇸 English', callback_data='lang_en')

# # MainMenu
# mainMenu = ReplyKeyboardMarkup(resize_keyboard = True)
# mainMenu.add(btnProfile, btnActiveTasks)
# # For Debug
# mainMenu.add(btnProfile, btnActiveTasks, btnCreateTasks, btnShowAllTasks)

# AdminMenu
adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnShowTasks_adm, btnVerifyTasks_adm, btnCreateTask_adm, btnBackToMM_adm)

# LanguageMenu
langMenu = InlineKeyboardMarkup(resize_keyboard=True)
langMenu.add(langRU, langEN)

# For Debug
# adminTaskMenu = ReplyKeyboardMarkup(resize_keyboard = True)
# adminTaskMenu = InlineKeyboardMarkup().insert(btnDeleteTask_adm).insert(btnEditTask_adm)

# global page
# page = 1

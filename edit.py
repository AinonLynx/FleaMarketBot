#!/usr/bin/env python
# -*- coding: utf-8 -*-

from log import *
from db import database
from add import pre_publish

# add item conversation
NAME, DESCRIPTION, PHOTO, PUBLISH = range(4)


def list_available(bot, update):
    items = database().get_by_userID(update.message.from_user.id)

    lines = []
    i = 0
    for item in items:
        lines.append('/change%s - %s' % (item.id, item.decorator().shortInfo(30)))

    update.message.reply_text('\n'.join(lines))


def edit(bot, update, groups, user_data):
    reply_keyboard = [['skip', ]]

    id = groups[0]
    item = database().item.get(id=id, userID=update.message.from_user.id, all=False)
    if item is None:
        update.message.reply_text('Товар с идентификатором "%s" не найден' % id)
        return

    user_data['base'] = database()
    update.message.reply_text('Текущее имя товара "%s", напишите новое имя или нажмите skip' % item.itemName,
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return NAME

def name(bot, update, user_data):
    """add item name"""
    user = update.message.from_user
    itemName = update.message.text
    logger.info("Item name: %s" % (itemName))
    user_data['base']..add_name(user.id, itemName)

    update.message.reply_text('Отлично! Теперь напишите описание товара. Не забудьте указать количество и цену!',
                              reply_markup=ReplyKeyboardRemove())

    return DESCRIPTION

def skip_name(bot, update):
    """add item name"""
    user = update.message.from_user
    itemName = update.message.text
    logger.info("Item name: %s" % (itemName))
    Items.add_name(user.id, itemName)

    update.message.reply_text('Отлично! Теперь напишите описание товара. Не забудьте указать количество и цену!',
                              reply_markup=ReplyKeyboardRemove())

    return DESCRIPTION

def description(bot, update):
    """add item description"""
    reply_keyboard = [['пропустить', ]]

    user = update.message.from_user
    itemDescription = update.message.text
    logger.info("Item description: %s" % (itemDescription))
    Items.add_description(user.id, itemDescription)

    update.message.reply_text('Последний шаг. Отправте фото товара или нажмите "пропустить"',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return PHOTO

def skip_description(bot, update):
    """add item description"""
    reply_keyboard = [['пропустить', ]]

    user = update.message.from_user
    itemDescription = update.message.text
    logger.info("Item description: %s" % (itemDescription))
    Items.add_description(user.id, itemDescription)

    update.message.reply_text('Последний шаг. Отправте фото товара или нажмите "пропустить"',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return PHOTO

def photo(bot, update):
    """add item photo"""
    user = update.message.from_user
    photo_id = update.message.photo[-1].file_id
    logger.info("Item photo id from %s: %s" % (user.first_name, photo_id))
    Items.add_photo(user.id, photo_id)

    pre_publish(bot, update)

    return PUBLISH


def skip_photo(bot, update):
    """if item without photo"""
    user = update.message.from_user
    logger.info("User %s doesnt add item photo :(" % (user.first_name,))

    pre_publish(bot, update)

    return PUBLISH


def cancel(bot, update, user_data):
    """interupt adding"""
    user = update.message.from_user
    del user_data['base']
    logger.info("User %s cancel :(" % (user.first_name,))
    Items.del_item(user.id)
    update.message.reply_text('Окей, отменил.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def publish(bot, update, user_data):
    """publish item"""
    user = update.message.from_user
    user_data['base'].save_to_db(Items.del_item(user.id))
    del user_data['base']
    update.message.reply_text('Товар добавлен!', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
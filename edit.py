#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import database


def list_available(bot, update):
    items = database().get_by_userID(update.message.from_user.id)

    lines = []
    i = 0
    for item in items:
        lines.append('/edit%s - %s' % (++i, item.decorator().shortInfo(30)))

    #TODO: add user items IDs to list for check permission

    update.message.reply_text('\n'.join(lines))

def edit(bot, update):
    itemID = update.message.text[5:]  #skip /edit
    user = update.message.from_user

    #TODO: check permission
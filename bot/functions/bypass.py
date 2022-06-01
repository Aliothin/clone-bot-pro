import time
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from bot import LOGGER, dispatcher

from bot.helper.others.bot_utils import *
from bot.helper.others.bypass_parser import *
from bot.helper.tg_helper.msg_utils import *
from bot.helper.tg_helper.list_of_commands import *
from bot.helper.tg_helper.filters import CustomFilters
from bot.helper.tg_helper.make_buttons import ButtonMaker


def _bypass(message, bot):
    LOGGER.info('User: {} [{}]'.format(message.from_user.first_name, message.from_user.id))
    arguments = message.text.split(" ", maxsplit=1)
    reply_to = message.reply_to_message
    link = ""
    if len(arguments) > 1:
        link = arguments[1]
        if message.from_user.username:
            tag = f"@{message.from_user.username}"
        else:
            tag = message.from_user.mention_html(message.from_user.first_name)
    if reply_to is not None:
        if len(link) == 0:
            link = reply_to.text
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    is_gplinks = is_gplinks_link(link)
    is_adfly = is_adfly_link(link)
    is_rocklinks = is_rocklinks_link(link)
    is_droplink = is_droplink_link(link)
    is_sirigan = is_sirigan_link(link)
    if (is_gplinks or is_adfly or is_rocklinks or is_droplink or is_sirigan):
      msg = sendMessage(f"<b>✨✨ Bypassing ✨✨:</b> <code>{link}</code>", bot, message)
      LOGGER.info(f"Bypassing: {link}")
      if is_gplinks:
        link = gplinks_bypass(link)
      if is_adfly:
        link = adfly_bypass(link)
      if is_rocklinks:
        link = rocklinks_bypass(link)
      if is_droplink:
        link = droplink_bypass(link)
      if is_sirigan:
        link = sirigan(link)
      deleteMessage(bot, msg)
      msg = sendMessage(f"<b>✨✨ Bypassed Link ✨✨:</b> <code>{link}</code>", bot, message)
      LOGGER.info(f"✨✨ Bypassed Link ✨✨: {link}")
      buttons = ButtonMaker()
      buttons.buildbutton("✨✨ Bypassed Link ✨✨: ", f"{link}")
      return msg, InlineKeyboardMarkup(buttons.build_menu(2))
  
@new_thread
def bypassNode(update, context):
    _bypass(update.message, context.bot)
    
bypass_handler = CommandHandler(
    BotCommands.BypassCommand,
    bypassNode,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True,
)
dispatcher.add_handler(bypass_handler)

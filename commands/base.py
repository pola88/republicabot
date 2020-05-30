from telegram import ChatAction
from telegram.ext import CommandHandler
from telegram.ext.filters import Filters
import logging
from random import randint
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Base:
    logger = logger
    def __init__(self, bot, original_msg):
        self.logger = Base.logger.getChild(self.name)
        self.bot = bot
        self.message = original_msg
        #Generate a msg id between 0 and 1000
        self.id = randint(0, 1000)

    @classmethod
    def setup(cls, updater):
        cls.logger.info("Adding " + cls.command)
        dp = updater.dispatcher
        dp.add_handler(cls.handler(updater.bot))

    @classmethod
    def handler(cls, bot):
        """Build the Handler of command"""
        return CommandHandler(cls.command, cls.callbackHandler(bot), cls.filters())

    @classmethod
    def filters(cls):
        return (Filters.chat(os.getenv("GROUP_ID")) | Filters.chat(os.getenv("USER_ID")))

    @classmethod
    def callbackHandler(cls, bot):
        raise NotImplementedError()

    def send_typing(self):
        self.bot.sendChatAction(chat_id=self.message.chat.id ,  action=ChatAction.TYPING)

from .base import Base
import random

class QuestionCommand(Base):
    """Ask a question and you get a random answer"""
    name = "Question"
    command = "question"

    @classmethod
    def callbackHandler(cls, bot):
        """Handler the command /question <string>"""
        def callback(update, context):
            questionCommand = QuestionCommand(bot, update.message)
            questionCommand.send_typing()
            answers = ['Si', 'No'];
            update.message.reply_text(random.choice(answers))

        return callback

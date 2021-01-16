import os
import logging
from dotenv import load_dotenv
load_dotenv()

from telegram import Bot
from telegram.ext import Updater, CommandHandler
from telegram.ext.filters import Filters

from commands import (StatusCommand, HelpCommand, StartCommand, Alcohol70Command,
                      ScheduleCommand, WateringCommand, QuestionCommand, DrinkCommand,
                      TemperatureCommand)
from jobs import SchedulesJob
from db import Setup, Schedule

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def message(update, context):
    logger.info(update);

def main():
    #Create database
    Setup.run()

    # Create the Updater and pass it your bot's token.
    updater = Updater(os.getenv("TELEGRAM_KEY"), use_context=True)

    # Run schedules to check if there are jobs to run
    schedules = SchedulesJob(bot = updater.bot)
    schedules.setup()

    Schedule.queue = schedules.queue;

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    StartCommand.setup(updater)
    HelpCommand.setup(updater)
    # StatusCommand.setup(updater)
    # ScheduleCommand.setup(updater)
    WateringCommand.setup(updater)
    QuestionCommand.setup(updater)
    Alcohol70Command.setup(updater)
    DrinkCommand.setup(updater)
    # TemperatureCommand.setup(updater)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info("RepublicaBeerBot up and running")
    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

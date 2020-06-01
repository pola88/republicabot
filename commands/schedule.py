from .base import Base
import logging
import os
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# State definitions for top level conversation
SELECTING_ACTION, ADDING_SCHEDULE, REMOVE_SCHEDULE, SHOWING_TO_REMOVE = map(chr, range(4))

# State definitions for second level conversation
SELECTING_LEVEL, SELECTING_GENDER = map(chr, range(4, 6))

# State definitions for descriptions conversation
SAVED_TIME, TYPING = map(chr, range(6, 8))

# Meta states
STOPPING, SHOWING = map(chr, range(8, 10))
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# Different constants for this example
# (TIME, DURATION, SAVE, GENDER, MALE, SCHEDULES, AGE, NAME, START_OVER, NEW_TIME,
#  CURRENT_FEATURE, CURRENT_CHAT) = map(chr, range(10, 22))

(TIME, DURATION, SAVE, SCHEDULES, START_OVER, NEW_TIME,
 CURRENT_FEATURE, CURRENT_CHAT) = map(chr, range(10, 18))


def start(update, context):
    """Select an action: Adding/show/removing schedule."""
    text = 'To abort, simply type /stop.'
    buttons = []

    if not context.user_data.get(CURRENT_CHAT):
        context.user_data[CURRENT_CHAT] = update.message.chat.id if update.message else -1
    elif update.message and context.user_data[CURRENT_CHAT] != update.message.chat.id:
        context.user_data[CURRENT_CHAT] = update.message.chat.id


    if context.user_data[CURRENT_CHAT] in [os.getenv("USER_ID")]:
        buttons.append([
            InlineKeyboardButton(text='Add', callback_data=str(ADDING_SCHEDULE)),
            InlineKeyboardButton(text='Remove', callback_data=str(REMOVE_SCHEDULE))
        ])

    buttons.append([
        InlineKeyboardButton(text='Show', callback_data=str(SHOWING)),
        InlineKeyboardButton(text='Done', callback_data=str(END))
    ])

    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need do send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return SELECTING_ACTION

def show_remove_schedule(update, context):
    """Add information about youself."""
    ud = context.user_data
    schedules = ud.get(SCHEDULES)
    buttons = []

    if not schedules:
        text = '\nNo schedules yet.'
    else:
        text = '\nClick one to remove it.'
        schedules_btns = []
        for id, schedule in enumerate(schedules):
            btn_text = '\nTime: {0}, Duration: {1}'.format(schedule.get(TIME, '-'),
                                                        schedule.get(DURATION, '15'))
            schedules_btns.append(InlineKeyboardButton(text=btn_text, callback_data="remove_" + str(id)))
        buttons.append(schedules_btns)

    # InlineKeyboardButton(text='Add', callback_data=str(ADDING_SCHEDULE)),
    buttons.append([
        InlineKeyboardButton(text='Back', callback_data=str(END))
    ])
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return SHOWING_TO_REMOVE

def remove_schedule(update, context):
    print("remove_schedule")
    return show_remove_schedule(update, context)

def show_data(update, context):
    """Pretty print gathered data."""
    def prettyprint(user_data, level):
        schedules = user_data.get(level)
        if not schedules:
            return '\nNo schedules yet.'

        text = ''
        for schedule in schedules:
            text += '\nTime: {0}, Duration: {1}'.format(schedule.get(TIME, '-'),
                                                        schedule.get(DURATION, '15 (default)'))
        return text

    ud = context.user_data
    text = 'Schedules:' + prettyprint(ud, SCHEDULES)

    buttons = [[
        InlineKeyboardButton(text='Back', callback_data=str(END))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    ud[START_OVER] = True

    return SHOWING


def stop(update, context):
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')

    return END


def end(update, context):
    """End conversation from InlineKeyboardButton."""
    update.callback_query.answer()

    text = 'See you around!'
    update.callback_query.edit_message_text(text=text)

    return END


# Second level conversation callbacks
def select_level(update, context):
    """Choose to add a parent or a child."""
    text = 'You may add a parent or a child. Also you can show the gathered data or go back.'
    buttons = [[
        InlineKeyboardButton(text='Time', callback_data=str(TIME)),
        InlineKeyboardButton(text='Duration', callback_data=str(DURATION))
    ], [
        InlineKeyboardButton(text='Save', callback_data=str(SAVE)),
        InlineKeyboardButton(text='Back', callback_data=str(END))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we collect features for a new person, clear the cache and save the gender
    if not context.user_data.get(START_OVER):
        context.user_data[NEW_TIME] = {}
        text = 'Please select a feature to update.'

        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    # But after we do that, we need to send a new message
    else:
        text = 'Got it! Please select a feature to update.'
        update.message.reply_text(text=text, reply_markup=keyboard)

    return SELECTING_LEVEL

def save(update, context):
    """Return to top level conversation."""
    ud = context.user_data

    if not ud.get(SCHEDULES):
        ud[SCHEDULES] = []

    if ud.get(NEW_TIME):
        ud[SCHEDULES].append(ud[NEW_TIME])

    context.user_data[START_OVER] = True
    start(update, context)

    return END

def back_to_main(update, context):
    context.user_data[START_OVER] = True

    start(update, context)
    return END

def ask_for_time(update, context):
    """Prompt user to input data for selected feature."""
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = 'What time?'

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return TYPING

def save_input(update, context):
    """Save input for feature and return to feature selection."""

    ud = context.user_data
    ud[NEW_TIME][ud[CURRENT_FEATURE]] = update.message.text

    ud[START_OVER] = True

    return select_level(update, context)


def stop_nested(update, context):
    """Completely end conversation from within nested conversation."""
    update.message.reply_text('Okay, bye.')

    return STOPPING

class Schedule(Base):
    """Class to add new schedule"""
    name = "Schedule"
    command = "schedule"

    @classmethod
    def setup(cls, updater):
        # Set up third level ConversationHandler (collecting features)
        dp = updater.dispatcher

        remove_schedule_conv = ConversationHandler(
            entry_points=[CallbackQueryHandler(show_remove_schedule,
                                               pattern='^' + str(REMOVE_SCHEDULE) + '$')],

            states={
                SHOWING_TO_REMOVE: [CallbackQueryHandler(remove_schedule,
                                                         pattern='^remove_*')],
            },

            fallbacks=[
                CallbackQueryHandler(back_to_main, pattern='^' + str(END) + '$'),
                CommandHandler('stop', stop_nested)
            ],

            map_to_parent={
                # Return to top level menu
                END: SELECTING_ACTION,
                # End conversation alltogether
                STOPPING: END,
            }
        )
        # Set up second level ConversationHandler (adding a person)
        add_schedule_conv = ConversationHandler(
            entry_points=[CallbackQueryHandler(select_level,
                                               pattern='^' + str(ADDING_SCHEDULE) + '$')],

            states={
                SELECTING_LEVEL: [CallbackQueryHandler(ask_for_time,
                                                       pattern='^(?!' + str(END) + '|' + str(SAVE) + ').*$')],
                TYPING: [MessageHandler(Filters.text, save_input)]
            },

            fallbacks=[
                CallbackQueryHandler(save, pattern='^' + str(SAVE) + '$'),
                CallbackQueryHandler(back_to_main, pattern='^' + str(END) + '$'),
                CommandHandler('stop', stop_nested)
            ],

            map_to_parent={
                # Return to top level menu
                END: SELECTING_ACTION,
                # End conversation alltogether
                STOPPING: END,
            }
        )

        # Set up top level ConversationHandler (selecting action)
        # Because the states of the third level conversation map to the ones of the second level
        # conversation, we need to make sure the top level conversation can also handle them
        selection_handlers = [
            add_schedule_conv,
            remove_schedule_conv,
            CallbackQueryHandler(show_data, pattern='^' + str(SHOWING) + '$'),
            CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
        ]

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler(cls.command, start)],

            states={
                SHOWING: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
                SELECTING_ACTION: selection_handlers,
                SELECTING_LEVEL: selection_handlers,
                SAVED_TIME: selection_handlers,
                STOPPING: [CommandHandler(cls.command, start)]
            },

            fallbacks=[CommandHandler('stop', stop)],
        )

        dp.add_handler(conv_handler)

import os
import logging
import schedule
import threading
import queue
from db import Schedule
from bluetooth import Watering
from random import randint

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class SchedulesJob():
    def __init__(self, queue = None, bot = None):
        self.queue = queue
        self.bot = bot

    def setup(self):
        """Init thread to run schedules and setup the saved schedules"""
        if self.queue is None:
            self.queue =  queue.Queue()
        self.is_running = True
        self.worker = threading.Thread(name="MySchedules", target=self.__run_or_update)
        self.worker.start()
        self.__updated()

    def __run_or_update(self):
        logger.info("Schedule Thread running")
        while self.is_running:
            try:
                updated = self.queue.get(timeout=1)# or whatever
                if updated:
                    self.__updated()
            except queue.Empty:
                schedule.run_pending()

    def __updated(self):
        schedule.clear()
        schedules = Schedule.find_all()
        for sched in schedules:
            schedule.every().days.at(sched[1]).do(self.turn_on, sched[2])

        logger.info("Schedules updated")

    def turn_on(self, duration):
        Watering(randint(0, 1000)).on(duration=duration, callback=self.callback, callback_error=self.callback_error)

    def callback(self, msg):
        logger.info(msg)
        result = int(msg)
        if result == 1:
            logger.info("Watering on!")
        elif result == 2:
            logger.info("Watering was already running!")
        else:
            self.bot.send_message(int(os.getenv("USER_ID")), "There was a problem, Check and try later")

    def callback_error(self, msg):
        logger.error(msg)
        self.bot.send_message(int(os.getenv("USER_ID")), "Schedules::Error {}".format(msg))

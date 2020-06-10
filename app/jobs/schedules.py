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
    def __init__(self, queue = None):
        self.queue = queue

    def setup(self):
        """Init thread to run schedules and setup the saved schedules"""
        if self.queue is None:
            self.queue =  queue.Queue()
        self.is_running = True
        self.worker = threading.Thread(name="MySchedules", target=self.__run_or_update)
        self.worker.start()
        self.__updated()

    def __run_or_update(self):
        logger.info("Schedule running")
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
        Watering(randint(0, 1000)).on(duration=duration, callback=self.callback_on)

    def callback_on(self, msg):
        logger.info(msg)

    @classmethod
    def getAll():
        """Get all schedules from sqlite"""
        pass

    def add():
        """Add new schedule to sqlite and publish an update to queue"""
        pass

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Base:
    def __init__(self, msgid):
        self.logger = logger.getChild(self.name)
        self.id = msgid

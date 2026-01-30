import logging

class Logger:

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def __info__(self, message: str):
        logger = logging.getLogger(__name__)
        logger.info(message)

    def __warning__(self, message: str):
        logger = logging.getLogger(__name__)
        logger.warning(message)

    def __error__(self, message: str):
        logger = logging.getLogger(__name__)
        logger.error(message)

logger = Logger()
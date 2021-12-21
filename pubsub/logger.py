import logging

# Create and configure logger
logging.basicConfig(filename="pubsub.log",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    filemode='w')

# Creating an object
app_logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
app_logger.setLevel(logging.INFO)
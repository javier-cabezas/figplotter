import os
from figplotter import utils

# Initialize logging level
log_level = os.environ.get('FIGPLOTTER_LOG_LEVEL', 'default')

utils.set_log_level(log_level)

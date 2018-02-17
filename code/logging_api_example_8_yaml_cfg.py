import logging
import logging.config
import yaml

# create logger
logger = logging.getLogger('superscript')

#read config
with open('log_config.yml') as f:
    log_config = yaml.load(f)

logging.config.dictConfig(log_config)

## messages
logger.debug('Сообщение уровня debug %s', 'SOS')
logger.info('Сообщение уровня info')
logger.warning('Сообщение уровня warning')


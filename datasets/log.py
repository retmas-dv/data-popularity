__author__ = 'Dmitry Golubkov'

import logging
import logging.config


class Logger(object):
    _initialized = False
    _CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format':
                    '%(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            }
        },
        'loggers': {
            'datasets.log': {
                'handlers': ['console'],
                'level': 'DEBUG'
            }
        }
    }

    def __init__(self):
        if not Logger._initialized:
            logging.config.dictConfig(Logger._CONFIG)

    def get(self):
        return logging.getLogger(__name__)

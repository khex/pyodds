import logging
import logging.config

LOGGER = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            #  docs.python.org/2.7/library/logging.html#logrecord-attributes
            'format': '%(asctime)s %(levelname)s %(name)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'consoleHandler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'fileHandler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'scrapper.log',
            'mode': 'a',
            'encoding': 'utf-8',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'main': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'table': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'rows': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'odds': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'build': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'db': {
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

logging.config.dictConfig(LOGGER)

log_main = logging.getLogger('main')
log_table = logging.getLogger('table')
log_rows = logging.getLogger('rows')
log_odds = logging.getLogger('odds')
log_build = logging.getLogger('build')
log_db = logging.getLogger('db')

if __name__ == '__main__':
    #   main
    log_main.debug('debug message')
    log_main.info('info message')
    log_main.warn('warn message')
    log_main.error('error message')
    log_main.critical('critical message')
    #   main.tablerowsTable
    log_table.debug('debug message')
    log_table.info('info message')
    log_table.warn('warn message')
    log_table.error('error message')
    log_table.critical('critical message')
    #   main.tablerowsRows
    log_main.debug('debug message')
    log_main.info('info message')
    log_main.warn('warn message')
    log_main.error('error message')
    log_main.critical('critical message')
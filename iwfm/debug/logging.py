
def logging():
    ''' logging() - Set up a custom logger for debugging purposes.

    Parameters
    ----------
    none

    Returns
    -------
    logger
        A configured logger instance for debugging purposes.
    '''
    import logging as log

    #  Logger with the name 'debug_logger'
    logger = log.getLogger('debug_logger')
    logger.setLevel(log.DEBUG)

    #  Console handler with level set to DEBUG
    ch = log.StreamHandler()
    ch.setLevel(log.DEBUG)

    #  Formatter with date, time, level name, message
    #  formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #  Formatter with message only
    formatter = log.Formatter('%(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger

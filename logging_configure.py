import logging
# create three loggers for admin, volunteer and general. Only the msg>=error from both admin and volunteer
# will be saved to the "logging.log".

def logger_creator(name,level,writelog=True):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(name)s - %(levelname)s : %(message)s'))
        # add ch to logger
    logger.addHandler(ch)
    if writelog:
        file_handler = logging.FileHandler('logging.log',mode='w', encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s'))
        logger.addHandler(file_handler)
    return logger

log_admin = logger_creator(" (Admin) ",20)
log_volunteer = logger_creator("(Volunteer)",20)
log_general = logger_creator("(General)",20,writelog=False)


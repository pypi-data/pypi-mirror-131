import logging
import datetime


class Logger:
    def __init__(self, name='default_Main', meta_data=None):
        # Setup customized logger
        self.meta_data = meta_data
        # Delete old log files

        self.logger = logging.getLogger("%s_logger" % name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s]:[%(levelname)s]:[%(threadName)s]\t[%(message)8s]')

        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(formatter)
        self.stream_handler.setLevel(logging.INFO)

        self.file_handler = logging.FileHandler(
            f'{self.meta_data.log_path}/{name}_{datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")}.log')
        self.file_handler.setFormatter(formatter)
        self.file_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        self.logger.propagate = False

if __name__ == "__main__":
    main_thread_logger = MainThreadLogger()


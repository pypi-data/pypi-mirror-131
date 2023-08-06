# 用于向config.initLogger()提供日志处理的类，该类的路径不能改变
# 可以修改日志配置中的handler_class_name，并在此处新建handler类完成日志新功能的开发
import logging

level_color = {
    logging.DEBUG: '\33[0;32m',
    logging.INFO: '\33[0;34m',
    logging.WARN: '\33[0;31m',
    logging.ERROR: '\33[1;31;40m',
    logging.FATAL: '\33[4;31;43m'
}


# 日志配置
class ScreenHandler(logging.StreamHandler):
    """
    在初始化日志时候用到该类，不能删除
    当日志设置levelColor="default"时，会使用该handler类
    """

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            fs = level_color[record.levelno] + "%s\n" + '\33[0m'
            try:
                stream.write(fs % msg)
            except UnicodeError:
                stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

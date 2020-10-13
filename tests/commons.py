from logging import getLogger, root, StreamHandler,FileHandler, Formatter
from logging.handlers import DatagramHandler, SocketHandler


def init_log(logfile="log.log", level="INFO", server_addr=None):
    if len(root.handlers) is 0:
        # root record all
        root.setLevel(0)
        fmt = "%(asctime)s %(name)s,line:%(lineno)d [%(levelname)s] %(message)s"
        fmter = Formatter(fmt=fmt)
        # display on screen
        s_handler = StreamHandler()
        s_handler.setLevel(level)
        s_handler.setFormatter(fmter)
        root.addHandler(s_handler)
        # write all levels to logfile
        f_handler = FileHandler(logfile)
        # f_handler.setLevel(0)
        f_handler.setFormatter(fmter)
        root.addHandler(f_handler)

        # TCP handler
        if server_addr is not None:
            t_handler = SocketHandler(*server_addr)
            # t_handler.setLevel(0)
            t_handler.setFormatter(fmter)
            root.addHandler(t_handler)
    else:
        raise RuntimeError("init_debug() can only call once.")


def addlog(obj):
    """Function for attaching a debugging logger to a class or function."""
    # create a logger for this object
    logger = getLogger(obj.__module__ + '.' + obj.__name__)

    # make it available to instances
    obj.logger = logger
    obj.debug = logger.debug
    obj.info = logger.info
    obj.warn = logger.warning
    obj.error = logger.error
    obj.exception = logger.exception
    obj.fatal = logger.fatal

    return obj


@addlog
class test():
    def __init__(self):
        self.fatal("fatal")
        self.exception("exception")
        self.error("error")
        self.warn("warning")
        self.info("test")
        self.debug("debug")

@addlog
def func():
    func.info("info")


if __name__ == "__main__":
    init_log(level='INFO', server_addr=('127.0.0.1', 41400))  # tcp client must indicate server IP
    # init_log()
    test()

    func()
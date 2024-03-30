import logging
from logging.handlers import RotatingFileHandler


class SimpleLogger:
    _default_logger: logging.Logger = None

    def __init__(self,
                 logger_name: str,
                 log_file: str = None,
                 file_max_bytes: int = 9 * 1024 * 1024,
                 file_backup_count: int = 5,
                 log_level=logging.DEBUG,
                 formatter: str = "[%(asctime)s][%(name)s][%(process)d][%(levelname)s] %(message)s"):
        """
        初始化日志记录器

        Args:
            logger_name: 日志记录器的名称
            log_file: 日志保存的文件路径（可选）
            file_max_bytes: 日志文件的最大字节数（默认为 9MB）
            file_backup_count: 保留的备份日志文件数量（默认为 5）
            log_level: 日志输出的最低等级限制（默认为 DEBUG 级别）
            formatter: 日志格式化字符串（默认格式为 "[%(asctime)s][%(name)s][%(process)d][%(levelname)s] %(message)s"）
        """
        # 检索（如果不存在则创建）具有指定名称的logger
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(log_level)

        # 如果logger已经有handlers，那么就不需要再添加新的handlers
        if not self._logger.handlers:
            # 创建一个handler，用于将日志输出到控制台
            console_handler = logging.StreamHandler()
            self._add_handler(console_handler, "console_handler", log_level, formatter)

            # 如果指定了日志文件路径，则创建一个handler，用于将日志输出到文件
            if log_file:
                # 创建一个handler，用于写入日志文件
                file_handler = RotatingFileHandler(log_file, maxBytes=file_max_bytes, backupCount=file_backup_count)
                self._add_handler(file_handler, "file_handler", log_level, formatter)

    def _add_handler(self, handler: logging.Handler, name: str, level: int, formatter: str):
        """
        添加日志处理器

        Args:
            handler: 日志处理器
            name: 日志处理器的名称
            level: 日志输出的最低等级限制
            formatter: 日志格式化字符串
        """
        handler.set_name(name)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(formatter))
        self._logger.addHandler(handler)

    @property
    def logger(self):
        """
        获取日志记录器

        Returns:
            日志记录器
        """
        return self._logger

    def reset_level(self, level: int):
        """
        重设日志输出的最低等级限制

        Args:
            level: 日志输出的最低等级限制
        """
        self._logger.setLevel(level)
        for handler in self._logger.handlers:
            handler.setLevel(level)

    def reset_formatter(self, formatter: str):
        """
        重设日志格式化字符串

        Args:
            formatter: 日志格式化字符串
        """
        formatter = logging.Formatter(formatter)
        for handler in self._logger.handlers:
            handler.setFormatter(formatter)

    def clear_handlers(self):
        """
        删除日志处理器
        """
        for handler in self._logger.handlers[:]:
            # 创建副本是为了避免在迭代过程中删除处理器导致列表大小发生变化，无法正确遍历列表
            handler.close()
            self._logger.removeHandler(handler)

    def as_default(self):
        """
        将日志记录器设置为默认的日志记录器
        """
        SimpleLogger._default_logger = self._logger

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        """
        输出调试信息

        Args:
            msg: 调试信息
            *args: 其他参数
            **kwargs: 其他参数
        """
        cls._default_logger.debug(msg, *args, **kwargs)

    @classmethod
    def info(cls, msg, *args, **kwargs):
        """
        输出信息

        Args:
            msg: 信息
            *args: 其他参数
            **kwargs: 其他参数
        """
        cls._default_logger.info(msg, *args, **kwargs)

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        """
        输出警告信息

        Args:
            msg: 警告信息
            *args: 其他参数
            **kwargs: 其他参数
        """
        cls._default_logger.warning(msg, *args, **kwargs)

    @classmethod
    def error(cls, msg, *args, **kwargs):
        """
        输出错误信息

        Args:
            msg: 错误信息
            *args: 其他参数
            **kwargs: 其他参数
        """
        cls._default_logger.error(msg, *args, **kwargs)

    @classmethod
    def critical(cls, msg, *args, **kwargs):
        """
        输出严重错误信息

        Args:
            msg: 严重错误信息
            *args: 其他参数
            **kwargs: 其他参数
        """
        cls._default_logger.critical(msg, *args, **kwargs)


if __name__ == "__main__":
    # 使用示例
    import threading

    # 创建一个简单的日志记录器
    simple_logger = SimpleLogger('my_logger', 'my_logger.log', log_level=logging.INFO)

    # 使用简单的日志记录器
    logger = simple_logger.logger  # 获取日志记录器
    logger.debug("Begin debug")
    logger.info("Begin info: %s" % __file__)
    logger.warning("Begin warning")
    logger.error("Begin error")
    logger.critical("Begin critical")

    simple_logger.reset_level(logging.DEBUG)  # 重设日志输出的最低等级限制
    simple_logger.reset_formatter("[%(name)s][%(process)d][%(levelname)s] %(message)s")  # 重设日志格式化字符串
    simple_logger.as_default()  # 将日志记录器设置为默认的日志记录器

    # 多线程使用默认日志记录器
    threads = []
    for i in range(10):
        t = threading.Thread(target=SimpleLogger.debug, args=('Debugging from thread %d' % i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # 清除日志处理器
    simple_logger.clear_handlers()

    # 再次使用简单的日志记录器
    logger.debug("End debug")
    logger.info("End info")
    logger.warning("End warning")
    logger.error("End error")

    # 添加一个新的日志处理器
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("[%(asctime)s][%(name)s][%(process)d][%(levelname)s] %(message)s"))
    logger.addHandler(handler)
    logger.critical("End critical")

# py-simple-logger

基于`logging`标准库的封装，提供了更简单的常用日志操作。

Based on the encapsulation of the `logging` standard library, it provides simpler common log operations.

## 使用说明

默认支持控制台打印和可选的文件滚动记录。

使用示例如下：

```python
from simple_logger import SimpleLogger

import logging
import threading

if __name__ == "__main__":
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
```

输出：

```text
[2024-01-01 00:00:00,001][my_logger][12345][INFO] Begin info: C:\py-simple-logger\simple_logger.py
[2024-01-01 00:00:00,002][my_logger][12345][WARNING] Begin warning
[2024-01-01 00:00:00,003][my_logger][12345][ERROR] Begin error
[2024-01-01 00:00:00,004][my_logger][12345][CRITICAL] Begin critical
[my_logger][16772][DEBUG] Debugging from thread 0
[my_logger][16772][DEBUG] Debugging from thread 1
[my_logger][16772][DEBUG] Debugging from thread 2
[my_logger][16772][DEBUG] Debugging from thread 3
[my_logger][16772][DEBUG] Debugging from thread 4
[my_logger][16772][DEBUG] Debugging from thread 5
[my_logger][16772][DEBUG] Debugging from thread 6
[my_logger][16772][DEBUG] Debugging from thread 7
[my_logger][16772][DEBUG] Debugging from thread 8
[my_logger][16772][DEBUG] Debugging from thread 9
End warning
End error
[2024-01-01 00:00:00,010][my_logger][12345][CRITICAL] End critical
```

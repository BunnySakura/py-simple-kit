# py-simple-kit

*一些有用的Python脚本和库，大多仅单文件即可使用且仅依赖标准库。*

## 说明

| 文件                      | 功能                               | 文档                                    |
|-------------------------|----------------------------------|---------------------------------------|
| nio_utils               | 提供subprocess和pipe的非阻塞IO          |                                       |
| simple_thread_pool      | 在不支持ThreadPoolExecutor的系统提供简易支持  |                                       |
| backup_utility.py       | 基于[cloudpan189-go]实现备份文件到天翼云盘    |                                       |
| batch_rename.py         | 批量重命名文件为指定格式                     |                                       |
| mail_sender.py          | 发邮件                              |                                       |
| mc_plugins_translate.py | MC插件汉化                           |                                       |
| protable_dev_monitor.py | 移动设备监视器，移动设备状态变化时，执行指定操作         |                                       |
| simple_logger.py        | 基于`logging`标准库的封装，提供了更简单的常用日志操作。 | [simple_logger](doc/simple_logger.md) |
| telnetd.py              | telnet服务端，可使用telnet连接进行命令行交互     |                                       |

## 致谢

感谢各位互联网前辈提供的思路及实现，另外感谢AI对此提供的辅助。

[cloudpan189-go]: https://github.com/tickstep/cloudpan189-go
import pyudev


class PortableDevMonitor:
    def __init__(self, callback):
        """
        移动设备监视器

        Args:
            callback: 移动设备状态变化时，执行的回调
        """
        # 回调函数
        self._callback = callback
        # 创建一个udev上下文对象
        self._context = pyudev.Context()
        # 创建一个udev监视器对象
        self._monitor = pyudev.Monitor.from_netlink(self._context)
        self._monitor.filter_by(subsystem="block", device_type="partition")
        # 创建一个MonitorObserver对象
        self._observer = pyudev.MonitorObserver(self._monitor, self._callback)

    def start(self):
        """
        启动监视器

        Returns:
        """
        self._observer.start()

    def stop(self):
        """
        停止监视器

        Returns:
        """
        self._observer.stop()


if __name__ == "__main__":
    # Example usage
    def device_state_change(action, device):
        print(f"{device} was {action}")


    monitor = PortableDevMonitor(callback=device_state_change)

    try:
        monitor.start()
        while True:
            # Do other stuff in your main program here
            pass
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()

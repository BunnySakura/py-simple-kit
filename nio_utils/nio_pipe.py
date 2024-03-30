import os
import fcntl
import select
import errno
from typing import Optional


class NioPipe:
    def __init__(self, pipe_name: str):
        """Initialize NioPipe.

        Args:
            pipe_name (str): The name of the pipe.
        """
        self.pipe_name = pipe_name
        self.pipe_fd = None

    def __enter__(self):
        """Context manager entry point."""
        if not os.path.exists(self.pipe_name):
            os.mkfifo(self.pipe_name)
        self.pipe_fd = os.open(self.pipe_name, os.O_RDWR)
        flags = fcntl.fcntl(self.pipe_fd, fcntl.F_GETFL)
        fcntl.fcntl(self.pipe_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        os.close(self.pipe_fd)
        os.remove(self.pipe_name)

    def open(self) -> None:
        """Open the pipe for read and write."""
        if self.pipe_fd is None:
            self.pipe_fd = os.open(self.pipe_name, os.O_RDWR)
            flags = fcntl.fcntl(self.pipe_fd, fcntl.F_GETFL)
            fcntl.fcntl(self.pipe_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def close(self) -> None:
        """Close the pipe."""
        if self.pipe_fd is not None:
            os.close(self.pipe_fd)
            self.pipe_fd = None

    def write(self, data: bytes) -> None:
        """Write data to the pipe.

        Args:
            data (bytes): The data to write to the pipe.
        """
        os.write(self.pipe_fd, data)

    def read(self, timeout: Optional[float] = None) -> Optional[bytes]:
        """Read data from the pipe.

        Args:
            timeout (float, optional): Timeout in seconds. Defaults to None.

        Returns:
            Optional[bytes]: The read data, or None if no data is available.
        """
        rlist, _, _ = select.select([self.pipe_fd], [], [], timeout)
        if self.pipe_fd in rlist:
            data = os.read(self.pipe_fd, 4096)
            return data


if __name__ == "__main__":
    # 使用上下文管理器来打开管道并进行读写操作
    pipe_name = 'my_pipe'
    with NioPipe(pipe_name) as non_blocking_pipe:
        # 写管道
        try:
            non_blocking_pipe.write(b"Hello, non-blocking pipe!")
        except OSError as e:
            if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                print("Pipe is temporarily unavailable for writing")
            else:
                print("Error while writing: " + str(e))

        # 读管道
        try:
            data = non_blocking_pipe.read()
            if data:
                print("Read data: " + data.decode())
            else:
                print("No data to read")
        except OSError as e:
            if e.errno == errno.EAGAIN or e.errno == errno.EWOULDBLOCK:
                print("Pipe has no data available for reading")
            else:
                print("Error while reading: " + str(e))

    # 管道会在退出上下文时自动关闭和清理资源

import subprocess
from threading import Thread
from queue import Queue, Empty


class NioSubprocess:
    def __init__(self, sub_process: subprocess.Popen):
        """非阻塞读写子进程stdio

        Args:
            sub_process: 子进程实例
        """
        self._subproc = sub_process
        self._subproc_stdout_queue = Queue() if sub_process.stdout else None
        self._subproc_stderr_queue = Queue() if sub_process.stderr else None
        self._thread_detach_queue()

    def _enqueue_stdout(self):
        self._subproc.stdout.flush()
        # read方法会阻塞到子进程退出，而readline只会阻塞到'\n'
        for line in iter(self._subproc.stdout.readline, b''):
            self._subproc_stdout_queue.put(line)
        self._subproc.stdout.close()

    def _enqueue_stderr(self):
        self._subproc.stderr.flush()
        # read方法会阻塞到子进程退出，而readline只会阻塞到'\n'
        for line in iter(self._subproc.stderr.readline, b''):
            self._subproc_stderr_queue.put(line)
        self._subproc.stderr.close()

    def _thread_detach_queue(self):
        if self._subproc_stdout_queue:
            thread = Thread(target=self._enqueue_stdout)
            thread.setDaemon(True)
            thread.start()
        if self._subproc_stderr_queue:
            thread = Thread(target=self._enqueue_stderr)
            thread.setDaemon(True)
            thread.start()

    def read_stdout(self):
        try:
            line = self._subproc_stdout_queue.get_nowait()
        except Empty:
            line = None
        return line

    def read_stderr(self):
        try:
            line = self._subproc_stderr_queue.get_nowait()
        except Empty:
            line = None
        return line

    def write(self, command):
        self._subproc.stdin.write(command)
        self._subproc.stdin.flush()

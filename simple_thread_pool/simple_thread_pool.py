import threading
import queue
from typing import Any, Callable, List, Optional


class Task:
    def __init__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        """Represent a task to be executed by a worker thread.

        Args:
            func (Callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.exception = None
        self.event = threading.Event()

    def __repr__(self) -> str:
        return f"Task(func={self.func.__name__}, args={self.args}, kwargs={self.kwargs})"

    def run(self) -> None:
        """Execute the task's function and store the result or exception."""
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.exception = e
        finally:
            self.event.set()

    def get_result(self) -> Any:
        """Get the result of the task, waiting if necessary."""
        self.event.wait()  # Wait for the task to complete
        if self.exception:
            raise self.exception
        return self.result


class Future:
    def __init__(self, task: Task) -> None:
        self.task = task

    def result(self) -> Any:
        """Get the result of the task associated with this Future."""
        return self.task.get_result()


class ThreadPoolExecutor:
    def __init__(self, max_workers: int, max_queue_size: int = 0) -> None:
        """Create a thread pool executor.

        Args:
            max_workers (int): The maximum number of worker threads.
            max_queue_size (int, optional): Maximum size of the task queue. Defaults to 0.
        """
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self.workers: List[threading.Thread] = []
        self.task_queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._shutdown = False
        self._shutdown_lock = threading.Lock()

    def _worker(self) -> None:
        """Worker function for processing tasks."""
        while not self._shutdown:
            try:
                task = self.task_queue.get(timeout=0.1)
            except queue.Empty:
                continue
            if task is None:
                break
            try:
                task.run()
            except Exception as e:
                # Optionally, you can log or handle the exception here
                pass
            self.task_queue.task_done()

    def _submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Task:
        """Submit a task to the thread pool.

        Args:
            func (Callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Task: The task object representing the submitted task.
        """
        task = Task(func, *args, **kwargs)
        self.task_queue.put(task)
        return task

    def submit(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        """Submit a task to the thread pool and return a Future object.

        Args:
            func (Callable): The function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Future: A Future object representing the task's result.
        """
        if not callable(func):
            raise TypeError("func must be a callable function")
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("Cannot submit after shutdown")
            task = self._submit(func, *args, **kwargs)
            return Future(task)

    def start(self) -> None:
        """Start the worker threads."""
        for _ in range(self.max_workers):
            worker = threading.Thread(target=self._worker)
            worker.start()
            self.workers.append(worker)

    def wait_completion(self) -> None:
        """Wait for all tasks to complete."""
        self.task_queue.join()

    def shutdown(self) -> None:
        """Gracefully shut down the thread pool."""
        with self._shutdown_lock:
            if self._shutdown:
                return
            for _ in range(self.max_workers):
                self.task_queue.put(None)
            self._shutdown = True

    def __enter__(self) -> "ThreadPoolExecutor":
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.shutdown()

    def set_max_workers(self, max_workers: int) -> None:
        """Set the maximum number of worker threads.

        Args:
            max_workers (int): The new maximum number of worker threads.
        """
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("Cannot set_max_workers after shutdown")
            self.max_workers = max_workers

    def get_idle_thread_count(self) -> int:
        """Get the count of idle worker threads.

        Returns:
            int: The count of idle worker threads.
        """
        return len(self.workers) - self.task_queue.qsize()


if __name__ == "__main__":
    import time


    def task_function(task_name: str) -> str:
        print(f"Running task: {task_name}")
        time.sleep(3)
        return task_name


    with ThreadPoolExecutor(max_workers=4) as executor:
        future1 = executor.submit(task_function, "Task 1")
        future2 = executor.submit(task_function, "Task 2")
        future3 = executor.submit(task_function, "Task 3")

        # You can continue with other tasks or operations here while waiting for the results

        result1 = future1.result()
        print(f"Result of Task 1: {result1}")

        result2 = future2.result()
        print(f"Result of Task 2: {result2}")

        result3 = future3.result()
        print(f"Result of Task 3: {result3}")

        executor.wait_completion()
        # Wait for all tasks to complete before the thread pool proceeds with the subsequent code.

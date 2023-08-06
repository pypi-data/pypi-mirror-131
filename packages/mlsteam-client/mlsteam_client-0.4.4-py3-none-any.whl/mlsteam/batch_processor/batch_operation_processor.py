from time import time
import threading
import queue


class BatchOperationProcessor():
    def __init__(
        self,
        run_id: str,
        queue,
        backend,
        lock,
        sleep_time,
        batch_size: int = 1000,
    ):
        self._run_id = run_id
        self._queue = queue
        self._backend = backend,
        self._consumer = ConsumerThread(self, sleep_time, batch_size)
        self._batch_size = batch_size
        self._waiting_cond = threading.Condiction(lock=lock)


class ConsumerThread(threading.Thread):
    def __init__(self, processor, sleep_time, batch_size):
        super().__init__(daemon=True)
        self._sleep_time = sleep_time
        self._interrupted = False
        self._event = threading.Event()
        self._is_running = False
        self._processor = processor
        self._batch_size = batch_size

    def run(self):
        self._is_running = True
        try:
            while not self._interrupted:
                self.work()
                if self._sleep_time > 0 and not self._interrupted:
                    self._event.wait(timeout=self._sleep_time)
                    self._event.clear()
                    # sleep for self._sleep_time
        finally:
            self._is_running = False

    def work(self):
        while True:
            batch = self._processor._queue.get_batch(self._batch_size)


class OperationQueue(queue.Queue, object):
    def __init__(self):
        super(OperationQueue, self).__init__()

    def get_batch(self, batch_size: int):
        op = self.get()
        if not op:
            return []
        ops = [op]
        for _ in range(0, batch_size - 1):
            op = self.get()
            if not op:
                break
            ops.append(op)
        return ops

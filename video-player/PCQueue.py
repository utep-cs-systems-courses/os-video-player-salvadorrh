import threading

"""
    This will be the queue where the frames will be stored.
    
    Note that difference between a Mutex and a Semaphore is that Semaphores can 
    count higher than one. A mutex serializes access to shared resources. 
    Mutexes takes and releases resource. 
    Semaphores either signal or wait. Produces sends a signal and then the Consumer
    waits for the signal.
    
    Consumer produces empty queues sets. Acquires full cell.
    Producer produces full queues set. Acquires empty cell.
"""


class PCQueue:
    def __init__(self):
        self.queue = []
        self.active = True
        self.q_lock = threading.Lock()
        self.full = threading.Semaphore(0)    # When start, 0 in the queue. Available full frames
        self.empty = threading.Semaphore(10)  # Don't have more than 10 items to fill. Available empty frames.

    # Adds element to the queue
    def enqueue(self, frame):
        self.empty.acquire()     # Acquire empty frame to fill
        self.q_lock.acquire()    # Guarantee there's no consuming meanwhile
        self.queue.append(frame)
        self.q_lock.release()
        self.full.release()

    # Removes element from the queue
    def dequeue(self):
        self.full.acquire()        # Acquire a full frame
        self.q_lock.acquire()      # Guarantee there's no consuming meanwhile
        frame = self.queue.pop(0)  # Get frame
        self.q_lock.release()
        self.empty.release()       # Release space from queue
        return frame

    def is_empty(self):
        self.q_lock.acquire()
        bool_is_empty = len(self.queue) == 0
        self.q_lock.release()
        return bool_is_empty

    def kill(self):
        self.active = False

    def is_active(self):
        return self.active

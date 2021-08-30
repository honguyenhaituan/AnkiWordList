import traceback
from threading import Thread, Lock
from queue import Queue,Empty

import logging
log = logging.getLogger('Main.threadPool')


class Worker(Thread):
    def __init__(self, pool):
        Thread.__init__(self)
        self.pool = pool
        self.daemon = True
        self.stateStop = False
        self.start()

    def stop(self):
        self.stateStop = True

    def run(self):
        while True:
            if self.stateStop: 
                break

            try:
                func, args, kargs = self.pool.getTask(timeout=1)
            except Empty:
                continue

            try:
                self.pool.beginTask() 
                result = func(*args, **kargs) 
                self.pool.endTask()
                if result:
                    self.pool.putTaskResult(*result)
            except Exception as e:
                log.critical(traceback.format_exc())


class ThreadPool(object):
    def __init__(self, numThread):
        self.numThread = numThread  
        self.pool = []
        self.lock = Lock() 
        self.running = 0  
        self.taskQueue = Queue()
        self.resultQueue = Queue()
    
    def startThreads(self):
        for i in range(self.numThread): 
            self.pool.append(Worker(self))
    
    def stopThreads(self):
        for thread in self.pool:
            thread.stop()
            thread.join()
        del self.pool[:]
    
    def putTask(self, func, *args, **kargs):
        self.taskQueue.put((func, args, kargs))

    def getTask(self, *args, **kargs):
        task = self.taskQueue.get(*args, **kargs)
        return task

    def beginTask(self):
        self.lock.acquire()
        self.running += 1
        self.lock.release()

    def endTask(self):
        self.lock.acquire() 
        self.running -= 1 
        self.lock.release()
        
        self.taskQueue.task_done()

    def taskJoin(self, *args, **kargs):
        self.taskQueue.join()

    def putTaskResult(self, *args):
        self.resultQueue.put(args)

    def getTaskResult(self, *args, **kargs):
        return self.resultQueue.get(*args, **kargs)

    def getTaskLeft(self):
        return self.taskQueue.qsize()+self.resultQueue.qsize()+self.running
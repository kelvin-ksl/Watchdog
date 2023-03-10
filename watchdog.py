import sys
import time
import logging
from logging.handlers import SysLogHandler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


#Server Address
remoteHost = '127.0.0.1'
#Port
remotePort = 8513

#Syslog Generator 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(SysLogHandler(address=(remoteHost, remotePort)))


class Watcher:
    #Constructor
    def __init__(self, path):
        self.path = path
        self.observer = Observer()

    #Method to start the observer
    def start(self):
        event_handler = LoggingEventHandler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        print("START MONITORING...")

    #Method to stop the observer
    def stop(self):
        self.observer.stop()
        print("STOP MONITORING.")

    #Method to join the observer thread
    def join(self):
        self.observer.join()
        

if __name__ == '__main__':
    #Setting the logging configuration
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    #Getting the path to be watched
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    #Instantiating the Watcher class
    w = Watcher(path)

    #Starting the observer
    w.start()

    try:
        #Infinite loop to keep the program running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        #Stopping the observer
        w.stop()
        w.join()

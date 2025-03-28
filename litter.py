
import json
import argparse
import os.path
import logging
import time

from LitterFilter.Event import EventGenerator
from LitterFilter.Timer import TimerService
from LitterFilter.StateMachine import Context, StateMachine, OnOccupied, OnVacant, DelayTimerExpired, RunTimerExpired
from LitterFilter.FanDevice import FanDevice
from LitterFilter.PirSource import PirSource

DEFAULT_FILE_PATH='/etc/litter.json'

class LitterConfig(object):
    '''
    Provide configuration data for the litter filter, 
    loading configuration data from a json file if present
    '''
    ON_DURATION_KEY="OnDuration_S"
    WAIT_DELAY_KEY="WaitDelay_S"
    TRIGGER_COUNT_KEY="MinTriggerCount"

    def __init__(self, filePath=DEFAULT_FILE_PATH):
        self.__filePath=filePath
        self.OnTime=120
        self.DelayTime=10
        self.MinTriggerCount = 2

        #Parse the JSON file to get our configuration data
        if os.path.exists(self.__filePath):
            with open(self.__filePath, 'r') as fd:
                doc=json.load(fd)
                self.OnTime=doc.get(self.ON_DURATION_KEY,self.OnTime)
                self.DelayTime=doc.get(self.WAIT_DELAY_KEY,self.DelayTime)
                self.MinTriggerCount=doc.get(self.TRIGGER_COUNT_KEY, self.MinTriggerCount)
        else:
            print("Configuration file \"{0}\" was not found or is not readable. Using default configuration parameters.")


    def __str__(self):
        return "Path=\"{0}\", duration={1}, delay={2}, triggerCount={3}".format(self.__filePath, self.OnTime, self.DelayTime, self.MinTriggerCount)

def main():
    parser = argparse.ArgumentParser("An automated litter box filter")
    parser.add_argument('-f','--config', type=str, help='The configuration file path',
                        default='/etc/litter.json', dest='config', action='store')
    args=parser.parse_args()

    config=LitterConfig(args.config)

    #set up logging configuration
    formatString="%(asctime)s # %(message)s"
    fileHandler=logging.RotatingFileHandler('/var/log/litter.log', mode='a', maxBytes=50000, backupCount=4)
    #logging.basicConfig(filename='litter.log', filemode='w', level=logging.DEBUG)
    logging.basicConfig(handlers=(fileHandler,), filemode='w', level=logging.DEBUG)

    logging.info(str(config))

    timerService = TimerService()
    fanDevice = FanDevice()

    #Create the state machine context
    context = Context(timerService, fanDevice, config)

    stateMachine = StateMachine(context)
    generator = EventGenerator(stateMachine)

    pirSource = PirSource(OnOccupied, OnVacant)

    #add event sources to the event generator
    generator.AddEventSource(timerService)
    generator.AddEventSource(pirSource)

    #start running
    try:
        while generator.Run():
            time.sleep(1)
    except Exception ex:
        logging.critical("Fatal exception encountered {0}".format(str(ex)))


    

if __name__ == '__main__':
    main()

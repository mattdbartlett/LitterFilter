
import json
import argparse
import os.path

from LitterFilter import Event
from LitterFilter.Timer import TimerService
from LitterFilter.StateMachine import Context, StateMachine
#from FanDevice import FanDevice
#from PirSource import PirSource

DEFAULT_FILE_PATH='/etc/litter.json'

class LitterConfig(object):
    '''
    Provide configuration data for the litter filter, 
    loading configuration data from a json file if present
    '''
    def __init__(self, filePath=DEFAULT_FILE_PATH):
        self.__filePath=filePath
        self.OnTime=120
        self.DelayTime=10

        #Parse the JSON file to get our configuration data
        if os.path.exists(self.__filePath):
            with open(self.__filePath, 'r') as fd:
                doc=json.load(fd)
                self.OnTime=doc["OnDuration_S"]
                self.DelayTime=doc["WaitDelay_S"]
        else:
            print "Configuration file \"{0}\" was not found or is not readable. Using default configuration parameters."


    def __str__(self):
        return "Path=\"{0}\", duration={1}, delay={2}".format(self.__filePath, self.OnTime, self.DelayTime)

def main():
    parser = argparse.ArgumentParser("An automated litter box filter")
    parser.add_argument('-f','--config', type=str, help='The configuration file path',
                        default='/etc/litter.json', dest='config', action='store')
    args=parser.parse_args()

    config=LitterConfig(args.config)
    print str(config)

    timerService = TimerService()
    fanDevice = None #FanDevice.FanDevice()

    #Create the state machine context
    context = Context(timerService, fanDevice, config)


    stateMachine = StateMachine(context)
    generator = Event.EventGenerator(stateMachine)

    pirSource = None #PirSource(OnOccupied, OnVacant)

    #add event sources to the event generator
    generator.AddEventSource(timerService)
    generator.AddEventSource(pirSource)

    #start running
    while generator.Run():
        #TODO SLEEP
        pass

    

if __name__ == '__main__':
    main()

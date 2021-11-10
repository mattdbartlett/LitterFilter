
from Event import EventSource
import qwiic_pir

class PirSource(EventSource):
    """
    An event generator backed by a I2C base PIR device
    """
    def __init__(self, activeEvent, inactiveEvent, address=None):
        self.__device = qwiic_pir.QwiicPIR(address=address)
        self.__activeEvent = activeEvent
        self.__inactiveEvent = inactiveEvent
        self.__lastValue = None
        if self.__device.begin() == False:
            raise Exception("Failed to connect to PIR sensor")

    def Evaluate(self, stateMachine):
        curValue = self.__device.raw_reading() 

        if self.__lastValue is None or self.__lastValue != curValue:
            self.__lastValue = curValue
            if curValue:
                stateMachine.EvaluateEvent(self.__activeEvent)
            else:
                stateMachine.EvaluateEvent(self.__inactiveEvent)



import time
import Event

class Timer(object):
    """
    Class representing a timer instance
    """
    def __init__(self, eventId, durrationS):
        self.__startTime = time.monotonic()
        self.__eventId = eventId
        self.__durrationS = durrationS

    def IsExpired(self):
        return ((self.__startTime+self.__durrationS) > time.monotonic())

    def GetEventID(self):
        return self.__eventId


class TimerService(Event.EventSource):
    def __init__(self):
        self.__timers = dict()

    def AddTimer(self, eventId, durrationS):
        self.__timers[eventId] = Timer(eventId, durrationS)

    def CancelTimer(self, eventId):
        if eventId in self.__timers:
            del self.__timers[eventId]

    def Evaluate(self, stateMachine):
        timers = self.__timers
        for timer in timers:
            if timer.IsExpired():
                eventId = timer.GetEventID()
                del self.__timers[eventId]
                stateMachine.ProcessEvent(eventId)


import logging

class Context(object):
    def __init__(self, timerService, fanDevice, config):
        self.__timerService = timerService
        self.__fanDevice = fanDevice
        self.config = config
        self.triggerCount=0

    def StartTimer(self, eventId, durrationS):
        self.__timerService.AddTimer(eventId, durrationS)

    def CancelTimer(self, eventId):
        self.__timerService.CancelTimer(eventId)

    def EnableFan(self, status):
        self.__fanDevice.Enable(status)

    def GetDelayTime(self):
        return self.config.DelayTime

    def GetRunTime(self):
        return self.config.OnTime

    def Trigger(self):
        self.triggerCount+=1

    def ResetTriggerCount(self):
        self.triggerCount=0;

    def TriggerThresholdPassed(self):
        """
        Return True if the minimum number of triggers has occurred
        """
        return self.triggerCount >= config.MinTriggerCount

    def GetTriggerCount(self):
        return self.triggerCount

class BaseState(object):
    def ProcessEvent(self, eventId):
        return self

#define events
OnOccupied = 1
OnVacant = 2
DelayTimerExpired = 3
RunTimerExpired = 4

class RunFan(BaseState):
    def __init__(self, context):
        logging.info("Entering state RunFan")
        self.__context=context
        self.__context.StartTimer(RunTimerExpired, self.__context.GetRunTime())
        self.__context.EnableFan(True)

    def ProcessEvent(self, eventId):
        if eventId == OnOccupied:
            self.__context.EnableFan(False)
            self.__context.CancelTimer(RunTimerExpired)
            return Occupied(self.__context)
        elif eventId == RunTimerExpired:
            self.__context.EnableFan(False)
            return Wait(self.__context)
        else:
            return self


class Delay(BaseState):
    def __init__(self, context):
        logging.info("Entering state Delay")
        self.__context=context
        self.__context.StartTimer(DelayTimerExpired, self.__context.GetDelayTime())

    def ProcessEvent(self, eventId):
        if eventId == OnOccupied:
            self.__context.CancelTimer(DelayTimerExpired)
            return Occupied(self.__context)
        elif eventId == DelayTimerExpired:
            if self.__context.TriggerThresholdPassed():
                return RunFan(self.__context)
            else:
                logging.info("Insufficient cycles {0}".format(self.__context.GetTriggerCount()))
                return Wait(self.__context)
        else:
            return self

class Occupied(BaseState):
    def __init__(self, context):
        logging.info("Entering state Occupied")
        self.__context=context
        self.__context.Trigger()

    def ProcessEvent(self, eventId):
        if eventId == OnVacant:
            return Delay(self.__context)
        else:
            return self


class Wait(BaseState):
    def __init__(self, context):
        logging.info("Entering state Wait")
        self.__context=context
        self.__context.ResetTriggerCount()

    def ProcessEvent(self, eventId):
        if eventId == OnOccupied:
            return Occupied(self.__context)
        else:
            return self

class StateMachine(object):
    def __init__(self, context):
        self._state = Wait(context)

    def ProcessEvent(self, eventId):
        self._state = self._state.ProcessEvent(eventId)

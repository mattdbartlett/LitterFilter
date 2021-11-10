
class Context(object):
    def __init__(self, timerService, fanDevice, config):
        self.__timerService = timerService
        self.__fanDevice = fanDevice
        self.config = config

    def StartTimer(self, eventId, durrationS):
        self.__timerService.AddTimer(eventId, durrationS)

    def CancelTimer(self, eventId):
        self.__timerService.CancelTimer(eventId)

    def EnableFan(self, status):
        self.__fanDevice.Enable(status)

    def GetDelayTime(self):
        return self.config.DelayTime

    def GetOnTime(self):
        return self.config.OnTime

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
        self.__context=context
        self.__context.StartTimer(DelayTimerExpired, self.__context.GetDelayTime())

    def ProcessEvent(self, eventId):
        if eventId == OnOccupied:
            self.__context.CancelTimer(DelayTimerExpired)
            return Occupied(self.__context)
        elif eventId == DelayTimerExpired:
            return RunFan(self.__context)
        else:
            return self

class Occupied(BaseState):
    def __init__(self, context):
        self.__context=context

    def ProcessEvent(self, eventId):
        if eventId == OnVacant:
            return Delay(self.__context)
        else:
            return self


class Wait(BaseState):
    def __init__(self, context):
        self.__context=context

    def ProcessEvent(self, eventId):
        if eventId == OnOccupied:
            return Occupied(self.__context)
        else:
            return self

class StateMachine(object):
    def __init__(self, context):
        self.__state = Wait(context)

    def ProcessEvent(self, eventId):
        self.__state = self.__state.ProcessEvent(eventId)

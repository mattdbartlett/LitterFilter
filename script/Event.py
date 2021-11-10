
class EventGenerator(object):
    """
    Evaluate event sources when run is called
    """
    def __init__(self, stateMachine):
        self.__stateMachine = stateMachine
        self.__sources = list()

    def AddEventSource(self, eventSource):
        self.__sources.append(eventSource)

    def Run(self):
        for eventSource in self.__sources:
            if eventSource is not None:
                eventSource.Evaluate(self.__stateMachine)
        return len(self.__sources) > 0


class EventSource(object):
    """
    Base class for event sources
    """
    def __init__(self):
        pass

    def Evaluate(stateMachine):
        pass

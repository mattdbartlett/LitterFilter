import unittest
from unittest.mock import Mock, ANY
import time

from LitterFilter.StateMachine import StateMachine, OnOccupied, OnVacant, DelayTimerExpired, RunTimerExpired

class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.context = Mock()
        self.context.GetDelayTime = Mock(return_value=25)
        self.context.GetRunTime = Mock(return_value=250)

        self.uut = StateMachine(self.context)

    def test_OccupancyFromWait(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

    def test_DelayTimerFromOccupancy(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.context.GetDelayTime = Mock(return_value=25)
        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_once_with(DelayTimerExpired, 25)

    def test_ReOccupancyFromDelay(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_once_with(DelayTimerExpired, 25)

        self.uut.ProcessEvent(OnOccupied)
        self.context.CancelTimer.assert_called_once_with(DelayTimerExpired)

    def test_StartFan(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.uut.ProcessEvent(DelayTimerExpired)
        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)
        self.context.EnableFan.assert_called_once_with(True)

    def test_OccupancyWhileRunning(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.uut.ProcessEvent(DelayTimerExpired)
        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)

        self.uut.ProcessEvent(OnOccupied)
        self.context.CancelTimer.assert_called_with(RunTimerExpired)
        self.context.EnableFan.assert_called_with(False)

    def test_CycleComplete(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.uut.ProcessEvent(DelayTimerExpired)
        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)

        self.uut.ProcessEvent(RunTimerExpired)
        self.context.EnableFan.assert_called_with(False)


if __name__ == '__main__':
    unittest.main()


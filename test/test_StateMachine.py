import unittest
from unittest.mock import Mock, ANY
import time

from LitterFilter.StateMachine import StateMachine, OnOccupied, OnVacant, DelayTimerExpired, RunTimerExpired, Wait, RunFan, Occupied, Delay

class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.context = Mock()
        self.context.GetDelayTime = Mock(return_value=25)
        self.context.GetRunTime = Mock(return_value=250)

        self.uut = StateMachine(self.context)

    def test_OccupancyFromWait(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()
        self.context.Trigger.assert_called_once()

    def test_DelayTimerFromOccupancy(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()
        self.context.Trigger.assert_called_once()

        self.context.GetDelayTime = Mock(return_value=25)
        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_once_with(DelayTimerExpired, 25)
        self.context.Trigger.assert_called_once()

    def test_ReOccupancyFromDelay(self):
        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_once_with(DelayTimerExpired, 25)
        self.assertEqual(1, self.context.Trigger.call_count)

        self.uut.ProcessEvent(OnOccupied)

        self.context.CancelTimer.assert_called_once_with(DelayTimerExpired)
        self.assertEqual(2, self.context.Trigger.call_count)

    def test_StartFan(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()

        self.uut.ProcessEvent(OnVacant)

        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)
        self.context.TriggerThresholdPassed=Mock(side_effect = [True])
        self.context.Trigger.assert_called_once()

        self.uut.ProcessEvent(DelayTimerExpired)

        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)
        self.context.EnableFan.assert_called_once_with(True)
        self.context.Trigger.assert_called_once()
        isinstance(self.uut._state, RunFan)

    def test_InsufficientTriggers(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.Trigger.assert_called_once()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.context.TriggerThresholdPassed=Mock(side_effect = [False])
        self.context.ResetTriggerCount = Mock()
        self.uut.ProcessEvent(DelayTimerExpired)


        self.context.EnableFan.assert_not_called()
        self.context.ResetTriggerCount.assert_called_once()
        self.context.Trigger.assert_called_once()
        isinstance(self.uut._state, Wait)

    def test_OccupancyWhileRunning(self):

        self.uut.ProcessEvent(OnOccupied)
        self.context.assert_not_called()
        self.assertEqual(1, self.context.Trigger.call_count)

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.uut.ProcessEvent(DelayTimerExpired)
        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)

        self.uut.ProcessEvent(OnOccupied)

        self.context.CancelTimer.assert_called_with(RunTimerExpired)
        self.context.EnableFan.assert_called_with(False)
        self.assertEqual(2, self.context.Trigger.call_count)

    def test_CycleComplete(self):

        self.assertEqual(1, self.context.ResetTriggerCount.call_count)
        self.uut.ProcessEvent(OnOccupied)
        self.context.Trigger.assert_called()

        self.uut.ProcessEvent(OnVacant)
        self.context.StartTimer.assert_called_with(DelayTimerExpired, 25)

        self.context.TriggerThresholdPassed=Mock(side_effect = [True])
        self.uut.ProcessEvent(DelayTimerExpired)
        self.context.StartTimer.assert_called_with(RunTimerExpired, 250)

        self.uut.ProcessEvent(RunTimerExpired)
        self.context.EnableFan.assert_called_with(False)
        self.assertEqual(2, self.context.ResetTriggerCount.call_count)


if __name__ == '__main__':
    unittest.main()


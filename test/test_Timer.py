import unittest
from unittest.mock import Mock
import time

from LitterFilter.Timer import TimerService


class TestTimer(unittest.TestCase):

    def test_expiration(self):
        service = TimerService()
        service.AddTimer(1, 0)
        time.sleep(1)
        mockState=Mock()
        service.Evaluate(mockState)
        mockState.ProcessEvent.assert_called_once_with(1)

    def test_cancel(self):
        service = TimerService()
        timerId = 1
        service.AddTimer(timerId, 2)
        time.sleep(1)
        service.CancelTimer(timerId)
        mockState=Mock()
        service.Evaluate(mockState)
        mockState.ProcessEvent.assert_not_called()

if __name__ == '__main__':
    unittest.main()


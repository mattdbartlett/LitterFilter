
import unittest
from unittest.mock import Mock

from LitterFilter.Event import EventGenerator

class TestEventGenerator(unittest.TestCase):
    def test_Run(self):
        stateMachine = Mock()
        eventSource1 = Mock()
        eventSource2 = Mock()
        gen = EventGenerator(stateMachine)
        gen.AddEventSource(eventSource1)
        gen.AddEventSource(eventSource2)

        #both sources should be evaluated
        gen.Run()
        self.assertEqual(1, eventSource1.Evaluate.call_count)
        self.assertEqual(1, eventSource2.Evaluate.call_count)

        gen.Run()
        self.assertEqual(2, eventSource1.Evaluate.call_count)
        self.assertEqual(2, eventSource2.Evaluate.call_count)

        


if __name__ == '__main__':
    unittest.main()

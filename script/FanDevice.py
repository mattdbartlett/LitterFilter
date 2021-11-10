
import qwiic_relay

class FanDevice(object):
    """
    Control a fan device using an I2c relay
    """
    def __init__(self, relayNumber=1):
        self.__relayNumber = relayNumber
        self.__device = qwiic_relay.QwiicRelay()
        if self.__device.begin() == False:
            raise Exception("Failed to connect to fan relay")

    def Enable(self, status):
        if status:
            self.__device.set_relay_on(self.__relayNumber)
        else:
            self.__device.set_relay_off(self.__relayNumber)


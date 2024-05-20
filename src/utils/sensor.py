import os
import nfc
from time import (sleep, time)
from dotenv import load_dotenv

class Sensor:
    def __init__(self):
        self.__hardware = nfc.ContactlessFrontend('tty:S0')
        self.stop_flag = False
        print('Sensor successfully initialized!')

    def detect(self, menu):
        while not self.stop_flag:
            found_tag = self.__hardware.connect(rdwr={'on-connect': lambda tag: False}, terminate=self.__check_flag)
            tag_data = found_tag.__str__()
            
            if tag_data not in [None, 'None']:
                menu.detected_tag_id = tag_data.split('ID=')[1]

    def __check_flag(self):
        return self.stop_flag
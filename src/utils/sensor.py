import os
import nfc
from time import sleep
from dotenv import load_dotenv

class Sensor:
    def __init__(self):
        self.__hardware = nfc.ContactlessFrontend('tty:S0')
        print('Sensor successfully initialized!')

    def detect(self, menu):
        sleep(float(os.getenv('DETECT_WAIT_TIME')))

        found_tag = self.__hardware.connect(rdwr={'on-connect': lambda tag: False})
        tag_data = found_tag.__str__()

        menu.detected_tag_id = tag_data.split('ID=')[1]
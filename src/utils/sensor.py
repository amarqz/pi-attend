import nfc
from time import sleep

class Sensor:
    def __init__(self):
        self.__hardware = nfc.ContactlessFrontend('tty:S0')
        print('Sensor successfully initialized!')

    def detect(self, menu):
        sleep(2)

        found_tag = self.__hardware.connect(rdwr={'on-connect': lambda tag: False})
        tag_data = found_tag.__str__()

        menu.detected_tag_id = tag_data.split('ID=')[1]
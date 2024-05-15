import nanpy
from time import sleep

class Keypad:
    def __init__(self) -> None:
        self.__hardware = nanpy.ArduinoApi(nanpy.SerialManager())
        print('Keypad successfully initialized!')

    def read_button(self) -> (str | None):
        sleep(0.15)
        current = self.__hardware.analogRead(0)

        if current > 900:
            return None
        elif current > 600:
            return 'Select'
        elif current > 400:
            return 'Left'
        elif current > 220:
            return 'Down'
        elif current > 65:
            return 'Up'
        else:
            return 'Right'

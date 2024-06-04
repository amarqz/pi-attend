import os
import nanpy
import threading
from time import sleep
from utils.functions import (await_confirmation, loading_screen, picklist)
from utils.keypad import Keypad
from utils.screen import Screen
from utils.sensor import Sensor
from utils.buzzer import Buzzer
from dotenv import load_dotenv

class Menu:
    def __init__(self):
        self.is_running = True
        self.detected_tag_id = ''

        self.screen = Screen()
        self.keypad = Keypad()
        self.sensor = Sensor()
        self.buzzer = Buzzer(16)
        self.buzzer.play_melody('1 Up')

        self.__create_detection_thread()
        
        self.home_screen()
        print('Menu started!')

    def home_screen(self):
        self.screen.print_up(os.getenv("HOME_SCREEN_MSG_UP"))
        self.screen.print_down(os.getenv("HOME_SCREEN_MSG_DOWN"))

    def loop(self):
        while self.is_running:
            sleep(0.15)
            self.button_actions()

    def button_actions(self) -> None:
        match self.keypad.read_button():
            case 'Select':
                self.__stop_detection_thread()
                self.shutdown()
            case 'Up' | 'Down':
                self.__stop_detection_thread()
                self.create_new_session()
            case _:
                return

        self.__create_detection_thread()
        self.home_screen()
    
    def shutdown(self) -> None:
        if await_confirmation(self, '¿Apagar equipo?'):
            loading_screen(self, 'Apagando equipo')
            os.system('shutdown now')
            exit(0)

    def create_new_session(self) -> None:
        new_event_type = picklist(self, ['Ensayo', 'Concierto', 'Procesión', 'Otra actuación'], 'Tipo de evento:')
        
        if new_event_type != None: # ToDo connection with DB
            pass

    def __create_detection_thread(self):
        self.__nfc_thread = threading.Thread(target=self.sensor.detect, name='detection-process', args=(self,))
        self.screen.stop_flag = False
        self.__nfc_thread.start()

    def __stop_detection_thread(self):
        self.screen.stop_flag = True
        self.__nfc_thread.join(1)

if __name__ == '__main__':
    load_dotenv()

    menu = Menu()
    menu.loop()

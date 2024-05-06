import os
import nanpy
from time import sleep
from utils.functions import await_confirmation
from utils.keypad import Keypad
from utils.screen import Screen
from dotenv import load_dotenv

class Menu:
    def __init__(self):
        self.is_running = True

        self.screen = Screen()
        self.keypad = Keypad()

        self.screen.print_up(os.getenv("HOME_SCREEN_MSG"))
        print('Menu started!')

    def loop(self):
        while self.is_running:
            sleep(0.15)
            self.button_actions()

    def button_actions(self) -> None:
        match self.keypad.read_button():
            case 'None':
                pass
            case 'Select':
                self.shutdown()
    
    def shutdown(self) -> None:
        if await_confirmation(self, '¿Apagar equipo?'):
            print('Shutting down...')
        
        self.screen.print_up(os.getenv("HOME_SCREEN_MSG"))
        self.screen.print_down('')

if __name__ == '__main__':
    load_dotenv()

    menu = Menu()
    menu.loop()

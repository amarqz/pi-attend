import os
import subprocess
import nanpy
from time import sleep
from utils.functions import (await_confirmation, loading_screen)
from utils.keypad import Keypad
from utils.screen import Screen
from dotenv import load_dotenv

class Menu:
    def __init__(self):
        self.is_running = True

        self.screen = Screen()
        self.keypad = Keypad()

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
            case 'None':
                pass
            case 'Select':
                self.shutdown()
    
    def shutdown(self) -> None:
        if await_confirmation(self, '¿Apagar equipo?'):
            loading_screen(self, 'Apagando equipo')
            subprocess.run(["shutdown", "-h", "now"])
        
        self.home_screen()

if __name__ == '__main__':
    load_dotenv()

    menu = Menu()
    menu.loop()

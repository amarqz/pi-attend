import warnings
import time
from time import sleep


def await_confirmation(menu, message: str = '¿Estás seguro?', countdown_time: int = 7) -> bool:
    is_yes = True

    if len(message) > 16:
        warnings.warn('The confirmation message was longer than expected. Using default value...')
        message = '¿Seguro?'
    
    menu.screen.print_up(message)
    menu.screen.print_down(' No  <Sí>')

    sleep(0.4)
    
    start_time = time.time()
    while time.time() - start_time < countdown_time:
        if menu.keypad.read_button() == 'Left':
            menu.screen.print_down('<No>  Sí ')
            is_yes = False
        elif menu.keypad.read_button() == 'Right':
            menu.screen.print_down(' No  <Sí>')
            is_yes = True
        elif menu.keypad.read_button() == 'Select':
            return is_yes

    return False

def loading_screen(menu, message: str = 'Espera...', countdown_time: int = 3) -> None:
    menu.screen.clear()    
    menu.screen.print_up(message)
    menu.screen.print_at(0, 1, '[')
    menu.screen.print_at(menu.screen.n_col - 1, 1, ']')

    interval = countdown_time / (menu.screen.n_col - 2)
    
    start_time = time.time()
    chars_inserted = 0
    while chars_inserted < 14:
        if time.time() - start_time > interval * chars_inserted:
            chars_inserted += 1
            menu.screen.print_at(chars_inserted, 1, '#')
        
    
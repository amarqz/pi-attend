import warnings
from time import sleep

def await_confirmation(menu, message: str = '¿Estás seguro?') -> bool:
    timer = 7
    is_yes = True

    if len(message) > 16:
        warnings.warn('The confirmation message was longer than expected. Using default value...')
        message = '¿Seguro?'
    
    menu.screen.print_up(message)
    menu.screen.print_down(' No  <Sí>')

    sleep(0.4)
    
    while timer >= 0: # ToDo finish timer
        if menu.keypad.read_button() == 'Left':
            menu.screen.print_down('<No>  Sí ')
            is_yes = False
            timer = 7
        elif menu.keypad.read_button() == 'Right':
            menu.screen.print_down(' No  <Sí>')
            is_yes = True
            timer = 7
        elif menu.keypad.read_button() == 'Select':
            return is_yes

    return False
    
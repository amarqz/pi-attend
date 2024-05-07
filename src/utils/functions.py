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
        pressed_button = menu.keypad.read_button()

        if pressed_button == 'Left':
            menu.screen.print_down('<No>  Sí ')
            is_yes = False
        elif pressed_button == 'Right':
            menu.screen.print_down(' No  <Sí>')
            is_yes = True
        elif pressed_button == 'Select':
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
        
def picklist(menu, options: list, message: str = 'Elige:', countdown_time: int = 20) -> (str | int | float | None):
    
    format_selected = lambda x: f'<{x}>'.center(menu.screen.n_col, ' ')
    
    display_max_width = menu.screen.n_col - 2

    for index, element in enumerate(options, start=0):
        if len(element) > display_max_width:
            warnings.warn(f'The option: {element} is too long for the display. Cropping the text...')
            options[index] = element[:display_max_width]
    
    number_of_options = len(options)
    options.insert(0, message)
    
    in_view = [0, 1]
    selected = 1

    menu.screen.full_print(options[0], format_selected(options[1]))

    start_time = time.time()
    while time.time() - start_time < countdown_time:
        pressed_button = menu.screen.read_button()

        if pressed_button == 'Up':
            pass
        elif pressed_button == 'Down':
            pass
        elif pressed_button == 'Select':
            return options[selected]
        elif pressed_button == 'Left' or pressed_button == 'Right':
            return None

    return None
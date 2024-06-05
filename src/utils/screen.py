import nanpy
import warnings

class Screen:
    def __init__(self, pins: list = [8, 9, 4, 5, 6, 7], n_col: int = 16, n_row: int = 2) -> None:
        self.__lcd = nanpy.Lcd(pins, [n_col, n_row])
        self.n_col = n_col
        self.__define_special_chars()
        self.print_up('Iniciando')

        print('Screen successfully initialized!')

    def full_print(self, top_message: str, bottom_message: str) -> None:
        self.print_up(top_message)
        self.print_down(bottom_message)

    def print_up(self, message: str) -> None:
        special_chars_found = {}

        message = self.__check_size(message)
        message = message.center(self.n_col, ' ')
        message = self.__check_special_chars(message, special_chars_found)

        self.__lcd.setCursor(0, 0)
        self.__lcd.printString(message)
        self.__print_special_chars(special_chars_found, 0)

    def print_down(self, message: str) -> None:
        special_chars_found = {}

        message = self.__check_size(message)
        message = message.center(self.n_col, ' ')
        message = self.__check_special_chars(message, special_chars_found)
        
        self.__lcd.setCursor(0, 1)
        self.__lcd.printString(message)
        self.__print_special_chars(special_chars_found, 1)
    
    def print_at(self, col: int, row: int, msg: str) -> None:
        self.__lcd.setCursor(col, row)
        self.__lcd.printString(msg)

    def clear(self) -> None:
        self.__lcd.clear()

    def __check_size(self, txt: str) -> str:
        if len(txt) > self.n_col:
            warnings.warn(f'Warning! The message "{txt}" overflows the LCD size.')
            warnings.warn(f'Cropping the message to adjust it to the correct size...')
            txt = txt[0:self.n_col]
        return txt

    def __check_special_chars(self, txt: str, chars_found: dict) -> list:
        for index, char in enumerate(txt, start=0):
            if char in self.__special_chars:
                if char not in chars_found:
                    chars_found[char] = []
                chars_found[char].append(index)
                txt = txt[:index] + ' ' + txt[index + 1:]

        return txt

    def __print_special_chars(self, chars_found: dict, row: int) -> None:
        for index, char in enumerate(chars_found.keys(), start=0):
            if index > 3: break
            self.__lcd.createChar(index + 4 * row, self.__special_char_mapping[char])
            for position in chars_found[char]:
                self.__lcd.setCursor(position, row)
                self.__lcd.write(index + 4 * row)

    def __define_special_chars(self) -> None:
        self.__special_chars = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú', 'ñ', 'Ñ', '¡', '¿', 'ç']
        
        self.__a_acute = [0b00010,
                          0b00100,
                          0b01110,
                          0b00001,
                          0b01111,
                          0b10001,
                          0b01111,
                          0b00000]
        self.__cap_a_acute = [0b00010,
                              0b00100,
                              0b01110,
                              0b10001,
                              0b10001,
                              0b11111,
                              0b10001,
                              0b00000]
        self.__e_acute = [0b00010,
                          0b00100,
                          0b01110,
                          0b10001,
                          0b11111,
                          0b10000,
                          0b01110,
                          0b00000]
        self.__cap_e_acute = [0b00010,
                              0b00100,
                              0b11111,
                              0b10000,
                              0b11110,
                              0b10000,
                              0b11111,
                              0b00000]
        self.__i_acute = [0b00010,
                          0b00100,
                          0b00000,
                          0b01100,
                          0b00100,
                          0b00100,
                          0b01110,
                          0b00000,]
        self.__cap_i_acute = [0b00010,
                              0b00100,
                              0b01110,
                              0b00100,
                              0b00100,
                              0b00100,
                              0b01110,
                              0b00000]
        self.__o_acute = [0b00010,
                          0b00100,
                          0b01110,
                          0b10001,
                          0b10001,
                          0b10001,
                          0b01110,
                          0b00000]
        self.__u_acute = [0b00010,
                          0b00100,
                          0b10001,
                          0b10001,
                          0b10001,
                          0b10011,
                          0b01101,
                          0b00000]
        self.__cap_u_acute = [0b00010,
                              0b00100,
                              0b10001,
                              0b10001,
                              0b10001,
                              0b10001,
                              0b01110,
                              0b00000]
        self.__spanish_n = [0b01110,
                            0b00000,
                            0b10110,
                            0b11001,
                            0b10001,
                            0b10001,
                            0b10001,
                            0b00000]
        self.__cap_spanish_n = [0b01110,
                                0b10001,
                                0b11001,
                                0b10101,
                                0b10011,
                                0b10001,
                                0b10001,
                                0b00000]
        self.__open_interrogation = [0b00100,
                                     0b00000,
                                     0b00100,
                                     0b01000,
                                     0b10000,
                                     0b10001,
                                     0b01110,
                                     0b00000]
        self.__open_exclamation = [0b00000,
                                   0b00100,
                                   0b00000,
                                   0b00000,
                                   0b00100,
                                   0b00100,
                                   0b00100,
                                   0b00100]
        self.__music_quaver = [0b00100,
                               0b00110,
                               0b00101,
                               0b00101,
                               0b00100,
                               0b01100,
                               0b11100,
                               0b01000,
                               ]

        self.__special_char_mapping = {'á': self.__a_acute, 'é': self.__e_acute, 'í': self.__i_acute, 'ó': self.__o_acute, 'ú': self.__u_acute,
                          'Á': self.__cap_a_acute, 'É': self.__cap_e_acute, 'Í': self.__cap_i_acute, 'Ó': self.__o_acute, 'Ú': self.__u_acute,
                          'ñ': self.__spanish_n, 'Ñ': self.__cap_spanish_n, '¡': self.__open_exclamation, '¿': self.__open_interrogation,
                          'ç': self.__music_quaver}
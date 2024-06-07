import os
import nanpy
import threading
import time
from time import sleep
from utils.functions import (await_confirmation, loading_screen, picklist)
from utils.keypad import Keypad
from utils.screen import Screen
from utils.sensor import Sensor
from utils.buzzer import Buzzer
from utils.api import APIHandler
from datetime import datetime
from dotenv import load_dotenv

class Menu:
    def __init__(self):
        self.is_running = True
        self.detected_tag_id = ''

        self.screen = Screen()

        self.screen.print_down('botonera...')
        self.keypad = Keypad()

        self.screen.print_down('sensor...')
        self.sensor = Sensor()

        self.screen.print_down('zumbador')
        self.buzzer = Buzzer(16)

        self.screen.print_down('conexión API...')
        self.api = APIHandler(os.getenv("POCKETBASE_URL"), os.getenv("POCKETBASE_USERNAME"), os.getenv("POCKETBASE_PASSWORD"))

        self.__find_active_session()
        self.__create_detection_thread()
        
        self.home_screen()
        print('Menu started!')

    def home_screen(self) -> None:
        self.screen.print_up(os.getenv("HOME_SCREEN_MSG_UP"))
        self.screen.print_down(self.__session_type)

    def loop(self) -> None:
        while self.is_running:
            sleep(0.15)
            self.button_actions()

            if self.detected_tag_id != '':
                self.__check_in()

    def button_actions(self) -> None:
        match self.keypad.read_button():
            case 'Select':
                self.__stop_detection_thread()
                self.shutdown()
            case 'Up' | 'Down':
                self.__stop_detection_thread()
                self.create_new_session()
            case 'Right':
                self.__pair_card_user()
                self.home_screen()
                return
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
        
        if new_event_type == None:
            return
        
        current_session_info = self.api.get(f"collections/{os.getenv('POCKETBASE_ATTENDANCE_COLLECTION')}/records", \
            params={'filter': f'evento = "{self.__current_session}"'})['items']

        self.__session_type = new_event_type
        if len(current_session_info) == 0:
            self.api.patch(f'collections/{os.getenv("POCKETBASE_EVENTS_COLLECTION")}/records/{self.__current_session}', \
                data={'tipo': self.__session_type})
        else:
            self.__current_session = self.api.post(f'collections/{os.getenv("POCKETBASE_EVENTS_COLLECTION")}/records', \
                json={'tipo': self.__session_type})['id']

    def __create_detection_thread(self) -> None:
        self.__nfc_thread = threading.Thread(target=self.sensor.detect, name='detection-process', args=(self,))
        self.screen.stop_flag = False
        self.__nfc_thread.start()

    def __stop_detection_thread(self) -> None:
        self.screen.stop_flag = True
        self.__nfc_thread.join(1)

    def __find_active_session(self) -> None:
        today_event = self.api.get(f'collections/{os.getenv("POCKETBASE_EVENTS_COLLECTION")}/records', \
            params={'filter': f"""created >= '{datetime.today().strftime("%Y-%m-%d")} 00:00:00'""", 'sort': '-created'})['items']
        if len(today_event) == 0:
            self.__session_type = 'Ensayo'
            self.__current_session = self.api.post(f'collections/{os.getenv("POCKETBASE_EVENTS_COLLECTION")}/records', \
                json={'tipo': self.__session_type})['id']
        else:
            self.__current_session = today_event[0]['id']
            self.__session_type = today_event[0]['tipo']

    def __pair_card_user(self) -> None:
        not_paired_users = self.api.get(f'collections/{os.getenv("POCKETBASE_MEMBERS_COLLECTION")}/records', \
            params={'filter': 'tarjeta_UID = ""', 'sort': 'nombre'})['items']
        if len(not_paired_users) == 0:
            self.screen.full_print('No hay nadie', 'por registrar.')
            sleep(3)
            return
        
        selected_user = picklist(self, [user['nombre'] for user in not_paired_users], '¿Quién?')
        if selected_user == None:
            return

        user_id = not_paired_users[next((index for index, user in enumerate(not_paired_users) if user['nombre'].startswith(selected_user)), 0)]['id']
        self.screen.full_print(selected_user, 'Acercar tarjeta')
        start = time.time()
        while time.time() - start < 5:
            if self.detected_tag_id != '':
                self.buzzer.play_melody('1 Up')
                self.screen.full_print(selected_user, self.detected_tag_id)

                card_uid_coincidences = self.api.get(f'collections/{os.getenv("POCKETBASE_MEMBERS_COLLECTION")}/records', \
                    params={'filter': f'tarjeta_UID = "{self.detected_tag_id}"'})['items']
                if len(card_uid_coincidences) > 0:
                    self.screen.full_print("Error:registrado", f"@ {card_uid_coincidences[0]['nombre']}")
                    sleep(0.5)
                else:
                    self.api.patch(f'collections/{os.getenv("POCKETBASE_MEMBERS_COLLECTION")}/records/{user_id}', \
                        data={'tarjeta_UID': self.detected_tag_id})
                    self.screen.print_down("¡Éxito!")
                    

                self.detected_tag_id = ''
        return

    def __check_in(self):
        card_uid_coincidences = self.api.get(f'collections/{os.getenv("POCKETBASE_MEMBERS_COLLECTION")}/records', \
            params={'filter': f'tarjeta_UID = "{self.detected_tag_id}"'})['items']

        if len(card_uid_coincidences) == 0:
            self.buzzer.play_melody('Error')
            self.screen.full_print('Error: tarjeta', 'desconocida')
            sleep(1)
        else:
            user_id = card_uid_coincidences[0]['id']
            user_name = card_uid_coincidences[0]['nombre']
            if 'code' in self.api.post(f'collections/{os.getenv("POCKETBASE_ATTENDANCE_COLLECTION")}/records', \
                json={'componente': user_id, 'evento': self.__current_session, 'presente': True, \
                    'porcentaje_suma': 100}).keys():
                self.buzzer.play_melody('Error')
                self.screen.full_print("¡Ya has pasado", "la tarjeta!")
            else:
                self.buzzer.play_melody('Check in')
                self.screen.full_print("ç Hola, ç", user_name.split(' ')[0])
            sleep(1)

        self.detected_tag_id = ''
        self.home_screen()
        

if __name__ == '__main__':
    load_dotenv()

    menu = Menu()
    menu.loop()

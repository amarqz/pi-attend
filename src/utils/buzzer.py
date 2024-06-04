import RPi.GPIO as GPIO
from time import sleep

class Buzzer:
    def __init__(self, buzzer_pin: int):
        self.__define_notes_melodies()
        self.__BUZZER_PIN = buzzer_pin

    def __play_sound(self, bpm: float, figure: float, frequency: float) -> None:
        duration = self.__compute_duration(bpm, figure, frequency)
        for i in range(duration):
            GPIO.output(self.__BUZZER_PIN, GPIO.HIGH)
            sleep(1/frequency)
            GPIO.output(self.__BUZZER_PIN, GPIO.LOW)
            sleep(1/frequency)

    @staticmethod
    def __compute_duration(bpm: float, figure: float, frequency: float) -> int:
        crotchet_duration = 60/bpm
        note_cycles = crotchet_duration / (2 / frequency)
        return round(figure * note_cycles)
    
    def play_melody(self, melody: str) -> None:
        if melody not in self.__melodies.keys():
            print('Error: Non-existent melody name.')
            return
        if len(self.__melodies[melody]['notes']) != len(self.__melodies[melody]['figures']):
            print('Error: Melody\'s notes and figures do not have the same length.')
            return

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__BUZZER_PIN, GPIO.OUT)

        bpm = self.__melodies[melody]['BPM']
        for note, figure in zip(self.__melodies[melody]['notes'], self.__melodies[melody]['figures']):
            self.__play_sound(bpm, figure, self.__notes[note])

        GPIO.cleanup()

    def __define_notes_melodies(self):
        self.__notes = {
            'C4': 261, 'Cs4': 277, 'D4': 293, 'Ds4': 311, 'E4': 329,
            'F4': 349, 'Fs4': 369, 'G4': 392, 'Gs4': 415, 'A4': 440,
            'As4': 466, 'B4': 493, 'C5': 523, 'Cs5': 554, 'D5': 587,
            'Ds5': 622, 'E5': 659, 'F5': 698, 'Fs5': 739, 'G5': 784,
            'Gs5': 830, 'A5': 880, 'As5': 932, 'B5': 987
        }

        self.__melodies = {
            'Happy birthday': {
                'BPM': 180,
                'notes': ('C5', 'C5', 'D5', 'C5', 'F5', 'E5'),
                'figures': (3/4, 1/4, 1, 1, 1, 2)
            },
            'Check in': {
                'BPM': 220,
                'notes': ('E5', 'A5'),
                'figures': (1/4, 3/4)
            },
            'Error': {
                'BPM': 220,
                'notes': ('A4', 'Ds4'),
                'figures': (1/4, 1/4)
            }
        }
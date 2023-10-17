# Software Name: Generatore CW (Morse)
# Author: Bocaletto Luca
# Description: Questo programma genera e riproduce segnali CW (Morse) da testo e viceversa.

# Importa i moduli necessari
import tkinter as tk
import winsound
import threading  # Importa il modulo threading per gestire il thread di generazione audio

# Definizione delle costanti per la durata dei punti e dei trattini
DOT_DURATION = 100  # Durata in millisecondi di un punto
DASH_DURATION = 300  # Durata in millisecondi di un trattino

# Definizione del codice Morse
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    ' ': ' ', ',': '--..--', '.': '..-.-.-', '?': '..--..',
}

# Variabile globale per il thread di generazione audio
audio_thread = None

# Funzione per generare il segnale CW e l'audio Morse
def generate_cw(text, speed, repetitions):
    global audio_thread  # Utilizza la variabile globale per il thread audio
    morse_text = ""
    audio_morse = ""
    for char in text:
        if char.isalpha():
            morse_char = char.upper()
            if morse_char in morse_code:
                morse_sequence = morse_code[morse_char]
                for symbol in morse_sequence:
                    if symbol == '.':
                        morse_text += "."  # Aggiungi un punto al codice Morse
                        audio_morse += "."  # Aggiungi un punto al suono Morse
                    elif symbol == '-':
                        morse_text += "-"  # Aggiungi un trattino al codice Morse
                        audio_morse += "-"  # Aggiungi un trattino al suono Morse
                morse_text += " "  # Aggiungi uno spazio tra i caratteri Morse
                audio_morse += " "  # Aggiungi uno spazio tra i caratteri Morse
    morse_text = morse_text.strip()
    morse_label.config(text="Conversione in Codice Morse: " + morse_text)
    audio_morse = audio_morse.replace(" ", "")  # Rimuovi gli spazi

    # Funzione per generare audio Morse in un thread separato
    def play_audio():
        for _ in range(repetitions):
            if audio_thread is None:
                return  # Interrompi la generazione se il thread è nullo
            for char in audio_morse:
                if char == '.':
                    winsound.Beep(800, int(DOT_DURATION * speed))  # Riproduci un punto
                elif char == '-':
                    winsound.Beep(800, int(DASH_DURATION * speed))  # Riproduci un trattino

    audio_thread = StoppableThread(target=play_audio)
    audio_thread.start()  # Avvia il thread audio

# Funzione per fermare la generazione audio
def stop_audio_generation():
    global audio_thread
    if audio_thread is not None:
        audio_thread.stop()  # Chiudi il thread audio se esiste
        audio_thread = None  # Imposta il thread audio su None

# Funzione per convertire da Morse a testo e generare l'audio Morse
def morse_to_text_conversion():
    morse_text = morse_entry.get()
    text = ""
    for morse_word in morse_text.split(" "):
        for morse_char in morse_word.split(" "):
            for key, value in morse_code.items():
                if value == morse_char:
                    text += key
                    for symbol in morse_char:
                        if symbol == '.':
                            winsound.Beep(800, int(DOT_DURATION))  # Riproduci un punto
                        elif symbol == '-':
                            winsound.Beep(800, int(DASH_DURATION))  # Riproduci un trattino
            text += " "  # Aggiungi uno spazio tra le parole
    text_entry.delete(0, tk.END)
    text_entry.insert(0, text)

# Classe Thread personalizzata che può essere interrotta
class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

# Creazione della GUI
root = tk.Tk()
root.title("Generatore CW (Morse)")

text_label = tk.Label(root, text="Inserisci il Testo da convertire:")
text_label.pack()

text_entry = tk.Entry(root, width=40)
text_entry.pack()

text_label = tk.Label(root, text="Inserisci il Codice Morse da convertire:")
text_label.pack()

morse_entry = tk.Entry(root, width=40)
morse_entry.pack()

morse_label = tk.Label(root, text="Conversione in Morse:")
morse_label.pack()

text_to_morse_button = tk.Button(root, text="Da Testo a Morse", command=lambda: generate_cw(text_entry.get(), speed_scale.get(), repetitions_scale.get()))
text_to_morse_button.pack()

morse_to_text_button = tk.Button(root, text="Da Morse a Testo", command=morse_to_text_conversion)
morse_to_text_button.pack()

stop_button = tk.Button(root, text="Arresta Generazione", command=stop_audio_generation)
stop_button.pack()

repetitions_label = tk.Label(root, text="Ripetizioni Audio:")
repetitions_label.pack()
repetitions_scale = tk.Scale(root, from_=1, to=10, orient="horizontal")
repetitions_scale.pack()

speed_label = tk.Label(root, text="Velocità dei Beep:")
speed_label.pack()
speed_scale = tk.Scale(root, from_=0.1, to=2, orient="horizontal", resolution=0.1)
speed_scale.set(1.0)  # Imposta il valore predefinito a 1.0
speed_scale.pack()

root.mainloop()

# Software Name: CW (Morse) Generator
# Author: Luca Bocaletto
# Description: This program generates and plays CW (Morse code) signals from text and vice versa.

# Import necessary modules
import tkinter as tk
import winsound
import threading  # Import the threading module to manage the audio generation thread

# Define constants for the duration of dots and dashes
DOT_DURATION = 100  # Duration in milliseconds of a dot
DASH_DURATION = 300  # Duration in milliseconds of a dash

# Define Morse code
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

# Global variable for the audio generation thread
audio_thread = None

# Function to generate CW signal and Morse audio
def generate_cw(text, speed, repetitions):
    global audio_thread  # Use the global variable for the audio thread
    morse_text = ""
    audio_morse = ""
    for char in text:
        if char.isalpha():
            morse_char = char.upper()
            if morse_char in morse_code:
                morse_sequence = morse_code[morse_char]
                for symbol in morse_sequence:
                    if symbol == '.':
                        morse_text += "."  # Add a dot to the Morse code
                        audio_morse += "."  # Add a dot to the Morse sound
                    elif symbol == '-':
                        morse_text += "-"  # Add a dash to the Morse code
                        audio_morse += "-"  # Add a dash to the Morse sound
                morse_text += " "  # Add a space between Morse characters
                audio_morse += " "  # Add a space between Morse characters
    morse_text = morse_text.strip()
    morse_label.config(text="Morse Code: " + morse_text)
    audio_morse = audio_morse.replace(" ", "")  # Remove spaces

    # Function to generate Morse audio in a separate thread
    def play_audio():
        for _ in range(repetitions):
            if audio_thread is None:
                return  # Stop generation if the thread is null
            for char in audio_morse:
                if char == '.':
                    winsound.Beep(800, int(DOT_DURATION * speed))  # Play a dot
                elif char == '-':
                    winsound.Beep(800, int(DASH_DURATION * speed))  # Play a dash

    audio_thread = StoppableThread(target=play_audio)
    audio_thread.start()  # Start the audio thread

# Function to stop audio generation
def stop_audio_generation():
    global audio_thread
    if audio_thread is not None:
        audio_thread.stop()  # Close the audio thread if it exists
        audio_thread = None  # Set the audio thread to None

# Function to convert from Morse to text and generate Morse audio
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
                            winsound.Beep(800, int(DOT_DURATION))  # Play a dot
                        elif symbol == '-':
                            winsound.Beep(800, int(DASH_DURATION))  # Play a dash
            text += " "  # Add a space between words
    text_entry.delete(0, tk.END)
    text_entry.insert(0, text)

# Custom Thread class that can be stopped
class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

# Create the GUI
root = tk.Tk()
root.title("CW (Morse) Generator")

text_label = tk.Label(root, text="Enter Text to Convert:")
text_label.pack()

text_entry = tk.Entry(root, width=40)
text_entry.pack()

text_label = tk.Label(root, text="Enter Morse Code to Convert:")
text_label.pack()

morse_entry = tk.Entry(root, width=40)
morse_entry.pack()

morse_label = tk.Label(root, text="Morse Conversion:")
morse_label.pack()

text_to_morse_button = tk.Button(root, text="Text to Morse", command=lambda: generate_cw(text_entry.get(), speed_scale.get(), repetitions_scale.get()))
text_to_morse_button.pack()

morse_to_text_button = tk.Button(root, text="Morse to Text", command=morse_to_text_conversion)
morse_to_text_button.pack()

stop_button = tk.Button(root, text="Stop Generation", command=stop_audio_generation)
stop_button.pack()

repetitions_label = tk.Label(root, text="Audio Repetitions:")
repetitions_label.pack()
repetitions_scale = tk.Scale(root, from_=1, to=10, orient="horizontal")
repetitions_scale.pack()

speed_label = tk.Label(root, text="Beep Speed:")
speed_label.pack()
speed_scale = tk.Scale(root, from_=0.1, to=2, orient="horizontal", resolution=0.1)
speed_scale.set(1.0)  # Set the default value to 1.0
speed_scale.pack()

root.mainloop()

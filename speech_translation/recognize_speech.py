from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import threading
import time

from rich.console import Console

import typer

console = Console()
engine = pyttsx3.init()

def loading_effect(text="Loading..."):
    """Animated loading effect."""
    with console.status(f"[bold green]{text}[/bold green]", spinner="dots"):
        time.sleep(1)

def translate_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        loading_effect("Please say something")
        while True:
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                print(f"[You]: {text}\n", end="\r")
                return text

            except sr.UnknownValueError:
                message = " Couldn't understand what you said.. Can you repeat what you said?"
                typer.echo(f"[AI]: {message}")
                engine.say(message)
                engine.runAndWait()

            except sr.RequestError as e:
                typer.echo(f"Oops!. An Error Occured from our end. Please run the application again. {e}")

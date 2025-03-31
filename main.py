import typer
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
import time

# from text_to_speech.tts import speak
from ai_processing.interview_ai import prompt
from gtts import gTTS
import pyttsx3

# CLI app setup
app = typer.Typer()
console = Console()

# Initialize python pyttsx3 engine
engine = pyttsx3.init()



def clear_screen():
    loading_effect("Starting Application. Please wait..")
    print("Loading Application.. Almost there!..")
    # time.sleep(4)
    os.system("cls")
    show_title()


def show_title():
    """Displays the HIREDGPT title with colors."""
    title = Text("""
██   ██ ██ ██████  ███████ ██████   ██████   ██████   ██████  ████████
██   ██ ██ ██   ██ ██      ██   ██ ██    ██ ██    ██ ██    ██    ██
███████ ██ ██████  █████   ██████  ██    ██ ██    ██ ██    ██    ██
██   ██ ██ ██   ██ ██      ██   ██ ██    ██ ██    ██ ██    ██    ██
██   ██ ██ ██   ██ ███████ ██   ██  ██████   ██████   ██████     ██

AI-Powered Job Interview Simulator 🚀 - Command Line Edition
""", style="bold yellow")
    console.print(title)

def loading_effect(text="Loading..."):
    """Animated loading effect."""
    with console.status(f"[bold green]{text}[/bold green]", spinner="dots"):
        time.sleep(3)

@app.command()
def start():
    """Launch the AI interview simulator."""
    clear_screen()
    console.print(Panel("[bold magenta]Welcome to HIREDGPT![/bold magenta]\n\n"
                        "📝 [cyan]1. Start Interview\n"
                        "💡 [cyan]2. Get AI Feedback\n"
                        "🎤 [cyan]3. Use Voice Mode\n"
                        "❌ [cyan]4. Exit\n",
                        title="Main Menu", expand=False))

    choice = typer.prompt("\nEnter your choice (1-4)")

    if choice == "1":
        loading_effect("Preparing interview questions...")
        # time.sleep(3)
        typer.echo("🚀 Starting Interview...")
        # time.sleep(3)
        start_interview()
        # Call interview function
    elif choice == "2":
        loading_effect("Analyzing your response...")
        typer.echo("💡 Generating AI Feedback...")
        # Call feedback function
    elif choice == "3":
        loading_effect("Enabling voice mode...")
        typer.echo("🎤 Voice Recognition Activated!")
        # Call speech-to-text function
    elif choice == "4":
        typer.echo("❌ Exiting HIREDGPT. Goodbye!")
        raise typer.Exit()
    else:
        typer.echo("[red]Invalid choice! Please enter a number between 1 and 4.[/red]")
        start()  # Restart menu

def start_interview():
    role = str(input("[AI]: What role would you like to be interviewd for? (e.g Fullstack Developer, Product Designer):\n[You]: "))
    keywords = str(input("[AI]: Enter Job Description Keywords (e.g Python, Figma or None):\n[You]: "))
    job_desc = str(input("[AI]: Paste or type Job Description here:\n[You]: "))
    data = prompt(role, keywords, job_desc)
    print(data)


    for index, item in enumerate(data):
        print("got here")
        print(f"[AI]: {str(index)}. {item['question']}:\n")

        # tts = gTTS(data["question"], lang="en")
        # # Save to a temporary file
        # tts.save("files/temp.mp3")

        # Play the audio
        engine.say(item['question'])
        print("Got to pyttsx3 engine")
        engine.runAndWait()

        # get user responses
        user_response = str(input("[You]: "))

if __name__ == "__main__":
    app()


if __name__ == "__main__":
    os.system("cls")
    role = input("What role are applying for or what role would like to be interviewd for? (e.g Fullstack Developer): \n")

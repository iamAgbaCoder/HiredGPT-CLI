import typer
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
import time
import threading

# from text_to_speech.tts import speak
from ai_processing.interview_ai import prompt
from gtts import gTTS
import pyttsx3
import speech_recognition as sr
# from speech_recognition.recognize_speech import recognize_speech


from ai_processing.feedback import compare_responses
from ai_processing.utils import db_save, load_db, custom_datetime_format


# CLI app setup
app = typer.Typer()
console = Console()

# Initialize python pyttsx3 engine
engine = pyttsx3.init()

# Load existing results to avoid overwriting
db = load_db()



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
    print(type(choice))

    if choice == "1":
        loading_effect("Preparing interview questions...")
        # time.sleep(3)
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

@app.command()
def start_interview():
    role = str(input("[AI]: What role would you like to be interviewd for? (e.g Fullstack Developer, Product Designer):\n[You]: "))
    keywords = str(input("[AI]: Enter Job Description Keywords (e.g Python, Figma or None):\n[You]: "))
    job_desc = str(input("[AI]: Paste or type Job Description here:\n[You]: "))

    loading_effect("🚀 Starting Interview...")

    interview_title = f"{role.title()} Interview ({custom_datetime_format()}) "  # Change dynamically as needed

    typer.echo("==========================================================================")
    typer.echo(interview_title)
    typer.echo("==========================================================================")
    data = prompt(role, keywords, job_desc)


    for index, item in enumerate(data):
        typer.echo(f"[AI]: {item['question']}:\n")

        # tts = gTTS(data["question"], lang="en")
        # # Save to a temporary file
        # tts.save("files/temp.mp3")

        # Play the question using text-to-speech
        engine.say(item["question"])
        engine.runAndWait()

        # Get user response
        # user_response = typer.prompt("[You]\n")
        from speech_translation.recognize_speech import translate_speech
        user_response = translate_speech()

        # Compute similarity score (Replace `compare_responses` with actual function)
        ideal_answer = item["ideal_answer"]
        score = compare_responses(user_response, ideal_answer)

        # Generate unique question ID
        # question_id = f"question_{len(results[interview_title]) + 1}"
        question_id = index

        if interview_title not in db:
            db[interview_title] = {}

        db[interview_title][question_id] = {
            "question": item["question"],
            "user_response": user_response,
            "evaluation": {
                "similarity_score": score,
                "ideal_response": ideal_answer
            },
        }

        # Save results
        db_save(db)
        # typer.echo("Interview completed! Results saved to interview_results.json.")


if __name__ == "__main__":
    app()

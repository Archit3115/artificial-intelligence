import os
import speech_recognition as sr
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from elevenlabs.client import ElevenLabs
from elevenlabs import play, stream

# --- CONFIGURATION ---
# It's best practice to use environment variables for API keys.
# Set this in your terminal before running: export ELEVEN_API_KEY="your_key_here"
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
if not ELEVEN_API_KEY:
    raise ValueError("ELEVEN_API_KEY environment variable not set. Please set it before running.")

# Initialize the ElevenLabs client
try:
    client = ElevenLabs(api_key=ELEVEN_API_KEY)
except Exception as e:
    print(f"Error initializing ElevenLabs client: {e}")
    exit()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """
    Converts text to speech using the recommended low-latency model and plays it.
    This uses the 'eleven_flash_v2_5' model, which is optimized for real-time use [7, 8].
    """
    print(f"Jarvis: {text}")
    try:
        # Use stream for the lowest latency possible
        audio_stream = client.generate(
            text=text,
            voice="Rachel", # You can choose any voice you like
            model="eleven_flash_v2_5" # Recommended for real-time agents [7]
        )
        stream(audio_stream)
    except Exception as e:
        print(f"An error occurred during text-to-speech generation: {e}")

def listen_for_command():
    """
    Listens for a command from the user via the microphone and transcribes it.
    """
    with sr.Microphone() as source:
        print("\nListening for a command...")
        recognizer.pause_threshold = 1.0
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-gb')
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")
        return None

def process_command(command):
    """
    Processes the transcribed command and returns a response.
    This is the core logic of the agent.
    """
    if not command:
        return

    if "hello jarvis" in command or "hello" in command:
        speak("Hello, sir. How can I assist you today?")
    elif "what time is it" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"Sir, the current time is {now}.")
    elif "tell me about this project" in command:
        # This response is based on the purpose described in your repo's README [1]
        speak("This project is a lightweight playground for AI experiments, focusing on real-time voice integration using LiveKit, WebRTC, and ElevenLabs.")
    elif "goodbye" in command or "exit" in command:
        speak("Goodbye, sir.")
        return False # Signal to exit the loop
    else:
        speak("I'm sorry, I don't have a function for that yet.")
    
    return True # Signal to continue the loop

def main():
    """
    Main loop for the Jarvis agent.
    """
    speak("Jarvis is online and ready.")
    
    running = True
    while running:
        command = listen_for_command()
        if command:
            running = process_command(command)

if __name__ == "__main__":
    main()
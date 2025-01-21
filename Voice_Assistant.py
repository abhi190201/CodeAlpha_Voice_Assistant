import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pywhatkit

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak a text message
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's command with retry on error
def listen():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Adjust time limits as needed
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand. Could you please repeat?")
            return None
        except sr.RequestError:
            speak("Sorry, I could not connect to the service. Please check your internet connection.")
            return None
        except sr.WaitTimeoutError:
            speak("Sorry, no input detected. Please try again.")
            return None
        except KeyboardInterrupt:
            speak("Operation cancelled by user.")
            return None

# Function to perform actions based on the command
def process_command(command):
    if command is None:
        return

    if 'time' in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {time}")

    if 'date' in command:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {date}")

    if 'write date and time' in command:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("date_time.txt", "w") as file:
            file.write(f"Current date and time: {now}")
        speak("The current date and time have been written to date_time.txt")
    
    elif 'wikipedia' in command:
        query = command.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results for this topic. Please be more specific.")
        except wikipedia.exceptions.HTTPTimeoutError:
            speak("Wikipedia request timed out.")
    
    elif 'search' in command:
        query = command.replace("search", "")
        pywhatkit.search(query)
        speak(f"Searching for {query} on Google.")
    
    elif 'open' in command:
        website = command.replace("open", "").strip()
        url = f"https://{website}.com"
        webbrowser.open(url)
        speak(f"Opening {website}")
    
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        exit()

# Main function to run the assistant
def run_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            process_command(command)

# Run the assistant
if __name__ == "__main__":
    run_assistant()


import speech_recognition as sr
import webbrowser  # builtin module
import pyttsx3
import musiclibrary
import requests
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi="4ac990d0bcc547a89bf3e170a16cb0ad"

def speak(text):
    engine.say(text)
    engine.runAndWait()  # Corrected indentation


def processCommand(c):
    print("Command recognized:", c)
    # Add your command processing logic here
    if "open youtube" in c.lower():
        webbrowser.open("youtube.com")
    elif "open" in c.lower():
        search_term = c.lower().replace("open", "").strip() #extract search query
        webbrowser.open(f"{search_term}.com")
    # ... add more command handling logic
    elif c.lower().startswith("play"):
        word=c.lower().replace("play","").strip()
        webbrowser.open(musiclibrary.music[word])
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json()
            articles=data.get('articles',[])    
            for article in articles:
                speak(article['title'])

    else:
      pass         


if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        # listen for the wake word "Jarvis"
        # obtain audio from the microphone

        print("Listening for wake word...")
        try:
            with sr.Microphone() as source:
                print("Calibrating microphone for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1) # Calibrate for noise
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5) # Increased timeout and phrase limit
            wake_word = recognizer.recognize_google(audio).lower() # Using google recognizer, more common and often works without API key
            print("Wake word detected:", wake_word)

            if "jarvis" in wake_word:  # More robust wake word detection (allow for slight variations)
                speak("Yes, sir?") # More natural response
                with sr.Microphone() as source:
                    print("Jarvis Active... Listening for command...")
                    audio = recognizer.listen(source, timeout=7, phrase_time_limit=10) # Increased timeout and phrase limit for commands
                    try:
                        print(audio)
                        command = recognizer.recognize_google(audio).lower() # Using google recognizer for commands as well
                        print(command)
                        processCommand(command)
                    except sr.UnknownValueError:
                        speak("Sorry, I did not understand that.")
                        print("Could not understand audio")
                    except sr.RequestError as e:
                        speak("Could not request results from Google Speech Recognition service; {}".format(e))
                        print("Could not request results from speech recognition service; {}".format(e))


        except sr.WaitTimeoutError: # Handle timeout when no speech is detected for wake word
            print("Listening for wake word...") # Keep prompting
            pass # Just continue listening if no wake word is heard in timeout
        except sr.UnknownValueError: # Handle errors during wake word recognition
            print("Could not understand audio for wake word")
            pass # Continue listening for wake word
        except sr.RequestError as e: # Handle API request errors
            print("Could not request results from Google Speech Recognition service; {}".format(e))
            print("Make sure you have internet connection and Google Speech API is working.")
            break # Exit the loop if there's a persistent API issue, or handle it differently

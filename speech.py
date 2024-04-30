#pip install pocketsphinx
#pip install SpeechRecognition pyttsx3
#pip install pyaudio

import speech_recognition as sr
import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text(recognizer, source):
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

    try:
        # Use PocketSphinx for offline speech recognition
        text = recognizer.recognize_sphinx(audio)
        return text.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Error retrieving results from PocketSphinx service: {e}")
        return None

def run_chatbot(responses):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")  # Print the message only once at the beginning
        text = speech_to_text(recognizer, source)
        triggered = False
        while True:
            if text and "hi robo" in text and not triggered:
                triggered = True
                print("Trigger word detected.")
                text_to_speech("Hello, How can I help you?")
            
            text = speech_to_text(recognizer, source)
            
            if text:
                if "bye robo" in text:
                    text_to_speech("Ok, See you later.")
                    break
                else:
                    found_response = False
                    for command in responses:
                        if isinstance(command, tuple):
                            if any(word in text for word in command):
                                text_to_speech(responses[command])
                                print("robo:", responses[command])
                                found_response = True
                                break
                        else:
                            if command in text:
                                text_to_speech(responses[command])
                                print("robo:", responses[command])
                                found_response = True
                                break
                    if not found_response:
                        text_to_speech(responses["default"])
                        print("robo:", responses["default"])
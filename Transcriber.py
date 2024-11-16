import speech_recognition as sr
import pyttsx3
import os
# CONNECTION TO INTERNET IS MUST!!

# Asks the user where the text should be stored
def text_file_path_input():
    file = str(input(">> Enter the path to your file: ")) # Takes the input as a string
    file = os.path.normpath(file) # Get's rid of any anomalies
    with open(file, 'a') as file_initialization: # Makes the file
        pass # Does nothing to the file, acts as a placeholder
    return file # Returns the name of the file

# Converts text into speech when given a string argument
def text_to_speech(text):
    engine = pyttsx3.init() # Initializes the engine
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id ) # set the voice type, 0 for male, 1 for female
    engine.setProperty('rate', 150)  # Set speech speed
    engine.setProperty('volume', 1)  # Set volume level
    engine.say(text) # Speaks
    engine.runAndWait() # Waits until task is complete

# Transcribes the speech 
# Returns "True" if the program runs without issue or with issue, it's a signal that the program will go through another loop
# Returns "False" if the user chooses to exit the program, signaling that there is no need for another loop
def transcribe(file_name):
    # It takes microphone input from the user and produces string output

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(">> You can say \"exit the program\" to exit OR \"read the text\" to listen to what you have transcribed")
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")    
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n") # Prints out the input for user to confirm, can be disable without affecting the program

        # Important to exit the program, transcribe and read
        # Exists the program if users ask
        if query.lower() == "exit the program":
            print(f">> Successfully exited the program")
            return False # Signaling to exit the program
        
        # Reads out the text if users asks
        elif query.lower() == "read the text":
            if os.path.exists(file_name): # Checks if the file exists
                with open(file_name, "r") as tts:
                    lines = tts.readlines()
                for line in lines:
                    text_to_speech(line.rstrip("\n"))
            else:
                print(f">> Error: The file \"{file_name}\" does not exist.\n")

        # Transcribes if no specific command is given
        else:
            with open(file_name, "a") as script:
                script.writelines(f"{query}\n")
        

    # Throws an error if there is an issue, Internet connection is must
    except Exception as e: 
        print("Say that again please...\n")  

    return True # Continues the program if everything completes without interruption

def main():
    file_name = text_file_path_input()
    while True:
        if not transcribe(file_name):
            break

if __name__ == "__main__":
    main()
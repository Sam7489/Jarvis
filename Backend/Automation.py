from AppOpener import close, open as appopen  # Import functions to open and close apps
from webbrowser import open as weboopen   # Import web browser functionality.
from pywhatkit import search, playonyt    # Import functions for Google search and Youtube playback
from dotenv import dotenv_values   # Import dotenv to manage environment variables
from bs4 import BeautifulSoup      # Import beautifulsoup for parsing HTML content
from rich import print             # Import rich for styled console output.
from groq import Groq              # Import Groq for AI chat functionalities.
import webbrowser   # Import webbrowser for opening urls
import subprocess   # Import subprocess for interacting with the system.
import requests     # Import requests for making HTTP requests.
import keyboard   # Import keyboard for keyboard related actions.
import asyncio   # Import asyncio for asynchronous programming.
import os    # Import os for operating system functionalities. 

# Load environment variables from the .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")    # Retrive the groq api key

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests
useragent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask."
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write contect like letters, codes, applications, essays, notes, songs, poems etc."}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search
    return True   # Indicate success

# Function to generate content using AI and save it to a file.
def Content(Topic):
    
    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, File])   # open the file in notepad.
        
    # Nested function to generate content using the ai chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})   # add the user's prompt to messages
        
        completion = client.chat.completions.create(
        model= 'mixtral-8x7b-32768',   # specify the model
        messages= SystemChatBot + messages,   # include system instructions and chat history
        max_tokens= 2048,    # limit the miximum tokens in the response
        temperature = 0.7,   # adjust response randomness
        top_p=1,  # use nucleus sampling for response diversity
        stream= True,   # Enable streaming response.
        stop=None    # allow the model to determine stopping conditions
        )
        '''
        Answer = completion.choices[0].message.content
        '''
        Answer = ""   # Initialize an empty string for the response
        
        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:     # check for content in the current chunk.
                Answer += chunk.choices[0].delta.content   # append the content to the answer
        
        
        Answer = Answer.replace("</s>", "") # remove unwanted tokens from the response
        messages.append({"role": "assistant", "content": " Answer"})   # Add the AI's response to messages.
        return Answer
    
    #Topic: str = Topic.replace("Content ","")   # remove "Content " from the topic.
    Topic= Topic.replace("Content ","")
    ContentByAI = ContentWriterAI(Topic)     # Generate content using AI
    
    # save the generated content to a text file
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)     # write the content to the file
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")    # open the file in notepad
    return True     # Indicate success

# Function to search for a topic on Youtube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"     # construct the youtube search url
    webbrowser.open(Url4Search)     # open the search url in a web browser.
    return True    # Indicate success

# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query)     # use pywhatkit's playonyt function to play the video.
    return True   # Indicate success

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.session()):
    
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)   # attempt to open the app
        return True   # indicate success
    
    except:
        # Nested function to extract links from HTML content.
        def extract_links(html):
            if html is None:
                return[]
            soup = BeautifulSoup(html, 'html.parser')  # parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'})    # find relevant links
            return [link.get('href') for link in links]    # Return the links
        
        # Nested function to perform a google search and retrive HTML
        def search_google(query):
            url= f"https://www.google.com/search?q={query}"   # construct the google search url
            headers = {"User-Agent": useragent}    # Use the predefined user-agent
            response = sess.get(url, headers=headers) # perform the get request
            
            if response.status_code == 200:
                return response.text   # Return the HTML content
            else:
                print("Failed to retrieve search results.") # print an error message
            return None
        
        html = search_google(query=app)   # Perform the google search
        try:
            if html:
                link = extract_links(html)[0]    # Extract the first link from the search results.
                weboopen(link)  # open the link in a web browser
        except:
            weboopen(f"https://{app}.com")
        return True   # Indicate success.

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass   # skip if the app is chrome
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)   # Attempt to close the app
            return True   # Indicate success
        except:
            return False  # Indicate failure

# Function to execute system-level commands.
def System(command):
    
    # Nested function to unmute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")   # Simulate the mute key press
        
    # Nested function to unmute the system volume
    def unmute():
        keyboard.press_and_release("volume mute")   # Simulate the unmute key press
        
    # Nested function to increase the system volume
    def volume_up():
        keyboard.press_and_release("volume up")     # Simulate the volume up key press
        
    # Nested function to decrease the system volume
    def volume_down():
        keyboard.press_and_release("volume down")    # Simulate the volume down key press
        
    # Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True   # Indicate success.


# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    
    funcs = []   # list to store asynchronous tasks.
    
    for command in commands:
        
        if command.startswith("open "):    # Handle "open "  commands.
            
            if "open it" in command:     # Ignore "open it"  commands.
                pass
            
            if "open file" ==command:   # ignore "open file"  commands.
                pass
            else:
                fun= asyncio.to_thread(OpenApp, command.removeprefix("open "))   # Schedule app opening
                funcs.append(fun)
                
        elif command.startswith("general "):    # Placeholder for general commands.
            pass
        
        elif command.startswith("realtime "):    # Placeholder fro real-time commands.
            pass
        
        elif command.startswith("close "):    # Handle "close commands."
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))   # Schedule app closing.
            funcs.append(fun)

        elif command.startswith("play "):    # handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))    # schedule youtube playback
            funcs.append(fun) 

        elif command.startswith("content "):   # handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))    # schedule content creation
            funcs.append(fun)
            
        elif command.startswith("google search "):   # handle "google search" commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))    # schedule google search creation
            funcs.append(fun)
            
        elif command.startswith("youtube search "):   # handle "youtube search" commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))    # schedule youtube search creation
            funcs.append(fun)
            
        elif command.startswith("system "):   # handle "system" commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))    # schedule system creation
            funcs.append(fun)
            
        else:
            print(f"No Function Found. For {command}")    # Print an error fro unrecognized commands.
            
    results = await asyncio.gather(*funcs)     # Execute all tasks concurrently.
    
    for result in results:     # Process the results
        if isinstance(result, str):
            yield result
        else: 
            yield result
            
# Asynchronous function to automate command execution
async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):    # Translate and execute commands
        pass
    return True     # Indicate success
'''
if __name__ == "__main__":
    asyncio.run(Automation(["close settings", "open notepad", "play uyi amma", "close instagram"]))
    
    '''


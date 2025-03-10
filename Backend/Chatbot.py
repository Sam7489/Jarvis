from groq import Groq   # importing the groq library to use its api
from json import load, dump    # importing functions to read and write json files.
import datetime             #  importing the datetime module for real time date and time information
from dotenv import dotenv_values    # importing dotenv values to read environment variables from a .env file

#load environment variable form the .env file 
env_vars = dotenv_values(".env")

# retrive specific environment variables for username, assistant name, and api key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")
  
# initialize the Groq client using the provided API key
client = Groq(api_key=GroqAPIKey)

# Initialize an empty list to store chat messages
messages = []

# Define a system message that provides context to the AI chatbot about its role and behavior
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# A list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

# Attempt to load the chat log from a JSON file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)    # load existing messages from the chat log
except FileNotFoundError:
    # if the file doesn't exist, create an empty JSON file to store chat logs
    with open(r"Data\ChatLog.json", "w") as f:
        dump([],f)   

# Function to get real-time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now() # get the current date and time
    day = current_date_time.strftime("%A")    # day of the week
    date = current_date_time.strftime("%d")   # day of the month
    month = current_date_time.strftime("%B")  # full  month name
    year = current_date_time.strftime("%Y")   #year
    hour = current_date_time.strftime("%H")   # hour in 24 hour format
    minute = current_date_time.strftime("%M") #minute
    second = current_date_time.strftime("%S") # second
    
    # Format the information into a string 
    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours : {minute} minutes :{second} seconds.\n"
    return data

# Function to modify the chatbot's response for better formatting
def AnswerModifier(Answer):
    lines = Answer.split('\n')   # split the response into lines
    non_empty_lines = [line for line in lines if line.strip()]     # remove empty lines
    modified_answer = '\n'.join(non_empty_lines)   # join the cleaned lines back together
    return modified_answer

# main chatbot function to handle user queries
def ChatBot(Query):
    """ this function sends the user's query to the chatbot and returns the AI's response. """
     
    try:
         # Load the existing chat log from the JSON file.
        with open(r"Data\Chatlog.json", "r") as f:
            messages = load(f)

            #Appent the user's query to the messages list
            messages.append({"role": "user" , "content": f"{Query}"})

            # Make a request to the groq api for a response
            completion = client.chat.completions.create(
                model= "llama3-70b-8192",  # specify the AI model to use
                messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,  # include system instructions , real time info , 
                max_tokens= 1024,  # limit the maximum tokens in the response
                temperature=0.7, # adjust response randomness ( higher means more random)
                top_p=1, # enalbe streaming response
                stop=None # allow the model to determine when to stop
            )
            
            # ✅ Extract the correct response from the completion object
            Answer = completion.choices[0].message.content
            
            """
            Answer = ""  # Initialize an empty string to store the AI's response
            
            #Process the streamed response chunks.
            for chunk in completion:      # check if there's content in the current chunk
                if chunk.choices[0].delta.content:   # append the content to the answer
                    Answer += chunk.choices[0].delta.content   # appent the content to the answer
            """
                    
            Answer = Answer.replace("</s>", "")   # Clean up any unwanted tokens from the response
            
            # Append the chatbot's response to the messages list.
            messages.append({"role": "assistant", "content": Answer})

            # Save the updated chat log to the JSON file.
            with open(f"Data\ChatLog.json", "w") as f:
                dump(messages, f, indent=4)

            # Return the formatted response.
            return AnswerModifier(Answer=Answer)
            
    except Exception as e:
        # Handle errors by printing the exceptionand resetting the chat log.
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)   # Retry the query after resetting the log.
    
# Main program entry point.
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # Prompt the user for a question.
        print(ChatBot(user_input))   # Call the chatbot function and print
            
        
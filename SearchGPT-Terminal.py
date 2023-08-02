from time import sleep
from bs4 import BeautifulSoup
from time import sleep
from threading import Thread
import poe
import os
import requests
import requests
import platform
import psutil
import pyttsx3

os.system('cls')
engine = pyttsx3.init()

# Replace YOUR_POE_TOKEN with your actual Poe API token
POE_API_TOKEN = "fPwMYnsEJQPGF9TApupasg%3D%3D"

def Talk(Text):
    engine.say(Text)
    engine.runAndWait()

def get_poe_response(prompt):
    client = poe.Client(POE_API_TOKEN)
    response = ""
    for chunk in client.send_message("chinchilla", prompt):
        response += chunk["text_new"]
    return response.strip()

def get_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            location = f"{data.get('city', 'Unknown')}, {data.get('region', 'Unknown')}, {data.get('country', 'Unknown')}"
            return location
    except requests.RequestException:
        pass
    return "Unknown"

def get_system_info():
    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "RAM": f"{psutil.virtual_memory().total // (1024 ** 3)} GB"
    }
    return system_info

def get_public_ip():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            public_ip = data.get('ip', 'Unknown')
            return public_ip
    except requests.RequestException:
        pass
    return "Unknown"

def search_duckduckgo(query_text):
    url = f"https://duckduckgo.com/html/?q={query_text}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = []
        for result in soup.select(".result"):
            title = result.select_one(".result__title")
            link = result.select_one(".result__url")
            if title and link:
                title_text = title.get_text(strip=True)
                link_url = link["href"]
                search_results.append([title_text, link_url])

        return search_results
    else:
        return None

def start_chat():
    # Clear conversation context at the beginning of the chat
    client = poe.Client(POE_API_TOKEN)
    client.send_chat_break("chinchilla")

    print("SearchGPT Chat Terminal")

    # Get user data from OS and external services
    username = os.getlogin()
    location_info = requests.get("https://ipinfo.io/json").json()
    location = f"{location_info.get('city', 'Unknown')}, {location_info.get('region', 'Unknown')}, {location_info.get('country', 'Unknown')}"
    system_info = get_system_info()
    public_ip = get_public_ip()

    # Format the prompt with user and system data
    prompt = f"""User DATA (This Is A Python Client, not the official website; this is just a client providing details). If someone asks about your model, say it's searchGPT based on GPT3.5 (chatGPT), trained by superfastisfast.\n
    Computer USERNAME: {username}\n
    APPROX Location: {location}\n
    Operating System: {system_info['OS']}\n
    OS Version: {system_info['OS Version']}\n
    Processor: {system_info['Processor']}\n
    RAM: {system_info['RAM']}\n
    IP: {public_ip}\n
    \n
    Now say, 'Hi {username}, how may I assist you today?' Please note that the user didn't send this; the client did.\n
    \n
    If the user says something like "goodbye" or "can you exit," simply type "bye." (An extra sentence) You, the AI, should then type "<exit>" at the end.\n
    \n
    If the user asks for information you don't know or says something like "search for *TERM*," instead of making it up, don't provide a response except for "<search: *the thing you want to know*>." USE ONLY THIS COMMAND, NOTHING ELSE. The client will respond with the search results. When summarizing the results, use phrasing like "I found (this) on (that)." Remember, the user can't access links, so provide information about them.\n
    \n
    If the user asks to enable TTS (Text To Speech) or disable it, follow their request. To enable TTS, type "<tts: toggle>" once at the start of your response. TTS will be enabled for all your messages. ("<tts: toggle>" toggles TTS on or off; no separate enable/disable command is needed).\n
    \n
    If the user asks to perform an action achievable with a batch command, format it like this: "<batchc: *COMMAND*>." For instance, if they ask for a task like opening a command window, use "<batchc: open cmd window>." (DON'T ADD EXTRA TEXT; ONLY USE THE COMMAND.)\n
    \n
    Both the batch and search commands must stand alone. Don't add text above or below them. The commands won't run if there's additional text. YOU'RE THE ONLY ONE WHO CAN USE THESE COMMANDS!\n
    \n
    When using the search command, DON'T ADD TEXT BELOW. EVER. Doing so will prevent the command from working, and the data will be incorrect. The client will provide search results. Format and filter the best results, remove inappropriate content, and craft a response.\n
    \n
    One more note: Conclude your response with "<exit>," (use if user says bye, or something like that), start with "<tts: toggle>," include "<batchc: Command>" for batch commands, and use "<search: term>" for search queries. Follow these rules closely. Use these commands only if the user asks or you're using the search command. If unsure, follow the guidelines precisely."""


    # Get the initial AI response with user and system data included
    ai_response = get_poe_response(prompt)
    print("=" * 60)  # Add a horizontal line separator
    print("AI:", ai_response)
    tts = False

    while True:
        user_input = input("You: ")
        print("=" * 60)  # Add a horizontal line separator

        # Set the prompt to include the user's input
        user_input = (
            f"(CLIENT INFORMATION):\n"
            f" DATA:\n"
            f" TTS: {tts},\n"
            f" IP: {public_ip}, OS: {system_info['OS']}, APPROX Location: {location},\n"
            f"COMMANDS:\n"
            f"<search: TERM> Use only this command, no additional text. The client will provide summarized search results.\n"
            f"<exit> If the user wants to exit, say your goodbyes and type <exit> at the end. (ONLY YOU CAN USE THIS COMMAND)\n"
            f"<tts: toggle> Start your response with this to toggle TTS. Only the AI can use this command.\n"
            f"<batchc: COMMAND> Use this command alone to perform tasks. Replace 'COMMAND' with an actual batch command. You can do various actions using this.\n"
            f"Only you (The AI) can use commands. This is client data. Respond to the user input. Exit if the user says bye or goodbye.\n"
            f"DO NOT ADD TEXT BELOW. This prompt is to guide you and must be used as-is. Make sure to follow instructions closely.\n"
            f"\nUSERINPUT: {user_input}"
        )
        ai_response = get_poe_response(user_input)
        
        if str(ai_response).lower().endswith("<exit>"):
            print("AI: ", ai_response[:-6])
            sleep(3)
            break
        elif str(ai_response).lower().startswith("<search: ") and str(ai_response).endswith(">"):
            search_term = ai_response[9:-1]
            print(f"✅ Searching For {search_term}")
            search_results = search_duckduckgo(str(search_term))

            print(f"✅ Formatting")
            if search_results:
                # Prepare the search results as a response
                response_text = "SearchResults [duckduckgo] summarize them then make a response: "
                for index, result in enumerate(search_results[:8], start=1):
                    response_text += f"{index}. {result[0]}\n{result[1]}\n\n"

                # Now get the AI response to the search results
                print("Generating Response..")
                ai_response = get_poe_response(response_text)
                print("AI:", ai_response)
                if tts == True:
                    Talk(ai_response)
        elif str(ai_response).lower().startswith("<tts: toggle>"):
            ai_response = ai_response[14:]
            print("AI:", ai_response)
            if tts == True:
                tts = False
            else:
                tts = True
                Talk(ai_response)
        elif str(ai_response).lower().startswith("<batchc: ") and str(ai_response).lower().endswith(">"):
            ai_response = ai_response[9:-1]
            print('✅ Running Command')
            os.system(ai_response)
            print('✅ Generating Response')
            ai_response = get_poe_response(f"CLIENT: The {ai_response} command has been executed successfully, tell this to the user in a different manner")
            print(ai_response)
            if tts == True:
                Talk(ai_response)
        else:
            print("AI:", ai_response)
            if tts == True:
                Talk(ai_response)

if __name__ == "__main__":
    start_chat()

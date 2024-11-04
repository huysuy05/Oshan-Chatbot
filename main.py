from openai import OpenAI
import streamlit as st
import asyncio
import speech_recognition as sr
from config import API_KEY
import time
client = OpenAI(api_key=API_KEY)
import sqlite3
from datetime import datetime

# front end design for the chatbot



# '''
# Structure for the chatbot
# Step 1: Frontend design (Since this web has 2 features, create two pages for each feature
#
#
# '''
# Connect to a SQLite3 database
conn = sqlite3.connect("chatBot.db")
cur = conn.cursor()

# Create a table that can display texts
cur.execute('''
    CREATE TABLE IF NOT EXISTS chat_history (prev_question TEXT, prev_answer TEXT, prev_audio TEXT)
''')
conn.commit()

# def insert_message(question, answer):
#     cur.execute('''INSERT INTO chat_history (prev_question, prev_answer)  VALUES (?,?)''', (question, answer))
#     conn.commit()


def speech_to_text():
    st.title("You can transfer whatever you speak to text")
    st.write("Start speaking...")
    recognizer = sr.Recognizer()
    record = st.button("Say something")
    if record:
        with sr.Microphone() as source:
            st.write("Recording...")
            audio_data = recognizer.listen(source)
            time.sleep(2)


        try:
            text = recognizer.recognize_google(audio_data)
            st.write("You said:", text)
            st.write(f"Chat says: {chatBot(text)} ")


        except sr.UnknownValueError:
            st.error("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")


# Using the openai API to get the gpt model
def chatBot(question):
    # client = OpenAI(
    #     api_key=os.environ.get("OPEN_AI_KEY")
    # )

    response = client.chat.completions.create(model="gpt-4o",
                                              messages=[{
                                                  "role": "user",
                                                  "content": question}])
    return response.choices[0].message.content.strip()



prev = []
async def stream_lit():
    emp = ""

    st.write(f"Oshan says: {chatBot(emp)}")
    ask = st.chat_input()

    # Use asyncio to run chatBot asynchronously
    if ask:
        st.write(ask)
        with st.spinner("Wait a moment"):
            loop = asyncio.get_event_loop()
            answer = await loop.run_in_executor(None, lambda: chatBot(ask))



        st.write(f"Oshan answers: {answer}")
        cur.execute('''
        INSERT INTO chat_history (prev_question, prev_answer) VALUES (?,?)''', (ask, answer))
        cur.execute('''SELECT prev_question, prev_answer FROM chat_history''')
        row = cur.fetchall()
        # st.write(row)
        conn.close()
        



def home():
    st.title("Welcome to ChatBot App")
    st.balloons()

    st.write("You will be able to interact with a chat bot built with OpenAI API.")

    st.markdown("""
    #### Get Started

    To start chatting with the chatbot, click the button from the Features
    """)




def main():
    st.sidebar.image("ai.jpeg", use_column_width=True)
    st.sidebar.title("Welcome to Oshan AI")
    selection = st.sidebar.radio("Features", ["Home", "ChatBot", "Speech to Text"])

    if selection == "Home":
        home()
    elif selection == "ChatBot":
        asyncio.run(stream_lit())
    elif selection == "Speech to Text":
        speech_to_text()

main()

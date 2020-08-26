import webbrowser
import random
import speech_recognition as sr
import wikipedia
import datetime
import sys
import playsound
from gtts import gTTS
import os
def main():
    def speak(audio):
        print('Computer: ' + audio)
        myobj = gTTS(text=audio, lang='en', slow=False)
        myobj.save("welcome.mp3")
        playsound.playsound("welcome.mp3")
        os.remove("welcome.mp3")

    def greetMe():
        currentH = int(datetime.datetime.now().hour)
        if currentH >= 0 and currentH < 12:
            speak('Good Morning!')
            speak('jay heeind dosto')


        if currentH >= 12 and currentH < 18:
            speak('Good Afternoon!')
            speak('jay heeindd dosto')

        if currentH >= 18 and currentH !=0:
            speak('Good Evening!')
            speak('jay heeind dosto')

    greetMe()

    speak("I am your digital assistant!")
    speak('what can i do for you! MASter!')


    def myCommand():

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold =  1
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print('User: ' + query + '\n')

        except sr.UnknownValueError:
            speak('Sorry sir! I didn\'t get that! try again')
    #        query = str(input('Command: '))
            query=myCommand()

        return query


    if __name__ == '__main__':

        while True:

            query = myCommand();
            query = query.lower()
            if "open "in query:
                cnt=0
                for i in range(len(query)):
                    if query[i]==" ":
                        cnt+=1
                if cnt==1:
                    speak("done sir! Enjoy !")
                    x=query.split(' ', 1)[1]
                    site="www."+x+".com"
                    webbrowser.open(site)
                if query=="open youtube":
                    speak("would u like to open any channel??")
                    query = myCommand()
                    if query in "y yes yaa yeah yuup yup":
                        speak("alright")
                        speak("speak valid channel name")
                        x= myCommand()
                        x=str(x)
                        webbrowser.open("https://www.youtube.com/results?search_query="+x)
                elif(cnt==2):
                    speak("done sir! Enjoy !")
                    if query=="open google drive" :
                        webbrowser.open("drive.google.com")
                    elif query=="open google maps":
                        webbrowser.open("maps.google.com")
                    elif query=="open google translator":
                        webbrowser.open("translator.google.com")
                else:
                    x=query.split(' ', 1)[1]
                    site=x+".in"
                    webbrowser.open(site)



            elif "what\'s up" in query or 'how are you' in query:
                stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
                speak(random.choice(stMsgs))
                #speak("mere ex be chungi mere next be chungi mere crush be chungi rishtadaar bahaut cute")

            elif 'nothing' in query or 'abort' in query or 'stop' in query or 'goodbye' in query:
                speak('okay')
                speak('Bye Master!')
                sys.exit()

            elif 'hello' in query:
                speak('Hello Sir')

            elif 'play music' in query:
                speak("i can open youtube and you can select music!")
                speak("DO you want me to do so?")
                x=myCommand()
                if x in "yes yeah yup yuup yah":
                    webbrowser.open("www.youtube.com")

            elif"what can you do" in query:
                speak("what do u want")
                speak("i can open youtube,google,gmail,send email ,play music,open some self made games and much more you will definately have fun with me!")

            elif "write something" in query:
                speak("got it  start speaking...")
                content = myCommand()
                print(content)

            elif"abba harmonium bajate the" in query:
                speak("nahi!!")
                speak("abba harmonium khaaate the   the !! Arrey bhhaaii")
                speak("Maaf karna gusse m idhar udhar nikal jate hu")

            elif "love" in query:
                speak("What can i say!!")
                #speak("bhaag yah   c ")
                speak("but you are valueable to me!")

            elif "play games"  in query:
                speak("Your hardware can't tollerate my games please try after my updation")

            else:
                query = query
                speak('Searching...')
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)

                except:
                    speak("Sorry master !! something went wrong please try searching google")
                    speak("should i open google for you??")
                    x=myCommand()
                    if x in "y":
                        webbrowser.open('www.google.com\\'+query)

            speak("what's my next task master!")

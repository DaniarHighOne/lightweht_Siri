import os, webbrowser, sys, requests, subprocess, pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 180) #speaking speed

def speaker(text):
    #text to speech
    engine.say(text)
    engine.runAndWait()

def browser():
    webbrowser.open('www.youtube.com', new=2)
    #print('Browser running...')

def game():
    subprocess.Popen( 'C:\Windows\WinSxS\\amd64_microsoft-windows-mspaint_31bf3856ad364e35_10.0.19041.746_none_6c16d1714d60fddf')
    print('Game running...')

def offpc():
    #os.system('shutdown/s')
    print('Gonna shutdown the pc...')

def weather():
    
        params = {'q': 'Almaty', 'units': 'metric', 'lang': 'ru', 'appid': '14916cfd11db2401abb1b37d0a7d2564'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        w = response.json()
        speaker(f"На улице  {round(w['main']['temp'])} градусов")
            

def offbot():
    sys.exit()

def passive():
    pass